=================================
django-ckeditor-filebrowser-filer
=================================

.. image:: https://badge.fury.io/py/django-ckeditor-filebrowser-filer.png
    :target: https://badge.fury.io/py/django-ckeditor-filebrowser-filer

A django-filer based CKEditor filebrowser for **django CMS**

Documentation
-------------

A CKEditor filebrowser based on `django-filer`_ and `django CMS`_

Original code is taken from `django-ckeditor-filer`_

Quickstart
----------

Install django-ckeditor-filebrowser-filer::

    pip install django-ckeditor-filebrowser-filer

Then add it to INSTALLED_APPS along with its dependencies::

    'filer',
    'cmsplugin_filer_image',
    'ckeditor_filebrowser_filer',

Configure django-filer `Canonical URLs`_

Add `ckeditor_filebrowser_filer` to urlconf::

    url(r'^filebrowser_filer/', include('ckeditor_filebrowser_filer.urls')),

Add `FilerImage` button to you CKEditor configuration.

.. _Canonical URLs: http://django-filer.readthedocs.org/en/latest/installation.html#canonical-urls
.. _django CMS: https://pypi.python.org/pypi/django-cms
.. _django-filer: https://pypi.python.org/pypi/django-filer
.. _django-ckeditor-filer: https://github.com/ikresoft/django-ckeditor-filer/






History
-------

0.2.0 (2015-11-18)
++++++++++++++++++

* Update to use canonical urls feature of filer 1.0
* Update to work with djangocms-text-ckeditor 2.7

0.1.1 (2014-09-27)
++++++++++++++++++

* Fix static files position

0.1.0 (2014-01-27)
++++++++++++++++++

* First release on PyPI.


