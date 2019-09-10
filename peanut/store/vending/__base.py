'''
Created on 7 sep. 2019

@author: orishiku
'''
import abc
from abc import ABCMeta

from peanut.store.models import Customer, PaymentMethod

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

        self.customer        = customer
        self.payment_methods = []
        
        if not created:
            methods = PaymentMethod.objects.filter(customer=self.customer)
            
            for m in methods:
                self.add_payment_method(m.name, m.reference, m.exp_month,
                                        m.exp_year, m.customer)

    @abc.abstractmethod
    def update_customer(self, user, phone=None):
        '''
        Update most of the data from user instance.
        '''
        self.customer.name  = user.get_full_name()
        self.customer.email = user.email
        self.customer.user  = user
        
        if phone is None:
            self.customer.phone=phone
            
        self.customer.save()

    @abc.abstractmethod
    def delete_customer(self):
        self.customer.delete()
    
    @abc.abstractmethod
    def add_payment_method(self, method):
        
        self.payment_methods.append(method)
        
    @abc.abstractmethod
    def set_default(self):
        PaymentMethod.objects.filter(customer=self.customer,
                                     is_default=True).update(is_default=False)
        self.method.is_default = True
        self.method.save()
        
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
        
        if self.created:
            methods_count = PaymentMethod.objects.filter(customer=customer).count()
            
            if methods_count == 1:
                self.set_default()

    @abc.abstractmethod
    def update_payment_method(self, name):
        self.method.name = name
        self.method.save()

    @abc.abstractmethod
    def delete_payment_method(self):
        if not self.method.is_default:
            self.method.delete()

    @abc.abstractmethod
    def add_billing_address(self):
        if not self.method.is_default:
            self.method.delete()
    
    @abc.abstractmethod
    def set_default(self):
        PaymentMethod.objects.filter(customer=self.method.customer,
                                     is_default=True).update(is_default=False)
        self.method.is_default = True
        self.method.save()
        