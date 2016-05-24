from models import Manufacturer
from models import Car
from rest_framework import serializers


class ManufacturerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Manufacturer


class CarSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Car
