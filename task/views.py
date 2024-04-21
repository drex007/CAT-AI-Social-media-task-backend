from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import requests
from requests_oauthlib import OAuth1Session
from dotenv import load_dotenv
import os
from .models import TaskModel
from datetime import date
from .serializers import (GetTaskSerializer)
from account.models import AccountModel
from django.db.models import F
from helpers.logs import error_logs
load_dotenv()



class GetTasksAPIVIEW(APIView):
  serializer_class = GetTaskSerializer
  def get(self, request):
    try:
      all = TaskModel.objects.filter(end_date__gte = date.today())
      serializer = self.serializer_class(all, many=True)
      return Response(data=serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
      error_logs(e,"GetTasksAPIVIEW" )
      return Response(data="Bad request", status=status.HTTP_400_BAD_REQUEST)


class AddAccountToTask(APIView):
  def post (self, request):
    data = request.data
    try:
      user_account = AccountModel.objects.get(x_id = data['x_id'])
      task = TaskModel.objects.get(id= data['task_id'])
      if task.account.filter(id=user_account.id).exists():
        return Response(data="Account already added", status=status.HTTP_200_OK)   
      else:
        task.account.add(user_account)
        task.save()
        return Response(data="Account added", status=status.HTTP_200_OK)
    except Exception as e:
      error_logs(e,"AddAccountToTask")
      return Response(data="Account not added", status=status.HTTP_400_BAD_REQUEST)
    
class TaskRewards(APIView):
  def post(self,request):
    data = request.data
    try:
      task = TaskModel.objects.get(id= data['task_id'])
      if task.reward_disbursed == False:
        task.account.all().update(points = F('points') + 1000)
        task.reward_disbursed = True
        task.save()
      return Response(data="Reward disbursed", status=status.HTTP_200_OK)
    except Exception as e:
      error_logs(e, "TaskRewards")
      return Response(data="Reward not disbursed", status=status.HTTP_400_BAD_REQUEST)