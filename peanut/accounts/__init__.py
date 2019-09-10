from django.utils.module_loading import autodiscover_modules

def autodiscover():
    autodiscover_modules('peanut.accounts')

default_app_config = 'peanut.accounts.apps.AccountsConfig'