from django.contrib import admin
from .models import TaskModel, TaskRewardModel

# Register your models here.


admin.site.register(TaskRewardModel)
admin.site.register(TaskModel)