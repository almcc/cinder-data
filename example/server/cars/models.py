from __future__ import unicode_literals

from django.db import models


class Manufacturer(models.Model):
    """Manufacturer of cars."""

    name = models.CharField(max_length=100, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Car(models.Model):
    """Models of car made by a Manufacturer."""

    name = models.CharField(max_length=100, blank=False)
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.CASCADE, related_name='cars')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
