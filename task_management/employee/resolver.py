from django.core import signing, mail
import logging
from rest_framework.response import Response
from employee.models import *
from rest_framework import status, generics, permissions



logger = logging.getLogger(__name__)

def mail_trigger(subjects,content,ticket_no,employee_id):
        try:
            print("COMING INSIDEE")
            print(content,"contentcontent")
            plain_message = content
            employee_detail = Employee.objects.get(employee_id=employee_id)
            print(employee_detail)
            print(employee_detail.email,"employee_detail.emailemployee_detail.email")
            to_email = [employee_detail.email]
            from_email = 'shipirockz@gmail.com'
            pass_word = '9345902590'
            mail_sub = "{} - {}".format(ticket_no,subjects)
            mail.send_mail(subject=mail_sub, 
                           message=plain_message, 
                           from_email=from_email,
                           auth_user=from_email,
                           auth_password=pass_word,
                           recipient_list=to_email)

        except Exception as e:
            logger.exception('Exception {}'.format(e.args))
            return Response({'status': 'fail', 'message': 'Something went wrong. Please try again later'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)