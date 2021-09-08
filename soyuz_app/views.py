from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    # send back a text response
    return HttpResponse("Hello, world. You're at the index.")
