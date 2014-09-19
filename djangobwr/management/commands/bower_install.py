import os
import sys
import json
import tempfile
import shutil
from subprocess import call

from django.core.management.base import BaseCommand
from django.conf import settings

from djangobwr.finders import AppDirectoriesFinderBower


class Command(BaseCommand):
    """Command goes through apps. If description files are in the app,
    it will install it in a temporary folder:

        - package.json: npm install
        - Gruntfile.js: grunt default
        - bower.json: bower install
    """
    def npm_install(self, pkg_json_path):
        os.chdir(os.path.dirname(pkg_json_path))
        call(['npm', 'install'])

    def grunt_default(self, grunt_js_path):
        os.chdir(os.path.dirname(grunt_js_path))
        call(['grunt'])

    def bower_install(self, bower_json_path, dest_dir):
        """Runs bower commnand for the passed bower.json path.

        :param bower_json_path: bower.json file to install
        :param dest_dir: where the compiled result will arrive
        """
        # bower args
        args = ['bower', 'install', bower_json_path,
                '--config.cwd={}'.format(dest_dir), '-p']

        # run bower command
        call(args)

    def get_bower_main_list(self, bower_json_path):
        """Returns the bower.json main list or empty list.
        """

        main_list = json.load(open(bower_json_path)).get('main')

        if isinstance(main_list, list):
            return main_list

        if main_list:
            return [main_list]

        return []

    def clean_components_to_static_dir(self, bower_dir):

        for directory in os.listdir(bower_dir):

            # ensures dest dir
            static_root = os.path.join(settings.STATIC_ROOT, directory)
            if not os.path.exists(static_root):
                os.makedirs(static_root)

            bower_json_path = os.path.join(bower_dir, directory, 'bower.json')
            main_list = self.get_bower_main_list(bower_json_path)

            for path in filter(None, main_list):
                tmp_path = os.path.join(bower_dir, directory, path)
                print('{0} > {1}'.format(tmp_path, static_root))
                shutil.copy(tmp_path, static_root)

    def handle(self, *args, **options):

        npm_list = []
        grunt_list = []
        bower_list = []

        temp_dir = getattr(settings, 'BWR_APP_TMP_FOLDER', '.tmp')
        temp_dir = os.path.abspath(temp_dir)

        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        for path, storage in AppDirectoriesFinderBower().list([]):

            abs_path = unicode(os.path.join(storage.location, path))

            if path == 'package.json':
                npm_list.append(abs_path)
            elif path == 'Gruntfile.js':
                grunt_list.append(abs_path)
            elif path == 'bower.json':
                bower_list.append(abs_path)
            else:
                continue

        for path in npm_list:
            self.npm_install(path)

        for path in grunt_list:
            self.grunt_default(path)

        for path in bower_list:
            self.bower_install(path, temp_dir)

        bower_dir = os.path.join(temp_dir, 'static', 'bower_components')

        # nothing to clean
        if not os.path.exists(bower_dir):
            print('no app found bower.json file to build')
            sys.exit(0)

        self.clean_components_to_static_dir(bower_dir)
