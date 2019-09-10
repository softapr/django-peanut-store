from django.apps import AppConfig

class SimpleStoreConfig(AppConfig):
    """Simple AppConfig which does not do automatic discovery."""

    name = 'peanut.store'
    label = 'peanut_store'
    verbose_name = "Peanut Store"

class StoreConfig(SimpleStoreConfig):
    """The default AppConfig for admin which does autodiscovery."""

    def ready(self):
        super().ready()
        self.module.autodiscover()