from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    userEmail = models.EmailField(verbose_name = "email", max_length = 255, unique = True)
    userName = models.CharField(max_length=30)
    realTimePoint = models.IntegerField(default=0)
    totalPoint = models.IntegerField(default=0)
    commitDays = models.IntegerField(default=0)
    attendance = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'userEmail' # 유저 모델의 Unique Identifier. unique = True 가 옵션으로 설정된 필드 값으로 설정
    REQUIRED_FIELDS = [] # 필수로 받고 싶은 필드 값. USERNAME_FIELD 값과 패스워드는 항상 기본적으로 요구하기 때문에 따로 명시하지 않음.


    def __str__(self):
        return self.userEmail

    # def get_absolute_url(self):
    #     return reverse("myswsite:devtool_read", kwargs={"pk": self.pk})

    
    
    
    
    



