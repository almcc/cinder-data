from models import Manufacturer
from models import Car
from rest_framework import serializers


class ManufacturerSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for the Manufacturer model."""

    class Meta:
        model = Manufacturer


class CarSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for the Car model."""

    class Meta:
        model = Car
