from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib import messages
import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request
from django.views.generic.edit import FormView 
# Create your views here.


def Autoguy(request):
    if 'term' in request.GET:
        qs = Customer.objects.filter(name__icontains=request.GET.get('term'))
        names = list()
        for customer in qs:
            names.append(customer.name)
        return JsonResponse(names, safe=False)
    return render(request, 'testsearch.html')
class AutoCompleteView(FormView):
    def get(self,request,*args,**kwargs):
        data = request.GET
        name = data.get("term")
        if name:
            customers = Customer.objects.filter(name__icontains = name)
        else:
            customers = Customer.objects.all()
            results = []
        for customer in customers:
            customer_json = {}
            customer_json['id'] = customer.id
            customer_json['label'] = customer.name
            customer_json['value'] = customer.name
            results.append(customer_json)
            data = json.dumps(results)
            mimetype = 'application/json'
            
            return HttpResponse(data, mimetype)


def index(request):
    customers = Customer.objects.all()
    customercount = Customer.objects.all().count()
    inventcount = Inventory.objects.all().count()
    workordercount = Workorder.objects.all().count()
    context ={'customers':customers,
              'customercount':customercount,
              'inventcount':inventcount,
              'workordercount':workordercount
              }
    return render(request, 'index.html', context)


def Createcustomer(request):
    customer = Customer()
    inventorys = Inventory.objects.all()
    if request.method == "POST":
        
        if "createcustomer" in request.POST: 
            
            customer.name = request.POST["name"] 
            customer.number = request.POST["number"]
            
            inventoryid = request.POST["inventory_purchased"] 
            customer.inventory_purchased = get_object_or_404(Inventory,id=inventoryid)
            
            customer.quantity = request.POST["quantity"]
            
            inventory = Inventory.objects.get(id=inventoryid)
            inventory.quantity -= int(customer.quantity)
            inventory.save()

            customer.amount = request.POST["amount"]
            customer.balance = inventory.price - int(customer.amount)
            customer.addedby = request.user
            customer.save()
            
            messages.success(request, 'New Customer added Successfully!!')
            return redirect('index')
    context ={'inventorys':inventorys
              }
    return render(request, 'customer_create.html',context)

def Customerdetailfunc(request, pk):
    inventorys = Inventory.objects.all()
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        
        if "editcustomer" in request.POST: 
            
            customer.name = request.POST["name"] 
            customer.number = request.POST["number"]
            
            inventoryid = request.POST["inventory_purchased"] 
            customer.inventory_purchased = get_object_or_404(Inventory,id=inventoryid)
            
            customer.quantity = request.POST["quantity"]
            
            inventory = Inventory.objects.get(id=inventoryid)
            inventory.quantity -= int(customer.quantity)
            inventory.save()
            
            customer.amount = request.POST["amount"]
            customer.balance = inventory.price - int(customer.amount)
            customer.addedby = request.user
            customer.save()
            
            messages.warning(request, 'Customer updated Successfully!!')
            return redirect('index')
        
    context={'customer': customer, 'inventorys':inventorys}

    return render(request, 'customer_detail.html', context)

def inventory(request):
    inventorys = Inventory.objects.all()
    context ={'inventorys':inventorys
              }
    return render(request, 'inventory.html', context)

def technician(request):
    technicians = Technician.objects.all()
    context ={'technicians':technicians
              }
    return render(request, 'technician.html', context)

def workorder(request):
    workorders = Workorder.objects.all()
    context ={'workorders':workorders
              }
    return render(request, 'workorder.html', context)