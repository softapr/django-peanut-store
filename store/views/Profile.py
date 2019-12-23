from django.shortcuts               import render, redirect
from django.contrib.auth.decorators import login_required

from peanut.store.forms import CustomerForm

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
                      {'form': form,
                       "header_title": "Update Profile"})