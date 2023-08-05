# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import ModUser, UserType

# Register your models here.

class UserTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("_type",)}

admin.site.register(ModUser)
admin.site.register(UserType, UserTypeAdmin)
