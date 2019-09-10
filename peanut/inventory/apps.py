from django.apps import AppConfig

class SimpleInventoryConfig(AppConfig):
    """Simple AppConfig which does not do automatic discovery."""

    name = 'peanut.inventory'
    label = 'peanut_inventory'
    verbose_name = "Peanut Store Inventory"

class InventoryConfig(SimpleInventoryConfig):
    """The default AppConfig for admin which does autodiscovery."""

    def ready(self):
        super().ready()
        self.module.autodiscover()