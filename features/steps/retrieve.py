from behave import *
from hamcrest import assert_that, equal_to

from cinder_data.cache import MemoryCache
from cinder_data.store import Store


@given('we have setup a store for {server} {namespace}')
def step_impl(context, server, namespace):
    cache = MemoryCache()
    context.store = Store(server, namespace, cache=cache)

@when('we request {model_class_name} {id:d}')
def step_impl(context, model_class_name, id):
    model = getattr(context, '{}_model'.format(model_class_name.lower()))
    record = context.store.find_record(model, id)
    context.record = record

@then('we have a "{car_model_name}"')
def step_impl(context, car_model_name):
    assert_that(context.record.name, equal_to(car_model_name))
