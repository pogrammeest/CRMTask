from django.urls import path, include
from rest_framework.routers import DefaultRouter

from Front.views import *

urlpatterns = [

    path('', own_list),
    path('login/', login)
]
