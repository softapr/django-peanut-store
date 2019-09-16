from django.shortcuts               import render, redirect
from django.contrib.auth.decorators import login_required

from peanut.store.forms import ShippingContactForm

@login_required
def ShippingContactView(request, action=None):
    customer = request.user.get_vending_customer()
              
    if action == 'add':
        if request.method == 'POST':
            form = ShippingContactForm(request.POST)
            
            if form.is_valid():
                data = form.cleaned_data
                address_data = {"street1": data.street1,
                                "street2": data.street2,
                                "city": data.city,
                                "state": data.state,
                                "country": data.country,
                                "postalcode": data.postalcode,
                                "residential": data.residential}
                customer.add_shipping_address(data.phone, data.name, data. between_streets,
                                              address_data)
                  
                return redirect('peanut_accounts:peanut_store:ShippingContacts')
            
            return render(request, 'peanut/simple_form.html', {"form": form})
        else:
            form = ShippingContactForm()
        
            return render(request, 'peanut/simple_form.html', {"form": form})

    else:   
        return render(request, 'peanut/store/manage_contacts.html')
