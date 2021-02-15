from django.urls import path
from .views import *

urlpatterns = [
    path('', UserList.as_view()),
    path('current', current_user), # 현재 접속 중인 User 조회
    # path('logintest/', github_login_test)
]