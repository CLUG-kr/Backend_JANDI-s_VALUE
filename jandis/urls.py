from django.conf.urls import url, include 
from . import views 
from django.urls import path 


urlpatterns = [ 
    path('jwt_test/', views.jwt, name='jwt'),
    path('users/', views.user_list), 
    path('users/<int:pk>/', views.user), 
    path('is_user/', views.is_user),
]

