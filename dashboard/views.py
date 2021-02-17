from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from django.http import JsonResponse
# from rest_framework import serializers
import requests
import json

# Create your views here.

class GithubUserView(APIView) :
    def get(self, request):
        username = request.GET['username'] # username 받을거임
        url = 'https://api.github.com/users/%s' % username
        urlresponse = requests.get(url)
        # print(urlresponse.json())
        # JSON 잘 넘김
        ctx = urlresponse.json()
        data = {
            'username' : ctx['login'],
            'profile_img_url' : ctx['avatar_url']
        }
        json_data = json.dumps(data)
        
        return JsonResponse(data, safe=False) #data(dict)가 맞는 지 json_data(str) 맞는 지 헷갈림

    def post(self, request):
        username = request.GET['username'] # username 받을거임
        url = 'https://api.github.com/users/%s/repos' % username
        urlresponse = requests.get(url)
        # print(urlresponse.json()) # JSON 잘 넘김
        ctx = urlresponse.json()
        repositories = []
        for x in ctx : 
            repositories.append(x['name'])
        data = {
            'repositories' : repositories
        } 
        
        # for y in data.get('repositories') :
        #     url2 = 'https://api.github.com/repos/%s/%s/stats/punch_card' % (username, y)
        #     url2response = requests.get(url)
        #     ctx2 = url2response.json()
        #     bam = 0
            


        # daydata = {
        #     '0': bam
        # }
        json_data = json.dumps(data)
        return JsonResponse(data, safe=False)


# @api_view(['GET'])
# def events(request):
#     body = request.data
#     headers = {
#         'Accept': 'application/json'
#     }

#     url = 'https://github.com/users/{username}/events'
#     response = requests.post(url, data = body, headers = headers)   

#     return Response(response.json())   

# @api_view(['GET'])
# def dash_commits(request):
#     git = Github("token")
#     org = git.get_organization('organization')

#     for repo in org.get_repos():
#         repository_commit_date = repo.get_commit(sha='master')
#         stats_ = repository_commit_date.stats
#         print(stats_.total)