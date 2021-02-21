from django.urls import path
from .views import *

urlpatterns = [
    
    path('repolist/', ObtainRepositories.as_view(), name='ObtainRepositories'),

    path('dashboard/', GithubUserView.as_view(), name = 'GithubUserView'), #sarah api

    path('dashboard/commit/',CommitView.as_view(), name='CommitView'), #commit api

    path('dashboard/tendency/', DevTendencyView.as_view(), name='DevTendencyView'), #tendency api

    # graph
    path('dashboard/language/', LanguageView.as_view(), name='LanguageView'), 
    path('dashboard/contribution/', ContributionView.as_view(), name='ContributionView'),
    path('dashboard/day/',DayTendencyView.as_view(),name='DayTendencyView'),
    path('dashboard/time/', TimeTendencyView.as_view(), name='TimeTendencyView')
]