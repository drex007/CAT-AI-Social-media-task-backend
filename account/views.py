from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import requests
from requests_oauthlib import OAuth1Session
from dotenv import load_dotenv
import os
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from task.models import TaskRewardModel
from .models import AccountModel
from .serializer import AccountSerialzer, AccountLoginSerialzer
from utils.utils import choose_adverts, generate_random, telegram_send_message, aibot_message, tokenchecker_message, rugCheckFunction, rugChecker_send_message, formatRugCheckerMessage, get_coin_price, telegram_callback_query
from helpers.open_ai import text_compilation
from helpers.logs import error_logs, user_interaction_logs
load_dotenv()





class GenerateTwitterOAUTH(APIView):
  def get(self,request):
    print(request, 'REQUEST')  
    url = "https://api.twitter.com/oauth/request_token"
    oauth = OAuth1Session(os.getenv('X_CONSUMER_KEY'), client_secret=os.getenv('X_CONSUMER_SECRET'))
    try:
      response = oauth.fetch_request_token(url)
      print(response, 'RES')
      resource_owner_oauth_token = response.get('oauth_token')
      resource_owner_oauth_token_secret = response.get('oauth_token_secret')
      data = {}
      if resource_owner_oauth_token and resource_owner_oauth_token_secret:
        data['oauth_token'] = resource_owner_oauth_token
        data ['oauth_token_secret'] = resource_owner_oauth_token_secret
        data ['oauth_callback_confirmed'] = True
        return Response(data=data, status=status.HTTP_200_OK) 
      return Response(data="Bad request",status= status.HTTP_400_BAD_REQUEST)
    except (requests.exceptions.RequestException, Exception) as e:
      error_logs(e, "GenerateTwitterOAUTH")
      return Response(data="Bad request",status= status.HTTP_400_BAD_REQUEST)
    
class GetAccountTwitterDetails(APIView):
  def post(self,request):  
    payload = request.data
    try:
      req = requests.post(f"https://api.twitter.com/oauth/access_token?oauth_token={payload['oauth_token']}&oauth_verifier={payload['oauth_verifier']}")
      if req.status_code == 200:
        print(req.text, 'REQ')
        new_list = req.text.split('&')
        data = {}
        for pair_string in new_list:
          splitted = pair_string.split('=')
          data[splitted[0]] = splitted[1]
        account = AccountModel.objects.filter(x_id=data['user_id'])
        
        if len(account) == 0:
          AccountModel.objects.create(
            x_id = data['user_id'],
            x_username = data['screen_name'],
            x_auth = data['oauth_token'],
            x_auth_secret = data['oauth_token_secret']
          )
        else:
            account[0].x_auth =  data['oauth_token']
            account[0].x_auth_secret = data['oauth_token_secret']
            account[0].save()
        
        return Response(data=data,status= status.HTTP_200_OK)
      return Response(data="Bad request",status= status.HTTP_400_BAD_REQUEST) 
    except (requests.exceptions.RequestException, Exception) as e:
      error_logs(e, "GetAccountTwitterDetails")
      return Response(data="Bad request",status= status.HTTP_400_BAD_REQUEST)
      
       

class AccountSignup(APIView):
  def post(self, request):
    data = request.data
    ref_code = generate_random(7)
    try:
      account = AccountModel.objects.filter(x_id = data['x_id']).first()
      referee = AccountModel.objects.filter(referral_code = data['referee']).first()
      if account is not None and account.completed == False:
        account.tg_username = data['tg_username']
        account.tg_id = data['tg_id']
        account.referee = data['referee']
        account.completed = True
        account.referral_code = ref_code
        account.save()
        if referee:
          referee.points = int(referee.points) + 1000
          referee.save()
        return Response(data="Account created", status=status.HTTP_200_OK)
      return Response(data="Account created", status=status.HTTP_200_OK)
    except Exception as e:
      error_logs(e, 'AccountSignup')
      return Response(data="Bad request",status= status.HTTP_400_BAD_REQUEST)
    
class AllAccount(APIView):
  serializer_class = AccountSerialzer
  def get(self, request):
    try:
      all = AccountModel.objects.all()
      serializer = self.serializer_class(all, many=True)
      return Response(data=serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
      error_logs(e,"AllAccount")
      return Response(data="Bad request",status= status.HTTP_400_BAD_REQUEST)
    
    

class GetUserTwitterOauthForLogin(APIView):
  def get(self,request):
    print(os.getenv("LOGIN_CALLBACK"), 'CALLBACK')
    url = "https://api.twitter.com/oauth/request_token"
    oauth = OAuth1Session(os.getenv('X_CONSUMER_KEY'), client_secret=os.getenv('X_CONSUMER_SECRET'), callback_uri=os.getenv("LOGIN_CALLBACK")) #Add the call back to your twitter dev account 
    try:
      response = oauth.fetch_request_token(url)
      resource_owner_oauth_token = response.get('oauth_token')
      resource_owner_oauth_token_secret = response.get('oauth_token_secret')
      data = {}
      data['oauth_token'] = resource_owner_oauth_token
      data ['oauth_token_secret'] = resource_owner_oauth_token_secret
      data ['oauth_callback_confirmed'] = True
      return Response(data=data, status=status.HTTP_200_OK) 
    except (requests.exceptions.RequestException, Exception) as e:
      error_logs(e, "GetUserTwitterOauthForLogin")
      return Response(data="Bad request",status= status.HTTP_400_BAD_REQUEST)


class AccountLogin(APIView):
  serializer_class = AccountLoginSerialzer
  def post(self, request):
    payload = request.data 
    try:
      data = {}
      req = requests.post(f"https://api.twitter.com/oauth/access_token?oauth_token={payload['oauth_token']}&oauth_verifier={payload['oauth_verifier']}")
      if req.status_code == 200:
        new_list = req.text.split('&')
        for pair_string in new_list:
          splitted = pair_string.split('=')
          data[splitted[0]] = splitted[1]
        if 'user_id' in data: 
          instance = AccountModel.objects.filter(x_id = data['user_id']).first()
          if instance is not None:
            serializer = self.serializer_class(instance)
            return Response(data=serializer.data, status=status.HTTP_200_OK) 
          else:
            ref_code = generate_random(7)
            acc = AccountModel.objects.create(
              x_id = data['user_id'],
              x_username = data['screen_name'],
              referral_code = ref_code
            )
            serialized_data = self.serializer_class(acc)
            return Response(data=serialized_data.data, status=status.HTTP_200_OK)
        return Response(data={}, status=status.HTTP_200_OK)
      return Response(data="Bad request", status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
      error_logs(e, "AccountLogin")
      return Response(data="Bad request",status= status.HTTP_400_BAD_REQUEST)


class GetSignedUpUser(APIView):
  serializer_class = AccountLoginSerialzer
  def post(self, request):
    payload = request.data
    try:
      if payload != {}:
        instance = AccountModel.objects.get(x_id = payload['x_id'])
        serializer = self.serializer_class(instance)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
      return Response(data={}, status=status.HTTP_200_OK)
      
    except Exception as e:
      error_logs(e, "GetSignedUpUser")
      return Response(data="Bad request",status= status.HTTP_400_BAD_REQUEST)
    
    

class TelegramBotWebHook(APIView):
      
  @csrf_exempt
  def post(self,request):
    data = request.data
    try:
      if data.get('message'):
        id = data['message']['from']['id']
        username = data['message']['from']['username']
        
        if id and username: 
          user = AccountModel.objects.filter(tg_id = id).first()
          if user is None:
            mess=f"Welcome to KruxAI✅. \n\nClick the link below to complete the KruxAI onboarding process:\n\n{os.getenv('TELEGRAM_AUTH_LINK')}?tg_id={id}&username={username}"
            telegram_send_message(chat_id=id, text=mess)
            return Response(data={}, status=status.HTTP_200_OK)
          else:   
            user_text = data.get('message')['text']
            if user.bot_status == "aibot":
              res = text_compilation(user_text)
              if res['status'] == 1:
                advert =  choose_adverts()    
                aibot_message(id, f"{res['response']} {advert}", is_true=1)
              return Response(data={}, status=status.HTTP_200_OK)
            if user.bot_status == "tokenbot":
                #Get token price
                if user_text.lower()[0] == "/":
                  advert =  choose_adverts()
                  price_req = get_coin_price(user_text.lower()[1:])
                  tokenchecker_message(id, f"{price_req} {advert}", is_true=1)
                  return Response(data={}, status=status.HTTP_200_OK)
                #Check token contract addresss  
                req = rugCheckFunction(user_text.strip())
                if req['status'] == True:
                    advert =  choose_adverts()
                    message = formatRugCheckerMessage(req)
                    rugChecker_send_message(id, f"{message} {advert}" )
                rugChecker_send_message(id, req["message"])
                return Response(data={}, status=status.HTTP_200_OK)
      if data.get("callback_query"):
        telegram_callback_query(data)                             
        return Response(data={}, status=status.HTTP_200_OK)
      return Response(data={}, status=status.HTTP_200_OK)
    except Exception as e:
      error_logs(e, "TelegramBotWebHook")
      return Response(data={}, status=status.HTTP_200_OK)
    
    
class RedeemReferralCode(APIView):
  def post(self,request):
    data = request.data
    try:
      user = AccountModel.objects.filter(x_id = data['x_id']).first()
      if user is not None:   
        referee = AccountModel.objects.filter(referral_code = data['referee_code']).first()
        if referee is not None and referee.referral_code != user.referral_code and user.referee == None:
            referee.points = int(referee.points) + 1000
            referee.save()
            user.points = int(user.points) + 500
            user.referee = data['referee_code']
            user.save()
            return Response(data="Reward added", status=status.HTTP_200_OK)
        return Response(data="Referee does not exist", status=status.HTTP_400_BAD_REQUEST)
      return Response(data="Account does not exist", status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
      error_logs(e, "RedeemReferralCode")
      return Response(data={""}, status=status.HTTP_400_BAD_REQUEST)
    
class UpdateAccountTelegram(APIView):
  def post(self, request):
    data = request.data
    try:
      user = AccountModel.objects.filter(x_id = data['x_id']).first()
      if user:
            user.tg_id = data['tg_id']
            user.tg_username = data['tg_username']
            user.save()
      return Response(data="Account updated", status=status.HTTP_200_OK)
    except Exception as e:
      error_logs(e, "UpdateAccountTelegram")
      return Response(data={""}, status=status.HTTP_400_BAD_REQUEST)
      
      
      


class OneTimeTaskVerification(APIView):
  def post(self, request):
    data = request.data
    try:
        user = AccountModel.objects.filter(x_id = data['x_id']).first()
        task = TaskRewardModel.objects.all()[0]
        if user.tg_id is not None or user.tg_id != "":
          if data['task'] == "twitter_task" and user.twitter_task == False:
                user.twitter_task = True
                user.points = int(user.points) + int(task.follow)
                user.save()
          if data['task'] == "telegram_group" and user.telegram_task == False:
                user.telegram_task = True
                user.points = int(user.points) + int(task.join)
                user.save()
          if data['task'] == "telegram_channel_task" and user.telegram_channel_task == False:
                user.telegram_channel_task = True
                user.points = int(user.points) + int(task.join)
                user.save()
          return Response(data="account updated", status=status.HTTP_200_OK)
        return Response(data="Telegram Id not linked", status=status.HTTP_400_BAD_REQUEST)
                
    except Exception as e:
        error_logs(e, "OneTimeTaskVerification")
        return Response(data="Error occured", status=status.HTTP_400_BAD_REQUEST)