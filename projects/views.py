
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Project
from profiles.models import Profile
from .serializers import ProjectSerializer, CreateProjectSerializer, UpdateProjectSerializer
from django.db.models import Q


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProjects(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    projects = Project.objects.filter(
        Q(users=profile) | Q(author=user)).order_by('-createdAt').distinct()

    serializer = ProjectSerializer(
        projects, context={'request': request}, many=True)

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProject(request):
    user = request.user
    data = request.data

    project = Project.objects.create(
        author=user, title=data['title'], description=data['description'], dateOfStart=data['dateOfStart'], dateOfEnd=data['dateOfEnd'])
    if data['users']:
        for user in data['users']:
            profile = Profile.objects.get(id=user)
            project.users.add(profile)

    serializer = CreateProjectSerializer(project, many=False)

    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateProject(request):
    user = request.user
    data = request.data

    project = Project.objects.get(id=data['id'])
    if project.author != user:
        return Response(status=403)

    data = request.data
    project.title = data['title']
    project.description = data['description']
    project.dateOfStart = data['dateOfStart']
    project.dateOfEnd = data['dateOfEnd']
    project.status = data['status']
    project.users.set([])
    try:
        for user in data['users']:
            profile = Profile.objects.get(id=user)
            project.users.add(profile)
    except:
        pass

    serializer = UpdateProjectSerializer(project, many=False)

    project.save()

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProject(request, pk):

    project = Project.objects.get(id=pk)

    serializer = ProjectSerializer(
        project, context={'request': request}, many=False)

    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteProject(request, pk):
    user = request.user
    project = Project.objects.get(id=pk)

    if project.author != user:
        return Response(status=403)
    project.delete()

    return Response({'status': 'OK'})
