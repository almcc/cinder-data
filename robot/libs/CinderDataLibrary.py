from cinder_data.model import DjangoModel
from cinder_data.store import Store
from cinder_data.cache import MemoryCache
from schematics.types import StringType


class Manufacturer(DjangoModel):
    """Cinder data model for Manufacturer api endpoint."""

    name = StringType()


class Car(DjangoModel):
    """Cinder data model for Car api endpoint."""

    name = StringType()


class CinderDataLibrary(object):
    """Robot framework cinder data libary for the example server."""

    def __init__(self):
        """Initialise the store with an in-memory cache."""
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
        """Get a single model from the server.

        Args:
            model (string): The class as a string.
            model_id (string): The integer ID as a string.

        Returns:
            :class:`cinder_data.model.CinderModel`: A instance of the model.
        """
        return self._store.find_record(self._get_model_class(model), int(model_id))

    def get_models(self, model, page=None):
        """Get all the models from the server.

        Args:
            model (string): The class as a string.
            page (string, optional): The page number as a string

        Returns:
            list: A list of instances of the requested model.
        """
        if page is not None:
            return self._store.find_all(self._get_model_class(model), params={'page': int(page)})
        else:
            return self._store.find_all(self._get_model_class(model))

    def peek_models(self, model):
        """Get all the models from the stores cache.

        Args:
            model (string): A class as a string.

        Returns:
            list: A list of instances of the requested model.
        """
        return self._store.peek_all(self._get_model_class(model))
