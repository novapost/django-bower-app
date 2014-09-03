from django.contrib.staticfiles.finders import AppDirectoriesFinder
from django.contrib.staticfiles import utils
from django.utils import six
from djangobwr.storage import BowerAppStaticStorage


class AppDirectoriesFinderBower(AppDirectoriesFinder):
    storage_class = BowerAppStaticStorage

    def list(self, ignore_patterns):
        """
        List all files in all app storages.
        """
        for storage in six.itervalues(self.storages):
            if storage.exists(''):  # check if storage location exists
                for path in utils.get_files(storage, ignore_patterns):
                    if not path.startswith("bower_components"):
                        yield path, storage
