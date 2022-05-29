from .models import Profile
from rest_framework import serializers


class ProfilesSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    value = serializers.CharField(source="id")

    class Meta:
        model = Profile
        fields = ('label', 'value')
        ordering = ['createdAt']

    def get_label(self, obj):
        if obj.name:
            return f"{obj.name} {obj.surname} {obj.email} {obj.phoneNumber}".replace("None ", "").replace(" None", "")
        else:
            return f"{obj.email}"


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["name", "surname", "age", "sex", "phoneNumber", "email"]
        ordering = ['createdAt']

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["name", "surname", "age", "sex", "phoneNumber"]
