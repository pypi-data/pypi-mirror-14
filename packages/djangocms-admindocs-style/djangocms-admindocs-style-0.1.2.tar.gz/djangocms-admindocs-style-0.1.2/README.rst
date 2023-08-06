=============================
djangocms-admindocs-style
=============================

.. image:: https://badge.fury.io/py/djangocms-admindocs-style.png
    :target: https://badge.fury.io/py/djangocms-admindocs-style

.. image:: https://travis-ci.org/goldhand/djangocms-admindocs-style.png?branch=master
    :target: https://travis-ci.org/goldhand/djangocms-admindocs-style

Adds DjangoCMS Admin Styles to the admindocs

Documentation
-------------

The full documentation is at https://djangocms-admindocs-style.readthedocs.org.

Quickstart
----------

Install djangocms-admindocs-style::

    pip install djangocms-admindocs-style

Then use it in a project by adding it to your installed apps before 'django.contrib.admin'::

    INSTALLED_APPS = [
        ...
        'djangocms_admin_style',
        'djangocms_admindocs_style',
        'django.contrib.admin',
        'django.contrib.admindocs',
        ...
    ]

Running Tests
--------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements-test.txt
    (myenv) $ python runtests.py

Compiling CSS
-------------

Make sure `sassc` is installed and run::

    npm run sass
