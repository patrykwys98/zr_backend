from django.db import models
from base.models import User
from django.core.validators import MaxValueValidator, RegexValidator


class Profile(models.Model):
    user = models.OneToOneField(
        to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100, null=True, blank=True)
    age = models.PositiveIntegerField(
        null=True, blank=True, validators=[MaxValueValidator(150)])
    sex = models.CharField(max_length=20,  null=True, blank=True)
    phoneNumber = models.CharField(
        null=True, validators=[RegexValidator(r'^\d{3}-\d{3}-\d{4}$')], max_length=255)

    email = models.EmailField(max_length=100)

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
