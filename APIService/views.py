from django.shortcuts import render, HttpResponse


# Create your views here.

def my_view(reqeust):
    return HttpResponse('Hello!')
