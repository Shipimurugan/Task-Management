import datetime
import phonenumbers
import logging

from employee.models import *
from rest_framework import serializers
from rest_framework.exceptions import ValidationError as Error

logger = logging.getLogger(__name__)
from django.core.validators import validate_email

now = datetime.date.today()

def has_special_char(string=None, name=False):
    for character in string:
        if not (character.isalpha() or character.isdigit() or character == ' '):
            if not name and character != '.':
                return True
    return False

def valid_email_address(email_address=None):
    try:
      validate_email(email_address)
      return True
    except:
      return False


def valid_phone_number(phone_number=None):
    if str(phone_number).startswith('+91'):
        phone_number = phone_number[3:]
    if len(phone_number) != 10 or not str(phone_number).isdigit():
        return False
    return True


class EmployeeSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(required=False, error_messages={'invalid': 'Is Active must be True or False'.capitalize().replace('_', ' ')}, default=True)
    class Meta:
        model = Employee
        fields = ('first_name', 'last_name','initial', 'employee_age', 'gender', 'dob', 
                  'email', 'marital_status', 'dob', 'mobile_number', 'address_line_1', 
                  'address_line_2', 'state', 'city','country', 'is_active')

    def validate(self, attrs): 
        error_dictionary = {}       
        if 'first_name' in attrs and attrs['first_name'] and has_special_char(attrs['first_name'], name=True):
            error_dictionary.update({'first_name':'please enter valid first name'.capitalize().replace('_', ' ')})
        
        if 'last_name' in attrs  and attrs['last_name'] and has_special_char(attrs['last_name'], name=True):
            error_dictionary.update({'last_name':'please enter valid last name'.capitalize().replace('_', ' ')})

        if 'email' in attrs  and attrs['email'] and not valid_email_address(attrs.get('email')):
            error_dictionary.update({'email':'please enter valid email address'.capitalize().replace('_', ' ')})

        if 'mobile_number' in attrs and attrs['mobile_number']  and not valid_phone_number(attrs.get('mobile_number')):
            error_dictionary.update({'mobile_number':'please enter valid phone number'.capitalize().replace('_', ' ')})

        if 'dob' in attrs  and attrs['dob'] and attrs['dob'] > now:
            error_dictionary.update({'date_of_birth':'please enter valid date of birth'.capitalize().replace('_', ' ')})

        if error_dictionary:
            raise Error(error_dictionary)
        return attrs