import os
from subprocess import call
from django.core.management.base import BaseCommand
from djangobwr.finders import AppDirectoriesFinderBower
from django.conf import settings
class Command(BaseCommand):

    def handle(self, *args, **options):
        for path, storage in AppDirectoriesFinderBower().list([]):
            original_file = unicode(os.path.join(storage.location, path))
            if "bower.json" in path and not\
               os.path.split(path)[1].startswith("."):
                call(["bower",
                      "install",
                      original_file,
                      "--config.directory={}".format(settings.STATIC_ROOT),
                      "-p"])
