from django.urls import path
from .views import *

urlpatterns = [
    path('', GithubUserView.as_view(), name = 'GithubUserView'),
    path('repolist/', ObtainRepositories.as_view(), name='ObtainRepositories'),
    path('tendency/', DevTendencyView.as_view(), name='DevTendencyView'),
    path('language/', LanguageView.as_view(), name='LanguageView'),
    
]