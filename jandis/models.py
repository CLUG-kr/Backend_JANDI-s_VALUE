from django.db import models

# Create your models here.

class TEST(models.Model):
    test = models.CharField(max_length=100)