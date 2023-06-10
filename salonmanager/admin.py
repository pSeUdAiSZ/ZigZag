from django.contrib import admin

# Register your models here.
from .models import Appointment,Service,StaffMember,Branch,Customer
admin.site.register(Appointment)
admin.site.register(Service)
admin.site.register(StaffMember)
admin.site.register(Branch)
admin.site.register(Customer)