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
load_dotenv()



class GetTasksAPIVIEW(APIView):
  serializer_class = GetTaskSerializer
  def get(self, request):
    try:
      all = TaskModel.objects.filter(end_date__gte = date.today())
      serializer = self.serializer_class(all, many=True)
      return Response(data=serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
      print(e)
      return Response(data="Bad request", status=status.HTTP_400_BAD_REQUEST)
      