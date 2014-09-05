from django.contrib.staticfiles.finders import AppDirectoriesFinder
from django.contrib.staticfiles.storage import AppStaticStorage

class AppDirectoriesFinderBower(AppDirectoriesFinder):
    storage_class = AppStaticStorage

    def list(self, ignore_patterns):
        """
        List all files in all app storages.
        """
        ignore_patterns.append("bower_components")
        return super(AppDirectoriesFinderBower, self).list(ignore_patterns)
