
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Project
from profiles.models import Profile
from .serializers import ProjectSerializer, CreateProjectSerializer, UpdateProjectSerializer
from django.db.models import Q
from rest_framework import status


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProjects(request):
    return Response(ProjectSerializer(
        Project.objects.filter(
            Q(users=Profile.objects.get(user=request.user)) | Q(author=request.user)).order_by('-createdAt').distinct(),
        context={'request': request}, many=True).data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProject(request):

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

    project = Project.objects.get(id=request.data['id'])
    if project.author != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    project.title = request.data['title']
    project.description = request.data['description']
    project.dateOfStart = request.data['dateOfStart']
    project.dateOfEnd = request.data['dateOfEnd']
    project.status = request.data['status']
    project.users.set([])
    print(request.data['users'])
    if request.data['users'] != ['']:
        for user in request.data['users']:
            profile = Profile.objects.get(id=user)
            project.users.add(profile)

    project.save()

    return Response(UpdateProjectSerializer(project, many=False).data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProject(request, pk):
    return Response(ProjectSerializer(
        Project.objects.get(id=pk), context={'request': request}, many=False).data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteProject(request, pk):
    project = Project.objects.get(id=pk)

    if project.author != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    project.delete()
    return Response(status=status.HTTP_200_OK)
