from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    ATTENDANCE_CHOICES = {
        ('1','attendance'), #오른쪽에 있는 것이 화면에 보인다.
        ('0', 'absent'),
    }

    email = models.EmailField(verbose_name = "email", max_length = 255)
    name = models.CharField(max_length=30)
    realtimepoint = models.IntegerField(default=0)
    totalpoint = models.IntegerField(default=0)
    commitdays = models.IntegerField(default=0)
    attendance = models.CharField(max_length=30, choices=ATTENDANCE_CHOICES, blank=True, null=True, verbose_name='is_attendance')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    
    class Meta: 
        ordering = ['created_on']
        

    def __str__(self):
        return self.email

    # def get_absolute_url(self):
    #     return reverse("myswsite:devtool_read", kwargs={"pk": self.pk})

    
    
    
    
    



