from invoke import Context
from schematics.types import IntType, StringType
from time import sleep

from cinder_data.model import DjangoModel

ictx = Context()


class Manufacturer(DjangoModel):
    name = StringType()

class Car(DjangoModel):
    name = StringType()
    year = IntType()


def before_all(context):

    context.car_model = Car
    context.manufacturer_model = Manufacturer

    with ictx.cd('features/'):
        ictx.run('docker-compose down -v')
        ictx.run('docker-compose up -d api')
        sleep(1)


def after_all(context):
    with ictx.cd('features/'):
        ictx.run('docker-compose down -v')


# def before_scenario(context, scenario):
#     print('before_scenario: {}'.format(scenario.name))


# def before_feature(context, feature):
#     print('before_feature: {}'.format(feature.name))
