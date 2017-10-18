from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return HttpResponse("Hello World")

@csrf_exempt
def callback(request):
    return HttpResponse("callback")
