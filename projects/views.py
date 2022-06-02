
from datetime import date
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
    try:
        title = request.data.get('title').strip()
    except:
        return Response({"message": "Title is required"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        description = request.data.get('description').strip()
    except:
        return Response({"message": "Description is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    dateOfStart = request.data.get('dateOfStart')
    dateOfEnd = request.data.get('dateOfEnd')
        
    if not title:
        return Response({'message': 'You cannot send empty title'}, status=status.HTTP_400_BAD_REQUEST)
    elif not description:
        return Response({'message': 'You cannot send empty description'}, status=status.HTTP_400_BAD_REQUEST)
    elif not dateOfStart or not dateOfEnd or dateOfStart > dateOfEnd:
        return Response({'message': 'Enter a valid date'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        project = Project.objects.create(
            author=request.user, title=title, description=description,
            dateOfStart=dateOfStart, dateOfEnd=dateOfEnd)
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
    
    project = Project.objects.get(id=request.data.get("id"))
    try:
        title = request.data.get("title").strip()
    except:
        return Response({"message": "Title is required"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        description = request.data.get("description").strip()
    except:
        return Response({"message": "Description is required"}, status=status.HTTP_400_BAD_REQUEST)
    projectStatus = request.data.get("status")
    dateOfStart = request.data.get("dateOfStart")
    dateOfEnd = request.data.get("dateOfEnd")


    if project.author != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)
    elif not title:
        return Response({'message': 'Title field is required.'}, status=status.HTTP_400_BAD_REQUEST)
    elif not description:
        return Response({'message': 'Description field is required.'}, status=status.HTTP_400_BAD_REQUEST)
    elif not dateOfStart or not dateOfEnd or dateOfStart > dateOfEnd:
        return Response({'message': 'Please enter a valid start date and end date'}, status=status.HTTP_400_BAD_REQUEST)
    elif projectStatus not in ["New", "In progress", "Completed"]:
        return Response({'message': 'Status field is required.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        project.dateOfStart = dateOfStart
        project.dateOfEnd = dateOfEnd
        project.title = title
        project.description = description  
        project.status = projectStatus
        
        project.users.set([])
        if request.data['users'] != ['']:
            for user in request.data['users']:
                project.users.add(Profile.objects.get(id=user))

        project.save()

        return Response(UpdateProjectSerializer(project, many=False).data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


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
