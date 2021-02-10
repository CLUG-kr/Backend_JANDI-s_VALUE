from django.db import models

# Create your models here.

from django.db import models 

class Addresses(models.Model): 
    name = models.CharField(max_length=10) 
    phone_number = models.CharField(max_length=13) 
    address = models.TextField() 

