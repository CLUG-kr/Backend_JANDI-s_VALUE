from django.shortcuts import render 
from django.http import HttpResponse, JsonResponse 
from django.views.decorators.csrf import csrf_exempt 
from rest_framework.parsers import JSONParser
from .models import *
from .serializers import *


@csrf_exempt 
def user_list(request): 
    if request.method == 'GET': # userlist 조회
        query_set = User.objects.all() 
        serializer = UserSerializer(query_set, many=True) 
        return JsonResponse(serializer.data, safe=False) 
    elif request.method == 'POST': # createUser
        data = JSONParser().parse(request) 
        serializer = UserSerializer(data=data) 
        if serializer.is_valid(): 
            serializer.save() 
            return JsonResponse(serializer.data, status=201) 
        return JsonResponse(serializer.errors, status=400)



@csrf_exempt 
def user(request, pk): 

    obj = User.objects.get(pk=pk) 

    if request.method == 'GET': # readUser
        serializer = UserSerializer(obj) 
        return JsonResponse(serializer.data, safe=False) 

    elif request.method == 'POST': # updateUser
        data = JSONParser().parse(request) 
        serializer = UserSerializer(obj, data=data) 
        if serializer.is_valid(): 
            serializer.save() 
            return JsonResponse(serializer.data, status=201) 
        return JsonResponse(serializer.errors, status=400) 

    elif request.method == 'DELETE': # deleteUser
        obj.delete() 
        return HttpResponse(status=204)


@csrf_exempt 
def is_user(request): 
    if request.method == 'POST': 
        data = JSONParser().parse(request) 
        search_email = data['email'] 
        obj = Addresses.objects.get(email=search_email) 
        if data['name'] == obj.name: #name이 같으면 있는 유저로 response (status : 200)
            return HttpResponse(status=200) 
        else: 
            return HttpResponse(status=400)




