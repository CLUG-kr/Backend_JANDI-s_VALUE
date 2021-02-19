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
        print("그냥 response", urlresponse)
        print("json()형식으로!!", urlresponse.json()) # json() -> response를 json타입으로 인코딩되어 반환
        # JSON 잘 넘김
        ctx = urlresponse.json()
        # print(type(ctx)) # 딕셔너리타입임
        data = {
            'username' : ctx['login'],
            'profile_img_url' : ctx['avatar_url']
        }
        json_data = json.dumps(data) #dictionary를 json으로 변환
        # print(type(json_data)) # json.dumps를 쓰면 str타입(이게json타입이군..)으로 바뀌군..
        # json을 dictionary로 변환하고 싶다면 json.loads(json_val)
        return Response(data)  #data(dict)가 맞는 지 json_data(str) 맞는 지 헷갈림 
        # response는 렌더링되지 않은 컨텐츠를 가져와 올바른 타입으로 변환해준다.


# class GithubLanguageView(APIView) :
#     def get(self, request):
#         username = request.GET['username'] # username 받을거임
#         url = 'https://api.github.com/users/%s' % username
#         urlresponse = requests.get(url)
#         print("그냥 response", urlresponse)
        
#         ctx = urlresponse.json() # json() -> response를 json타입으로 인코딩되어 반환
#         # print(type(ctx)) # 딕셔너리타입임
#         data = {
#             'username' : ctx['login'],
#             'profile_img_url' : ctx['avatar_url']
#         }
#         return Response(data)  

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