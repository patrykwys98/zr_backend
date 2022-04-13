from .models import Profile
from rest_framework import serializers


class ProfilesSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    value = serializers.CharField(source="id")

    class Meta:
        model = Profile
        fields = ('label', 'value')

    def get_label(self, obj):
        if obj.surname:
            return obj.name + ' ' + obj.surname
        return obj.name


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
