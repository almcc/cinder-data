import mock
import unittest

from cinder_data.store import Store
from cinder_data.cache import MemoryCache
from cinder_data.model import DjangoModel
from schematics.types import StringType


class TestStore(unittest.TestCase):

    def setUp(self):
        pass

    def test_init(self):
        store = Store('http://localhost:1234')
        self.assertEqual(store._host, 'http://localhost:1234')
        self.assertEqual(store._namespace, '')
        self.assertEqual(store._cache, None)

    def test_init_with_namespace(self):
        store = Store('http://localhost:1234', 'api/v1')
        self.assertEqual(store._host, 'http://localhost:1234')
        self.assertEqual(store._namespace, 'api/v1')
        self.assertEqual(store._cache, None)

    def test_init_with_cache(self):
        store = Store('http://localhost:1234', cache=MemoryCache)
        self.assertEqual(store._host, 'http://localhost:1234')
        self.assertEqual(store._namespace, '')
        self.assertEqual(store._cache.__name__, 'MemoryCache')

    def test_init_with_cache_and_namespace(self):
        store = Store('http://localhost:1234', namespace='api/v1', cache=MemoryCache)
        self.assertEqual(store._host, 'http://localhost:1234')
        self.assertEqual(store._namespace, 'api/v1')
        self.assertEqual(store._cache.__name__, 'MemoryCache')

    def test_find_record_no_cache(self):
        class Car(DjangoModel):
            name = StringType()
        store = Store('http://localhost:1234', namespace='api/v1')
        # record = store.find_record(Car, 1)
        # print record

    def test_translate_name_simple(self):
        result = Store._translate_name('car')
        self.assertEqual(result, 'cars')

    def test_translate_name_two_words(self):
        result = Store._translate_name('FastCar')
        self.assertEqual(result, 'fast-cars')

    def test_translate_name_complex_plural(self):
        result = Store._translate_name('Country')
        self.assertEqual(result, 'countries')

    def test_translate_name_two_work_complex_plural(self):
        result = Store._translate_name('CountrySky')
        self.assertEqual(result, 'country-skies')

    def test_translate_name_singular_same_plural(self):
        result = Store._translate_name('Sheep')
        self.assertEqual(result, 'sheep')

    def test_translate_name_two_word_singular_same_plural(self):
        result = Store._translate_name('BigSheep')
        self.assertEqual(result, 'big-sheep')

    def test_build_param_string_empty_dict(self):
        result = Store._build_param_string({})
        self.assertEqual(result, '')

    def test_build_param_string_one_item(self):
        result = Store._build_param_string({'page': 1})
        self.assertEqual(result, '?page=1')

    def test_build_param_string_two_items(self):
        result = Store._build_param_string({'page': 1, 'bob': 'foo'})
        self.assertEqual(result, '?bob=foo&page=1')

    def test_build_param_string_bad_items_1(self):
        result = Store._build_param_string({'?': '?'})
        self.assertEqual(result, '??=?')

    def test_build_param_string_bad_items_2(self):
        result = Store._build_param_string({'&': '&'})
        self.assertEqual(result, '?&=&')

    def test_build_param_string_bad_items_3(self):
        result = Store._build_param_string({'bob': None})
        self.assertEqual(result, '?bob=')
