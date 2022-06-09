import logging

import requests.cookies
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.urls import reverse
from django.views import View
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
#         return render(request, 'Front/requests-grid.html', context={'user': user})
#     else:
#         return HttpResponse('FORBIDDEN')

def verification(request):
    token = request.COOKIES.get('token')
    url = request.build_absolute_uri(reverse('jwt-verify'))
    data = {'token': token}
    response = requests.post(url, data=data)
    if not response.json():
        return token, True
    return None, False


def own_list(request):
    token, flag = verification(request)
    if flag:
        user_data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_detail = UserDetails.objects.get(user=user_data['user_id'])
        user = User.objects.get(id=user_data['user_id'])
        headers = {"Authorization": f"Bearer {token}"}
        url = request.build_absolute_uri(reverse('customs-users-detail', kwargs={'pk': user_detail.id}))
        response = requests.get(url, headers=headers)
        own_tasks = response.json()['repair_request']
        try:
            q = request.GET['q']
            if str(q).strip() == '':
                objects = RepairRequest.objects.filter(id__in=own_tasks)
            else:
                objects = RepairRequest.objects.filter(title__search=q).filter(id__in=own_tasks) | \
                          RepairRequest.objects.filter(description__search=q).filter(id__in=own_tasks) | \
                          RepairRequest.objects.filter(status__search=q).filter(id__in=own_tasks)
        except KeyError:
            objects = RepairRequest.objects.filter(id__in=own_tasks)
        return render(request, 'Front/requests-grid.html', context={'user_detail': user_detail, 'objects': objects, 'user': user})
    else:
        return HttpResponse('FORBIDDEN')


class RequestDetailView(View):
    http_method_names = ['get', 'post', 'put', 'delete']

    def dispatch(self, request, pk, *args, **kwargs):
        token, flag = verification(request)
        if flag:
            method = self.request.POST.get('_method', '').lower()
            # user_data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            headers = {"Authorization": f"Bearer {token}"}
            url = request.build_absolute_uri(reverse('tasks-detail', kwargs={'pk': pk}))
            if method == 'put':
                title = self.request.POST.get('title', '')
                description = self.request.POST.get('description', '')
                response = requests.put(url, headers=headers, data={'title': title, 'description': description})
                print(response)
                return HttpResponseRedirect(reverse('request-detail', kwargs={'pk': pk}))
            if method == 'delete':
                return self.delete(*args, **kwargs)
            return super(RequestDetailView, self).dispatch(*args, **kwargs)
        else:
            return HttpResponse('FORBIDDEN')

    def put(self, *args, **kwargs):
        print("Hello, i'm %s!" % self.request.POST.get('_method'))
        return HttpResponseRedirect(reverse('request-detail'))

    def delete(self, *args, **kwargs):
        print("Hello, i'm %s!" % self.request.POST.get('_method'))


def request_detail(request, pk):
    token, flag = verification(request)
    if flag:
        task = get_object_or_404(RepairRequest, pk__exact=pk)
        return render(request, 'Front/request-details.html', context={'task': task, 'pk': pk})
    else:
        return HttpResponse('FORBIDDEN')

