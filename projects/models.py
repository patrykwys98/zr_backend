from django.db import models
from base.models import User
from profiles.models import Profile


class Project(models.Model):
    STATUS_CHOICES = (
        ("new", "New"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    )

    author = models.ForeignKey(
        to=User, on_delete=models.CASCADE)
    title = models.CharField(max_length=65)
    dateOfStart = models.DateField(null=False, blank=False)
    dateOfEnd = models.DateField(null=False, blank=False)
    description = models.TextField(null=False, blank=False, max_length=2000)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS_CHOICES,
                              default="New", max_length=20)
    users = models.ManyToManyField(to=Profile)

    def __str__(self):
        return self.title
