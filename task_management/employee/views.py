from django.shortcuts import render
from rest_framework import status, generics, permissions
import logging
from rest_framework.response import Response
from employee.models import *
from employee.resolver import mail_trigger
from django.db.models import Q,F,Value,Sum,Max,Count
from django.core import signing, mail


logger = logging.getLogger(__name__)



# Create your views here.

class TaskCreation(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        """
        Sample Response for create
        {
            "task_title": "Work in Api",
            "ticket_description": "All api want complete in short period",
            "assigner_id": 1
        }
        """
        try:
            data = request.data
            employee_id = request.employee_id 
            if not request.is_admin:
                return Response({'status': 'fail', 'message': 'Admin only able to create'}, status=status.HTTP_400_BAD_REQUEST)
            task_title = data.get('task_title')
            ticket_description = data.get('ticket_description')
            ticket_status = data.get('ticket_status',1)
            task_id = data.get('id')
            assigner_id = data.get('assigner_id')
            task_dict = {
                'task_title':task_title,
                'ticket_description':ticket_description,
                'ticket_status':ticket_status
            }
            if task_id:
                task_data = Task.objects.filter(id=task_id,).update(**task_dict)
                return Response({'status':'success','message':'Task data updated successfully'})
            else:
                task_dict['assigned_to_id'] = assigner_id
                task_dict['employee_id'] = employee_id
                ticket_no_check = Task.objects.aggregate(Max('ticket_no_sequence'))['ticket_no_sequence__max'] or 0
                print(ticket_no_check,"ticket_no_checkticket_no_checkticket_no_check")
                sequence_no = ticket_no_check + 1
                new_ticket_no = "M2S-{}".format(sequence_no)
                task_dict['ticket_no'] = new_ticket_no
                task_dict['ticket_no_sequence'] = sequence_no
                mail=mail_trigger(task_title,ticket_description,new_ticket_no,assigner_id)
                task = Task.objects.create(**task_dict)
                return Response({'status':'success','message':'Task data created successfully'})
        except Exception as e:
            logger.exception('Exception {}'.format(e.args))
            return Response({'status': 'fail', 'message': 'Something went wrong Please try again'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self,request):
        try:
            data=request.GET
            employee_id = request.employee_id if hasattr(request, 'employee_id') else data.get('employee_id')
            print(request.login,"LOGINNNNNNNNNNNSSSSSSSSSSS")
            print(request.user.login_user.is_logged_in,"employee_idemployee_id")
            status_check = data.get('status_check')
            task_title = data.get('task_title')
            ticket_no = data.get('ticket_no')
            search_date = {}
            if status_check:
                search_date['ticket_status'] = status_check
            if task_title:
                search_date['task_title__istartswith'] = task_title
            if ticket_no:   
                search_date['ticket_no__icontains'] = ticket_no
            task_list = Task.objects.filter(assigned_to_id=employee_id,is_active=True,**search_date).values()
            to_do_count = 0
            in_progress_count = 0
            Completed_count = 0
            Hold_count = 0
            for i in task_list:
                if i['ticket_status'] == 1:
                    to_do_count+=1
                    i['ticket_status'] = 'ToDo'
                if i['ticket_status'] == 2:
                    in_progress_count+=1
                    i['ticket_status'] = "Inprogress"
                if i['ticket_status'] == 3:
                    Completed_count+=1
                    i['ticket_status'] = "Completed"
                if i['ticket_status'] == 4:
                    Hold_count+=1
                    i['ticket_status'] = "Hold"
            return Response({'status': 'success', 'message': 'Task List', 'data': task_list,'total_task':len(task_list),'to_do_count':to_do_count,'in_progress_count':in_progress_count,'Completed_count':Completed_count,"Hold_count":Hold_count})
        except Task.DoesNotExist as ne:
            logger.exception('Exception {}'.format(ne.args))
            return Response({'status': 'fail', 'message': 'Invalid receipt id'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception('Exception {}'.format(e.args))
            return Response({'status': 'fail', 'message': 'Something went wrong Please try again'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self,request):
        try:
            employee_id = request.employee_id
            task_id = request.GET.get('id') 
            print(task_id,"task_idtask_idtask_id")
            task_data = Task.objects.get(id=task_id)
            if not request.is_admin:
                return Response({'status': 'fail', 'message': 'Admin only able to delete'}, status=status.HTTP_400_BAD_REQUEST)
            if not task_data.is_active:
                return Response({'status': 'fail', 'message': 'Task already deleted'}, status=status.HTTP_400_BAD_REQUEST)
            task_data.is_active = False
            task_data.save()
            return Response({'status': 'success', 'message': 'Task deleted successfully'})
        except Exception as e:
            logger.exception('Exception {}'.format(e.args))
            return Response({'status': 'fail', 'message': 'Something went wrong Please try again'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class EmployeeDelete(generics.GenericAPIView):
    def delete(self,request):
        try:
            employee_id = request.GET.get('employee_id')
            employee_data = Employee.objects.get(employee_id=employee_id)
            if not request.is_admin:
                return Response({'status': 'fail', 'message': 'Admin only able to delete'}, status=status.HTTP_400_BAD_REQUEST)
            if not employee_data.is_active:
                return Response({'status': 'fail', 'message': 'Employee data already deleted'}, status=status.HTTP_400_BAD_REQUEST)
            employee_data.is_active = False
            employee_data.save()
            return Response({'status': 'success', 'message': 'Employee deleted successfully'})

        except Exception as e:
            logger.exception('Exception {}'.format(e.args))
            return Response({'status': 'fail', 'message': 'Something went wrong Please try again'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        



        

