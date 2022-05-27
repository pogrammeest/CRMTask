from django.contrib import admin
from APIService.models import *


# Register your models here.


@admin.register(RepairRequest)
class RepairRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'id')
    list_display_links = ('title', 'id')


@admin.register(UserDetails)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    list_display = ('id', 'user')


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    list_display = ('id', 'user')
