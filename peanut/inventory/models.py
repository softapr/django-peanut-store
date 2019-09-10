from django.db import models

class Address(models.Model):
    street1     = models.CharField(max_length=100)
    street2     = models.CharField(max_length=100)
    city        = models.CharField(max_length=50)
    state       = models.CharField(max_length=50)
    country     = models.CharField(max_length=2)
    postalcode  = models.CharField(max_length=5)
    residential = models.BooleanField(default=True)