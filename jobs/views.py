from django.shortcuts import render
from django.http import HttpResponse

import json
import requests
import os

from line.views import push_message
from trello.views import get_all_cards

LINE_USERID = os.getenv('LINE_USERID')
LINE_GROUPID = os.getenv('LINE_GROUPID')

TRELLO_KEY = os.getenv('TRELLO_KEY')
TRELLO_TOKEN = os.getenv('TRELLO_TOKEN')

def index(request):
    return HttpResponse('jobs app')


def trello_to_line(request):
    behavior = request.GET.get('behavior')
    if behavior == 'due':
        get_due()
    else:
        pass
    return HttpResponse('trello to line')
