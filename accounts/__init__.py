from django.utils.module_loading import autodiscover_modules

def autodiscover():
    autodiscover_modules('dapricot.store.accounts')

default_app_config = 'dapricot.store.accounts.apps.AccountsConfig'