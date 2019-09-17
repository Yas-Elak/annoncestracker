from django.apps import AppConfig
from django.apps.config import AppConfig


class MainConfig(AppConfig):
    name = 'main'



class GrapMainConfig(AppConfig):
    name = 'main'
    verbose_name = 'main main' # this name will display in the Admin. You may translate this value if you want using ugettex_lazy

    def ready(self):
        import main.signals.handlers