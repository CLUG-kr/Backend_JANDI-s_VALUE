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
        print(data, type(json_data))
        
        return JsonResponse(data, safe=False) #data(dict)가 맞는 지 json_data(str) 맞는 지 헷갈림
        
