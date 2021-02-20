from django.urls import path
from .views import *

urlpatterns = [
    path('', GithubUserView.as_view(), name = 'GithubUserView'),
    path('repo/',GithubLanguageView.as_view())
]