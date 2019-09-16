from django.urls import path

from peanut.store import views

app_name    = 'peanut.store'
urlpatterns = [

# PROFILE VIEWS ---------------------------------------------------------------
    
    path('upd/', views.UpdateProfile, name='UpdateProfile'),
    
# PAYMENT METHOD VIEWS --------------------------------------------------------

    path('paymentmethod/', views.PaymentMethods, name='PaymentMethods'),
    path('paymentmethod/add/', views.AddPaymentMethod,
         name='AddPaymentMethod'),
    path('paymentmethod/<int:pk>/upd/', views.UpdatePaymentMethod,
         name='UpdatePaymentMethod'),
    path('paymentmethod/<int:pk>/spk/', views.SetDefaultPaymentMethod,
         name='SetDefaultPaymentMethod'),
    path('paymentmethod/<int:pk>/del/', views.DeletePaymentMethod,
         name='DeletePaymentMethod'),

    path('paymentmethod/<int:pk>/address/add/', views.AddBillingAddres,
         name='AddBillingAddress'),
    path('paymentmethod/<int:pk>/address/upd/', views.UpdateBillingAddres,
         name='UpdateBillingAddress'),
    path('paymentmethod/<int:pk>/address/del/', views.DeleteBillingAddres,
         name='DeleteBillingAddress'),

# SHIPPING CONTACT VIEWS ------------------------------------------------------

    path('shippingcontact/', views.ShippingContacts, name='ShippingContacts'),
    path('shippingcontact/add/', views.AddShippingContact,
         name='AddShippingContact'),
    path('shippingcontact/<int:pk>/upd/', views.UpdateShippingContact,
         name='UpdateShippingContact'),
    path('shippingcontact/<int:pk>/spk/', views.SetDefaultShippingContact,
         name='SetDefaultShippingContact'),
    path('shippingcontact/<int:pk>/del/', views.DeleteShippingContact,
         name='DeleteShippingContact'),
]
