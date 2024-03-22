from django.urls import path
from .views import GetTasksAPIVIEW, AddAccountToTask, TaskRewards

urlpatterns = [
    path("all", GetTasksAPIVIEW.as_view()),
    path("add-account", AddAccountToTask.as_view()),
    path("reward", TaskRewards.as_view())
    
]
