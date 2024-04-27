import random
import string
import requests
import os
from rest_framework.response import Response
from rest_framework import status
from dotenv import load_dotenv
from django.http import HttpResponse
from datetime import  datetime, date
import math

from account.models import AccountModel
from task.models import TaskRewardModel
from adverts.models import AdvertModel


def generate_random(length):
  letters = string.ascii_letters
  return ''.join(random.choice(letters.upper()) for _ in range(length))




    



load_dotenv()

TOKEN=os.getenv("TELEGRAM_TOKEN_KEY")


def telegram_send_message(chat_id,text):
    try:
        url =f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload ={'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML', 'reply_markup':{
             "inline_keyboard": [
            [
              {
                "text": "Main Menu",
                "callback_data": "menu"
              },
              
        
            ]
          ]
            }}
        r = requests.post(url, json=payload)
        print(r.status_code, 'STATS')
        if r.status_code == 200:
            # data = {
            #     'message_id': r.json()['result']['message_id'],
            #     'chat_id': r.json()['result']['chat']['id']
            # }
            return HttpResponse()
        else:
            return HttpResponse()
    except Exception as e:
        return HttpResponse()

    
    

def rugChecker_send_message(chat_id,text):
  
    try:
        user = AccountModel.objects.filter(tg_id = chat_id).first()
        task = TaskRewardModel.objects.filter().first()
        if user.last_bot_interaction is None or user.last_bot_interaction < date.today():
          user.last_bot_interaction = date.today()
          user.save()
        
        url =f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        
        payload ={'chat_id': chat_id, 'text':text,  'parse_mode': 'HTML', 'reply_markup':{
             "inline_keyboard": [
        [
          {
            "text": "Main Menu",
            "callback_data": "menu"
          },
     
        ]
      ]
        }}
        r = requests.post(url, json=payload)
        if r.status_code == 200:
          if int(user.bot_interaction_count) < 100:
            user.bot_point = int(user.bot_point) + int(task.others)
            user.bot_interaction_count = int(user.bot_interaction_count) + 1
            user.save()                  
          return HttpResponse()
        else:
            return HttpResponse()
    except Exception as e:
        return HttpResponse()



    


def timeConvertToDays(milliseconds):
    current_time_millis = datetime.now().timestamp() * 1000
    days_difference = (current_time_millis - milliseconds) / (1000 * 3600 * 24)
    days = str(days_difference).split(".")[0]
    hours = str(days_difference).split(".")[1]
    des = hours.split(".")[:2]
    decimal = f".{des[0]}"
    hrs = float(decimal) * 24
    return {"days": days, "hours": math.floor(hrs)}

def rugCheckFunction(address):
    req = requests.get(f"https://api.dexscreener.com/latest/dex/tokens/{address}")
    req2 = requests.get(f"https://api.honeypot.is/v2/IsHoneypot?address={address}")
    if req.status_code == 200 and req.json().get("pairs"):
        res = req.json()['pairs'][0]
        liquidity = res['liquidity']['quote']
        token = res['quoteToken']['symbol']
        dateCreated = timeConvertToDays(res['pairCreatedAt'])
        days = dateCreated['days']
        hrs =dateCreated['hours']
        
        is_honeypot = req2.json()['honeypotResult']['isHoneypot'] if req2.status_code ==200  else "N/A"
        holders = req2.json()['token']['totalHolders']  if req2.status_code ==200 else "N/A"
        buy_tax =  req2.json()['simulationResult']['buyTax'] if req2.status_code == 200 else "N/A"
        sell_tax = req2.json()['simulationResult']['sellTax'] if req2.status_code == 200 else "N/A"
        percentage_liquidity = round((req2.json()['pair']['liquidity']/res['fdv']) * 100, 3) if req2.status_code == 200 else "N/A"
    
        
        
        
        data = {
            "status":  True,
            "network": res['chainId'],
            "dex": res['dexId'],
            "symbol": res['baseToken']['symbol'],
            "name": res['baseToken']['name'],
            "ca": res['baseToken']['address'],
            "priceUsd": res['priceUsd'],
            "txn_24h_buy": res['txns']['h24']['buys'],
            "txn_24h_sell": res['txns']['h24']['sells'],
            "priceChange": res['priceChange']['h24'],
            "volume24h": res['volume']['h24'],
            "marketCap": res['fdv'],
            "liquidity": f"{liquidity} {token}",
            "dateCreated": f"{days} days {hrs} hrs",
            "url": res['url'],
            "is_honeypot": is_honeypot,
            "holders": holders,
            "buy_tax": buy_tax,
            "sell_tax": sell_tax,
            "liq_percent": percentage_liquidity
            
        }
        return data
    else:
        return {"status":False,"message":f"❌❌❌❌No response❌❌❌❌.\n\nEnsure the contract address '<b>{address}</b>' is correct."}
    


def aibot_message(chat_id,text, is_true = 0):
    try:
        user = AccountModel.objects.filter(tg_id = chat_id).first()
        task = TaskRewardModel.objects.filter().first()
        
        if user.last_bot_interaction is None or user.last_bot_interaction < date.today():
          user.last_bot_interaction = date.today()
          user.save()
        url =f"https://api.telegram.org/bot{TOKEN}/sendMessage"
      
        payload ={'chat_id': chat_id, 'text':f"{text}",  'parse_mode': 'HTML', 'reply_markup':{
             "inline_keyboard": [
            [
              {
                "text": "KruxAI",
                "callback_data": "aibot"
              },
              {
                "text": "Token Checker",
                "callback_data": "tokenbot"
              },
        
            ],
            [
              {
                "text": "How I Work",
                "callback_data": "work"
              },
            
        
            ]
          ]
            }}
        r = requests.post(url, json=payload)
        if r.status_code == 200:
            if int(user.bot_interaction_count) < 100 and is_true ==1:
              user.bot_point = int(user.bot_point) + int(task.others)
              user.bot_interaction_count = int(user.bot_interaction_count) + 1
              user.save()   
            
            return HttpResponse()
        else:
            return HttpResponse()
    except Exception as e:
        return HttpResponse()
    
def tokenchecker_message(chat_id,text, is_true = 0):
    try:
        user = AccountModel.objects.filter(tg_id = chat_id).first()
        task = TaskRewardModel.objects.filter().first()
        if user.last_bot_interaction is None or user.last_bot_interaction < date.today():
          user.last_bot_interaction = date.today()
          user.save()
        url =f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                
        payload ={'chat_id': chat_id, 'text':text,  'parse_mode': 'HTML', 'reply_markup':{
             "inline_keyboard": [
        [
          {
            "text": "KruxAI",
            "callback_data": "aibot"
          },
          {
            "text": "Token Checker",
            "callback_data": "tokenbot"
          },
     
        ],
         [
          {
            "text": "How I Work",
            "callback_data": "work"
          },
        
     
        ]
      ]
        }}
        r = requests.post(url, json=payload)
      
        if r.status_code == 200:
          if int(user.bot_interaction_count) < 100 and is_true == 1:
            user.bot_point = int(user.bot_point) + int(task.others)
            user.bot_interaction_count = int(user.bot_interaction_count) + 1
            user.save()   
            
            
          return HttpResponse()
        else:
            return HttpResponse()
    except Exception as e:
        return HttpResponse()
    
    
def mainmenu_message(chat_id,text):
    try:
        url =f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        
        payload ={'chat_id': chat_id, 'text':text,  'parse_mode': 'HTML', 'reply_markup':{
             "inline_keyboard": [
        [
          {
            "text": "KruxAI",
            "callback_data": "aibot"
          },
          {
            "text": "Token Checker",
            "callback_data": "tokenbot"
          },
     
        ],
        [
          {
            "text": "How I Work",
            "callback_data": "work"
          },
        
     
        ]
      ]
        }}
        r = requests.post(url, json=payload)
        if r.status_code == 200:
            data = {
                'message_id': r.json()['result']['message_id'],
                'chat_id': r.json()['result']['chat']['id']
            }
            
            return HttpResponse()

        else:
            return HttpResponse()
    except Exception as e:
        return HttpResponse()
      
      
def how_i_work_message(chat_id,text):
    try:
        url =f"https://api.telegram.org/bot{TOKEN}/sendMessage"

        payload ={'chat_id': chat_id, 'text':text,  'parse_mode': 'HTML', 'reply_markup':{
             "inline_keyboard": [
        [
          {
            "text": "KruxAI",
            "callback_data": "aibot"
          },
          {
            "text": "Token Checker",
            "callback_data": "tokenbot"
          },
     
        ],
        [
          {
            "text": "How I Work",
            "callback_data": "work"
          },
        
     
        ]
      ]
        }}
        r = requests.post(url, json=payload)
        if r.status_code == 200:
          # data = {
          #       'message_id': r.json()['result']['message_id'],
          #       'chat_id': r.json()['result']['chat']['id']
          #   }
            
          return HttpResponse()
            
        else:
            return HttpResponse()
    except Exception as e:
        return HttpResponse()
    
    

def deletebot_message(chat_id,message_id):
    try:
        url =f"https://api.telegram.org/bot{TOKEN}/deleteMessage"
        
        payload ={'chat_id': chat_id, 'message_id':message_id}
        r = requests.post(url, json=payload)
        if r.status_code == 200:
            return HttpResponse()
        else:
            return HttpResponse()
    except Exception as e:
        return HttpResponse()
      

  
  
def telegram_callback_query(data):
  # if data.get("callback_query") :
  user = data['callback_query']['from']['id']
  instance = AccountModel.objects.filter(tg_id = user).first()
  if instance is not None:
      message_text = data['callback_query']['data']
      if message_text== "aibot":
          instance.bot_status = "aibot"
          instance.save()
          res = aibot_message(instance.tg_id, "You are currently using <b>KruxAI</b>")
          return HttpResponse()
      if message_text == "tokenbot":
          instance.bot_status = "tokenbot"
          instance.save()
          res = tokenchecker_message(instance.tg_id, "You are currently using <b>KruxAI Token Checker</b>")
          return HttpResponse()
      if data['callback_query']['data'] == "menu":
          mainmenu_message(instance.tg_id, "Main Menu")
          return HttpResponse()
      if data['callback_query']['data'] == "work":
          res = how_i_work_message(instance.tg_id, """🚀 <b>Introducing the KruxAI Bot: Learn, Interact and Earn! </b> 🤖🌐\n\nThis incredible bot is the cornerstone of the KruxAI ecosystem, bringing you everything you need for Web3 education, token analysis, and airdrops - all in one sleek package!\n\n🎁 Get ready for a treasure trove of features designed to make Web3 a breeze, even for the newest of newbies. Here's what's inside: \n\n🧠 <b>AI-Powered Web3 Wisdom</b>: Dive into the AI section and fire away with your burning Web3 questions. Our bot, powered by ChatGPT, serves up detailed answers, making complex topics a walk in the digital park! \n\n📊 <b>Token Checker Magic</b>: Want to analyze tokens? No need to leave your comfy Telegram app! Head over to the Token Checker section, enter a contract address (CA), and watch the bot work its magic. It fetches basic token details in less than 5 seconds! For popular coins/tokens, just use '/ticker' (e.g., /eth) for a lightning-fast lookup.\n\n🪂 <b>Airdrops/ Revenue Sharing</b>: KruxAI bot users will receive airdrops in both $KRUX token and a percentage of every token airdropped to us by partner projects and communities. Revenue sharing is an important part of our ecosystem\n\n🔶🔶 <b>Token Checker Rating</b> 🔶🔶\n\nSafe: 🟢 🟢 🟢\n\nSafe with low liquidity: 🟡 🟡 🟡\n\nUnsafe: 🔴 🔴 🔴\n\n💡<b>How it Works</b>:\n\n1. Interact with the bot.\n2. Choose the bot section you want to explore.\n3. In the AI section, ask away for Web3 wisdom.\n4. In the Token Checker section, enter a CA to analyze tokens.\n5. Access a list of commands via the menu at the bottom left of the bot.\n\n🚨NOTE: The KruxAI bot rewards you with 100 points per interaction with a daily cap of 10000 points.\n\nAnd this is just the beginning! We're constantly building and fine-tuning to bring you even more fantastic features and updates.\n\nGet ready to supercharge your Web3 journey with the KruxAI Bot! 🚀🔥""")
          return HttpResponse()
        
  else:
      return HttpResponse()






def formatRugCheckerMessage(req):
      network = req['network']
      dex =f"{req['dex'][0].upper()}{req['dex'][1:]}"
      symbol= req['symbol']
      name = req['name']
      ca = req['ca']
      price = req["priceUsd"]
      buys= req["txn_24h_buy"]
      sells = req['txn_24h_sell']
      priceChange = req['priceChange']
      volume =  req["volume24h"]
      marketCap = req["marketCap"]
      liquidity= req["liquidity"]
      dateCreated = req["dateCreated"]
      info=req["url"]
      holders = req['holders']
      honeypot = req['is_honeypot']
      buy_tax = req['buy_tax']
      sell_tax = req['sell_tax']
      percentage = req['liq_percent']
      comments =  "🟢🟢🟢" if honeypot == False and float(percentage) >= 10 else ("🟡🟡🟡" if honeypot == False and float(percentage) < 10 else ("🔴🔴🔴" if honeypot == True else "N/A"))
                            
      return f"""
    \n\n\n\n\n\n
    
    🔶Token Rating: {comments}\n\n
    💡Name: {name}\n\n
    ⚡️Symbol: {symbol}\n\n
    ⛓️Network: {network.upper()}\n\n
    🏦Dex: {dex}\n\n
    💎Contract Address: {ca}\n\n
    💥Market Cap: ${marketCap}\n\n
    💦Liquidity: {liquidity} ({percentage} %)\n\n
    💰Price(USD): {price}\n\n
    ✊🏽Total Holders: {holders}\n\n
    🎃Honeypot: {honeypot}\n\n
    🟩BuyTax: {buy_tax}\n\n
    🟥Sell Tax : {sell_tax}\n\n
    💚24h Buy: {buys}\n\n
    ❤️24h Sell: {sells}\n\n
    📊Price Change 24h: {priceChange}%\n\n
    🏪Volume 24h: ${volume}\n\n
    ⏳Date Created: {dateCreated}\n\n
    🚀More Info: {info}\n\n<b>⚠️NOTE: We do not assure you that our Token checker can detect all scams. Be sure to DYOR before investing in cryptocurrencies.⚠️</b>\n\n
                      
    """
  
  

def get_coin_price(tag):
    url = f"https://data.messari.io/api/v1/assets/{tag}/metrics"
    response = requests.get(url=str(url))
    if response.status_code == 200:
        price = response.json()['data']['market_data']['price_usd']
        name = response.json()['data']['name']
        volume = response.json()['data']['market_data']['volume_last_24_hours']
        market_cap = response.json()['data']['marketcap']['current_marketcap_usd']
        return f"🚀 Name: {name} \n\n💹 Price: ${price} \n\n📊 MarketCap: ${market_cap} \n\n✅ 24hrs Volume: ${volume}"
    return "No response generated at the moment."
  
  
  
  
  
# https://api.telegram.org/bot123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11/setWebhook?url=https://www.example.com




def format_advertText(advert):
  return f"""\n\n\n\n🚨🚨 Sponsored Ad 🚨🚨
        \n\n<b>{advert.title}</b>
        \n{advert.body}
        \n\n<a href='{advert.web_link}'> 🌐 WEB</a> | <a href='{advert.tg_link}'>🔗 TELEGRAM</a> | <a href='{advert.twitter_link}'>💡 TWITTER</a>\n
"""



def choose_adverts():
  adverts = AdvertModel.objects.all()
  random_number = 0
  if len(adverts) > 1:
    random_number = random.randint(0, len(adverts)-1)
  return format_advertText(adverts[random_number])
  
  