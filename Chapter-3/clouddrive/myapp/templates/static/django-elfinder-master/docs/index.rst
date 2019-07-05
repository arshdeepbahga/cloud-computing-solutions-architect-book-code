dango-elfinder - Django connector for elFinder
==============================================

django-elfinder provides a Django-based connector for `elFinder`_, a
jQuery-based file browser.

The PHP-based connector provided with elFinder gives direct access to the
underlying file system. django-elfinder uses Django models to store the
files and directories.

This module is not ready for production use, and only a limited set of
elFinder commands are currently supported.

.. _elfinder: http://elfinder.org

Quickstart
----------

To view a demo, run these commands::

    git clone git://github.com/mikery/django-elfinder.git
    cd django-elfinder/test_project
    ./manage.py loaddata ../elfinder/fixtures/testdata.json --pythonpath="../"
    ./manage.py runserver 127.0.0.1:8080 --pythonpath="../"

Then browse to http://127.0.0.1:8080/elfinder/1/.
