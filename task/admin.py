from django.contrib import admin
from .models import TaskModel, TaskRewardModel
from django.db.models import F

# Register your models here.




class TaskModelReward(admin.ModelAdmin):
    model = TaskModel
    fields = ['task_type','task_title', 'task_category','task_link', 'account', 'reward_disbursed','end_date', ]
    actions = ['disburse_rewards']
    list_display = [field.name for field in TaskModel._meta.fields if field.name != "id"]
    
    def disburse_rewards(self,request, queryset):
        for x in queryset:
            if x.reward_disbursed == False:
                x.account.all().update(points = F('points') + 1000)
                x.reward_disbursed = True
                x.save()
            

admin.site.register(TaskRewardModel)
admin.site.register(TaskModel, TaskModelReward)

        
 

