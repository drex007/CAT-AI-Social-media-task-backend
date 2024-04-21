import os
from dotenv import load_dotenv
import requests
load_dotenv()


OPEN_AI_KEY=  os.getenv('OPENAI_API_KEY')

def text_compilation(prompt):
    #Call Openai API for text completion

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPEN_AI_KEY}", "Content-Type": "application/json"},
            json={
                 "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": f" You are an AI bot name KruxAI that is specialized in answering only Web3 and cryptocurrency related question. You are to take {prompt} and return a web3 related response to {prompt}"}]
            },
            timeout=60
        )
     
        data = response.json()
        if data['choices'][0]['message']['content'] != None:
        # if response.choices[0].message !=None:
            return {
            'status': 1,
            'response': data['choices'][0]['message']['content']
        
        }
    except Exception as e:
        print(e, "OPEN AI ERROR")
        return {
            'status': 0,
            'response': ''
        }
        
        
        


