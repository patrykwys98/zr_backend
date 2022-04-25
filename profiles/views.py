from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Profile
from base.models import User
from .serializers import ProfileSerializer, ProfilesSerializer
from rest_framework import status


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    serializer = ProfileSerializer(profile, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateProfile(request):
    profile = Profile.objects.get(user=request.user)

    profile.name = request.data['name']
    profile.surname = request.data['surname']
    profile.email = request.data['email']
    profile.sex = request.data['sex']
    profile.phoneNumber = request.data['phoneNumber']
    profile.age = request.data['age']

    profile.save()

    return Response(ProfileSerializer(profile, many=False).data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfiles(request):
    return Response(ProfilesSerializer(Profile.objects.all(), many=True).data, status=status.HTTP_200_OK)
