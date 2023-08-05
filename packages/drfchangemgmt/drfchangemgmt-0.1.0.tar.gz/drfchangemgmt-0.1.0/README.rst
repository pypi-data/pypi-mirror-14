drfchangemgmt
======================================

|build-status-image| |pypi-version|

Overview
--------

Django Rest Framework change management

Requirements
------------

-  Python (2.7, 3.3, 3.4)
-  Django (1.6, 1.7, 1.8)
-  Django REST Framework (2.4, 3.0, 3.1)

Installation
------------

Install using ``pip``\ …

.. code:: bash

    $ pip install drfchangemgmt

Example
-------

.. code:: python

    from .models import Actor
    from drfchangemgmt import ChangeMgmtSerializerMixin
    from rest_framework.serializers import ModelSerializer

    class ActorSerializer(ChangeMgmtSerializerMixin, ModelSerializer):
        """ Actor model serializer """

        class Meta(object):
            """ DRF ModelSerializer meta object """

            model = Actor

    ...
    ...

    def pre_save(..):
        changed = model.get_changed_fields()
        if 'superuser_role' in changed:
            raise PermissionDenied("you can't do that!")

Testing
-------

Install testing requirements.

.. code:: bash

    $ pip install -r requirements.txt

Run with runtests.

.. code:: bash

    $ ./runtests.py

You can also use the excellent `tox`_ testing tool to run the tests
against all supported versions of Python and Django. Install tox
globally, and then simply run:

.. code:: bash

    $ tox

Documentation
-------------

To build the documentation, you’ll need to install ``mkdocs``.

.. code:: bash

    $ pip install mkdocs

To preview the documentation:

.. code:: bash

    $ mkdocs serve
    Running at: http://127.0.0.1:8000/

To build the documentation:

.. code:: bash

    $ mkdocs build

.. _tox: http://tox.readthedocs.org/en/latest/

.. |build-status-image| image:: https://secure.travis-ci.org/sassoo/drfchangemgmt.svg?branch=master
   :target: http://travis-ci.org/sassoo/drfchangemgmt?branch=master
.. |pypi-version| image:: https://img.shields.io/pypi/v/drfchangemgmt.svg
   :target: https://pypi.python.org/pypi/drfchangemgmt
