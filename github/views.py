from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from trello.views import add_card, get_card_id, move_card

import os
import json
import requests

TODO_ID = os.getenv('TODO_ID')
DOING_ID = os.getenv('DOING_ID')
DONE_ID = os.getenv('DONE_ID')

ISSUES_LIST_ID = os.getenv('ISSUES_LIST_ID')
PULLREQUESTS_LIST_ID = os.getenv('PULLREQUESTS_LIST_ID')
WIP_LIST_ID = os.getenv('WIP_LIST_ID')
CLOSED_ID = os.getenv('CLOSED_LIST_ID')

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
                add_card(ISSUES_LIST_ID, name=title, desc=description)
            elif action == 'closed':
                pass
        elif event_type == 'label':
            pass
        elif event_type == 'pull_request':
            title = data['pull_request']['title']
            body = data['pull_request']['body']
            url = data['pull_request']['html_url']
            pr_id = data['pull_request']['id']
            description = url + '\n\n' + body + '\n\nid:' + pr_id
            if action == 'opened' or action_type == 'reopened':
                add_card(PULLREQUESTS_LIST_ID, name=title, desc=description)
            # elif action == 'labeled':
            #     for label in data['pull_request']['labels']
            #         if label['name'] == 'WIP':
            #             card_id = get_card_id('id:'+pr_id)
            #             move_card(card_id, WIP_LIST_ID)
            #         else:
            #             pass
            else:
                pass
        else:
            pass               
    except Exception as e:
        pass
    return HttpResponse("callback")
