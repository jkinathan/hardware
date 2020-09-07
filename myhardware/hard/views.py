from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.http import HttpResponseRedirect

# Create your views here.

def index(request):
    customers = Customer.objects.all()
    context ={'customers':customers
              }
    return render(request, 'customer.html', context)

def inventory(request):
    inventorys = Inventory.objects.all()
    context ={'inventorys':inventorys
              }
    return render(request, 'inventory.html', context)