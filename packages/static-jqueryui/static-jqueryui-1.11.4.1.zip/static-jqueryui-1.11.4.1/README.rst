Static jQuery UI
================

Requirements
------------

    `Django`_ 1.3 or later
	django-appconf

Installation
------------

::

    $ pip install static-jqueryui

    $ pip install static-jqueryui==1.11.4

Setup
-----

Just add ``'django.contrib.staticfiles'`` and ``'jqueryui'`` to INSTALLED\_APPS in your settings.py:

::

    INSTALLED_APPS = (
        # ...

        'django.contrib.staticfiles',
        'jqueryui',

        # ...
    )

Refer to Django `static files`_ documentation to configure and deploy
static files.

Usage
-----

You can refer to jquery in your template with:

::

    {% load jqueryui %}
    {% jqueryui_js %}
    {% jqueryui_js 1.11.4 %}
    {% jqueryui_css 1.11.4 %}
    {% jqueryui_css 1.11.4 redmond %}

.. _Django: https://www.djangoproject.com/
.. _static files: https://docs.djangoproject.com/en/dev/howto/static-files/
