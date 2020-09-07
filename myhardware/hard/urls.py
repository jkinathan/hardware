from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('inventory/',views.inventory,name='inventory'),
    path('technicians/',views.technician,name='technicians'),
    path('workorders/',views.workorder,name='workorders'),
    #path('',views.index,name='index'),
    #path('post/<int:pk>',views.PostDetailView.as_view(),name="post_detailfunc"),
    #path('post/like/<int:pk>',views.likepost,name="likepost"),
]