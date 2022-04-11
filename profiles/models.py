from django.db import models
from base.models import User
from projects.models import Project
from django.core.validators import MaxValueValidator


class Profile(models.Model):
    user = models.OneToOneField(
        to=User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    surname = models.CharField(max_length=100, null=True, blank=True)
    age = models.PositiveIntegerField(
        null=True, blank=True, validators=[MaxValueValidator(150)])
    sex = models.CharField(max_length=20,  null=True, blank=True)
    phoneNumber = models.CharField(max_length=12,  null=True, blank=True)
    email = models.EmailField(max_length=100,  null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True,  null=True, blank=True)
    updatedAt = models.DateTimeField(auto_now=True,  null=True, blank=True)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE,  null=True, blank=True)
