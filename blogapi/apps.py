from django.apps import AppConfig


class BlogapiConfig(AppConfig):
    name = 'blogapi'

    def ready(self):
        from . import signals
        