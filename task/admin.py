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
        reward = TaskRewardModel.objects.filter().first()
        for x in queryset:
            if x.reward_disbursed == False:
                if x.task_category == "Like":
                    x.account.all().update(points = F('points') + int(reward.like))
                if x.task_category == "Follow":
                    x.account.all().update(points = F('points') + int(reward.follow))
                if x.task_category == "Join":
                    x.account.all().update(points = F('points') + int(reward.join))
                if x.task_category == "Retweet":
                    x.account.all().update(points = F('points') + int(reward.retweet))
                if x.task_category == "Quote":
                    x.account.all().update(points = F('points') + int(reward.quote))
                if x.task_category == "Comment":
                    x.account.all().update(points = F('points') + int(reward.comment))
                if x.task_category == "Others":
                    x.account.all().update(points = F('points') + int(reward.follow))
                else:
                    x.account.all().update(points = F('points') + int(reward.like))
                x.reward_disbursed = True
                x.save()

admin.site.register(TaskRewardModel)
admin.site.register(TaskModel, TaskModelReward)

        
 

