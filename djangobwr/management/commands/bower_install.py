import os
import djangobwr
from subprocess import call
from django.core.management.base import BaseCommand
from djangobwr.finders import AppDirectoriesFinderBower
class Command(BaseCommand):

    def handle(self, *args, **options):
        cwd = options.get("cwd")
        if not cwd:
            cwd = os.path.dirname(djangobwr.__file__)
        for path, storage in AppDirectoriesFinderBower().list([]):
            original_file = unicode(os.path.join(storage.location, path))
            directory = "static"
            call(["bower",
                  "install",
                  original_file,
                  "--config.cwd={}".format(cwd),
                  "--config.directory={}".format(directory)])
