from django.apps import AppConfig
from django.contrib import admin
from django.apps import apps

class MainConfig(AppConfig):
    name = 'main'
    verbose_name = "Główne"

    def ready(self):
        # Import the model classes
        Hit = apps.get_model('hitcount', 'Hit')
        HitCount = apps.get_model('hitcount', 'HitCount')
        BlacklistIP = apps.get_model('hitcount', 'BlacklistIP')
        BlacklistUserAgent = apps.get_model('hitcount', 'BlacklistUserAgent')
        Tags = apps.get_model('taggit', 'Tag')
        # Unregister the models
        admin.site.unregister(Hit)
        admin.site.unregister(HitCount)
        admin.site.unregister(BlacklistIP)
        admin.site.unregister(BlacklistUserAgent)
        admin.site.unregister(Tags)

