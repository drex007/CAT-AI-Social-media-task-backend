from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import requests
from requests_oauthlib import OAuth1Session
from dotenv import load_dotenv
import os
from .models import AccountModel
from .serializer import AccountSerialzer, AccountLoginSerialzer
from utils.utils import generate_random, telegram_send_message
load_dotenv()

print(os.getenv('TELEGRAM_AUTH_LINK'), 'AUTH LINK')



class GenerateTwitterOAUTH(APIView):
  def get(self,request):  
    url = "https://api.twitter.com/oauth/request_token"
    oauth = OAuth1Session(os.getenv('X_CONSUMER_KEY'), client_secret=os.getenv('X_CONSUMER_SECRET'))
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
      print(e)
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
      print(e)
      return Response(data="Bad request",status= status.HTTP_400_BAD_REQUEST)
      
       

class AccountSignup(APIView):
  def post(self, request):
    data = request.data
    ref_code = generate_random(7)
    print(ref_code, data)
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
      print(e, 'EROR')
      return Response(data="Bad request",status= status.HTTP_400_BAD_REQUEST)
    
class AllAccount(APIView):
  serializer_class = AccountSerialzer
  def get(self, request):
    try:
      all = AccountModel.objects.all()
      serializer = self.serializer_class(all, many=True)
      return Response(data=serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
      return Response(data="Bad request",status= status.HTTP_400_BAD_REQUEST)
    
    

class GetUserTwitterOauthForLogin(APIView):
  def get(self,request):  
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
      print(e)
      return Response(data="Bad request",status= status.HTTP_400_BAD_REQUEST)


class AccountLogin(APIView):
  serializer_class = AccountLoginSerialzer
  def post(self, request):
    payload = request.data 
    try:
      req = requests.post(f"https://api.twitter.com/oauth/access_token?oauth_token={payload['oauth_token']}&oauth_verifier={payload['oauth_verifier']}")
      if req.status_code == 200:
        new_list = req.text.split('&')
        data = {}
        for pair_string in new_list:
          splitted = pair_string.split('=')
          data[splitted[0]] = splitted[1] 
      instance = AccountModel.objects.get(x_id = data['user_id'])
      serializer = self.serializer_class(instance)
      return Response(data=serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
      print(e)
      return Response(data="Bad request",status= status.HTTP_400_BAD_REQUEST)


class GetSignedUpUser(APIView):
  serializer_class = AccountLoginSerialzer
  def post(self, request):
    payload = request.data
    print(payload, 'USER SIGNED UP')  
    try:
      instance = AccountModel.objects.get(x_id = payload['user_id'])
      serializer = self.serializer_class(instance)
      return Response(data=serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
      print(e)
      return Response(data="Bad request",status= status.HTTP_400_BAD_REQUEST)
    
    

class TelegramBotWebHook(APIView):
  def post(self,request):
    data = request.data
    print(os.getenv('TELEGRAM_AUTH_LINK'), 'AUTH LINK')
    try:
      if data.get('message'):
        id = data['message']['from']['id']
        username = data['message']['from']['username']
        if id and username:  
          data=f"CAT-AI Telegram bot interaction successful ✅✅✅.\n\nClick on the link below to continue:\n\n{os.getenv('TELEGRAM_AUTH_LINK')}?tg_id={id}&username={username}"
          telegram_send_message(chat_id=id, text=data)
          return Response(data={}, status=status.HTTP_200_OK)
    except Exception as e:
      return Response(data={""}, status=status.HTTP_200_OK)