from django.contrib.admin import AdminSite

class PeanutAdminSite(AdminSite):
    site_header = 'Peanut administrations'
    
site = PeanutAdminSite(name='peanut_admin')