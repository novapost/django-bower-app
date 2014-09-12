import os
import json
import tempfile
import shutil
from subprocess import call

from django.core.management.base import BaseCommand
from django.conf import settings

from djangobwr.finders import AppDirectoriesFinderBower


class Command(BaseCommand):

    def handle(self, *args, **options):
        temp_dir = tempfile.mkdtemp()
        for path, storage in AppDirectoriesFinderBower().list([]):
            original_file = unicode(os.path.join(storage.location, path))
            if "bower.json" in path and not\
               os.path.split(path)[1].startswith("."):
                call(["bower",
                      "install",
                      original_file,
                      "--config.cwd={}".format(temp_dir),
                      "-p"])
        bower_dir = os.path.join(temp_dir, "bower_components")
        for directory in os.listdir(bower_dir):
            if directory != "static":
                bower = json.loads(
                    open(os.path.join(bower_dir, directory,
                                      "bower.json")).read())

                if not os.path.exists(
                        os.path.join(settings.STATIC_ROOT, directory)):
                    os.makedirs(os.path.join(settings.STATIC_ROOT, directory))

                if not isinstance(bower["main"], list):
                    main = [bower["main"]]
                else:
                    main = bower["main"]
                for path in main:
                    shutil.copy(os.path.join(bower_dir,
                                             directory,
                                             path),
                                os.path.join(settings.STATIC_ROOT, directory))
