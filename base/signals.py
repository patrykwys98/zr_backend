
from .models import User
from django.db.models.signals import post_save
from profiles.models import Profile


def createUserProfile(sender, instance, **kwargs):
    email = ""
    if instance.email != "":
        email = instance.email
    username = ""
    if instance.username != "":
        username = instance.username
    profile = Profile.objects.create(
        user=instance, name=username, surname="", age=0, phoneNumber=0, email=email, sex="")
    profile.save()


post_save.connect(createUserProfile, sender=User)
