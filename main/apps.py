from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'
    verbose = 'main'

    def ready(self):
        import main.signals
