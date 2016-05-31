User Documentation
==================

About
-----

Cinder Data is a library inspired by ember-data for ember.js. It tries to abstract
away all the complexities of dealing with REST and JSON api's and giving you an
orm style interface for creating, reading, updating and deleting models.

.. warning:: Cinder Data is in very early development and is not ready for production yet.

Right now cinder-data only supports a JSON API, it is specfically designed to work
with Django, with the Django Rest Framework and the JSON api plugin installed.

.. code-block:: bash

  pip install Django djangorestframework djangorestframework-jsonapi

Given time it will support adapters like ember-data allowing you to work with
your own API's. 

Installing
----------

From pip
~~~~~~~~

.. code-block:: bash

  pip install cinder-data

From source
~~~~~~~~~~~

.. code-block:: bash

  git clone https://github.com/almcc/cinder-data.git
  cd cinder-data
  python setup.py install

Quick example
-------------


.. code-block:: python

  from cinder_data.model import DjangoModel
  from cinder_data.store import Store
  from schematics.types import StringType

  class Car(DjangoModel):
      name = StringType()

  store = Store('http://server:8000')

  # GET http://server:8000/cars/1
  record = store.find_record(Car, 1)

  # GET http://server:8000/cars
  first_page = store.find_all(Car)

  # GET http://server:8000/cars?page=2
  second_page = store.find_all(Car, params={'page': 2})
