class Cache(object):
    """Cache interface."""

    def get_record(self, name, record_id):
        """Should retrieve a record with a given type name and record id.

        Args:
            name (string): The name which the record is stored under.
            record_id (int): The id of the record requested.

        Raises:
            NotImplementedError:

        Returns:
            :class:`cinder_data.model.CinderModel`: Should return the cached model.
        """
        raise NotImplementedError()

    def get_records(self, name):
        """Should get all the records in the cache under a given name.

        Args:
            name (string): The name which the records are stored under.

        Raises:
            NotImplementedError:

        Returns:
            list: Should return a list of :class:`cinder_data.model.CinderModel` models.
        """
        raise NotImplementedError()

    def set_record(self, name, record_id, record):
        """Should save the record to the cache.

        Args:
            name (string): The name which to store the record under.
            record_id (int): The id of the record.
            record (:class:`cinder_data.model.CinderModel`): The model

        Raises:
            NotImplementedError: Description
        """
        raise NotImplementedError()


class MemoryCache(Cache):
    """A cache which uses in-process memmory."""

    def __init__(self):
        """Initialise the cache."""
        super(MemoryCache, self).__init__()
        self._cache = {}

    def get_record(self, name, record_id):
        """Retrieve a record with a given type name and record id.

        Args:
            name (string): The name which the record is stored under.
            record_id (int): The id of the record requested.

        Returns:
            :class:`cinder_data.model.CinderModel`: The cached model.
        """
        if name in self._cache:
            if record_id in self._cache[name]:
                return self._cache[name][record_id]

    def get_records(self, name):
        """Return all the records for the given name in the cache.

        Args:
            name (string): The name which the required models are stored under.

        Returns:
            list: A list of :class:`cinder_data.model.CinderModel` models.
        """
        if name in self._cache:
            return self._cache[name].values()
        else:
            return []

    def set_record(self, name, record_id, record):
        """Save a record into the cache.

        Args:
            name (string): The name to save the model under.
            record_id (int): The record id.
            record (:class:`cinder_data.model.CinderModel`): The model
        """
        if name not in self._cache:
            self._cache[name] = {}
        self._cache[name][record_id] = record
