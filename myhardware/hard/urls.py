from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('inventory/',views.inventory,name='inventory'),
    path('technicians/',views.technician,name='technicians'),
    path('workorders/',views.workorder,name='workorders'),
    path('createcustomer',views.Createcustomer,name='createcustomer'),
    path('createworkorder',views.Createworkorder,name='createworkorder'),
    
    path('customerdetail/<int:pk>',views.Customerdetailfunc,name="customerdetail"),
    path('workorderdetail/<int:pk>',views.Workorderdetailfunc,name="workorderdetail"),
    
    path('autocompleter',views.Autoguy, name='autocomplete'),
    #path('post/like/<int:pk>',views.likepost,name="likepost"),
]