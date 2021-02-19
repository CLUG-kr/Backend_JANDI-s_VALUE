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
headers = {
            'Accept': 'application/json',
            'Authorization' : 'token 949d07f51185f05a3b04a6a9eb66772b9a0cbe62',
        }

query = {
     'visibility' : 'all',
     'per_page':  100, 
}

class GithubUserView(APIView) :
    def get(self, request):
        r = requests.get('https://api.github.com/user', headers=headers)
        # JSON 잘 넘김
        ctx = r.json()
        
        print(ctx)
        data = {
            'username' : ctx['login'],
            'profile_img_url' : ctx['avatar_url']
        }
        json_data = json.dumps(data)
        # print(data, type(json_data))
        
        
        return JsonResponse(data, safe=False) #data(dict)가 맞는 지 json_data(str) 맞는 지 헷갈림

    def username(self) :
        r = requests.get('https://api.github.com/user', headers=headers)
        username = r.json()
        return username['login']
        

class UserRepositories(GithubUserView) :

    def get(self, request) :
        r = requests.get('https://api.github.com/user/repos', headers=headers, params=query )
        ctx = r.json()
        repositories = []
        name = super().username()
        
        for x in ctx : 
            if x['owner']['login'] == name :
                repositories.append(x['name'])
                data = {
                    'repositories' : repositories
                } 

        json_data = json.dumps(data) 
         
        return JsonResponse(data, safe=False)






