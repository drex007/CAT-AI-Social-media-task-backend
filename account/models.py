from django.db import models

# Create your models here.


class AccountModel(models.Model):
  x_username = models.CharField(blank=True, null=True, max_length =100)
  x_id = models.CharField(blank=True, null=True, max_length =100, unique =True)
  x_auth = models.CharField(blank=True, null=True, max_length =100)
  x_auth_secret = models.CharField(blank=True, null=True, max_length =100)
  points = models.CharField(blank=True, default = "0", max_length =255)
  tg_username = models.CharField(blank=True, null=True, max_length =100)
  tg_id = models.CharField(blank=True, null=True, max_length =100)
  tg_auth = models.CharField(blank=True, null=True, max_length =100)
  wallet = models.CharField(blank=True, null=True, max_length =100)
  referral_code = models.CharField(blank=True, null=True, max_length =100)
  referee =  models.CharField(blank=True, null=True, max_length =100)
  airdrop_claimed =  models.BooleanField(default = False, blank=True)
  completed =  models.BooleanField(default = False, blank=True)
  date_joined = models.DateTimeField(auto_now_add = True)
  date_pending = models.DateField(blank = True, null=True)
  task_count = models.CharField(blank=True, default = "0", max_length =255)
  email = models.CharField(blank=True, null=True, max_length =100)
  
  def __str__(self):
    return f"{self.x_username} || {self.date_joined} "