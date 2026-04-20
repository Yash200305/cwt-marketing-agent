import os
import requests
import json
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# OpenRouter API endpoint for chat completions
url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

# Payload with a free Hermes model
data = {
    "model": "openrouter/free",
    "messages": [
        {
            "role": "system", 
            "content": "You are a helpful product marketing assistant."
        },
        {
            "role": "user", 
            "content": "In one short paragraph, define what a prediction market is."
        }
    ]
}

print("Sending request to OpenRouter...")

response = requests.post(url, headers=headers, data=json.dumps(data))

# Check if the request was successful
if response.status_code == 200:
    response_data = response.json()
    reply = response_data['choices'][0]['message']['content']
    print("\n--- LLM Response ---")
    print(reply)
else:
    print(f"Error {response.status_code}: {response.text}")