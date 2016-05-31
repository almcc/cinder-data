import unittest
import mock

from cinder_data.cache import MemoryCache
from cinder_data.model import DjangoModel
from cinder_data.store import Store
from fixtures import example_get_car
from fixtures import example_get_cars
from schematics.types import StringType


class TestStore(unittest.TestCase):

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

    @mock.patch.object(Store, '_get_record')
    def test_find_record_with_empty_cache(self, mock_get_record):
        class Car(DjangoModel):
            name = StringType()

        mock_cache = mock.create_autospec(MemoryCache)
        store = Store('http://localhost:1234', namespace='api/v1', cache=mock_cache)
        mock_cache.get_record.return_value = None
        store.find_record(Car, 1)
        mock_cache.get_record.assert_called_with('Car', 1)
        mock_get_record.assert_called_with(Car, 1)

    @mock.patch.object(Store, '_get_record')
    def test_find_record_item_in_cache(self, mock_get_record):
        class Car(DjangoModel):
            name = StringType()

        mock_cache = mock.create_autospec(MemoryCache)
        car = Car({'id': 1, 'name': 'F430'})
        store = Store('http://localhost:1234', namespace='api/v1', cache=mock_cache)
        mock_cache.get_record.return_value = car
        store.find_record(Car, 1)
        mock_cache.get_record.assert_called_with('Car', 1)
        self.assertFalse(mock_get_record.called)

    @mock.patch.object(Store, '_get_record')
    def test_find_record_no_cache(self, mock_get_record):
        class Car(DjangoModel):
            name = StringType()
        store = Store('http://localhost:1234', namespace='api/v1')
        store.find_record(Car, 1)
        mock_get_record.assert_called_with(Car, 1)

    @mock.patch.object(Store, '_get_json')
    def test_find_all_records_with_no_cache(self, mock_get_json):
        class Car(DjangoModel):
            name = StringType()
        store = Store('http://localhost:1234', namespace='api/v1')
        mock_get_json.return_value = example_get_cars
        records = store.find_all(Car)
        self.assertEqual(len(records), 10)
        for i in range(10):
            self.assertEqual(records[i].__class__, Car)

    @mock.patch.object(Store, '_get_json')
    def test_find_all_records_with_cache(self, mock_get_json):
        class Car(DjangoModel):
            name = StringType()
        mock_cache = mock.create_autospec(MemoryCache)
        store = Store('http://localhost:1234', namespace='api/v1', cache=mock_cache)
        mock_get_json.return_value = example_get_cars
        records = store.find_all(Car)
        self.assertEqual(len(records), 10)
        for i in range(10):
            self.assertEqual(records[i].__class__, Car)
        self.assertEqual(mock_cache.set_record.call_count, 10)

    def test_peek_all_with_no_cache(self):
        class Car(DjangoModel):
            name = StringType()
        store = Store('http://localhost:1234', namespace='api/v1')
        self.assertEqual(store.peek_all(Car), [])

    def test_peek_all_with_empty_cache(self):
        class Car(DjangoModel):
            name = StringType()
        mock_cache = mock.create_autospec(MemoryCache)
        mock_cache.get_records.return_value = []
        store = Store('http://localhost:1234', namespace='api/v1', cache=mock_cache)
        self.assertEqual(store.peek_all(Car), [])

    @mock.patch.object(Store, '_get_json')
    def test_get_record_with_no_cache(self, mock_get_json):
        class Car(DjangoModel):
            name = StringType()
        mock_get_json.return_value = example_get_car
        store = Store('http://localhost:1234', namespace='api/v1')
        record = store.find_record(Car, 1)
        self.assertEqual(record.id, 1)

    @mock.patch.object(Store, '_get_json')
    def test_get_record_with_cache(self, mock_get_json):
        class Car(DjangoModel):
            name = StringType()
        mock_get_json.return_value = example_get_car
        mock_cache = mock.create_autospec(MemoryCache)
        store = Store('http://localhost:1234', namespace='api/v1', cache=mock_cache)
        record = store._get_record(Car, 1)
        self.assertTrue(mock_cache.set_record.called)
        self.assertEqual(record.id, 1)

    @mock.patch('cinder_data.store.requests')
    def test_get_json(self, mock_requests):
        mock_result = mock.Mock()
        mock_result.json.return_value = 'result'
        mock_requests.get.return_value = mock_result
        self.assertEqual(Store._get_json('my_url'), 'result')
        mock_requests.get.assert_called_with('my_url')

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
