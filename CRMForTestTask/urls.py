from django.contrib import admin
from django.urls import path, include
import debug_toolbar
from CRMForTestTask.settings import DEBUG

urlpatterns = [
    path('admin/', admin.site.urls),
    # path to djoser end points
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    # path to our account's app endpoints
    path("api/accounts/", include("APIService.urls"))
]

if DEBUG:
    urlpatterns += path('__debug__/', include('debug_toolbar.urls')),
