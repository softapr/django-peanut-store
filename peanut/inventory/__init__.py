from django.utils.module_loading import autodiscover_modules

def autodiscover():
    autodiscover_modules('peanut.inventory')

default_app_config = 'peanut.inventory.apps.InventoryConfig'