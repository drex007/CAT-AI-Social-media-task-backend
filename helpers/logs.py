import requests
import os
from dotenv import load_dotenv
from datetime import date, datetime

load_dotenv()

user_interaction_url = os.getenv('USER_INTERACTIONS_WEBHOOK')
error_logs_url = os.getenv('ERROR_LOGS_WEBHOOK') 


def user_interaction_logs(user_name, text, response):
    body = f"""user_name: {user_name} \n\ntext: {text} \n\nresponse: {response}"""
    try:
            req = requests.post(
                user_interaction_url,
                json={"content":body}
                
            )
    except Exception as e:
        print(e)
        
        
        
def error_logs(error, action):
    d = datetime.now()
    body = f"""error: {error} \n\naction: {action} \n\ndatetime:{d} """
    try:
        req = requests.post(
            error_logs_url,
            json={"content":body}
            
        )
    except Exception as e:
        print(e)