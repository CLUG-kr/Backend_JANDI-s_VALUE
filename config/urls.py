from django.conf.urls import url, include 
from django.urls import path 

urlpatterns = [ 

    path('', include("jandis.urls")),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]