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
# class OAuth(APIView):


@api_view(['POST'])
def github_login_test(request):
    body = request.data
    headers = {
        'Accept': 'application/json'
    }

    url = 'https://github.com/login/oauth/access_token'
    response = requests.post(url, data = body, headers = headers)   
    # print(response.json()) # print('타타타타타입', response)
    return Response(response.json())