from django.db import models
# from utils_consts.constants import OTP_TYPES,GENDER

# Create your models here.

# class BaseModel(models.Model):
#     created_by = models.CharField(max_length=32,null=True,blank=True)
#     created_date = models.DateTimeField(auto_now=True)
#     modified_by = models.CharField(max_length=32,null=True,blank=True)
#     modified_date = models.DateTimeField(auto_now_add=True)

class LoginUser(models.Model):
    user_name = models.CharField(max_length=32)
    password = models.CharField(max_length=230)
    is_admin = models.BooleanField(default=False)
    is_logged_in = models.BooleanField(default=False)
    created_by = models.CharField(max_length=32,null=True,blank=True)
    created_date = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=32,null=True,blank=True)
    modified_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'login_user'
