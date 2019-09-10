from django.apps import AppConfig

class SimpleAccountsConfig(AppConfig):
    """Simple AppConfig which does not do automatic discovery."""

    name = 'peanut.accounts'
    label = 'peanut_accounts'
    verbose_name = "Peanut Store Auth"

class AccountsConfig(SimpleAccountsConfig):
    """The default AppConfig for admin which does autodiscovery."""

    def ready(self):
        super().ready()
        self.module.autodiscover()