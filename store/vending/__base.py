'''
Created on 7 sep. 2019

@author: orishiku
'''
import abc
from abc import ABCMeta

from peanut.store.models import Customer, PaymentMethod, ShippingContact, Address
from django.contrib.gis.geoip2.resources import City

class CustomerBaseObject:
    '''
    classdocs
    '''
    __metaclass__ = ABCMeta
    usable        = True
    
    def __init__(self, user, phone=None):
        '''
        Constructor 
        '''
        if phone is None:
            customer, created = Customer.objects.get_or_create(
                name=user.get_full_name(),
                email=user.email,
                user=user)

        else:
            customer, created = Customer.objects.get_or_create(
                name=user.get_full_name(),
                email=user.email,
                phone=phone,
                user=user)

        self.customer         = customer
        self.payment_methods  = []
        self.shipping_address = []

        if not created:
            methods = PaymentMethod.objects.filter(customer=self.customer, is_default=False)
            default_method = PaymentMethod.objects.filter(customer=self.customer, is_default=True)

            if default_method.count() == 0 and methods.count() > 0:
                self.set_default_payment_method(methods.last())

            elif default_method.count() > 1:
                self.set_default_payment_method(default_method[0])

            for m in default_method:
                self.add_payment_method(m.name, m.reference, m.exp_month,
                                        m.exp_year, m.customer)

            for m in methods:
                self.add_payment_method(m.name, m.reference, m.exp_month,
                                        m.exp_year, m.customer)

    @abc.abstractmethod
    def update_customer(self, data):
        '''
        Update most of the data from user instance.
        '''
        self.customer.user.first_name = data['first_name']
        self.customer.user.last_name = data['last_name']
        self.customer.user.email = data['email']
        self.customer.user.save()
        
        self.customer.name  = self.customer.user.get_full_name()
        self.customer.email = self.customer.user.email
        self.customer.phone=data['phone']
        
        if data['phone']=="" or data['phone']=='' or data['phone'] is None:
            self.customer.phone='+520000000000'
            
        self.customer.save()

    @abc.abstractmethod
    def delete_customer(self):
        self.customer.delete()
    
    @abc.abstractmethod
    def add_payment_method(self, method):
        self.payment_methods.append(method)

    @abc.abstractmethod
    def set_default_payment_method(self, method):
        PaymentMethod.objects.filter(customer=self.customer,
                                     is_default=True).update(is_default=False)
        method.is_default = True
        method.save()
        
    @abc.abstractmethod
    def add_shipping_address(self, address):
        self.shipping_address.append(address)

    @abc.abstractmethod
    def set_default_shipping_address(self, address):
        ShippingContact.objects.filter(customer=self.customer,
                                       is_default=True).update(is_default=False)
        address.is_default = True
        address.save()
        
class ShippingContactBaseObject:
    '''
    classdocs
    '''
    __metaclass__ = ABCMeta
    usable        = True
    
    def __init__(self, phone, name, between_streets, address_data, customer):
        '''
        Constructor
        '''
        try:
            contact = ShippingContact.objects.get(phone=phone,
                                                  name=name,
                                                  between_streets=between_streets,
                                                  customer=customer)
            self.created = False

        except:
            address = Address.objects.create(street1=address_data['street1'],
                                             street2=address_data['street2'],
                                             city=address_data['city'],
                                             state=address_data['state'],
                                             country=address_data['country'],
                                             postalcode=address_data['postalcode'],
                                             residential=address_data['residential'])

            contact = ShippingContact.objects.create(phone=phone,
                                                     name=name,
                                                     between_streets=between_streets,
                                                     address=address,
                                                     customer=customer)

            self.created = True

        self.contact = contact
    
    @abc.abstractmethod
    def update_shipping_contact(self, phone, name, between_streets, address_data):
        self.contact.address.street1 = address_data['street1']
        self.contact.address.street2 = address_data['street2']
        self.contact.address.city = address_data['city']
        self.contact.address.state = address_data['state']
        self.contact.address.country = address_data['country']
        self.contact.address.postalcode = address_data['postalcode']
        self.contact.address.residential = address_data['residential']
        self.contact.address.save()
        
        self.contact.phone = phone
        self.contact.name = name
        self.contact.between_streets = between_streets
        self.contact.save()

    @abc.abstractmethod
    def delete_shipping_contact(self):
        deleted = True
        contact_api_id = self.contact.api_id
        self.contact.delete()
        
        return deleted, contact_api_id

    @abc.abstractmethod
    def set_default(self):
        ShippingContact.objects.filter(customer=self.contact.customer,
                                     is_default=True).update(is_default=False)
        self.contact.is_default = True
        self.contact.save()

class PaymentMethodBaseObject:
    '''
    classdocs
    '''
    __metaclass__ = ABCMeta
    usable        = True
    
    def __init__(self, name, reference, exp_month, exp_year, customer,
                 api_data=None, m_type=None):
        '''
        Constructor
        
        @todo: this constructor works with credit cards, if needed other type
               of payment method this would need a totally new constructor.
        
        @param api_data: usage will be defined in the implementation.
        @param m_type: if None default value will be 'card'.
        '''
        if m_type is None:
            method, created = PaymentMethod.objects.get_or_create(name=name,
                                                         reference=reference,
                                                         customer=customer,
                                                         exp_month=exp_month,
                                                         exp_year=exp_year)

        else:
            method, created = PaymentMethod.objects.get_or_create(name=name,
                                                         reference=reference,
                                                         customer=customer,
                                                         type=m_type,
                                                         exp_month=exp_month,
                                                         exp_year=exp_year)

        self.created  = created
        self.method   = method

    @abc.abstractmethod
    def update_payment_method(self, name, exp_month, exp_year):
        self.method.name = name
        self.method.exp_month = exp_month
        self.method.exp_year = exp_year
        self.method.save()

    @abc.abstractmethod
    def delete_payment_method(self):
        '''
        @return: returns tuple of deleted bool & method_api_id of deleted method
        '''
        methods = PaymentMethod.objects.filter(customer=self.method.customer)
        method_api_id = None
        new_default_method = None
        
        if methods.count() > 1:
            self.__remove_billing_address()
            if self.method.is_default:
                methods = [method 
                           for method in methods 
                           if method.api_id != self.method.api_id]
                new_default_method = methods[0]

            method_api_id = self.method.api_id
            
            if new_default_method != None:
                self.method.delete()
                self.method = new_default_method
                self.set_default()
                    
            else:
                self.method.delete()

            self.usable = False
            deleted = True
            
        else:
            deleted = False

        return deleted, method_api_id

    @abc.abstractmethod
    def add_billing_address(self, address):
        self.method.address = address
        self.method.save()
        
    @abc.abstractmethod
    def update_billing_address(self):
        pass

    def __remove_billing_address(self):
        self.method.address.delete()

    @abc.abstractmethod
    def set_default(self):
        PaymentMethod.objects.filter(customer=self.method.customer,
                                     is_default=True).update(is_default=False)
        self.method.is_default = True
        self.method.save()
        