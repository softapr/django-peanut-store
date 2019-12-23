from django.utils.module_loading import autodiscover_modules

def autodiscover():
    autodiscover_modules('peanut.store')

default_app_config = 'peanut.store.apps.StoreConfig'