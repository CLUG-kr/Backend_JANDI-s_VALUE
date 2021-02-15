from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token
from .views import validate_jwt_token

urlpatterns = [

    path('admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('validate/', validate_jwt_token),
    path('login/', obtain_jwt_token),
    
    path('verify/', verify_jwt_token),
    path('refresh/', refresh_jwt_token),
    
    path('user/', include('user.urls')),
    # path('jandis/', include('jandis.urls'))

]