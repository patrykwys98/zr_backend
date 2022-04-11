from django.db import models
from base.models import User
from projects.models import Project


class Comment(models.Model):
    author = models.ForeignKey(
        to=User, on_delete=models.CASCADE,  null=True, blank=True)
    # project = models.ForeignKey(
    #     Project, on_delete=models.CASCADE,  null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
