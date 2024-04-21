from rest_framework import serializers
from .models import AccountModel


class AccountSerialzer(serializers.ModelSerializer):
  class Meta:
    model = AccountModel
    fields = "__all__"
    
class AccountLoginSerialzer(serializers.ModelSerializer):
  class Meta:
    model = AccountModel
    fields = ["id", "referee", "referral_code", "x_id","points", "task_count", "tg_id", "wallet", "x_username", "tg_username", "email", "bot_point"]