from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json
import requests
import os

REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
ACCESS_TOKEN = os.getenv('LINE_ACCESS_TOKEN')
HEADER = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + ACCESS_TOKEN
}

def index(request):
    return HttpResponse("Hello World")

@csrf_exempt
def callback(request):
    events = json.loads(request.body.decode('utf-8'))['events']
    for event in events:
        reply_token = event['replyToken']
        if event['type'] == 'message':
            reply = e['message']['text']
        else:
            reply = 'テキストメッセージのみ受付けます。'
        reply_message(reply_token, reply)
    return HttpResponse("callback")

def reply_message(reply_token, reply):
    reply_body = {
        "replyToken":reply_token,
        "messages":[
            {
                "type":"text",
                "text": reply
            }
        ]
    }
    requests.post(REPLY_ENDPOINT, headers=HEADER, data=json.dumps(reply_body))
