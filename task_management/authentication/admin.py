from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from authentication.models import *

# Register your models here.

class LoginUserGroup(ImportExportModelAdmin):
    list_display=['id','user_name','password','is_admin','is_logged_in']
admin.site.register(LoginUser,LoginUserGroup)
