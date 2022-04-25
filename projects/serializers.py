from .models import Project
from rest_framework import serializers
from comments.serializers import CommentSerializer


class ProjectSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    authorId = serializers.SerializerMethodField()
    isAuthor = serializers.SerializerMethodField()
    usersNames = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = "__all__"

    def get_author(self, obj):
        return obj.author.profile.name + " " + obj.author.profile.surname + " " + obj.author.profile.email

    def get_authorId(self, obj):
        return obj.author.id

    def get_isAuthor(self, obj):
        return obj.author == self.context.get("request").user

    def get_usersNames(self, obj):
        return [user.name + " " + user.surname + " " + user.email for user in obj.users.all()]


class ProjectsSerializer(ProjectSerializer):
    class Meta:
        model = Project
        fields = ("id", "title", "author", "status",
                  "isAuthor", "dateOfStart", "dateOfEnd", "authorId")


class SingleProjectSerializer(ProjectsSerializer):
    class Meta:
        model = Project
        fields = ProjectsSerializer.Meta.fields + \
            ("description", "usersNames", "comments", "users")


class CreateProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ["title", "description", "dateOfStart", "dateOfEnd", 'users']


class UpdateProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ["title", "description", "dateOfStart", "dateOfEnd", 'users']
