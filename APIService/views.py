from django.contrib.auth import authenticate
from django.shortcuts import render, HttpResponse
import requests
from rest_framework import viewsets, permissions, status
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView, )
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserDetails, Staff, RepairRequest
from .serializers import UserDetailSerializer, StaffSerializer, RepairRequestSerializer
from django.urls import reverse
from APIService.permissions import IsOwnerProfileOrReadOnly


class RepairRequestViewSet(viewsets.ModelViewSet):
    queryset = RepairRequest.objects.all()
    serializer_class = RepairRequestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=UserDetails.objects.get(user=self.request.user))


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class StaffViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [permissions.IsAdminUser]


class LoginView(APIView):
    def post(self, request, format=None):
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)

        url = request.build_absolute_uri(reverse('jwt-create'))

        data = {'username': username, 'password': password}

        r = requests.post(url, data=data)

        r = r.json()

        response = Response(r)


        response.set_cookie('token', r['access'], httponly=True)

        return response

        # user = authenticate(username=username, password=password)
        # if user is not None:
        #     if user.is_active:
        #         data = get_tokens_for_user(user)
        #         response.set_cookie(
        #             key=settings.SIMPLE_JWT['AUTH_COOKIE'],
        #             value=data["access"],
        #             expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
        #             secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        #             httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        #             samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        #         )
        #         csrf.get_token(request)
        #         email_template = render_to_string('login_success.html', {"username": user.username})
        #         login = EmailMultiAlternatives(
        #             "Successfully Login",
        #             "Successfully Login",
        #             settings.EMAIL_HOST_USER,
        #             [user.email],
        #         )
        #         login.attach_alternative(email_template, 'text/html')
        #         login.send()
        #         response.data = {"Success": "Login successfully", "data": data}
        #
        #         return response
        #     else:
        #         return Response({"No active": "This account is not active!!"}, status=status.HTTP_404_NOT_FOUND)
        # else:
        #     return Response({"Invalid": "Invalid username or password!!"}, status=status.HTTP_404_NOT_FOUND)
