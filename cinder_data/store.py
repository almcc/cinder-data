import requests
import inflection


class Store(object):
    def __init__(self, host, namespace, cache=None):
        super(Store, self).__init__()
        self._host = host
        self._namespace = namespace
        self._cache = cache

    def find_record(self, model_class, record_id, reload=False):
        cached_model = self._cache.get_record(model_class.__name__, record_id)
        if cached_model is not None and reload is False:
            return cached_model
        else:
            return self._get_record(model_class, record_id)

    def find_all(self, model_class, params={}):
        url = '{host}/{namespace}/{model}{params}'.format(
            host=self._host,
            namespace=self._namespace,
            model=self._translate_name(model_class.__name__),
            params=self._build_param_string(params)
        )
        request = requests.get(url)
        data = request.json()['data']
        fresh_models = []
        for item in data:
            fresh_model = model_class(item['attributes'])
            fresh_model.id = item['id']
            fresh_model.validate()
            fresh_models.append(fresh_model)
            self._cache.set_record(model_class.__name__, fresh_model.id, fresh_model)
        return fresh_models

    def _get_record(self, model_class, record_id):
        url = '{host}/{namespace}/{model}/{id}'.format(
            host=self._host,
            namespace=self._namespace,
            model=self._translate_name(model_class.__name__),
            id=record_id
        )
        request = requests.get(url)
        data = request.json()['data']
        fresh_model = model_class(data['attributes'])
        fresh_model.id = data['id']
        fresh_model.validate()
        self._cache.set_record(model_class.__name__, fresh_model.id, fresh_model)
        return fresh_model

    @staticmethod
    def _translate_name(name):
        pluralized = inflection.pluralize(name)
        underscored = inflection.underscore(pluralized)
        dasherized = inflection.dasherize(underscored)
        return dasherized

    @staticmethod
    def _build_param_string(params):
        pairs = []
        for key, value in params.iteritems():
            pairs.append('{}={}'.format(key, value))
        if len(pairs) > 0:
            return '?{}'.format('&'.join(pairs))
        return ''
