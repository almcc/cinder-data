import mock
import unittest

from cinder_data.cache import Cache
from cinder_data.cache import MemoryCache


class TestCache(unittest.TestCase):

    def setUp(self):
        self.cache = Cache()

    def test_get_record(self):
        with self.assertRaises(NotImplementedError):
            self.cache.get_record('Car', 1)

    def test_get_records(self):
        with self.assertRaises(NotImplementedError):
            self.cache.get_records('Car')

    def test_set_record(self):
        with self.assertRaises(NotImplementedError):
            self.cache.set_record('Car', 1, 'my_record')


class TestMemoryCache(unittest.TestCase):

    def setUp(self):
        self.cache = MemoryCache()

    def test_get_record_with_empty_cache(self):
        self.assertEqual(self.cache.get_record('Car', 1), None)

    def test_get_record_with_item_in_cache(self):
        self.cache._cache = {'Car': {1: 'my_car'}}
        self.assertEqual(self.cache.get_record('Car', 1), 'my_car')

    def test_get_record_with_item_in_cache_but_not_that_id(self):
        self.cache._cache = {'Car': {1: 'my_car'}}
        self.assertEqual(self.cache.get_record('Car', 2), None)

    def test_get_records_with_empty_cache(self):
        self.assertEqual(self.cache.get_records('Car'), [])

    def test_get_record_with_items_in_cache(self):
        self.cache._cache = {'Car': {1: 'my_car', 2: 'my_other_car'}}
        cached_records = self.cache.get_records('Car')
        self.assertEqual(cached_records[0], 'my_car')
        self.assertEqual(cached_records[1], 'my_other_car')

    def test_set_record_in_empty_cache(self):
        self.cache.set_record('Car', 1, 'my_other_car')
        self.assertEqual(self.cache._cache, {'Car': {1: 'my_other_car'}})

    def test_set_record_adding_to_existing_cache(self):
        self.cache._cache = {'Car': {1: 'my_car'}}
        self.cache.set_record('Car', 2, 'my_other_car')
        self.assertEqual(self.cache._cache, {'Car': {1: 'my_car', 2: 'my_other_car'}})

    def test_set_record_overiding_existing_record(self):
        self.cache._cache = {'Car': {1: 'my_car'}}
        self.cache.set_record('Car', 1, 'my_other_car')
        self.assertEqual(self.cache._cache, {'Car': {1: 'my_other_car'}})
