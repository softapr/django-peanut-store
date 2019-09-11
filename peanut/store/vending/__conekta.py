'''
Created on 7 sep. 2019

@author: orishiku
'''
import conekta
from django.conf import settings

from peanut.store.vending.__base import CustomerBaseObject, PaymentMethodBaseObject

class Customer(CustomerBaseObject):
    '''
    classdocs
    '''

    def __init__(self, user, phone=None):
        '''
        Constructor
        '''
        CustomerBaseObject.__init__(self, user, phone)
        conekta.api_key = settings.CONEKTA_PRIVATE_KEY

        if self.customer.api_id is None:
            try:
                customer = conekta.Customer.create({
                    "name": self.customer.name,
                    "email": self.customer.email})
                self.customer.api_id = customer.id
                self.customer.save()

            except conekta.ConektaError as e:
                self.usable = False
                raise Exception(e)

        else:
            self.usable = False if self.conekta_customer is None else True

    @property
    def conekta_customer(self):
        try:
            customer = conekta.Customer.find(self.customer.api_id)
            return customer

        except Exception as e:
            self.usable = False
            raise Exception(e)

        return None

    def update_customer(self, user, phone):
        '''
        Update most of the data from user instance.
        '''
        super(Customer, self).update_customer(user, phone=None)
        data = {"name": user.get_full_name(),
                "email": user.email,
                "phone": phone}

        try:
            self.conekta_customer.update(data)

        except Exception as e:
            raise Exception(e)

    def delete_customer(self):
        super(Customer, self).delete_customer()
        try:
            if not self.method.is_default:
                self.conekta_customer.delete()

        except Exception as e:
            raise Exception(e)

    def add_payment_method(self, name, reference, exp_month, exp_year,
                           api_data=None, m_type=None):
        method = PaymentMethod(name, reference, exp_month, exp_year,
                               self.customer, api_data, m_type)
        
        super(Customer, self).add_payment_method(method)
'''
    def set_default_payment_method(self, method):
        ''
        @todo: set default payment source in conekta
        ''
        super(Customer, self).set_default_payment_method(method)
        '''
class PaymentMethod(PaymentMethodBaseObject):
    '''
    classdocs
    '''

    def __init__(self, name, reference, exp_month, exp_year, customer,
                 api_data=None, m_type=None):
        '''
        Constructor
        '''
        PaymentMethodBaseObject.__init__(self, name, reference, exp_month,
                                         exp_year, customer, api_data, m_type)
        
        if self.created:
            try:
                customer = conekta.Customer.find(api_data["customer"])
                method = customer.createPaymentSource({
                    "type": self.method.type,
                    "token_id": api_data["token"]})
                self.method.api_id = method.id
                self.method.brand = method.brand
                self.method.save()
    
            except Exception as e:
                self.usable = False
                raise Exception(e)

    def conekta_method(self, method_id=None):
        try:
            customer = conekta.Customer.find(self.method.customer.api_id)
            methods  = customer.payment_sources
            
            for method in methods:
                if ((method_id is None and method.id==self.method.api_id) or
                    (method_id is not None and method.id==method_id)):
                    return method

            self.usable = False

        except Exception as e:
            self.usable = False
            raise Exception(e)

        return None

    def update_payment_method(self, name, exp_month, exp_year):
        super(PaymentMethod, self).update_payment_method(name,
                                                         exp_month,
                                                         exp_year)

        try:
            self.conekta_method().update({"name": self.method.name,
                                        "exp_month": self.method.exp_month,
                                        "exp_year": self.method.exp_year})

        except Exception as e:
            raise Exception(e)

    def delete_payment_method(self):
        deleted, method_api_id = super(PaymentMethod, self).delete_payment_method()

        try:
            if deleted:
                self.conekta_method(method_api_id).delete()
            
        except Exception as e:
            raise Exception(e)
    
    def set_default(self):
        '''
        @todo: set default payment source in conekta
        '''
        super(PaymentMethod, self).set_default()

    def add_billing_address(self, address):
        try:
            self.conekta_method().update({
                "address": {
                    "street1": address.street1,
                    "street2": address.street2,
                    "city": address.city,
                    "state": address.state,
                    "country": address.country,
                    "postal_code": address.postalcode}
                })
            super(PaymentMethod, self).add_billing_address(address)
            
        except Exception as e:
            raise Exception(e)
        
    def update_billing_address(self, address):
        
        try:
            self.conekta_method().update({
                "address": {
                    "street1": address.street1,
                    "street2": address.street2,
                    "city": address.city,
                    "state": address.state,
                    "country": address.country,
                    "postal_code": address.postalcode}
                })
            super(PaymentMethod, self).update_billing_address()
            
        except Exception as e:
            raise Exception(e)
