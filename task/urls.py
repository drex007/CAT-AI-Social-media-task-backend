from django.urls import path
from .views import GetTasksAPIVIEW

urlpatterns = [
    path("all", GetTasksAPIVIEW.as_view())
    
]
