from django.urls import path, include
from rest_framework.routers import DefaultRouter

from APIService.views import UserViewSet, StaffViewSet, RepairRequestViewSet, LoginView

router = DefaultRouter()
router.register(r'tasks', RepairRequestViewSet, basename='tasks')
router.register(r'users', UserViewSet, basename='customs-users')
router.register(r'staff', StaffViewSet)

urlpatterns = [

    path('', include(router.urls)),
    path('login/', LoginView.as_view())
]
