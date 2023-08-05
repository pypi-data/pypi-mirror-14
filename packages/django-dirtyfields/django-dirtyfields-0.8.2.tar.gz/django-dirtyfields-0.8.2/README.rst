===================
Django Dirty Fields
===================

.. image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/romgar/django-dirtyfields
   :target: https://gitter.im/romgar/django-dirtyfields?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
.. image:: https://travis-ci.org/romgar/django-dirtyfields.svg?branch=develop
    :target: https://travis-ci.org/romgar/django-dirtyfields?branch=develop
.. image:: https://coveralls.io/repos/romgar/django-dirtyfields/badge.svg?branch=develop
   :target: https://coveralls.io/r/romgar/django-dirtyfields?branch=develop
.. image:: http://readthedocs.org/projects/django-dirtyfields/badge/?version=develop
   :target: http://django-dirtyfields.readthedocs.org/en/develop/?badge=develop

Tracking dirty fields on a Django model instance.

Dirty means that there is a difference between field value in the database and the one we currently have on a model instance.

`Documentation <http://django-dirtyfields.readthedocs.org/en/develop/>`_

Install
=======

::

    $ pip install django-dirtyfields


Usage
=====

To use ``django-dirtyfields``, you need to:

- Inherit from ``DirtyFieldMixin`` in the Django model you want to track.

::
    
    from django.db import models
    from dirtyfields import DirtyFieldsMixin

    class TestModel(DirtyFieldsMixin, models.Model):
        """A simple test model to test dirty fields mixin with"""
        boolean = models.BooleanField(default=True)
        characters = models.CharField(blank=True, max_length=80)

- Use one of these 2 functions on a model instance to know if this instance is dirty, and get the dirty fields:

    * is\_dirty()
    * get\_dirty\_fields()


Example
-------

::

    >>> from tests.models import TestModel
    >>> tm = TestModel.objects.create(boolean=True,characters="testing")
    >>> tm.is_dirty()
    False
    >>> tm.get_dirty_fields()
    {}

    >>> tm.boolean = False

    >>> tm.is_dirty()
    True
    >>> tm.get_dirty_fields()
    {'boolean': True}


Checking foreign key fields.
----------------------------
By default, dirty functions are not checking foreign keys. If you want to also take these relationships into account, use ``check_relationship`` parameter:

::

    >>> from tests.models import TestModel
    >>> tm = TestModel.objects.create(fkey=obj1)
    >>> tm.is_dirty()
    False
    >>> tm.get_dirty_fields()
    {}

    >>> tm.fkey = obj2

    >>> tm.is_dirty()
    False
    >>> tm.is_dirty(check_relationship=True)
    True

    >>> tm.get_dirty_fields()
    {}
    >>> tm.get_dirty_fields(check_relationship=True)
    {'fkey': 1}


Saving dirty fields.
----------------------------
If you want to only save dirty fields from an instance in the database (only these fields will be involved in SQL query), you can use ``save_dirty_fields`` method.

Warning: this ``save_dirty_fields`` method will trigger the same signals as django default ``save`` method.
But, in django 1.4.22-, as we are using under the hood an ``update`` method, we need to manually send these signals, so be aware that only ``sender`` and ``instance`` arguments are passed to the signal in that context.


Why would you want this?
------------------------

When using signals_, especially pre_save_, it is useful to be able to see what fields have changed or not. A signal could change its behaviour depending on whether a specific field has changed, whereas otherwise, you only could work on the event that the model's `save()` method had been called.


Contributing
============
If you're interested in developing it, you can launch project tests on that way:

::

    $ pip install tox
    $ pip install -e .
    $ tox


Credits
-------

This code has largely be adapted from what was made available at `Stack Overflow`_.

.. _Stack Overflow: http://stackoverflow.com/questions/110803/dirty-fields-in-django
.. _signals: http://docs.djangoproject.com/en/1.2/topics/signals/
.. _pre_save: http://docs.djangoproject.com/en/1.2/ref/signals/#django.db.models.signals.pre_save

