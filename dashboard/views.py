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

import time
import datetime 

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
        ctx = r.json()
        dic_key = list(ctx.keys())
        dic_values = list(ctx.values())
        print(dic_key)
        print(type(dic_key))
        print(dic_values)
        print(type(dic_values))
        print(len(ctx))

        a=[]
        for key,value in zip(dic_key,dic_values):
            a.append(dict(language=key, value=value ))
        print(a)
        return JsonResponse(a, safe=False)



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
    
        x1 = dict(day="Mon")
        x1['value'] = activity[1][1]
        x2 = dict(day="Tue")
        x2['value'] = activity[2][1]
        x3 = dict(day="Wed")
        x3['value'] = activity[3][1]
        x4 = dict(day="Thu")
        x4['value'] = activity[4][1]
        x5 = dict(day="Fri")
        x5['value'] = activity[5][1]
        x6 = dict(day="Sat")
        x6['value'] = activity[6][1]
        x7 = dict(day="Sun")
        x7['value'] = activity[0][1]

        tendency = [x1,x2,x3,x4,x5,x6,x7]
        
        return JsonResponse(tendency, safe=False)

class TimeTendencyView(APIView) :
    
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

        activity = [[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],
                    [6,0],[7,0],[8,0],[9,0],[10,0],[11,0],
                    [12,0],[13,0],[14,0],[15,0],[16,0],[17,0],
                    [18,0],[19,0],[20,0],[21,0],[22,0],[23,0]]

        headers2 = {
            'Accept': 'application/json'
        }
        r = requests.get('https://api.github.com/repos/%s/%s/stats/punch_card' % (name , rn), headers=headers2, params=query )
        r2 = r.json()
        tendency = {}

        for x, y, z in r2 :
            if y == 0 : activity[0][1] += z 
            elif y == 1 : activity[1][1] += z 
            elif y == 2 : activity[2][1] += z 
            elif y == 3 : activity[3][1] += z
            elif y == 4 : activity[4][1] += z 
            elif y == 5 : activity[5][1] += z 
            elif y == 6 : activity[6][1] += z  
            elif y == 7 : activity[7][1] += z 
            elif y == 8 : activity[8][1] += z 
            elif y == 9 : activity[9][1] += z
            elif y == 10 : activity[10][1] += z 
            elif y == 11 : activity[11][1] += z 
            elif y == 12 : activity[12][1] += z 
            elif y == 13 : activity[13][1] += z 
            elif y == 14 : activity[14][1] += z 
            elif y == 15 : activity[15][1] += z
            elif y == 16 : activity[16][1] += z 
            elif y == 17 : activity[17][1] += z 
            elif y == 18 : activity[18][1] += z 
            elif y == 19 : activity[19][1] += z 
            elif y == 20 : activity[20][1] += z 
            elif y == 21 : activity[21][1] += z
            elif y == 22 : activity[22][1] += z 
            elif y == 23 : activity[23][1] += z 

        tendency["0"] = activity[0][1]
        tendency["1"] = activity[1][1]
        tendency["2"] = activity[2][1]
        tendency["3"] = activity[3][1]
        tendency["4"] = activity[4][1]
        tendency["5"] = activity[5][1]
        tendency["6"] = activity[6][1]
        tendency["7"] = activity[7][1]
        tendency["8"] = activity[8][1]
        tendency["9"] = activity[9][1]
        tendency["10"] = activity[10][1]
        tendency["11"] = activity[11][1]
        tendency["12"] = activity[12][1]
        tendency["13"] = activity[13][1]
        tendency["14"] = activity[14][1]
        tendency["15"] = activity[15][1]
        tendency["16"] = activity[16][1]
        tendency["17"] = activity[17][1]
        tendency["18"] = activity[18][1]
        tendency["19"] = activity[19][1]
        tendency["20"] = activity[20][1]
        tendency["21"] = activity[21][1]
        tendency["22"] = activity[22][1]
        tendency["23"] = activity[23][1]
        
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

        today= datetime.date.today()
        yesterday=today - datetime.timedelta(1)
        a_week_ago = today -datetime.timedelta(7) 

        str_today=str(today)
        str_yesterday=str(yesterday)
        str_a_week_ago=str(a_week_ago)

        today_count=0
        yesterday_count=0
        a_week_ago_count=0

        for x in ctx :
            print(x['commit']['author']['date'][:10])

        contribute={}
        # 여기에 다 담기.....

        for x in ctx :
            current_date = x['commit']['author']['date'][:10]
            if str_today ==  current_date :
                today_count=today_count+1
            elif str_yesterday == current_date :
                yesterday_count=yesterday_count+1
            elif str_a_week_ago == current_date :
                a_week_ago_cuont=a_week_ago_count+1

        print(today_count)
        print(yesterday_count)
        print(a_week_ago_count)

        r2 = requests.get('https://api.github.com/repos/%s/%s/contributors' % (name, rn) , headers=headers2, )
        
        ctx2=r2.json()

        # contribute['total_commit'] = 0 
        # pirnt(contribute)
        # for x in ctx : 
        #     contribute["total_commit"] =  contribute["total_commit"] + x['contributions']
        # print(contribute)
            
        return HttpResponse("hello")

