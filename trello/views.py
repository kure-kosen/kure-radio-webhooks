from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json
import requests
import os

from line.views import push_message

REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
ACCESS_TOKEN = os.getenv('LINE_ACCESS_TOKEN')
LINE_USERID = os.getenv('LINE_USERID')
LINE_GROUPID = os.getenv('LINE_GROUPID')
HEADER = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + ACCESS_TOKEN
}

def index(request):
    return HttpResponse("Hello World")

@csrf_exempt
def callback(request):
    try:
        action = json.loads(request.body.decode('utf-8'))['action']
        from pprint import pprint
        pprint(action)
        entities = action['display']['entities']
        action_type = action['display']['translationKey']
        if action_type == 'action_create_card':
            list_name = entities['list']['text']
            card_name = entities['card']['text']
            member_name = entities['memberCreator']['text']
            body = f'カード「{card_name}」がリスト「{list_name}」に追加されました。\n追加者:{member_name}'
            push_message(LINE_GROUPID, body)
        elif action_type == 'action_move_card_from_list_to_list':
            after_list_name = entities['listAfter']['text']
            before_list_name = entities['listBefore']['text']
            card_name = entities['card']['text']
            member_name = entities['memberCreator']['text']
            body = f'カード「{card_name}」がリスト「{before_list_name}」からリスト「{after_list_name}」に移動されました。\n移動者:{member_name}'
            push_message(LINE_GROUPID, body)
    except Exception as e:
        pass
    return HttpResponse("callback")

