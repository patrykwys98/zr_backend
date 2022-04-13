from django.db import models
from base.models import User
from profiles.models import Profile


class Project(models.Model):
    author = models.ForeignKey(
        to=User, on_delete=models.CASCADE,  null=True, blank=True)
    title = models.CharField(max_length=255,  null=True, blank=True)
    dateOfStart = models.DateTimeField(null=True, blank=True)
    dateOfEnd = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20,  null=True, blank=True)
    users = models.ManyToManyField(to=Profile)

    def __str__(self):
        return self.title
