import random
import string
import requests
import os
from rest_framework.response import Response
from rest_framework import status
from dotenv import load_dotenv
load_dotenv()
TELEGRAM_TOKEN=os.getenv('TELEGRAM_TOKEN_KEY')

def generate_random(length):
  letters = string.ascii_letters
  return ''.join(random.choice(letters.upper()) for _ in range(length))



def telegram_send_message(chat_id,text):
    try:
        url =f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload ={'chat_id': chat_id, 'text': text}
        r = requests.post(url, json=payload)
        if r.status_code == 200:
            return 
        else:
          pass
    except Exception as e:
      return