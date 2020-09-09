from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib import messages
import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request
from django.views.generic.edit import FormView 
from django.contrib.auth.decorators import login_required
# Create your views here.


def Autoguy(request):
    if 'term' in request.GET:
        qs = Customer.objects.filter(name__icontains=request.GET.get('term')).distinct()
        names = list()
        
        for customer in qs:
            names.append(customer.name) if customer.name not in names else names
        return JsonResponse(names, safe=False)
    return render(request, 'customer_create.html')

@login_required
def index(request):
    if request.user.is_staff:
        customers = Customer.objects.all()
        inventorys = Inventory.objects.all()
        customercount = Customer.objects.all().count()
        inventcount = Inventory.objects.all().count()
        workordercount = Workorder.objects.all().count()
        context ={'customers':customers,
              'customercount':customercount,
              'inventcount':inventcount,
              'workordercount':workordercount
              }
    customers = Customer.objects.filter(addedby=request.user)
    # print(customers)
    inventorys = Inventory.objects.all()
    customercount = Customer.objects.all().count()
    inventcount = Inventory.objects.all().count()
    workordercount = Workorder.objects.all().count()
    context ={'customers':customers,
              'customercount':customercount,
              'inventcount':inventcount,
              'workordercount':workordercount
              }
    
    for inventory in inventorys:
        #print(inventory)
        if request.user.is_staff and inventory.quantity < 12:
            #print(inventory)
            messages.warning(request, inventory.name+' are running low in stock Please add more!!')
            return render(request, 'index.html', context)
        
    return render(request, 'index.html', context)

@login_required
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
            
            if int(customer.quantity) < inventory.quantity:
                inventory.quantity -= int(customer.quantity)
                inventory.save()
                customer.amount = request.POST["amount"]
                customer.balance = inventory.price * int(customer.quantity) - int(customer.amount) * int(customer.quantity)
                customer.addedby = request.user
                customer.save()

                messages.success(request, 'New Customer added Successfully!!')
                return redirect('index')
            
            else:
                messages.warning(request, inventory.name+' are NOT enough in stock, please contact Administrator')
                return redirect('index')
            
            
    context ={'inventorys':inventorys
              }
    return render(request, 'customer_create.html',context)

@login_required
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
            if int(customer.quantity) < inventory.quantity:
                inventory.quantity -= int(customer.quantity)
                inventory.save()

                customer.amount = request.POST["amount"]
                customer.balance = inventory.price * int(customer.quantity) - int(customer.amount) * int(customer.quantity)
                customer.addedby = request.user
                customer.save()

                messages.warning(request, 'Customer updated Successfully!!')
                return redirect('index')
            else:
                messages.warning(request, 'Not enough inventory in stock, please contact Administrator')
                return redirect('index')
            
        
    context={'customer': customer, 'inventorys':inventorys}

    return render(request, 'customer_detail.html', context)

@login_required
def Createworkorder(request):
    workorder = Workorder()
    jobtypes = JobType.objects.all()
    customers = Customer.objects.filter(addedby=request.user)
    technicians = Technician.objects.all()
    if request.method == "POST":
        
        if "createworkorder" in request.POST: 
            
            workorder.ordername = request.POST["ordername"] 
            #workorder.number = request.POST["number"]
            customerid = request.POST["name"] 
            workorder.customer_name = get_object_or_404(Customer,id=customerid)
            
            jobid = request.POST["jobtype"] 
            workorder.jobtype = get_object_or_404(JobType,id=jobid)
            
            techid = request.POST["technician"] 
            workorder.technician = get_object_or_404(Technician,id=techid)
            
            workorder.order_status = request.POST["status"]
            
            workorder.amount_paid = request.POST["amount"]
            workorder.balance = request.POST["balance"]
            workorder.save()

            messages.success(request, 'Workorder added Successfully!!')
            return redirect('index')
                        
    context ={'customers':customers,'jobtypes':jobtypes,'technicians':technicians
              }
    return render(request, 'workorder_create.html',context)

@login_required
def Workorderdetailfunc(request, pk):
    jobtypes = JobType.objects.all()
    customers = Customer.objects.filter(addedby=request.user)
    technicians = Technician.objects.all()
    workorder = get_object_or_404(Workorder, pk=pk)
    if request.method == "POST":
        
        if "editworkorder" in request.POST: 
            
            workorder.ordername = request.POST["ordername"] 
            #workorder.number = request.POST["number"]
            customerid = request.POST["name"] 
            workorder.customer_name = get_object_or_404(Customer,id=customerid)
            
            jobid = request.POST["jobtype"] 
            workorder.jobtype = get_object_or_404(JobType,id=jobid)
            
            techid = request.POST["technician"] 
            workorder.technician = get_object_or_404(Technician,id=techid)
            
            workorder.order_status = request.POST["status"]
            
            workorder.amount_paid = request.POST["amount"]
            workorder.balance = request.POST["balance"]
            workorder.save()

            messages.success(request, 'Workorder Updated Successfully!!')
            return redirect('workorders')
                        
    context ={'customers':customers,'jobtypes':jobtypes,'technicians':technicians,'workorder':workorder
              }
    return render(request, 'workorder_detail.html',context)

@login_required
def inventory(request):
    inventorys = Inventory.objects.all()
    context ={'inventorys':inventorys
              }
    return render(request, 'inventory.html', context)

@login_required
def technician(request):
    technicians = Technician.objects.all()
    context ={'technicians':technicians
              }
    return render(request, 'technician.html', context)

@login_required
def workorder(request):
    workorders = Workorder.objects.all()
    context ={'workorders':workorders
              }
    return render(request, 'workorder.html', context)