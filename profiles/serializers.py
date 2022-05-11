from .models import Profile
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class ProfilesSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    value = serializers.CharField(source="id")

    class Meta:
        model = Profile
        fields = ('label', 'value')
        ordering = ['createdAt']

    def get_label(self, obj):
        if obj.surname:
            return f"{obj.name} {obj.surname}"
        return obj.name


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["name", "surname", "age", "sex", "phoneNumber", "email"]
        ordering = ['createdAt']


