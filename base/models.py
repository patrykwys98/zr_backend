from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    surname = models.CharField(max_length=100, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True, validators=[MaxValueValidator(150)])
    sex = models.CharField(max_length=20)
    phoneNumber = models.CharField(max_length=12)
    email = models.EmailField(max_length=100)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)



