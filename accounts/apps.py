from django.apps import AppConfig

class SimpleAccountsConfig(AppConfig):
    """Simple AppConfig which does not do automatic discovery."""

    name = 'dapricot.store.accounts'
    label = 'dapricot.store_accounts'
    verbose_name = "Django Apricot Store Accounts"

class AccountsConfig(SimpleAccountsConfig):
    """The default AppConfig for admin which does autodiscovery."""

    def ready(self):
        super().ready()
        self.module.autodiscover()