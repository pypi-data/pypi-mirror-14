Static jQuery
=============

Requirements
------------

django-appconf

`Django`_ 1.3 or later

Installation
------------

::

    $ pip install static-jquery

    $ pip install static-jquery==1.11.3

Setup
-----

Just add ``'django.contrib.staticfiles'`` and ``'jquery'`` to
INSTALLED\_APPS in your settings.py:

::

    INSTALLED_APPS = (
        # ...

        'django.contrib.staticfiles',
        'jquery',

        # ...
    )

Refer to Django `static files`_ documentation to configure and deploy
static files.

Usage
-----

You can refer to jquery in your template with::
    {% load jquery %}
	{% jquery\_js %}
	{% jquery\_js 1.11.3 %}

.. _Django: https://www.djangoproject.com/
.. _static files: https://docs.djangoproject.com/en/dev/howto/static-files/

