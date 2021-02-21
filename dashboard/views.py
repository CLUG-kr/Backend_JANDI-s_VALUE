from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
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
from .functions import *
query = {
     'visibility' : 'all',
     'per_page':  100, 
}

commonFunctions = CommonFunctions()

class GithubUserView(APIView) :
    def get(self, request): #sarah api
        rq = request.GET['access_token']
        headers = { 'Accept' : 'application/json' }
        token_str = 'token ' + rq
        headers['Authorization'] = token_str
        r = requests.get('https://api.github.com/user', headers=headers)
        # JSON 잘 넘김
        ctx = r.json()
        print(ctx)
        data = {
            'username' : ctx['login'],
            'profile_img_url' : ctx['avatar_url']
        }
        json_data = json.dumps(data) #dictionary를 json으로 변환
        # print(type(json_data)) # json.dumps를 쓰면 str타입(이게json타입이군..)으로 바뀌군..
        return JsonResponse(data, safe=False) #data(dict)가 맞는 지 json_data(str) 맞는 지 헷갈림   

class ObtainRepositories(APIView) :
    def get(self, request) : #repo list api
        rq = request.GET['access_token']
        headers = { 'Accept' : 'application/json' }
        token_str = 'token ' + rq
        headers['Authorization'] = token_str
        query = {
            'visibility' : 'all',
            'per_page':  100, 
        }
        r = requests.get('https://api.github.com/user/repos', headers=headers, params=query )
        ctx = r.json()
        repositories = []
        name = commonFunctions.username(headers)
        for x in ctx :
            if x['owner']['login'] == name :
                repositories.append(x['name'])

        data = {
            'repositories' : repositories
        } 
        
        json_data = json.dumps(data) 
        return JsonResponse(data, safe=False)

class ContributionView(APIView) :
    def get(self, request):
        at = request.GET['access_token']
        rn = request.GET['repository_name']
        headers = { 'Accept' : 'application/json' }
        token_str = 'token ' + at

        headers['Authorization'] = token_str
        query = {
            'visibility' : 'all',
            'per_page':  100, 
        }
        
        name = commonFunctions.username(headers)

        headers2 = {
            'Accept': 'application/json'
        }
        r = requests.get('https://api.github.com/repos/%s/%s/contributors' % (name, rn) , headers=headers, )
        ctx=r.json()

        contribute={}
        for x in ctx : 
            contribute[str(x['login'])] = x['contributions']

        
        return JsonResponse(contribute, safe=False)




class LanguageView(APIView) :
    def get(self, request):
        at = request.GET['access_token']
        rn = request.GET['repository_name']
        headers = { 'Accept' : 'application/json' }
        token_str = 'token ' + at

        headers['Authorization'] = token_str
        query = {
            'visibility' : 'all',
            'per_page':  100, 
        }
        
        name = commonFunctions.username(headers)

        headers2 = {
            'Accept': 'application/json'
        }
        r = requests.get('https://api.github.com/repos/%s/%s/languages' % (name, rn) , headers=headers, )
        print(r.json())

        ctx=r.json()
        hello={}
        for a in ctx :
            ctx[login]
        
        return JsonResponse(ctx, safe=False)



class DevTendencyView(APIView) :

    def get(self, request) :

        at = request.GET['access_token']
        rn = request.GET['repository_name']
        headers = { 'Accept' : 'application/json' }
        token_str = 'token ' + at

        headers['Authorization'] = token_str
        query = {
            'visibility' : 'all',
            'per_page':  100, 
        }

        name = commonFunctions.username(headers)

        activity = [[0,0],[1,0],[2,0],[3,0]]

        headers2 = {
            'Accept': 'application/json'
        }
        r = requests.get('https://api.github.com/repos/%s/%s/stats/punch_card' % (name , rn), headers=headers2, params=query )
        r2 = r.json()
        for x, y, z in r2 :
            if y < 6 :
                activity[0][1] += z 
            elif y < 12 :
                activity[1][1] += z
            elif y < 18 :
                activity[2][1] += z
            elif y < 24 :
                activity[3][1] += z 
            

        max = activity[0][1]
        # 최댓값알고리즘
        for i in range(4):
            if max < activity[i][1]:
                max = activity[i][1]

        tendency = {}
        if max == activity[0][1] :
            tendency["type"] = "새벽"
        elif max == activity[1][1] :
            tendency["type"] = "아침"
        elif max == activity[2][1] :
            tendency["type"] = "낮"
        elif max == activity[3][1] :
            tendency["type"] = "밤"

        return JsonResponse(tendency, safe=False)






