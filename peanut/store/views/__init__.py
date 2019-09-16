from peanut.store.views import PaymentMethod, ShippingContact, Profile as _Profile

# PROFILE VIEWS ---------------------------------------------------------------

def Profile(request):
    return _Profile.ProfileView(request)

def UpdateProfile(request):
    return _Profile.ProfileView(request, 'upd')

# PAYMENT METHOD VIEWS --------------------------------------------------------

def PaymentMethods(request):
    return PaymentMethod.PaymentMethodsView(request)

def AddPaymentMethod(request):
    return PaymentMethod.PaymentMethodsView(request, 'add')

def UpdatePaymentMethod(request, pk):
    return PaymentMethod.PaymentMethodsView(request, 'upd', pk)

def SetDefaultPaymentMethod(request, pk):
    return PaymentMethod.PaymentMethodsView(request, 'spk', pk)

def DeletePaymentMethod(request, pk):
    return PaymentMethod.PaymentMethodsView(request, 'del', pk)

def AddBillingAddres(request, pk):
    return PaymentMethod.BillingAddressView(request, 'add', pk)

def UpdateBillingAddres(request, pk):
    return PaymentMethod.BillingAddressView(request, 'upd', pk)

def DeleteBillingAddres(request, pk):
    return PaymentMethod.BillingAddressView(request, 'del', pk)

# SHIPPING CONTACT VIEWS ------------------------------------------------------

def ShippingContacts(request):
    return ShippingContact.ShippingContactView(request)

def AddShippingContact(request):
    return ShippingContact.ShippingContactView(request, 'add')

def UpdateShippingContact(request):
    return ShippingContact.ShippingContactView(request, 'upd')

def SetDefaultShippingContact(request):
    return ShippingContact.ShippingContactView(request, 'spk')

def DeleteShippingContact(request):
    return ShippingContact.ShippingContactView(request, 'del')
