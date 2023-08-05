|wq.db|

`wq.db <https://wq.io/wq.db>`__ is a collection of Python modules for
building robust, flexible schemas and REST APIs for use in creating
field data collection apps and (more generally) mobile-first websites
with progressive enhancement. wq.db is the backend component of
`wq <https://wq.io>`__ and is geared primarily for use with
`wq.app <https://wq.io/wq.app>`__, though it can be used separately.
wq.db is built on the `Django <https://www.djangoproject.com/>`__
platform.

|Latest PyPI Release| |Release Notes| |Documentation| |License| |GitHub
Stars| |GitHub Forks| |GitHub Issues|

|Travis Build Status| |Python Support| |Django Support|

Getting Started
---------------

.. code:: bash

    pip3 install wq.db
    # Or, if using together with wq.app and/or wq.io
    pip3 install wq

See `the documentation <https://wq.io/docs/>`__ for more information.

Features
--------

wq.db provides the following modules:

`wq.db.rest <https://wq.io/docs/about-rest>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Extends the excellent `Django REST
Framework <http://django-rest-framework.org>`__ with a collection of
views, serializers, and context processors useful for creating a
progresively enhanced website that serves as its own mobile app and `its
own REST API <https://wq.io/docs/website-rest-api>`__. The core of the
library is an admin-like `ModelRouter <https://wq.io/docs/router>`__
that connects REST urls to registered models, and provides a descriptive
`configuration object <https://wq.io/docs/config>`__ for consumption by
`wq.app's client-side router <https://wq.io/docs/app-js>`__. wq.db.rest
also includes a CRS-aware GeoJSON serializer/renderer.

`wq.db.patterns <https://wq.io/docs/about-patterns>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A collection of `design
patterns <https://wq.io/docs/about-patterns>`__ (e.g.
`identify <https://wq.io/docs/identify>`__,
`relate <https://wq.io/docs/relate>`__) that provide long-term
flexibility and sustainability for user-maintained data collection
applications. These patterns are implemented as installable Django apps.

.. |wq.db| image:: https://raw.github.com/wq/wq/master/images/256/wq.db.png
   :target: https://wq.io/wq.db
.. |Latest PyPI Release| image:: https://img.shields.io/pypi/v/wq.db.svg
   :target: https://pypi.python.org/pypi/wq.db
.. |Release Notes| image:: https://img.shields.io/github/release/wq/wq.db.svg
   :target: https://github.com/wq/wq.db/releases
.. |Documentation| image:: https://img.shields.io/badge/Docs-0.8-blue.svg
   :target: https://wq.io/wq.db
.. |License| image:: https://img.shields.io/pypi/l/wq.db.svg
   :target: https://wq.io/license
.. |GitHub Stars| image:: https://img.shields.io/github/stars/wq/wq.db.svg
   :target: https://github.com/wq/wq.db/stargazers
.. |GitHub Forks| image:: https://img.shields.io/github/forks/wq/wq.db.svg
   :target: https://github.com/wq/wq.db/network
.. |GitHub Issues| image:: https://img.shields.io/github/issues/wq/wq.db.svg
   :target: https://github.com/wq/wq.db/issues
.. |Travis Build Status| image:: https://img.shields.io/travis/wq/wq.db/master.svg
   :target: https://travis-ci.org/wq/wq.db
.. |Python Support| image:: https://img.shields.io/pypi/pyversions/wq.db.svg
   :target: https://pypi.python.org/pypi/wq.db
.. |Django Support| image:: https://img.shields.io/badge/Django-1.8%2C%201.9-blue.svg
   :target: https://pypi.python.org/pypi/wq.db
