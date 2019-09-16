from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from peanut.accounts import views
from django.urls import reverse_lazy

app_name    = 'peanut_accounts'
urlpatterns = [
    path('', views.ProfileView, name='profile'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignupView, name='signup'),

    path('password_change/', views.ChangePasswordView, name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

if 'peanut.store' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('', include('peanut.store.urls')),
    ]