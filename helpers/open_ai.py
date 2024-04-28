import os
from dotenv import load_dotenv
import requests
from requests.exceptions import RequestException
from helpers.logs import error_logs
load_dotenv()

OPEN_AI_KEY=  os.getenv('OPEN_AI_KEY')
def text_compilation(prompt):

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPEN_AI_KEY}", "Content-Type": "application/json"},
            json={
                 "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": f" You are an AI bot named KruxAI that is specialized in answering only Web3 and cryptocurrency related question in four detailed paragraphs. You are to take {prompt} and return a web3 related response to {prompt}"}]
            },
            timeout=60
        )
        
        if response.status_code == 200:
            
     
            data = response.json()
            
            if data['choices'][0]['message']['content'] != None:
                return {
                'status': 1,
                'response': data['choices'][0]['message']['content']
            
            }
        else:
            error_logs(response.json(), "OPEN AI REQUEST")
            
    except (Exception, RequestException) as e:
        error_logs(e, "OPEN AI REQUEST")
        return {
            'status': 0,
            'response': ''
        }
        
        
        


