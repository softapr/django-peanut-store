from django import forms
from django.utils.translation import gettext_lazy as _

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