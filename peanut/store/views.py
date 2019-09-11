from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from peanut.inventory.forms import AddressForm
from peanut.inventory.models import Address
from peanut.store.forms import PaymentMethodForm

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
                      {'form': form})

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

    else:
        return render(request, 'peanut/store/manage_payments.html', {"customer": customer})