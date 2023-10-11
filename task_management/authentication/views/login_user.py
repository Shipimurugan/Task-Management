import bcrypt
import json
import logging
from authentication.models import LoginUser
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from employee.models import Employee


logger = logging.getLogger(__name__)




class LoginUsersView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []
    def post(self, request, *args, **kwargs):
        """
        Sample Request
        {
            "user_name": "sethu_001",
            "password": "sethu@12345",
            "is_admin": true,
            "employee_id":1
        }
        Sample Response
        {
            "status": "success",
            "message": "User created successfully"
        }
        """
        try:
            data = request.data
            user_name = data.get('user_name')
            password = data.get('password')
            is_admin = data.get('is_admin')
            employee_id = data.get('employee_id')
            if LoginUser.objects.filter(user_name=user_name).first():
                return Response({'status': 'fail', 'message': 'User Name Already Exist'.capitalize().replace('_', ' ')}, status=status.HTTP_400_BAD_REQUEST)
            
            hashed_passwd = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt(10)).decode('utf8')
            login_details = {
                'user_name':user_name,
                'password':hashed_passwd,
                'is_admin': is_admin
            }

            log_in_user = LoginUser.objects.create(**login_details)
            employee = Employee.objects.get(employee_id=employee_id)
            employee.login_user = log_in_user
            employee.save()
            return Response({'status':'success','message':'User Created Successfully'.capitalize().replace('_', ' ')})

        except Employee.DoesNotExist as a:
            logger.exception('Exception {}'.format(a.args))
            return Response({'status': 'fail', 'message': 'employee Detail Does Not Exist'.capitalize().replace('_', ' ')}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception('Exception {}'.format(e.args))
            return Response({'status': 'fail', 'message': 'Something went wrong. Please try again later.'.capitalize().replace('_', ' ')},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)