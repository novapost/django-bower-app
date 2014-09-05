Django Bower App
================

Library to manage bower.json dependancies with ease

WHY
---

Managing assets for django is more and more complicated when you need
to interact with heavy javascript page. Now many javascripts
developers use bower to manger their dependancies.

Bower then need to be interfaced with Django as seemlessly as
possible. Neither the javascript developer nor the django developper
must change the way they work.

django-bower-app aims to be the glue between javascript and django
with simple, easy to manage code.

HOW
---

A simple command, bower_install will look in each of the static
directory of each app and extract the bower.json, letting
bower_components untouched and build each module dependancies in the
settings.STATIC_ROOT directory.

You can now develop your javascript apps with bower and create a
production ready environnment with bower_install

Requirements
------------

Obviousely, to run django-bower-app, you need bower and django. That's
all.

INSTALL
-------

First download this module and install it with

>>> python setup.py install

Then add "djangobwr" to your INSTALLED_APPS

>>> INSTALLED_APPS = (
...
"djangobwr",
...
)

you are ready to run the command each time you want to collect the
bower dependancies:

>>> python manage.py bower_install
