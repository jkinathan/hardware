from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Inventory),
admin.site.register(JobType),
admin.site.register(Technician),
admin.site.register(Customer),
admin.site.register(Workorder)