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
        # rq = request.GET.get('access_token')
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
        # rq = request.GET.get('access_token')
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
        print(">>>>", name)
        for x in ctx :
            if x['owner']['login'] == name :
                repositories.append(x['name'])

        print(repositories)

        data = {
            'repositories' : repositories
        } 
        
        json_data = json.dumps(data) 
        return JsonResponse(data, safe=False)



class LanguageView(APIView) :
    def get(self, request):
        print("aaaaaa")
        at = request.GET['access_token']
        # at = request.GET.get('access_tokem')
        rn = request.GET['repository_name']
        # rn = request.GET.get('respository_name')
        print("aaaaaa")
        headers = { 'Accept' : 'application/json' }
        token_str = 'token ' + at

        headers['Authorization'] = token_str
        query = {
            'visibility' : 'all',
            'per_page':  100, 
        }

        username = commonFunctions.username(headers)

        headers2 = {
            'Accept': 'application/json'
        }

        # repos=self.obtain_repositories()
        # repositories = repos['repositories']
        # print(len(repos['repositories']))
        r = requests.get('https://api.github.com/repos/%s/%s/languages' %(username, rn) , headers=headers2, params=query )
        ctx= r.json()
        print(ctx)

        # print(ctx['Python'])

        # to-do
        # 1. 언어가 없으면 pass / 언어별로 담을 list 하나 생성
        # 2. 해당 list에 ctx키값이 없으면 생성 후 값 담기 
        # 3. 있으면 있는 곳에 값 담기
        # 4. 완성한 list를 json형식으로 response 보내기 

        return Respones(ctx)


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
        print(activity)
        return JsonResponse(tendency, safe=False)

class DayTendencyView(APIView) :
    
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

        activity = [[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0]]

        headers2 = {
            'Accept': 'application/json'
        }
        r = requests.get('https://api.github.com/repos/%s/%s/stats/punch_card' % (name , rn), headers=headers2, params=query )
        r2 = r.json()
        for x, y, z in r2 :
            if x == 0 :
                activity[0][1] += z 
            elif x == 1 :
                activity[1][1] += z 
            elif x == 2 :
                activity[2][1] += z 
            elif x == 3 :
                activity[3][1] += z
            elif x == 4 :
                activity[1][1] += z 
            elif x == 5 :
                activity[2][1] += z 
            elif x == 6 :
                activity[3][1] += z  
    

        tendency = {}
        
        tendency["Mon"] = activity[1][1]
        tendency["Tue"] = activity[2][1]
        tendency["Wed"] = activity[3][1]
        tendency["Thu"] = activity[4][1]
        tendency["Fri"] = activity[5][1]
        tendency["Sat"] = activity[6][1]
        tendency["Sun"] = activity[0][1]
        print(tendency)
        return JsonResponse(tendency, safe=False)



class CommitView(APIView) :
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

        headers2 = {
            'Accept': 'application/json'
        }

        r = requests.get('https://api.github.com/repos/%s/%s/commits' % (name , rn), headers=headers2, params=query )
        ctx = r.json()
        datelist = []
        
        for x in ctx :
            print(x['commit']['author']['date'])
            datelist.append(x['commit']['author']['date'])  

        print(datelist)
        return HttpResponse("hello")


