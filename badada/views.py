from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializers import TestDataSerializer


def print(request):
    return HttpResponse("This is badada app")


@api_view(['GET'])
def question(request):
    data = Question.objects.all()
    serializer = TestDataSerializer(data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def answer(request):
    data = Answer.objects.all()
    serializer = TestDataSerializer(data, many=True)
    return Response(serializer.data)