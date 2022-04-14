from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    isAuthor = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'
        ordering = ['createdAt']

    def get_author(self, obj):
        return obj.author.profile.name + " " + obj.author.profile.surname + " " + obj.author.profile.email

    def get_isAuthor(self, obj):
        return obj.author == obj.project.author


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
