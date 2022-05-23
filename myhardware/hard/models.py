from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
# Create your models here.

class Inventory(models.Model):
    TYPES = (
        ('Elements', 'Elements'),
        ('Nozzles', 'Nozzles'),
        ('Rotarheads', 'Rotarheads'),
        ('Valves', 'Valves'),
        ('Pumps', 'Pumps'),
        ('Camplates', 'Camplates'),
        ('Feedpumps', 'Feedpumps'),
        ('Housings', 'Housings'),
        ('Switches', 'Switches'),
        ('Gasket Kit', 'Gasket Kit'),
        ('Air Cleaners', 'Air Cleaners'),
        ('Pistons', 'Pistons'),
        ('Bearings', 'Bearings'),
        ('Brake Pads', 'Brake Pads'),
        ('Rings', 'Rings'),
        ('Piece & Main', 'Piece & Main'),
        ('Filters', 'Filters'),
        ('Oil Seals', 'Oil Seals'),
    )
    LOCATION = (
        ('Home Store', 'Home Store'),
        ('Work Store', 'Work Store'),
    )
    name = models.CharField(max_length=100)
    picture = models.ImageField(null=True, blank=True,upload_to='images/')
    inventory_Type = models.CharField(max_length=50, choices=TYPES,blank=True)
    i_type = models.CharField(max_length=100,blank=True)
    engine = models.CharField(max_length=100,blank=True)
    stamping_number = models.CharField(max_length=100,blank=True)
    part_number = models.CharField(max_length=100,blank=True)
    millimeter = models.CharField(max_length=100,blank=True)
    cut = models.CharField(max_length=100,blank=True)
    calibration = models.CharField(max_length=100,blank=True)
    direction_side = models.CharField(max_length=100,blank=True)
    holes = models.CharField(max_length=100,blank=True)
    voltage = models.CharField(max_length=100,blank=True)
    location = models.CharField(max_length=50, choices=LOCATION,blank=True)
    quantity = models.IntegerField()
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    #date_added = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))
    
    class Meta:
        ordering = ["-name"]
        verbose_name = 'Inventory'
        verbose_name_plural = 'Inventories'
        
    def picture_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.picture.url))
    picture_tag.short_description = 'Picture'
       
    # def serialize(self):
    #     return self.__dict__
    def __str__(self):
        return self.name
# class InventoryType(models.Model):
#     name = models.CharField(max_length=100)
    
#     def __str__(self):
#         return self.name
class JobType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=255)
    
    def __str__(self):
        return self.name

class Technician(models.Model):
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=15)
    date = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))
    
    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=15)
    inventory_purchased = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1,null=False)
    amount = models.CharField(max_length=100)
    balance = models.CharField(max_length=100, blank=True)
    date = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))
    addedby = models.ForeignKey(User,on_delete=models.PROTECT, default=1)
    
    def get_absolute_url(self):
        return reverse("customerdetail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.name

class Workorder(models.Model):
    MY_CHOICES = (
        ('Complete', 'Complete'),
        ('Incomplete', 'Incomplete'),
    )
    ordername = models.CharField(max_length=50)
    customer_name = models.ForeignKey(Customer, on_delete=models.CASCADE)
    jobtype = models.ForeignKey(JobType, on_delete=models.CASCADE)
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE)
    order_status = models.CharField(max_length=20, choices=MY_CHOICES)
    amount_paid = models.CharField(max_length=200)
    balance = models.CharField(max_length=100, blank=True)
    date = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))
    
    def __str__(self):
        return self.ordername

class ReturnJobs(models.Model):
    MY_CHOICES = (
        ('Complete', 'Complete'),
        ('Incomplete', 'Incomplete'),
    )
    jobname = models.CharField(max_length=100, blank=False)
    customer_name = models.ForeignKey(Customer, on_delete=models.CASCADE)
    complaint = models.TextField(max_length=200, blank=True)
    partnumber = models.CharField(max_length=50, blank=True)
    datedone = models.DateTimeField()
    status = models.CharField(max_length=20, choices=MY_CHOICES)
    
    def __str__(self):
        return self.jobname
    
class Supplier(models.Model):
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    item = models.CharField(max_length=100)
    itype = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name