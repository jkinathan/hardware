from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib.auth import get_user_model
from django.contrib import messages
import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request
from django.views.generic.edit import FormView 
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import serializers
from django.forms.models import model_to_dict
from django.db.models.functions import TruncMonth
from django.db.models import Count

User = get_user_model()
# Create your views here.

def dashboard(request):

    labels = []
    data = []

    stocks = Inventory.objects.all().order_by('-name')
    customers2 = Customer.objects.all()
    customers = Customer.objects.values('inventory_purchased').annotate(mycount=Count('inventory_purchased')).order_by('inventory_purchased').filter(date__lte="2022-06-06")
    # Chart data
    
    for stockData in stocks:
        labels.append(stockData.name)
    
    
    for stockData in customers:
        data.append(stockData['mycount'])

    
    context ={'labels': labels,
              'data': data,
    }
    return render(request,'base/dashboard.html',context)

def get_data(request):

    #  Inventory.objects.all()
    invents = serializers.serialize("json", Inventory.objects.all())
    works = serializers.serialize("json", Workorder.objects.all())
    
    #workorders
    worker = []
    amountpaid = []

    for p in json.loads(works):
        amountpaid.append(p["fields"]["balance"])

    for j in json.loads(works):
        print(j)
        worker.append(j["fields"]["balance"])
            
    worklabels = []
    for i in json.loads(works):
        worklabels.append(i["fields"]["date"])    




    #inventory
    inventnum = []
    
    for j in json.loads(invents):
        inventnum.append(j["fields"]["quantity"])
            
    labels = []
    for i in json.loads(invents):
        labels.append(i["fields"]["name"])
    
    
    
    default_items  = inventnum 
    data = {
        "labels":labels,
        "default":default_items,
        "worklabels":worklabels,
        "worker":worker
    }
    return JsonResponse(data)


class ChartData(APIView):
    
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        #qs_count = User.objects.all().count()
        
        invents = Inventory.objects.filter(quantity>1)
        dict_obj = model_to_dict( invents )
        invent = json.dumps(dict_obj)
        labels = []
        for i in invent:
            labels.append(i)
        inventnum = []
        for j in invent:
            inventnum.append(j.quantity)
        
        default_items  = inventnum 

        data = {
                "labels":labels,
                "default":default_items,
                
            }
        return JsonResponse(data)





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
def Createreturnjob(request):
    returnjob = ReturnJobs()
    customers = Customer.objects.filter(addedby=request.user)
    if request.method == "POST":
        
        if "createreturnjob" in request.POST: 
            
            returnjob.jobname = request.POST["rjname"] 
            #workorder.number = request.POST["number"]
            customerid = request.POST["name"] 
            returnjob.customer_name = get_object_or_404(Customer,id=customerid)
            returnjob.complaint = request.POST["complaint"]
            returnjob.partnumber = request.POST["partnumber"]
            returnjob.datedone  = request.POST["datedone"]
            returnjob.status = request.POST["statusr"]
            returnjob.save()

            messages.success(request, 'Returnjob added Successfully!!')
            return redirect('returnjobs')
                        
    context ={'customers':customers
              }
    return render(request, 'returnjob_create.html',context)

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
def Returnjobdetailfunc(request, pk):

    customers = Customer.objects.filter(addedby=request.user)

    returnjob = get_object_or_404(ReturnJobs, pk=pk)
    if request.method == "POST":
        
        if "updatereturnjob" in request.POST: 
            
            returnjob.jobname = request.POST["rjname"] 
            #workorder.number = request.POST["number"]
            customerid = request.POST["name"] 
            returnjob.customer_name = get_object_or_404(Customer,id=customerid)
            
            returnjob.complaint = request.POST["complaint"] 
            returnjob.partnumber = request.POST["partnumber"]
            returnjob.datedone = request.POST["datedone"]
            returnjob.status = request.POST["statusr"]

            returnjob.save()

            messages.success(request, 'Return Job Updated Successfully!!')
            return redirect('returnjobs')
                        
    context ={'customers':customers,'returnjob':returnjob
              }
    return render(request, 'returnjob_detail.html',context)

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


@login_required
def ReturnJobo(request):
    returnjobs = ReturnJobs.objects.all()
    context ={'returnjobs':returnjobs
              }
    return render(request, 'returnjobs.html', context)
