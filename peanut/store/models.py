from django.db import models
from django.contrib.auth import get_user_model

COUNTRY_OPTIONS = (
    ('MX', 'Mexico'),)

CURRENCY_OPTIONS = (
    ('MXN', 'Mexian Pesos'),)

PAYMENT_METHOD_TYPE_OPTIONS = (
    ('card','Card'),
    ('oxxo_cash','Oxxo Cash'),
    ('banorte','Banorte'))

class Customer(models.Model):
    api_id = models.CharField(max_length=21, unique=True, blank=True,
                              null=True, editable=False)
    name   = models.CharField(max_length=50)
    phone  = models.CharField(max_length=50, null=True)
    email  = models.EmailField(unique=True)
    user   = models.OneToOneField(get_user_model(),
                                  on_delete=models.SET_NULL,
                                  null=True, editable=False)

class PaymentMethod(models.Model):
    api_id     = models.CharField(max_length=21, 
                                  unique=True,
                                  blank=True,
                                  null=True)
    type       = models.CharField(choices=PAYMENT_METHOD_TYPE_OPTIONS,
                                  max_length=20,default='card')
    created_at = models.DateField(auto_now_add=True)
    reference  = models.CharField(max_length=50)
    exp_month  = models.CharField(max_length=2)
    exp_year   = models.CharField(max_length=4)
    name       = models.CharField(max_length=50)
    is_default = models.BooleanField(default=False)
    brand      = models.CharField(max_length=20, null=True)
    customer   = models.ForeignKey('Customer', on_delete=models.CASCADE)
    address    = models.ForeignKey('Address', 
                                   on_delete=models.SET_NULL,
                                    null=True)

###############################################################################

class Address(models.Model):
    street1     = models.CharField(max_length=100)
    street2     = models.CharField(max_length=100)
    city        = models.CharField(max_length=50)
    state       = models.CharField(max_length=50)
    country     = models.CharField(max_length=2, choices=COUNTRY_OPTIONS,
                                   default='MX')
    postalcode  = models.CharField(max_length=5)
    residential = models.BooleanField(default=True)