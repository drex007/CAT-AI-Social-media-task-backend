from rest_framework import serializers
from .models import TaskModel

class GetTaskSerializer(serializers.ModelSerializer):
  class Meta:
    model = TaskModel
    fields = "__all__"