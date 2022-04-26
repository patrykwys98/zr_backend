from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from projects.models import Project
from .models import Comment
from .serializers import CreateCommentSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addComment(request):
    if request.data['text'] == '':
        return Response({'message': 'Comment cannot be empty'})

    return Response(CreateCommentSerializer(Comment.objects.create(
        author=request.user, text=request.data["text"], project=Project.objects.get(id=request.data['project_id'])), many=False).data)
