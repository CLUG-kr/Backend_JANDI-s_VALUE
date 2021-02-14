from .models import *
from rest_framework import serializers 


class UserSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = User
        fields = ['email', 'name', 'realtimepoint', 'totalpoint', 'commitdays', 'attendance','created_on', 'updated_on' ]

