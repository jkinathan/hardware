from django.db import models
from django.utils import timezone
# Create your models here.

class Inventory(models.Model):
    name = models.CharField(max_length=100)
    itype = models.CharField(max_length=100)
    quantity = models.CharField(max_length=20)
    date_added = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))
    
    class Meta:
        ordering = ["-name"]
        verbose_name = 'Inventory'
        verbose_name_plural = 'Inventories'
        
    def __str__(self):
        return self.name

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
    amount = models.CharField(max_length=100)
    balance = models.CharField(max_length=100, blank=True)
    date = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))
    
    
    def __str__(self):
        return self.name

class Workorder(models.Model):
    MY_CHOICES = (
        ('a', 'Complete'),
        ('b', 'Incomplete'),
    )
    ordername = models.CharField(max_length=50)
    customer_name = models.ForeignKey(Customer, on_delete=models.CASCADE)
    jobtype = models.ForeignKey(JobType, on_delete=models.CASCADE)
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE)
    order_status = models.CharField(max_length=1, choices=MY_CHOICES)
    amount_paid = models.CharField(max_length=200)
    balance = models.CharField(max_length=100, blank=True)
    date = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))
    
    def __str__(self):
        return self.ordername