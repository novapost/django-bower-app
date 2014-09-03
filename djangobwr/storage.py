from django.contrib.staticfiles.storage import AppStaticStorage

class BowerAppStaticStorage(AppStaticStorage):
    source_dir = 'bower'
