from cinder_data.model import DjangoModel
from cinder_data.store import Store
from cinder_data.cache import MemoryCache
from schematics.types import StringType


class Manufacturer(DjangoModel):
    name = StringType()


class Car(DjangoModel):
    name = StringType()


class CinderDataLibrary(object):

    def __init__(self):
        cache = MemoryCache()
        self._store = Store('http://server:8000', 'api/v1', cache=cache)

    @staticmethod
    def _get_model_class(model_name):
        """A help function to a turn a string into the class of the same name.

        Needed because arguments from robot test scripts are strings.
        """
        if model_name == 'Manufacturer':
            return Manufacturer
        if model_name == 'Car':
            return Car

    def get_model(self, model, model_id):
        return self._store.find_record(self._get_model_class(model), int(model_id))

    def get_models(self, model, page=None):
        if page is not None:
            return self._store.find_all(self._get_model_class(model), params={'page': int(page)})
        else:
            return self._store.find_all(self._get_model_class(model))

    def peek_models(self, model):
        return self._store.peek_all(self._get_model_class(model))
