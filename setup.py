# -*- coding: utf-8 -*-
"""Python packaging."""
import os

from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))

NAME = u'Django Bower App'
DESCRIPTION = u"Library to manage bower.json dependancies with ease"
README = open(os.path.join(here, 'README.rst')).read()
VERSION = open(os.path.join(here, 'VERSION')).read().strip()
AUTHOR = u'Yohann Gabory'
EMAIL = u'yohann@gabory.fr'
URL = u'https://github.com/boblefrag/django-bower-app'
CLASSIFIERS = ['Development Status :: 3 - Alpha',
               'License :: OSI Approved :: BSD License',
               'Programming Language :: Python :: 2.7',
               'Framework :: Django']
PACKAGES = ['djangobwr']
REQUIREMENTS = ['Django']
ENTRY_POINTS = {}


if __name__ == '__main__':  # Don't run setup() when we import this module.
    setup(name=NAME,
          version=VERSION,
          description=DESCRIPTION,
          long_description=README,
          classifiers=CLASSIFIERS,
          keywords="",
          author=AUTHOR,
          author_email=EMAIL,
          url=URL,
          packages=PACKAGES,
          include_package_data=True,
          zip_safe=False,
          install_requires=REQUIREMENTS,
          setup_requires=['setuptools'],
          entry_points=ENTRY_POINTS)
