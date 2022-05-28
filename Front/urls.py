from django.urls import path, include
from rest_framework.routers import DefaultRouter

from Front.views import *

urlpatterns = [

    path('', landing, name='home-page'),
    path('login/', login, name='login'),
    path('reg/', registration, name='registration'),
    path('logout/', logout, name='logout'),
    path('my-request/', own_list, name='my-request')
]
