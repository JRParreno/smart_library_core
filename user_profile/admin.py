from django.contrib import admin
from .models import UserProfile
from django.contrib.auth.models import Group
from django.contrib.auth.models import Group as OriginalGroup

admin.site.register(UserProfile)


admin.site.unregister(Group)
