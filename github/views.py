from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json
import requests

def index(request):
    return HttpResponse("Hello GitHub")

@csrf_exempt
def callback(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        from pprint import pprint
        pprint(data)
    except Exception as e:
        pass
    return HttpResponse("callback")
