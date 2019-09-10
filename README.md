# django-peanut-store

***
## Installation

```python
INSTALLED_APPS = [
    ...

    'peanut.accounts',
    'peanut.inventory',
    'peanut.store',
]

AUTH_USER_MODEL = 'peanut_accounts.User'
CONEKTA_PRIVATE_KEY = 'conekta_api_private_key'
PAYMENT_API = 'conekta'
```

### Recomended settings

```python
LOGIN_URL          = 'peanut_accounts:login'
LOGIN_REDIRECT_URL = 'peanut_accounts:profile'
```