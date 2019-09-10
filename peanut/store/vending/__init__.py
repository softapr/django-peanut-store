'''
Created on 7 sep. 2019

@author: orishiku
'''
from django.conf import settings
from peanut.store.vending import __conekta

def __GetAPI():
    if settings.PAYMENT_API == 'conekta':
        return __conekta

def CustomerObject(user, phone=None):
    customer = __GetAPI().Customer(user, phone)
    return customer

def PaymentMethodObject(name, reference, exp_month, exp_year, api_data,
                        m_type=None):
    method = __GetAPI().PaymentMethod(name, reference, exp_month, exp_year,
                                      api_data, m_type)
    return method