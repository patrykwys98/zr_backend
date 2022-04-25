from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from projects.models import Project
from .models import Comment
from profiles.models import Profile
from .serializers import CreateCommentSerializer
from django.db.models import Q


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addComment(request):

    if request.data['text'] == '':
        return Response({'message': 'You cannot send empty comment'}, status=status.HTTP_400_BAD_REQUEST)

    return Response(CreateCommentSerializer(project=Comment.objects.create(
        author=request.user, text=request.data["text"], project=Project.objects.get(id=request.data['project_id'])), many=False).data)
