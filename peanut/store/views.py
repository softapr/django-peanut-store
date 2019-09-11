from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from peanut.store.forms import PaymentMethodForm, PaymentMethodUpdateForm, AddressForm, CustomerForm

@login_required
def ProfileView(request, action):
    customer = request.user.get_vending_customer()
    customer_data = {'first_name': request.user.first_name,
                     'last_name': request.user.last_name,
                     'phone': customer.customer.phone,
                     'email': request.user.email}
    
    if action == 'upd':
        if request.method == 'POST':
            form = CustomerForm(request.POST)

            if form.is_valid():
                customer.update_customer(form.cleaned_data)

            return redirect('peanut_accounts:profile')

        else:
            customer_data['phone'] = ('' if customer_data['phone'] == '+520000000000'
                                         else customer_data['phone'])
            form = CustomerForm(customer_data)

        return render(request, 'peanut/simple_form.html',
                      {'form': form})

@login_required
def PaymentMethodsView(request, action=None, pk=None):
    customer = request.user.get_vending_customer()
    
    if action == 'add':
        if request.method == 'POST':
            form = PaymentMethodForm(request.POST)
            
            if form.is_valid():
                data = form.cleaned_data
                api_data = {"token": data['token_id'],
                            "customer": customer.customer.api_id}
                customer.add_payment_method(data['name'],
                                            data['reference'], 
                                            data['exp_month'], 
                                            data['exp_year'],
                                            api_data)
            return redirect('peanut_accounts:peanut_store:payment_methods')

        else:
            form = PaymentMethodForm()
        
        return render(request, 'peanut/store/add_payment_method.html',
                      {'form': form, 'action': 'add'})

    elif action == 'del':
        for method in customer.payment_methods:
            if method.method.pk == pk:
                method.delete_payment_method()
                return redirect('peanut_accounts:peanut_store:payment_methods')

    elif action == 'spk':
        for method in customer.payment_methods:
            if method.method.pk == pk:
                method.set_default()
                return redirect('peanut_accounts:peanut_store:payment_methods')

    elif action == 'upd':
        method = None
        for method in customer.payment_methods:
            if method.method.pk == pk:
                method_data = method

        if request.method == 'POST':
            form = PaymentMethodUpdateForm(request.POST)
            
            if form.is_valid():
                data = form.cleaned_data
                method.update_payment_method(data['name'], 
                                             data['exp_month'], 
                                             data['exp_year'])
                
            return redirect('peanut_accounts:peanut_store:payment_methods')

        else:
            method_data = {'name': method.method.name,
                           'exp_month': method.method.exp_month,
                           'exp_year': method.method.exp_year}

            form = PaymentMethodUpdateForm(method_data)
        
        return render(request, 'peanut/store/add_payment_method.html',
                      {'form': form, 'action': 'upd'})

    else:
        return render(request, 'peanut/store/manage_payments.html', {"customer": customer})

@login_required
def BillingAddresView(request, action, pk):
    customer = request.user.get_vending_customer()
    
    if action == 'add':
        if request.method == 'POST':
            form = AddressForm(request.POST)

            if form.is_valid():
                address = form.save(commit=True)

                for method in customer.payment_methods:
                    if method.method.pk == pk:
                        method.add_billing_address(address)

                address.save()
                return redirect('peanut_accounts:peanut_store:payment_methods')

            return render(request, 'peanut/simple_form.html', {"form": form})

        else:
            form = AddressForm()
            return render(request, 'peanut/simple_form.html', {"form": form})

    elif action == 'upd':
        address_instance = None
        for method in customer.payment_methods:
            if method.method.pk == pk:
                address_instance = method.method.address
                
        if request.method == 'POST':
            form = AddressForm(request.POST, instance=address_instance)

            if form.is_valid():
                address = form.save(commit=True)

                for method in customer.payment_methods:
                    if method.method.pk == pk:
                        method.update_billing_address(address)

                address.save()
                return redirect('peanut_accounts:peanut_store:payment_methods')

            return render(request, 'peanut/simple_form.html', {"form": form})

        else:
            form = AddressForm(instance=address_instance)
            return render(request, 'peanut/simple_form.html', {"form": form})

    else:
        return render(request, 'peanut/store/manage_payments.html')
