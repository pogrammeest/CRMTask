import logging

import requests.cookies
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse
from django.urls import reverse
from rest_framework.response import Response
from rest_framework import status
from .forms import LoginForm, RegForm
import jwt
from CRMForTestTask.settings import SECRET_KEY
from APIService.models import User, RepairRequest, UserDetails
from django.db.models import Q

global logger
logger = logging.getLogger(__name__)  # for logging in DJDT


def landing(request):
    token = request.COOKIES.get('token')
    try:
        user_data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user = User.objects.get(id=user_data['user_id'])
    except jwt.exceptions.PyJWTError:
        user = None

    # logger.debug(user.username)

    return render(request, 'Front/base.html', context={'user': user})


def logout(request):
    response = HttpResponseRedirect('/')
    response.delete_cookie('token')
    return response


def login(request):
    alert = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            url = request.build_absolute_uri(reverse('jwt-create'))
            data = form.cleaned_data
            r = requests.post(url, data=data)
            alert = r.json()
            alert['status'] = str(r.status_code)
            alert[
                'message'] = "Вы вошли!" if r.status_code == status.HTTP_200_OK else f"{''.join(list(alert.values())[0])}"
            response = render(request, 'Front/login.html', context={'form': form, 'alert': alert})
            try:
                r = r.json()
                response.set_cookie('token', r['access'], httponly=True)
            except KeyError:
                response.set_cookie('token', '', httponly=True)
            return response
    else:
        form = LoginForm()
    return render(request, 'Front/login.html', context={'form': form, 'alert': alert})


def registration(request):
    alert = None

    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            url = request.build_absolute_uri('/auth/users/')
            data = form.cleaned_data
            r = requests.post(url, data=data)
            alert = r.json()
            alert['status'] = str(r.status_code)
            alert[
                'message'] = "Вы успешно зарегистрированы!" if r.status_code == status.HTTP_201_CREATED else f"{''.join(list(alert.values())[0])}"
    else:
        form = RegForm()

    return render(request, 'Front/register.html', context={'form': form, 'alert': alert})


# def own_list(request):
#     token = request.COOKIES.get('token')
#     url = request.build_absolute_uri(reverse('jwt-verify'))
#     data = {'token': token}
#     response = requests.post(url, data=data)
#     if not response.json():
#         user_data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#         user = User.objects.get(id=user_data['user_id'])
#
#         return render(request, 'Front/blog-grid.html', context={'user': user})
#     else:
#         return HttpResponse('FORBIDDEN')


def own_list(request):
    token = request.COOKIES.get('token')
    url = request.build_absolute_uri(reverse('jwt-verify'))
    data = {'token': token}
    response = requests.post(url, data=data)
    if not response.json():
        user_data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_detail = UserDetails.objects.get(user=user_data['user_id'])
        user = User.objects.get(id=user_data['user_id'])
        headers = {"Authorization": f"Bearer {token}"}
        url = request.build_absolute_uri(reverse('customs-users-detail', kwargs={'pk': user_detail.id}))
        response = requests.get(url, headers=headers)
        own_tasks = response.json()['repair_request']
        try:
            q = request.GET['q']
            objects = RepairRequest.objects.filter(title__search=q).filter(id__in=own_tasks)
        except KeyError:
            objects = RepairRequest.objects.filter(id__in=own_tasks)
        return render(request, 'Front/blog-grid.html',
                      context={'user_detail': user_detail, 'objects': objects, 'user': user})
    else:
        return HttpResponse('FORBIDDEN')
