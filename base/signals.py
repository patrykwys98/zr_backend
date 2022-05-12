from .models import User
from django.db.models.signals import post_save
from profiles.models import Profile


def createUserProfile(sender, created, instance, **kwargs):
    if created:
        email = ""
        if instance.email != "":
            email = instance.email   
        profile = Profile.objects.create(
            user=instance, email=email, name="", surname="", sex="Other", phoneNumber="")
        profile.save()

post_save.connect(createUserProfile, sender=User)
