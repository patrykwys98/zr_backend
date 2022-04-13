from django.urls import path
from .views import getProjects, createProject, updateProject, getProject, deleteProject

urlpatterns = [
    path("getProjects/", getProjects, name="getProjects"),
    path("getProject/<str:pk>/", getProject, name="getProject"),
    path("createProject/", createProject, name="createProject"),
    path("updateProject/", updateProject, name="updateProject"),
    path("deleteProject/<str:pk>/", deleteProject, name="deleteProject"),
]
