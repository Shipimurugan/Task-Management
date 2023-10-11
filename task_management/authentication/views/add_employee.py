from datetime import datetime,timedelta
import re
from rest_framework import status, generics, permissions
from rest_framework.response import Response
import bcrypt
import logging
import jwt
from django.conf import settings
from authentication.models import *
from employee.models import Employee
# from utils_consts.constants import PASSWORD_REGEX
# from utils_consts.views import encrypt_token_data, generate_otp, most_used_apis, send_mail
# from sms import send_sms
from django.db.models import F
from cryptography.fernet import Fernet
from authentication.serializer import EmployeeSerializer
# from axes.decorators import axes_dispatch

from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict

logger = logging.getLogger(__name__)

def serializer_errors(errors):
    error_dict = {}
    if type(errors) == ReturnDict:
        for field_name, field_errors in errors.items():
            error_dict[field_name] = str(field_errors[0])
        return error_dict
    
    if type(errors) == ReturnList:
        for error in errors:
            error_list = []
            for field_name, field_errors in error.items():
                error_dict[field_name] = str(field_errors[0])
                error_list.append(error_dict)
            return error_list
        
class AddEmployeeView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []
    def post(self, request):
        """
        Sample Request 
        {
            "first_name":"Sethu",
            "last_name":"Pathy",
            "initial": "S",
            "employee_age":21,
            "gender":"m",
            "email": "sethu@gmail.com",
            "marital_status":1,
            "mobile_number":9876545676,
            "address_line_1":"Coimbatore",
            "state":"TAMIL NABU",
            "city":"coimbatore",
            "country":"INDIA"
        }
        Sample Response
        {
            "status": "success",
            "message": "Employee created successfully",
            "employee_id": 1
        }
        """
        try:
            data = request.data
            serializer = EmployeeSerializer(data=data, partial=True)

            try:
                is_valid = serializer.is_valid(raise_exception=True)
            except:
                serializer.is_valid(raise_exception=True)
                errors = serializer.errors
                logger.exception('Exception {}'.format(errors))
                error_list = serializer_errors(errors)
                return Response({'status': 'fail', 'message': "Something Went Wrong".capitalize().replace('_', ' '), 'errors':error_list}, status=status.HTTP_400_BAD_REQUEST)

            if is_valid:
                employee_data = serializer.validated_data
                employee = Employee.objects.create(**employee_data)

                return Response({'status': 'success', 'message': 'employee Created successfully'.capitalize().replace('_', ' '), 'employee_id':employee.employee_id})

        except Exception as e:
            logger.exception('Exception {}'.format(e.args))
            return Response({'status': 'fail', 'message': 'Something went wrong. Please try again later'.capitalize().replace('_', ' ')},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


    def put(self, request):
        try:
            data = request.data
            serializer = EmployeeSerializer(data=data, partial=True)

            try:
                is_valid = serializer.is_valid(raise_exception=True)
            except:
                errors = serializer.errors
                field_names = {}
                logger.exception('Exception {}'.format(errors))
                error_list = serializer_errors(errors)
                return Response({'status': 'fail', 'message': "Something Went Wrong".capitalize().replace('_', ' '), 'errors':error_list}, status=status.HTTP_400_BAD_REQUEST)

            if is_valid:
                employee_data = serializer.validated_data
                employee = Employee.objects.create(**employee_data)

                return Response({'status': 'success', 'message': 'employee updated successfully'.capitalize().replace('_', ' '), 'employee_id':employee.employee_id})

        except Exception as e:
            if employee:
                Employee.objects.filter(id=employee.id).delete()
            logger.exception('Exception {}'.format(e.args))
            return Response({'status': 'fail', 'message': 'Something went wrong. Please try again later'.capitalize().replace('_', ' ')},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)