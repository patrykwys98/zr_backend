from django.contrib import admin
from .models import User
from profiles.models import Profile
from projects.models import Project
from comments.models import Comment

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(Comment)
