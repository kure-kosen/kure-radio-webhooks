from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello World")

def callback(request):
    context_instance=RequestContext(request)
    return HttpResponse("callback" + context_instance)
