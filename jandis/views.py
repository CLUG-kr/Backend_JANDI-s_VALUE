from django.shortcuts import render 
from django.http import HttpResponse, JsonResponse 
from django.views.decorators.csrf import csrf_exempt 
from rest_framework.parsers import JSONParser


# @csrf_exempt 
# def address_list(request): 
#     if request.method == 'GET': 
#         query_set = Addresses.objects.all() 
#         serializer = AddressesSerializer(query_set, many=True) 
#         return JsonResponse(serializer.data, safe=False) 
#     elif request.method == 'POST': 
#         data = JSONParser().parse(request) 
#         serializer = AddressesSerializer(data=data) 
#         if serializer.is_valid(): 
#             serializer.save() 
#             return JsonResponse(serializer.data, status=201) 
#         return JsonResponse(serializer.errors, status=400)



# @csrf_exempt 
# def address(request, pk): 

#     obj = Addresses.objects.get(pk=pk) 

#     if request.method == 'GET': 
#         serializer = AddressesSerializer(obj) 
#         return JsonResponse(serializer.data, safe=False) 

#     elif request.method == 'POST': 
#         data = JSONParser().parse(request) 
#         serializer = AddressesSerializer(obj, data=data) 
#         if serializer.is_valid(): 
#             seri alizer.save() 
#             return JsonResponse(serializer.data, status=201) 
#         return JsonResponse(serializer.errors, status=400) 
#     elif request.method == 'DELETE': 
#         obj.delete() 
#         return HttpResponse(status=204)


