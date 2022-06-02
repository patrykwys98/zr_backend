from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer, ProfilesSerializer, UpdateProfileSerializer
from rest_framework import status
import re

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfile(request):

    if request.method == 'OPTIONS':
        return Response(status=status.HTTP_200_OK)

    return Response(ProfileSerializer(Profile.objects.get(user=request.user), many=False).data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateProfile(request):
    name = request.data.get('name').strip()
    surname = request.data.get('surname').strip()
    sex = request.data.get('sex')
    age = request.data.get('age')
    phoneNumber = request.data.get('phoneNumber')
    if not name:
        return Response({'message': 'You cannot send empty name'}, status=status.HTTP_400_BAD_REQUEST)
    elif not surname:
        return Response({'message': 'You cannot send empty surname'}, status=status.HTTP_400_BAD_REQUEST)
    elif sex not in ["Male", "Female", "Other"]:
        return Response({'message': 'Please enter a valid gender'}, status=status.HTTP_400_BAD_REQUEST)
    elif not age and type(age)!=int or age < 18 or age > 100:
        return Response({'message': 'Please enter a valid age'}, status=status.HTTP_400_BAD_REQUEST)
    elif not phoneNumber or re.match("^(\+)?([ 0-9]){10,16}$", phoneNumber) is None:
        return Response({'message': 'Please enter a valid phone number'}, status=status.HTTP_400_BAD_REQUEST)
    else:    
        profile = Profile.objects.get(user=request.user)
        profile.name = name
        profile.surname = surname
        profile.sex = sex
        profile.phoneNumber = phoneNumber
        profile.age = age

        profile.save()

        return Response(UpdateProfileSerializer(profile, many=False).data, status=status.HTTP_200_OK)
    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfiles(request):
    if request.method == 'OPTIONS':
        return Response(status=status.HTTP_200_OK)
    return Response(ProfilesSerializer(Profile.objects.all(), many=True).data, status=status.HTTP_200_OK)
