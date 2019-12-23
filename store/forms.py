from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from peanut.store.models import Address, Customer, ShippingContact

class PaymentMethodForm(forms.Form):
    token_id = forms.CharField(widget=forms.HiddenInput(),
                               required=False)
    name = forms.CharField(label=_('Nombre del tarjetahabiente'),
                           max_length=25,
                           widget=forms.TextInput(attrs={
                               'size': 25,
                               'maxlength': 25,
                               'data-conekta': 'card[name]'}))
    reference = forms.CharField(label=_('Numero de tarjeta de credito'),
                                max_length=26,
                                widget=forms.TextInput(attrs={
                                    'size': 26,
                                    'maxlength': 26,
                                    'data-conekta': 'card[number]'}))
    card_cvc = forms.CharField(label='CVC',
                               max_length=4, 
                               widget=forms.TextInput(attrs={
                                   'size': 4,
                                   'maxlength': 4,
                                   'data-conekta': 'card[cvc]'}))
    exp_month = forms.CharField(label='Fecha de expiracion (MM/AAAA)',
                               max_length=2, 
                               widget=forms.TextInput(attrs={
                                   'size': 2,
                                   'maxlength': 2,
                                   'data-conekta': 'card[exp_month]'}))
    exp_year = forms.CharField(label='/',
                               max_length=4, 
                               widget=forms.TextInput(attrs={
                                   'size': 4,
                                   'maxlength': 4,
                                   'data-conekta': 'card[exp_year]'}))

class PaymentMethodUpdateForm(forms.Form):
    name = forms.CharField(label=_('Nombre del tarjetahabiente'),
                           max_length=25,
                           widget=forms.TextInput(attrs={
                               'size': 25,
                               'maxlength': 25,
                               'data-conekta': 'card[name]'}))
    exp_month = forms.CharField(label='Fecha de expiracion (MM/AAAA)',
                               max_length=2, 
                               widget=forms.TextInput(attrs={
                                   'size': 2,
                                   'maxlength': 2,
                                   'data-conekta': 'card[exp_month]'}))
    exp_year = forms.CharField(label='/',
                               max_length=4, 
                               widget=forms.TextInput(attrs={
                                   'size': 4,
                                   'maxlength': 4,
                                   'data-conekta': 'card[exp_year]'}))

class ShippingContactForm(forms.Form):
    name            = forms.CharField(max_length=50)
    phone           = forms.CharField(max_length=50)
    between_streets = forms.CharField(max_length=100)
    street1         = forms.CharField(max_length=100)
    street2         = forms.CharField(max_length=100)
    city            = forms.CharField(max_length=50)
    state           = forms.CharField(max_length=50)
    country         = forms.CharField(max_length=2)
    postalcode      = forms.CharField(max_length=5)
    residential     = forms.BooleanField()

class AddressForm(ModelForm):
    
    class Meta:
        model = Address
        fields = '__all__'

class CustomerForm(forms.Form):
    first_name  = forms.CharField(label=_('first name'), max_length=30)
    last_name   = forms.CharField(label=_('last name'), max_length=30)
    phone       = forms.CharField(max_length=50, required=False)
    email       = forms.EmailField(label=_('email address'))