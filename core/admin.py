from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import PlatformUser  # Import your custom user model

admin.site.register(PlatformUser, UserAdmin)
