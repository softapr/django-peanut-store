from django.shortcuts               import render, redirect
from django.contrib.auth.decorators import login_required

from peanut.store.forms import PaymentMethodForm, PaymentMethodUpdateForm, AddressForm

@login_required
def BillingAddressView(request, action, pk=None):
    customer = request.user.get_vending_customer()
    method = [method for method in customer.payment_methods
              if method.method.pk==pk][0]

    if action == 'add':
        if request.method == 'POST':
            form = AddressForm(request.POST)

            if form.is_valid():
                address = form.save(commit=True)
                method.add_billing_address(address)
                address.save()
                return redirect('peanut_accounts:peanut.store:PaymentMethods')

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
                return redirect('peanut_accounts:peanut.store:PaymentMethods')

            return render(request, 'peanut/simple_form.html', {"form": form})

        else:
            form = AddressForm(instance=address_instance)
            return render(request, 'peanut/simple_form.html', {"form": form})
    
@login_required
def PaymentMethodsView(request, action=None, pk=None):
    customer = request.user.get_vending_customer()
    method = [method for method in customer.payment_methods
              if method.method.pk==pk]
    

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
                return redirect('peanut_accounts:peanut.store:PaymentMethods')

        else:
            form = PaymentMethodForm()
        
        return render(request, 'peanut/store/add_payment_method.html',
                      {'form': form,
                       "header_title": "Add Payment Method",
                       'action': 'add'})

    elif action == 'del':
        method[0].delete_payment_method()
        return redirect('peanut_accounts:peanut.store:PaymentMethods')

    elif action == 'spk':
        method[0].set_default()
        return redirect('peanut_accounts:peanut.store:PaymentMethods')

    elif action == 'upd':
        if request.method == 'POST':
            form = PaymentMethodUpdateForm(request.POST)
            
            if form.is_valid():
                data = form.cleaned_data
                method[0].update_payment_method(data['name'], 
                                             data['exp_month'], 
                                             data['exp_year'])
                
                return redirect('peanut_accounts:peanut.store:PaymentMethods')

        else:
            method_data = {'name': method[0].method.name,
                           'exp_month': method[0].method.exp_month,
                           'exp_year': method[0].method.exp_year}

            form = PaymentMethodUpdateForm(method_data)
        
        return render(request, 'peanut/simple_form.html',
                      {'form': form,
                       "header_title": "Update Payment Method",
                       "action": 'upd'})

    return render(request, 'peanut/store/manage_payments.html', {"customer": customer,
                                                                 "header_title": "Payment Methods"})
