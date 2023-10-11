from django.db import models
from authentication.models import LoginUser
from employee.constant import MARITAL_STATUS,TICKET_STATUS,GENDER


# Create your models here.

class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=32, blank=True, null=True)
    last_name = models.CharField(max_length=32, blank=True, null=True)
    initial = models.CharField(max_length=32, blank=True, null=True)
    employee_age = models.SmallIntegerField(blank=True, null=True)
    gender = models.CharField(choices=GENDER,max_length=255, blank=True, null=True)
    login_user = models.ForeignKey(LoginUser, on_delete=models.CASCADE, null=True,blank=True)
    dob = models.DateField(blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null=True)
    marital_status = models.IntegerField(choices=MARITAL_STATUS, blank=True, null=True)
    mobile_number= models.CharField(max_length=13, blank=True, null=True)
    address_line_1 = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=32, blank=True, null=True, default='India')
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.CharField(max_length=32,null=True,blank=True)
    created_date = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=32,null=True,blank=True)
    modified_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'employee_detail'

class Task(models.Model):
    assigned_to = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True,blank=True)
    employee = models.ForeignKey(Employee, related_name="employee_admin",on_delete=models.CASCADE, null=True,blank=True)
    task_title = models.CharField(max_length=255, blank=True, null=True)
    ticket_no = models.CharField(max_length=200, blank=True, null=True)
    ticket_no_sequence = models.IntegerField(blank=True, null=True)
    ticket_description = models.TextField(blank=True, null=True)
    ticket_status = models.IntegerField(choices=TICKET_STATUS, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.CharField(max_length=32,null=True,blank=True)
    created_date = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=32,null=True,blank=True)
    modified_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'task'
