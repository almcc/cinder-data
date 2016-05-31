from models import Manufacturer
from models import Car
from rest_framework import viewsets
from .serializers import ManufacturerSerializer
from .serializers import CarSerializer


class ManufacturerViewSet(viewsets.ModelViewSet):
    """View set for Manufacturer model."""

    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer


class CarViewSet(viewsets.ModelViewSet):
    """View set for Car model."""

    queryset = Car.objects.all()
    serializer_class = CarSerializer
