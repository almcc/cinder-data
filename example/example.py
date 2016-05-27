from cinder_data.model import DjangoModel
from cinder_data.store import Store
from cinder_data.cache import MemoryCache
from schematics.types import StringType


class Manufacturer(DjangoModel):
    name = StringType()


class Car(DjangoModel):
    name = StringType()


if __name__ == '__main__':
    cache = MemoryCache()
    store = Store('http://server:8000', 'api/v1', cache=cache)

    record = store.find_record(Car, 1)
    record = store.find_record(Car, 1, reload=True)

    records = store.find_all(Car)
    for record in records:
        print record.name

    records = store.find_all(Car, params={'page': 2})
    for record in records:
        print record.name

    records = store.find_all(Manufacturer)
    for record in records:
        print record.name

    records = store.peek_all(Car)
    for record in records:
        print record.name
