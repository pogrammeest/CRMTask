from django.urls import path, include
from APIService.views import my_view

urlpatterns = [
    path('', my_view),
]
