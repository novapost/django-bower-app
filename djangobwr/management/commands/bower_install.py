import os
import sys
import json
import tempfile
import shutil

from optparse import make_option
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

    option_list = BaseCommand.option_list + (
        make_option('--verbose', action='store_true', dest='verbose',
                    default=False, help='Display steps and commands.'),
        make_option('--interactive', action='store_true', dest='interactive',
                    default=False, help='Do not use bower force parameter.'),
        )

    def npm_install(self, pkg_json_path, verbose=False):
        """Calls 'npm install' command from an app static dir.
        """
        os.chdir(os.path.dirname(pkg_json_path))

        args = ['npm', 'install']

        if verbose:
            print('\n > {0}\n'.format(' '.join(args)))

        call(args)

    def grunt_default(self, grunt_js_path, verbose=False):
        """Calls 'grunt' command from an app static dir.
        """
        os.chdir(os.path.dirname(grunt_js_path))

        args = ['grunt']

        if verbose:
            print('\n > {0}\n'.format(' '.join(args)))

        call(args)

    def bower_install(self, bower_json_path, dest_dir, verbose=False,
                      interactive=False):
        """Runs bower commnand for the passed bower.json path.

        By default it add the -F parameter to force the latest version of
        dependencies to be installed. Otherwise it should be chosen manually.

        :param bower_json_path: bower.json file to install.
        :param dest_dir: where the compiled result will arrive.
        :param interactive: if True does not add -F parameter that force latest
                            versions to install.
        """
        # bower args
        args = ['bower', 'install', bower_json_path,
                '--config.cwd={}'.format(dest_dir), '-p']

        if verbose:
            print('\n > {0}\n'.format(' '.join(args)))

        if not interactive:
            args.append('-F')

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

        verbose = options.get('verbose')
        interactive = options.get('interactive')

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
            self.npm_install(path, verbose=verbose)

        for path in bower_list:
            self.bower_install(path, temp_dir, verbose=verbose,
                               interactive=interactive)

        for path in grunt_list:
            self.grunt_default(path, verbose=verbose)

        bower_dir = os.path.join(temp_dir, 'static', 'bower_components')

        # nothing to clean
        if not os.path.exists(bower_dir):
            print('no app found bower.json file to build')
            sys.exit(0)

        self.clean_components_to_static_dir(bower_dir)
