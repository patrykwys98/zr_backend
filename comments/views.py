from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from projects.models import Project
from .models import Comment
from .serializers import CreateCommentSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addComment(request):

    if request.method == 'OPTIONS':
        return Response(status=status.HTTP_200_OK)

    try:
        project = Project.objects.get(id=request.data.get('project_id'))
    except Project.DoesNotExist:
        return Response({"message": "Project does not exist"}, status=status.HTTP_404_NOT_FOUND)

    user = request.user

    try:
        text = request.data.get('text').strip()
        if len(text) > 150:
            return Response({"message": "Text is too long"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"message": "Text is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    if request.user.profile in project.users.all() or project.author == user:
        if not text:
            return Response({'message': 'Comment cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(CreateCommentSerializer(Comment.objects.create(
            author=user, text=text, project=project), many=False).data)
    else:
        return Response({"message": "You cant comment this project"}, status=status.HTTP_403_FORBIDDEN)
