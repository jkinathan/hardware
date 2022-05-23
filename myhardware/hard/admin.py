from django.contrib import admin
from .models import *
# Register your models here.

class InventoryAdmin(admin.ModelAdmin):
    list_display = ['name','picture_tag','inventory_Type', 'location','quantity','price']

class WorkorderAdmin(admin.ModelAdmin):
    list_display = ['ordername','customer_name','jobtype', 'technician','order_status']

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name','number','inventory_purchased', 'quantity','date']

admin.site.register(Inventory,InventoryAdmin),
admin.site.register(JobType),
admin.site.register(Technician),
admin.site.register(Customer,CustomerAdmin),
admin.site.register(ReturnJobs),
admin.site.register(Workorder,WorkorderAdmin)
admin.site.register(Supplier),