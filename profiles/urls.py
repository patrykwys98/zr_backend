from django.urls import path
from .views import getProfile, updateProfile, getProfiles

urlpatterns = [
    path("getProfile/", getProfile, name="getProfile"),
    path("getProfiles/", getProfiles, name="getProfiles"),
    path("updateProfile/", updateProfile, name="updateProfile"),
]
