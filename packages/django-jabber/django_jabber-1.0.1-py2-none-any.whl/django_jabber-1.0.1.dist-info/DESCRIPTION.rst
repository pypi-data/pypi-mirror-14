django-jabber
=============

Send Jabber notifications from Django

.. image:: https://travis-ci.org/alexmorozov/django-jabber.svg?branch=master
    :target: https://travis-ci.org/alexmorozov/django-jabber

Usage
-----

.. code-block:: python

    from django_jabber import send_message

    recipients = ['user1', 'user2', ] # without @domain.com part
    send_message(u'Hello there', recipients)

    # You can also pass this job to your Celery instance
    send_message.delay(u'Async message', recipients)


Installation
------------

Install the package via Pypi: `pip install django-jabber`

Add some lines to your settings.py:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_jabber',
        ...
    )

    JABBER_HOST = 'jabber.domain.com'
    JABBER_USER = 'robot@domain.com'
    JABBER_PASSWORD = 'someStr0ngOne!1'
    JABBER_USE_TLS = True
    JABBER_USE_SSL = False
    JABBER_DRY_RUN = False  # Useful for testing

Requirements
^^^^^^^^^^^^

- sleekxmpp
- celery
- django

Compatibility
-------------

We use this package on Python 2.7 and Django 1.7+.

License
-------

GPLv3

Authors
-------

`django-jabber` was written by `Alex Morozov <inductor2000@mail.ru>`_.


