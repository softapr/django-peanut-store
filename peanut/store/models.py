from django.db import models
from django.conf import settings

CURRENCY_OPTIONS = (
    ('MXN', 'Mexian Pesos'),)

PAYMENT_METHOD_TYPE_OPTIONS = (
    ('card','Card'),
    ('oxxo_cash','Oxxo Cash'),
    ('banorte','Banorte'))

class Customer(models.Model):
    api_id = models.CharField(max_length=21,
                              unique=True,
                              blank=True,
                              null=True)
    name   = models.CharField(max_length=50)
    phone  = models.CharField(max_length=50)
    email  = models.EmailField(unique=True)
    user   = models.OneToOneField(settings.AUTH_USER_MODEL,
                                  on_delete=models.SET_NULL,
                                  null=True)

class PaymentMethod(models.Model):
    api_id     = models.CharField(max_length=21, 
                                  unique=True,
                                  blank=True,
                                  null=True)
    type       = models.CharField(choices=PAYMENT_METHOD_TYPE_OPTIONS, max_length=20, default='card')
    created_at = models.DateField(auto_now_add=True)
    reference  = models.CharField(max_length=50)
    exp_month  = models.CharField(max_length=2)
    exp_year   = models.CharField(max_length=4)
    name       = models.CharField(max_length=50)
    is_default = models.BooleanField(default=False)
    brand      = models.CharField(max_length=20, null=True)
    customer   = models.ForeignKey('Customer', on_delete=models.CASCADE)
    address    = models.ForeignKey('peanut_inventory.Address', 
                                   on_delete=models.SET_NULL,
                                    null=True)

