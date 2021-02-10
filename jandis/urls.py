from django.conf.urls import url, include 
from . import views 
from django.urls import path 

urlpatterns = [ 
    path('addresses/', views.address_list),

    path('addresses/<int:pk>/', views.address), 
  
]

