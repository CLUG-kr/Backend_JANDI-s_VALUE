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
        rq = request.data.get("access_token")
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
         

class CommonFunctions :
    
    def username(self, headers) : # token 이용하여 username get api
        # self,headers로 바뀌려나?
        r = requests.get('https://api.github.com/user', headers=headers)
        username = r.json()
        return username['login']


    def obtain_repositories(self) :
        r = requests.get('https://api.github.com/user/repos', headers=headers, params=query )
        ctx = r.json()
        repositories = []

        githubUserView =GithubUserView()
        name = githubUserView.username()
        # name = super().username()
        
        for x in ctx : 
            if x['owner']['login'] == name :
                repositories.append(x['name'])
        data = {
            'repositories' : repositories
        } 
        print(type(data))
        json_data = json.dumps(data) 
        print(type(json_data)) 
         
        return data #딕셔너리타입


class GithubLanguageView(APIView) :

    def get(self, request):
        # a = request.get.토큰~
        githubUserView =GithubUserView()
        username = githubUserView.username() # 나중에 username()함수의 파라미터에 a변수 넣으면 될듯?

        repos=self.obtain_repositories()
        repositories = repos['repositories']
        print(len(repos['repositories']))
        for repo in repositories :
            url = 'https://api.github.com/repos/%s/%s/languages' %(username, repo)
            # 한 5초걸림 ㅎㅎ ^^....
            urlresponse = requests.get(url)
            ctx = urlresponse.json()
            print(ctx)
            # print(ctx['Python'])

            # to-do
            # 1. 언어가 없으면 pass / 언어별로 담을 list 하나 생성
            # 2. 해당 list에 ctx키값이 없으면 생성 후 값 담기 
            # 3. 있으면 있는 곳에 값 담기
            # 4. 완성한 list를 json형식으로 response 보내기 

        return HttpResponse("hello world~~")


class DevTendencyView(APIView) :

    def get(request) :
        name = commonfunctions.username
        data = commonfunctions.obtain_repositories
        repositories = data.get('repositories')
        activity = [[0,0],[1,0],[2,0],[3,0]]
        
        r = requests.get('https://api.github.com/repos/%s/%s/stats/punch_card' % (name , y), headers=headers, params=query )
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
            
        print (activity)
        return JsonResponse(data, safe=False)






