import bcrypt
import datetime
import jwt
import json
import logging
import re

from cryptography.fernet import Fernet
from authentication.models import LoginUser
from django.core import mail
from django.db.models import Q
from random import randint
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from task_management import settings
from employee.models import Employee

logger = logging.getLogger(__name__)

EMAIL_REGEX = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'


def encrypt_token_data(data):
    cipher_suite = Fernet(settings.TOKEN_SECRET_KEY)
    encoded_data = json.dumps(data).encode()
    encrypted_data = cipher_suite.encrypt(encoded_data)
    return encrypted_data.decode()

class LoginAuthenticationView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []
    def post(self, request, *args, **kwargs):
        """
        Sample Request
        {
            "user_name": "sethu_001",
            "password": "sethu@12345"
        }
        Sample Response
        {
            "status": "success",
            "message": "Login successful",
            "data": {
                "token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoiZ0FBQUFBQmxBMUgtZVBNTjJOOEJIaE5FUTVYSndydFdqSE9QU1ZEMmxSSjZnb0RfcWR0dkpXZXdiQS1ENUNjQUhMVEZuSkgxWWRPNTV0RlJuQmV2VVA5aTFMNFJqUmR3WjExRFNNbjYxZmdrdEU0Wml1UkpreHBzNDhWMVRTbGxzaml6RGNLTWZnTU8iLCJleHAiOjE2OTQ4MDI4MTR9.A06taDQCq-mbJbhKemNExm1PKeNWxzbWZ1UCYhcX4Y1gKtuEb8lVJpTJ5GsDwogxXPlOp7DFqqcoqjpeZIRTBnID4QIwpmdM0vnei5FxSylT6WmLy7CXGPBh2o59qFf7T_ywuhsWOfA8NlSfir9Wf-jXvRYOvAq6YBKC-hmLgnxVHaVPFlU_bcslgKcbZ7_r7djDunjGbegitx2x51KLMVLI8n8oQNu7FzCg3ngTvJyUuUaaDCDu8ohvCuEvCE31mYe7N6ggX9vb56S13K4MdazNuk2OD9xyEiP2jfZ4PEOc9ZZy2AbaJwDJA8rPrEVbPnWNK7m2OtLCXGUS3fnJww",
                "is_admin": true,
                "employee_id": 1
            }
        }
        """
        try:
            data = request.data

            logger.info('Request Payload {}'.format(data))
            username = data.get('user_name')
            passwd = data.get('password')


            if not username or not passwd:
                return Response({'status': 'fail', 'message': 'Invalid username/password'.capitalize().replace('_', ' ')}, status=status.HTTP_400_BAD_REQUEST)

            if re.search(EMAIL_REGEX, username):
                return Response({'status': 'fail', 'message': 'Please enter username'.capitalize().replace('_', ' ')},
                                status=status.HTTP_400_BAD_REQUEST)

            user = LoginUser.objects.filter(user_name=username).first()

            if not user:
                return Response({'status': 'fail', 'message': 'Username does not exist'.capitalize().replace('_', ' ')},
                                status=status.HTTP_400_BAD_REQUEST)

            if not bcrypt.checkpw(bytes(passwd, 'utf-8'), bytes(user.password, 'utf-8')):
                return Response({'status': 'fail', 'message': 'Invalid username/password'.capitalize().replace('_', ' ')},
                                status=status.HTTP_400_BAD_REQUEST)
    
            if user.is_logged_in:
                return Response({'status': 'fail', 'message': 'User Already Logged in'.capitalize().replace('_', ' ')},
                                                status=status.HTTP_400_BAD_REQUEST)
            
            token_data = {}
            employee_id = Employee.objects.get(login_user=user)
            if user.is_admin:
                token_data['is_admin'] = True
            token_data['employee_id'] = employee_id.employee_id
            token_data['login'] = user.id
            current_dt = datetime.datetime.now()
            expiry_time = current_dt + datetime.timedelta(minutes=1440)
            encrypted_data = encrypt_token_data(token_data)

            private_key = open('private_key.pem').read()
            token = jwt.encode({'data': encrypted_data, 'exp': expiry_time}, private_key, algorithm='RS256')
            response_data = {'token': token}

            if user.is_admin:
                response_data['is_admin'] = True

            response_data['employee_id'] = employee_id.employee_id

            user.is_logged_in = True
            user.save()

            return Response({'status': 'success', 'message': 'Login successful'.capitalize().replace('_', ' '), 'data': response_data})

        except LoginUser.DoesNotExist as le:
            logger.exception('Exception {}'.format(le.args))
            return Response({'status': 'fail', 'message': 'Invalid username/password'.capitalize().replace('_', ' ')},
                            status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception('Exception {}'.format(e.args))
            return Response({'status': 'fail', 'message': 'Something went wrong. Please try again later'.capitalize().replace('_', ' ')},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []
    def post(self, request, *args, **kwargs):
        data = request.data
        employee_id = request.employee_id
        # request.login.is_logged_in = True
        # print(request.employee_id ,"request.loginrequest.loginrequest.login")
        # print(request.login.is_logged_in,"request.loginrequest.loginrequest.login")
        if request.login:
            if request.login.is_logged_in:
                request.login.is_logged_in = False
                request.login.save()
            return Response({'status': 'success', 'message': 'Logged out successfully'.capitalize().replace('_', ' ')})
        return Response({'status': 'fail', 'message': 'Something went wrong. Please try again later'.capitalize().replace('_', ' ')},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
