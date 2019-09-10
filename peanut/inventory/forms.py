from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from peanut.inventory.models import Address

class AddressForm(ModelForm):
    
    class Meta:
        model = Address
        fields = '__all__'