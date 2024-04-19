import os
import requests
from utils.prompts import prompt_classification, prompt_extraction
def query_classification(base64_image, detail="low"):
    url = "https://api.openai.com/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
    }

    json = {
        "model":"gpt-4-turbo",
        "temperature": 0,
        "messages":[
            {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt_classification},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}", "detail": detail}}
            ],
            }
        ]
    }

    response = requests.post(url=url, headers=headers, json=json)
    completion = response.json()

    tokens_prompt = completion['usage']['prompt_tokens']
    tokens_completion = completion['usage']['completion_tokens']
    tokens_total = completion['usage']['total_tokens']
    print(f"Classification:\t{tokens_prompt} + {tokens_completion}\t= {tokens_total} tokens used")
    
    return completion['choices'][0]['message']['content']


def query_extraction(base64_image, detail="high"):
  url = "https://api.openai.com/v1/chat/completions"
  
  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
  }

  json = {
      "model":"gpt-4-turbo",
      "temperature":0,
      "messages":[
        {
          "role": "user",
          "content": [
            {"type": "text", "text": prompt_extraction},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}", "detail": detail}}
          ],
        }
      ]
  }

  response = requests.post(url=url, headers=headers, json=json)
  completion = response.json()
  
  tokens_prompt = completion['usage']['prompt_tokens']
  tokens_completion = completion['usage']['completion_tokens']
  tokens_total = completion['usage']['total_tokens']
  print(f"Extraction:\t{tokens_prompt} + {tokens_completion}\t= {tokens_total} tokens used")
  
  return completion['choices'][0]['message']['content']