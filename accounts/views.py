from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from dapricot.store.accounts import forms

@login_required
def ProfileView(request):
    customer = request.user.get_vending_customer()

    return render(request, 'dapricot/store/accounts/profile.html',{
        "is_customer": False if customer is None else True,
        "header_title": "Profile"})


@login_required
def ChangePasswordView(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dapricot_store_accounts:profile')

        else:
            messages.error(request, 'Please correct the error below.')

    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'dapricot/store/accounts/change_password.html', {
        'form': form
    })

def SignupView(request):
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False) 
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')

            user.save()
            user = authenticate(request, username=email, password=raw_password)
            
            if user is not None:
                login(request, user)
            
            return redirect('dapricot_store_accounts:profile')

    else:
        form = forms.SignUpForm()

    return render(request, 'dapricot/store/accounts/signup.html', {'form': form,
                                                           "header_title": "Signup"})