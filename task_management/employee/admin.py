from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from employee.models import Task,Employee

# Register your models here.

class TaskGroup(admin.ModelAdmin):
    list_display=['id',"assigned_to",'task_title','ticket_no','ticket_no_sequence','is_active']
admin.site.register(Task,TaskGroup)

class EmployeeGroup(admin.ModelAdmin):
    list_display=['employee_id',"first_name",'login_user','gender','is_active']
admin.site.register(Employee,EmployeeGroup)