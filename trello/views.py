from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json
import requests
import os

from line.views import push_message

LINE_USERID = os.getenv('LINE_USERID')
LINE_GROUPID = os.getenv('LINE_GROUPID')

TRELLO_KEY = os.getenv('TRELLO_KEY')
TRELLO_TOKEN = os.getenv('TRELLO_TOKEN')

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

def add_card(idList,  desc='', due='', fileSource='', idAttachmentCover='', idBoard='', idCardSource='', idLabels='', idMembers='', keepFromSource='', labels='', name='', pos='top', urlSource=''):
    query = {
        "desc": desc,
        "due": due,
        "fileSource": fileSource,
        "idAttachmentCover": idAttachmentCover,
        "idBoard": idBoard,
        "idCardSource": idCardSource,
        "idLabels": idLabels,
        "idList": idList,
        "idMembers": idMembers,
        "keepFromSource": keepFromSource,
        "labels": labels,
        "name": name,
        "pos": pos,
        "urlSource": urlSource,
    }
    r = requests.post("https://api.trello.com/1/cards", json=query, params={"key": TRELLO_KEY, "token": TRELLO_TOKEN})
    print(r.text)

def move_card(idCard, idList, closed='', desc='', due='', fileSource='', idAttachmentCover='', idBoard='', idCardSource='', idLabels='', idMembers='', keepFromSource='', labels='', name='', pos='top', urlSource='', dueComplete=''):
    query = {
        "closed": closed,
        "desc": desc,
        "due": due,
        "fileSource": fileSource,
        "idAttachmentCover": idAttachmentCover,
        "idBoard": idBoard,
        "idCardSource": idCardSource,
        "idLabels": idLabels,
        "idList": idList,
        "idMembers": idMembers,
        "keepFromSource": keepFromSource,
        "labels": labels,
        "name": name,
        "pos": pos,
        "urlSource": urlSource,
        "dueComplete": dueComplete
    }
    r = requests.put(f'https://api.trello.com/1/cards/{idCard}', json=query, params={"key": TRELLO_KEY, "token": TRELLO_TOKEN})
    print(r.text)


def get_card_id(search_id):
    query = {"query": search_id}
    cards = request.get("https://api.trello.com/1/search", json=query, params={"key": TRELLO_KEY, "token": TRELLO_TOKEN}).json()['cards']
    card_id = cards[0]['id']
    return card_id
    
