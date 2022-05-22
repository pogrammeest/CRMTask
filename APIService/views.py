from django.shortcuts import render, HttpResponse
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView, )
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .serializers import userProfileSerializer
from APIService.permissions import IsOwnerProfileOrReadOnly
from rest_framework.permissions import IsAdminUser


class UserProfileListCreateView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = userProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class userProfileDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = userProfileSerializer
    permission_classes = [IsOwnerProfileOrReadOnly, IsAuthenticated]


def my_view(reqeust):
    return render(reqeust, 'APIService\landing.html')
