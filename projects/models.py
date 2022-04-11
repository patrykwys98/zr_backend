from django.db import models
from base.models import User


class Project(models.Model):
    author = models.OneToOneField(
        to=User, on_delete=models.CASCADE,  null=True, blank=True)
    title = models.CharField(max_length=255,  null=True, blank=True)
    dateOfStart = models.DateTimeField(blank=True, null=True)
    dateOfEnd = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20,  null=True, blank=True)

