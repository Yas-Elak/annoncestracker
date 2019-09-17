from django.apps import AppConfig
from django.apps.config import AppConfig


class MainConfig(AppConfig):
    name = 'main'

    def ready(self):
        import main.signals.handlers

