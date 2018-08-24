Developer Documentation
=======================

Your environment
----------------

The cinder-data development environment relies a lot on docker, so there are
relativily few requirements for your development enviroment, namely docker,
docker-compose and python-fabric. Everything else is handled by docker.

To get started just do the following:

.. code-block:: bash

  git clone https://github.com/almcc/cinder-data.git
  cd cinder-data
  fab --list

You will get a list of the available helper commands.

.. tip::

  If your unfortunate enought to suffer from `#slowinternet <https://twitter.com/search?q=%23slowinternet>`_
  run ``fab prep_docker`` and go make yourself a cup of tea. It will download and
  build all the docker containers you will need.

Testing
-------

There are unit tests, run with ``fab run_unit_tests`` and there is some robot
tests that loads up an example server application and tests using cinder-data
to communicate with it. These are run with ``fab run_robot_tests``

Building
--------

`travis-ci.org <https://travis-ci.org/almcc/cinder-data>`_ builds cinder-data, if
there is a tag (should be in the form v<major>.<minor>.<patch>) it will also publish
a pip package to `pypi <https://pypi.python.org/pypi/cinder-data/>`_.
