from django.urls import path
from .views import *

urlpatterns = [
    path('', GithubUserView.as_view(), name = 'GithubUserView'),
    path('repolist/', ObtainRepositories.as_view(), name='ObtainRepositories'),
    path('commit/',CommitView.as_view(), name='CommitView'),
    path('tendency/', DevTendencyView.as_view(), name='DevTendencyView'),
    path('language/', LanguageView.as_view(), name='LanguageView'),
    path('day/',DayTendencyView.as_view(),name='DayTendencyView'),
    
]