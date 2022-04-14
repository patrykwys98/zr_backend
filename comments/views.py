from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from projects.models import Project
from .models import Comment
from profiles.models import Profile
from .serializers import CreateCommentSerializer
from django.db.models import Q


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addComment(request):
    user = request.user
    data = request.data

    project = Project.objects.get(id=data['project_id'])

    project = Comment.objects.create(
        author=user, text=data["text"], project=project)

    serializer = CreateCommentSerializer(project, many=False)

    return Response(serializer.data)
