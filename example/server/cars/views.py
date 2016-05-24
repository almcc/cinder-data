from django.contrib.auth.models import User, Group
from models import Manufacturer
from models import Car
from rest_framework import viewsets
from .serializers import ManufacturerSerializer
from .serializers import CarSerializer


class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
