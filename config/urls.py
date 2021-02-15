from django.conf.urls import url, include 
from django.urls import path ,include
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token


urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('api/token/', obtain_jwt_token), # jwt 토큰을 발행할 때 사용
    path('api/token/verify/', verify_jwt_token), # jwt 토큰이 유효한 지 검증할 때 사용
    path('api/token/refresh/', refresh_jwt_token), # jwt 토튼을 갱신할 때 사용
    path('api/jandi/', include("jandis.urls")),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]