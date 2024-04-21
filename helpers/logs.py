import requests
import os
from dotenv import load_dotenv

load_dotenv()

user_interaction_url = os.getenv('USER_INTERACTIONS_WEBHOOK')
error_logs_url = os.getenv('ERROR_LOGS_WEBHOOK') 


def user_interaction_logs(user_name, text, response):
    body = f"""
        user_name: {user_name} \n\n
        text: {text} \n\n
        response: {response}
        """
    try:
            req = requests.post(
                user_interaction_url,
                json={"content":body}
                
            )
    except Exception as e:
        print(e)
        
        
        
def error_logs(error, action):
    body = f"""
        error: {error} \n\n
        action: {action}
        """
    try:
            req = requests.post(
                error_logs_url,
                json={"content":body}
                
            )
    except Exception as e:
        print(e)