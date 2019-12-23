from django.apps import AppConfig

class SimpleInventoryConfig(AppConfig):
    """Simple AppConfig which does not do automatic discovery."""

    name = 'dapricot.store.inventory'
    label = 'dapricot_store_inventory'
    verbose_name = "Django Apricot Store Inventory"

class InventoryConfig(SimpleInventoryConfig):
    """The default AppConfig for admin which does autodiscovery."""

    def ready(self):
        super().ready()
        self.module.autodiscover()