from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model

class SignUpForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name')
        field_classes = {'email': UsernameField}