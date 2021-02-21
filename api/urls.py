from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token


urlpatterns = [

    path('admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # path('validate/', validate_jwt_token), #JWT 받아 토큰을 검증해서 상태코드로 반환
    # path('login/', obtain_jwt_token), #Github의 ID 토큰 받아서 JWT 반환
    
    
    # path('verify/', verify_jwt_token),
    # path('refresh/', refresh_jwt_token), #JWT를 받아 토큰을 검증하여 새로운 토큰 반환
    
    path('oauth/', include('oauth.urls')),
    path('', include('dashboard.urls')),

]