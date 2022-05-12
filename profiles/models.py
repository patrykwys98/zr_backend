from django.db import models
from base.models import User
from django.core.validators import MaxValueValidator, RegexValidator


class Profile(models.Model):
    user = models.OneToOneField(
        to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,  null=True, blank=True)
    surname = models.CharField(max_length=100, null=True, blank=True)
    age = models.PositiveIntegerField(
        null=True, blank=True, validators=[MaxValueValidator(150)])
    sex = models.CharField(max_length=20,  null=True, blank=True)
    phoneNumberRegex = RegexValidator(regex = "^\\+?\\d{1,4}?[-.\\s]?\\(?\\d{1,3}?\\)?[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,9}$")
    phoneNumber = models.CharField(validators = [phoneNumberRegex], max_length = 16, null=True, blank=True)

    email = models.EmailField(max_length=100)

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
