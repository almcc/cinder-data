import requests
import inflection

class Store(object):
    """A central store for all CRUD like activilty for models."""

    def __init__(self, host, namespace='', cache=None):
        """Initialise the store.

        Args:
            host (string): The host of your api, e.g. http://localhost:8000
            namespace (string, optional): An aditional name space to append
                to the host, e.g. api/v1
            cache (:class:`cinder_data.cache.Cache`, optional): An instance of your chosen caching
                system that must be must adhear to the :class:`cinder_data.cache.Cache` interface.
        """
        super(Store, self).__init__()
        self._host = host
        self._namespace = namespace
        self._cache = cache

    def find_record(self, model_class, record_id, reload=False):
        """Returns a instance of model_class from the API or the local cache.

        Args:
            model_class (:class:`cinder_data.model.CinderModel`): A subclass of
                :class:`cinder_data.model.CinderModel` of your chosen model.
            record_id (int): The id of the record requested.
            reload (bool, optional): Don't return the cached version if reload==True.

        Returns:
            :class:`cinder_data.model.CinderModel`: An instance of model_class or None.
        """
        cached_model = self.peek_record(model_class, record_id)
        if cached_model is not None and reload is False:
            return cached_model
        else:
            return self._get_record(model_class, record_id)

    def peek_record(self, model_class, record_id):
        """Returns an instance of the model_class from the cache if it is present.

        Args:
            model_class (:class:`cinder_data.model.CinderModel`): A subclass of
                :class:`cinder_data.model.CinderModel` of your chosen model.
            record_id (int): The id of the record requested.

        Returns:
            :class:`cinder_data.model.CinderModel`: An instance of model_class or None.
        """
        if self._cache:
            return self._cache.get_record(model_class.__name__, record_id)
        else:
            return None

    def find_all(self, model_class, params={}):
        """Returns an list of models from the API and caches the result.

        Args:
            model_class (:class:`cinder_data.model.CinderModel`): A subclass of
                :class:`cinder_data.model.CinderModel` of your chosen model.
            params (dict, optional): Description

        Returns:
            list: A list of instances of you model_class or and empty list.
        """
        url = '{host}/{namespace}/{model}{params}'.format(
            host=self._host,
            namespace=self._namespace,
            model=self._translate_name(model_class.__name__),
            params=self._build_param_string(params)
        )
        data = self._get_json(url)['data']
        fresh_models = []
        for item in data:
            fresh_model = model_class(item['attributes'])
            fresh_model.id = item['id']
            fresh_model.validate()
            fresh_models.append(fresh_model)
            if self._cache is not None:
                self._cache.set_record(model_class.__name__, fresh_model.id, fresh_model)
        return fresh_models

    def peek_all(self, model_class):
        """Returns a list of models from the local cache.

        Args:
            model_class (:class:`cinder_data.model.CinderModel`): A subclass of
                :class:`cinder_data.model.CinderModel` of your chosen model.

        Returns:
            list: A list of instances of you model_class or and empty list.
        """
        if self._cache:
            return self._cache.get_records(model_class.__name__)
        else:
            return []

    def _get_record(self, model_class, record_id):
        """Gets a single record from the API.

        Args:
            model_class (:class:`cinder_data.model.CinderModel`): A subclass of
                :class:`cinder_data.model.CinderModel` of your chosen model.
            record_id (int): The id of the record requested.

        Returns:
            :class:`cinder_data.model.CinderModel`: An instance of model_class or None.
        """
        url = '{host}/{namespace}/{model}/{id}'.format(
            host=self._host,
            namespace=self._namespace,
            model=self._translate_name(model_class.__name__),
            id=record_id
        )
        data = self._get_json(url)['data']
        fresh_model = model_class(data['attributes'])
        fresh_model.id = data['id']
        fresh_model.validate()
        if self._cache is not None:
            self._cache.set_record(model_class.__name__, fresh_model.id, fresh_model)
        return fresh_model

    @staticmethod
    def _get_json(url):
        """Helper function for getting JSON from the API.

        Args:
            url (string): A valid url which will return JSON.

        Returns:
            object: A serialised JSON object.
        """
        request = requests.get(url)
        return request.json()

    @staticmethod
    def _translate_name(name):
        """Translates the class name to the API endpoint.

        For example, Car would become cars, FastCar would become fast-cars.

        Args:
            name (string): Camel case name (singular)

        Returns:
            string: A pluraised, dasherized string.
        """
        underscored = inflection.underscore(name)
        dasherized = inflection.dasherize(underscored)
        words = dasherized.split('-')
        last_word = words.pop()
        words.append(inflection.pluralize(last_word))
        return '-'.join(words)

    @staticmethod
    def _build_param_string(params):
        """Builds query params string from a dictionary.

        Args:
            params (dict): A dictionary of params

        Returns:
            string: A valid url query params string.
        """
        pairs = []
        for key, value in params.iteritems():
            if value is None:
                value = ''
            pairs.append('{}={}'.format(key, value))
        if len(pairs) > 0:
            return '?{}'.format('&'.join(pairs))
        return ''
