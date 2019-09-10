from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from peanut.accounts import forms

@login_required
def ProfileView(request):
    customer = request.user.get_vending_customer()

    return render(request, 'peanut/accounts/profile.html',{
        "is_customer": False if customer is None else True})
    
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
            
            return redirect('peanut_accounts:profile')

    else:
        form = forms.SignUpForm()

    return render(request, 'peanut/accounts/signup.html', {'form': form})