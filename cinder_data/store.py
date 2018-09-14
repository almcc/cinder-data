import logging
from urllib.parse import urlencode, urlsplit, urlunsplit

import inflection
import requests

logger = logging.getLogger('cinder_data.store')

# TODO: If response size != page_size throw a WARNING


class Store():
    """A central store for all CRUD like activilty for models."""

    def __init__(self, host, namespace='', cache=None, page_size=100, default_max_pages=100):
        """Initialise the store.

        Args:
            host (string): The host of your api, e.g. http://localhost:8000
            namespace (string, optional): An aditional name space to append
                to the host, e.g. api/v1
            cache (:class:`cinder_data.cache.Cache`, optional): An instance of your chosen caching
                system that must be must adhear to the :class:`cinder_data.cache.Cache` interface.
            page_size (int): API page_size to use per request
            default_max_results (int): Default maximum number of pages to requests
        """

        if namespace.endswith('/'):
            namespace = namespace[:-1]

        if namespace.startswith('/'):
            namespace = namespace[1:]

        super(Store, self).__init__()
        split_result = urlsplit(host)
        self._scheme = split_result.scheme
        self._netloc = split_result.netloc
        self._namespace = namespace
        self._cache = cache
        self._page_size = page_size
        self._default_max_pages = default_max_pages

    def find_record(self, model_class, record_id, reload=False):
        """Return a instance of model_class from the API or the local cache.

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
        return self._get_record(model_class, record_id)

    def peek_record(self, model_class, record_id):
        """Return an instance of the model_class from the cache if it is present.

        Args:
            model_class (:class:`cinder_data.model.CinderModel`): A subclass of
                :class:`cinder_data.model.CinderModel` of your chosen model.
            record_id (int): The id of the record requested.

        Returns:
            :class:`cinder_data.model.CinderModel`: An instance of model_class or None.

        """
        if self._cache:
            return self._cache.get_record(model_class.__name__, record_id)
        return None

    def find_all(self, model_class):
        """Return an list of models from the API and caches the result.

        Args:
            model_class (:class:`cinder_data.model.CinderModel`): A subclass of
                :class:`cinder_data.model.CinderModel` of your chosen model.

        Returns:
            list: A list of instances of you model_class or and empty list.

        """

        url_path = self._translate_name(model_class.__name__)
        url_query = query={
            'page': 1,
            'page_size': self._page_size
        }

        first_url = self._build_url(path=url_path, query=url_query)
        page_1_data, page_1_meta, page_1_links = self._get_json_list(first_url)

        total_pages = min(self._default_max_pages, page_1_meta.get('pagination').get('pages'))

        pages = [page_1_data]
        for i in range(2, total_pages + 1):
            url_query['page'] = i
            next_url = self._build_url(path=url_path, query=url_query)
            page_data, page_meta, page_links = self._get_json_list(next_url)
            pages.append(page_data)

        fresh_models = []
        for data in pages:
            for item in data:
                fresh_model = model_class(item['attributes'])
                fresh_model.id = item['id']
                fresh_model.validate()
                fresh_models.append(fresh_model)
                if self._cache is not None:
                    self._cache.set_record(model_class.__name__, fresh_model.id, fresh_model)
        return fresh_models

    # def peek_all(self, model_class):
    #     """Return a list of models from the local cache.
    #
    #     Args:
    #         model_class (:class:`cinder_data.model.CinderModel`): A subclass of
    #             :class:`cinder_data.model.CinderModel` of your chosen model.
    #
    #     Returns:
    #         list: A list of instances of you model_class or and empty list.
    #
    #     """
    #     if self._cache:
    #         return self._cache.get_records(model_class.__name__)
    #     return []

    def _get_record(self, model_class, record_id):
        """Get a single record from the API.

        Args:
            model_class (:class:`cinder_data.model.CinderModel`): A subclass of
                :class:`cinder_data.model.CinderModel` of your chosen model.
            record_id (int): The id of the record requested.

        Returns:
            :class:`cinder_data.model.CinderModel`: An instance of model_class or None.

        """
        url_path = '{model}/{id}'.format(
            model=self._translate_name(model_class.__name__),
            id=record_id
        )
        url = self._build_url(url_path)
        data = self._get_json(url)['data']
        fresh_model = model_class(data['attributes'])
        fresh_model.id = data['id']
        fresh_model.validate()
        if self._cache is not None:
            self._cache.set_record(model_class.__name__, fresh_model.id, fresh_model)
        return fresh_model

    @staticmethod
    def _get_json(url):
        """Get url and return as json.

        Args:
            url (string): A valid url which will return JSON.

        Returns:
            object: A serialised JSON object.

        """
        logger.debug('Getting JSON: GET %s', url)
        request = requests.get(url)
        return request.json()

    @classmethod
    def _get_json_list(cls, url):
        """Get a API listing and return data, meta and links."""
        response = cls._get_json(url)
        data = response.get('data')
        meta = response.get('meta')
        links = response.get('links')
        return (data, meta, links)

    @staticmethod
    def _translate_name(name):
        """Translate the class name to the API endpoint.

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

    def _build_url(self, path, query=None):
        if query is None:
            query = {}
        full_path = '{0}/{1}'.format(self._namespace, path)
        query_params = urlencode(query)
        url = urlunsplit((self._scheme, self._netloc, full_path, query_params, None))
        return url
