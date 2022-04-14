from django.urls import path
from .views import addComment

urlpatterns = [
    path('addComment/', addComment, name='addComment'),
]
