from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from trello.views import add_card

import os
import json
import requests

TODO_ID = os.getenv('TODO_ID')
DOING_ID = os.getenv('DOING_ID')
DONE_ID = os.getenv('DONE_ID')

def index(request):
    return HttpResponse("Hello GitHub")

@csrf_exempt
def callback(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        event_type = request.META['HTTP_X_GITHUB_EVENT']
        action = data['action']
        if event_type == 'issues':
            if action == 'opened' or action == 'reopened':
                title = data['issue']['title']
                body = data['issue']['body']
                url = data['issue']['html_url']
                description = url + '\n\n' + body
                add_card(TODO_ID, name=title, desc=description)
            elif action == 'closed':
                pass
        elif event_type == 'label':
            pass
    except Exception as e:
        pass
    return HttpResponse("callback")
