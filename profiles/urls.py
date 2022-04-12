from django.urls import path
from .views import getProfile, updateProfile

urlpatterns = [
    path("getProfile/", getProfile, name="getProfile"),
    path("updateProfile/", updateProfile, name="updateProfile"),
]
