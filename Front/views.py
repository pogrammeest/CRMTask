import requests.cookies
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse
from django.urls import reverse
from rest_framework.response import Response
from rest_framework import status
from .forms import LoginForm


def landing(request):
    return render(request, 'Front/index-5.html', context={})


def login(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            url = request.build_absolute_uri(reverse('jwt-create'))

            data = form.cleaned_data

            r = requests.post(url, data=data)
            response = HttpResponseRedirect('/')
            try:
                r = r.json()
                response.set_cookie('token', r['access'], httponly=True)
            except KeyError:
                response.set_cookie('token', '', httponly=True)
            return response

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(request, 'Front/login.html', context={'form': form})


def own_list(request):
    token = request.COOKIES.get('token')
    url = request.build_absolute_uri(reverse('jwt-verify'))
    data = {'token': token}
    response = requests.post(url, data=data)
    if not response.json():
        return render(request, 'Front/index-5.html', context={})
    else:
        return HttpResponse('FORBIDDEN')
