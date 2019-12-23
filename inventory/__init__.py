from django.utils.module_loading import autodiscover_modules

def autodiscover():
    autodiscover_modules('dapricot.store.inventory')

default_app_config = 'dapricot.store.inventory.apps.InventoryConfig'