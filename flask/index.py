from flask import Flask, request
from flask_cors import CORS
import json
import requests
import time
import sys

auth = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + "open ai api key here"
}

app = Flask(__name__)
CORS(app)

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return json.dumps({
            "msg": "to the moon",
            "time_taken": 5
        })
    start = time.time()
    received = json.loads(request.data) #array of base64 strings
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "Imagine you are a league of legends coach"
                    }
                ]   
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Give me advice on how to improve and actionable steps" 
                    }
                ]
            }
            ],
            "max_tokens": 400
    }
    for i in range(10):
        payload["messages"][1]["content"].append({
            "type": "image_url",
            "image_url": {
                "url": received[i],
                "detail": "low"
            }
        })

    resp_raw = requests.post("https://api.openai.com/v1/chat/completions", json=payload, headers=auth)
    print(resp_raw)
    resp = resp_raw.json()
    print(resp)
    time_taken = time.time() - start
    response = json.dumps({
        "msg": resp["choices"][0]["message"]["content"],
        "time_taken": time_taken
    })
    return response
        

    
if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug = False, port = 80)