from django.db import models
from account.models import AccountModel

# Create your models here.



TASK_TYPE_CHOICES = [
        ("twitter", "twitter"),
        ("telegram", "telegram"),
      
    ]


TASK_CATEGORIES_CHOICES = [
        ("Like", "Like"),
        ("Follow", "Follow"),
        ("Quote", "Quote"),
        ("Retweet", "Retweet"),
        ("Join", "Join"),
        ("Comment", "Comment"),

      
    ]


class TaskModel(models.Model):
  task_type = models.CharField(max_length=100, blank = True, null=True, choices = TASK_TYPE_CHOICES)
  task_category = models.CharField(max_length=100, blank = True, null=True, choices = TASK_CATEGORIES_CHOICES)
  task_title = models.CharField(max_length=100, blank = True, null=True)
  task_link = models.CharField(max_length=100, blank = True, null=True)
  start_date = models.DateField(auto_now_add = True)
  end_date = models.DateField(blank=True, null = True)
  account = models.ManyToManyField(AccountModel, null = True, blank = True)
  
  
  def __str__(self):
    return f"{self.task_type} || {self.task_category}"

  
class TaskRewardModel(models.Model):
  like = models.CharField(max_length=100, blank=True, null=True, default="1000")
  comment = models.CharField(max_length=100, blank=True, null=True, default="1000")
  join = models.CharField(max_length=100, blank=True, null=True, default="1000")
  follow = models.CharField(max_length=100, blank=True, null=True, default="1000")
  retweet = models.CharField(max_length=100, blank=True, null=True, default="1000")
  quote = models.CharField(max_length=100, blank=True, null=True, default="1000")
  others = models.CharField(max_length=100, blank=True, null=True, default="1000")
  created = models.DateField(auto_now_add = True)
  
  
  def __str__(self):
    return f"{self.created}"