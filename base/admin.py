from django.contrib import admin
from .models import User
from profiles.models import Profile
admin.site.register(User)
admin.site.register(Profile)