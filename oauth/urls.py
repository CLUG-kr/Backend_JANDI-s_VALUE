from django.urls import path
from .views import *

urlpatterns = [
    # path('', UserList.as_view()),
    path('', github_login_test),
    path('users/', GithubUserView.as_view(), name = 'GithubUserView'),
]