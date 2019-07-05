#!/usr/bin/env python

from distutils.core import setup

setup(name='django-elfinder',
      version='0.2',
      description='Django connector for elFinder 2',
      author='Mike Ryan',
      author_email='mike@fadedink.co.uk',
      url='https://github.com/mikery/django-elfinder/',
      download_url='https://github.com/mikery/django-elfinder/tarball/v0.2',
      packages=['elfinder', 'elfinder.volume_drivers'],
      requires=['django (>=1.3)', 'mptt (>=0.5.2)'],
      )
