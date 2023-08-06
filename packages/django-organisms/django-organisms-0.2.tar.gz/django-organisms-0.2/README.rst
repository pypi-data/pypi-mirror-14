=========
Organisms
=========

Organisms is a simple Django app to represent organisms.


Download and Install
--------------------

This package is registered as "django-organisms" in PyPI and is pip
installable:

.. code-block:: shell

  pip install django-organisms

If ``django`` is not found on your system, ``pip`` will install it too.


Quick Start
-----------

1. Add **'organisms'** to your ``INSTALLED_APPS`` setting like this::

    INSTALLED_APPS = (
        ...
        'organisms',
    )

2. Run ``python manage.py migrate`` command to create ``organisms`` model.


Usage of Management Command
---------------------------

This app includes a management command
``management/commands/organisms_create_or_update.py``,
which can be used to populate the organisms table in the database.
It takes 3 arguments:

* taxonomy_id
* scientific_name
* common_name

For example, to populate the Human object in the database, we would enter:

.. code-block:: shell

  python manage.py organisms_create_or_update --taxonomy_id=9606 --scientific_name="Homo sapiens" --common_name="Human"
