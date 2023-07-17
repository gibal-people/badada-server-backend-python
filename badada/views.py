from django.shortcuts import render
from django.http import HttpResponse


def print(request):
    return HttpResponse("This is badada app")