from django.urls import path

from peanut.store.views import PaymentMethodsView, BillingAddresView, ProfileView

app_name    = 'peanut_store'
urlpatterns = [
    path('paymentmethod/', PaymentMethodsView, name='payment_methods'),
    path('paymentmethod/<action>/', PaymentMethodsView, name='payment_method'),
    path('paymentmethod/<int:pk>/<action>/', PaymentMethodsView, name='payment_method'),
    path('paymentmethod/<int:pk>/address/<action>', BillingAddresView, name='payment_methods_address'),

    path('<action>/', ProfileView, name='profile'),
]
