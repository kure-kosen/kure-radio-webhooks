from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json
import requests
import os

REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
PUSH_ENDPOINT = 'https://api.line.me/v2/bot/message/push'
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
            if event['message']['type'] == 'text':
                if 'debug' in event['message']['text']:
                    reply = event['message']['text']
                    if 'userId' in event['source']:
                        reply += '\nuserId:' + event['source']['userId']
                    if 'groupId' in event['source']:
                        reply += '\ngroupId:' + event['source']['groupId']
                    if 'roomId' in event['source']:
                        reply += '\nroomId:' + event['source']['roomId']
                    reply_message(reply_token, reply)
    return HttpResponse("callback")

def reply_message(reply_token, reply):
    reply_body = {
        "replyToken":reply_token,
        "messages":[
            {
                "type": "text",
                "text": reply
            }
        ]
    }
    requests.post(REPLY_ENDPOINT, headers=HEADER, data=json.dumps(reply_body))

def push_message(to, message):
    push_body = {
        "to": to,
        "messages":[
            {
                "type": "text",
                "text": message
            }
        ]
    }
    requests.post(PUSH_ENDPOINT, headers=HEADER, data=json.dumps(push_body))
    
