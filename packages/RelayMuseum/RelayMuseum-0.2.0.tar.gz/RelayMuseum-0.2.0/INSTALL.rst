============
Installation
============

You'll need ``Python 2.7.x``, ``Python 3.4.x`` or newer.

You will need a database supported by ``django``. ``Python 2.7`` and newer
includes ``sqlite3``, which is adequate.

Install it with ``pip``.

If running the museum itself as a website you'll need to place the
following settings in a file called ``RelayMuseumConf.py`` in either
``/etc/django-sites.d``, ``/usr/local/etc/django-sites.d`` or the same
directory as this file.

The following settings will need to be set, at a minimum:

* ALLOWED_HOSTS
* DATABASES
* LOGGING
* SECRET_KEY
* MEDIA_ROOT
* STATIC_ROOT

The locations pointed to by ``MEDIA_ROOT`` and ``STATIC_ROOT`` must be
accessible by a web-server.
