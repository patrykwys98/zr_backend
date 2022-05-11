
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Project
from profiles.models import Profile
from .serializers import ProjectsSerializer, CreateProjectSerializer, UpdateProjectSerializer, SingleProjectSerializer
from django.db.models import Q
from rest_framework import status


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProjects(request):
    
    if request.method == 'OPTIONS':
        return Response(status=status.HTTP_200_OK)
        
    return Response(ProjectsSerializer(
        Project.objects.filter(
            Q(users=Profile.objects.get(user=request.user)) | Q(author=request.user)).order_by('-createdAt').distinct(),
        context={'request': request}, many=True).data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProject(request, pk):

    if request.method == 'OPTIONS':
        return Response(status=status.HTTP_200_OK)
        
    if request.user.profile in Project.objects.get(id=pk).users.all() or Project.objects.get(id=pk).author == request.user:
        return Response(SingleProjectSerializer(Project.objects.get(id=pk), context={'request': request}).data, status=status.HTTP_200_OK)
    else:
        return Response({"message": "You cant watch this project"}, status=status.HTTP_403_FORBIDDEN)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProject(request):

    if request.method == 'OPTIONS':
        return Response(status=status.HTTP_200_OK)
        
    if request.data['title'] == '':
        return Response({'message': 'You cannot send empty title'}, status=status.HTTP_400_BAD_REQUEST)

    if request.data['description'] == '':
        return Response({'message': 'You cannot send empty description'}, status=status.HTTP_400_BAD_REQUEST)

    if request.data['dateOfStart'] > request.data['dateOfEnd']:
        return Response({'message': 'Start date must be before end date'}, status=status.HTTP_400_BAD_REQUEST)

    project = Project.objects.create(
        author=request.user, title=request.data['title'], description=request.data['description'],
        dateOfStart=request.data['dateOfStart'], dateOfEnd=request.data['dateOfEnd'])
    if request.data['users'] != ['']:
        for user in request.data['users']:
            profile = Profile.objects.get(id=user)
            project.users.add(profile)

    return Response(CreateProjectSerializer(project, many=False).data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateProject(request):

    if request.method == 'OPTIONS':
        return Response(status=status.HTTP_200_OK)
        
    project = Project.objects.get(id=request.data['id'])
    if project.author != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    if request.data['title'] != '':
        project.title = request.data['title']
    else:
        return Response({'message': 'Title field is required.'}, status=status.HTTP_400_BAD_REQUEST)

    project.description = request.data['description']

    if request.data['dateOfStart'] > request.data['dateOfEnd']:
        return Response({'message': 'Start date must be before end date'}, status=status.HTTP_400_BAD_REQUEST, )

    project.dateOfStart = request.data['dateOfStart']
    project.dateOfEnd = request.data['dateOfEnd']

    project.status = request.data['status']
    project.users.set([])
    if request.data['users'] != ['']:
        for user in request.data['users']:
            profile = Profile.objects.get(id=user)
            project.users.add(profile)

    project.save()

    return Response(UpdateProjectSerializer(project, many=False).data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteProject(request, pk):

    if request.method == 'OPTIONS':
        Response(status=status.HTTP_200_OK)
        
    project = Project.objects.get(id=pk)

    if project.author != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    project.delete()
    return Response({"message": "Project deleted"}, status=status.HTTP_200_OK)
