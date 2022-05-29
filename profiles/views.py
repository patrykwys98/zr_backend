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

    if not 'name' in request.data or request.data['name'] == "":
        return Response({'message': 'You cannot send empty name'}, status=status.HTTP_400_BAD_REQUEST)
    elif not 'surname' in request.data or request.data['surname'] == "":
        return Response({'message': 'You cannot send empty surname'}, status=status.HTTP_400_BAD_REQUEST)
    elif not 'sex' in request.data or request.data['sex'] != "Male" and request.data['sex'] != "Female" and request.data['sex'] != "Other":
        return Response({'message': 'Please enter a valid gender'}, status=status.HTTP_400_BAD_REQUEST)
    elif not 'age' in request.data or request.data['age'] and  type(request.data['age'])!=int or request.data['age'] < 18 or request.data['age'] > 100:
        return Response({'message': 'Please enter a valid age'}, status=status.HTTP_400_BAD_REQUEST)
    elif not "phoneNumber" in request.data or re.match("^\\+?\\d{1,4}?[-.\\s]?\\(?\\d{1,3}?\\)?[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,9}$", request.data['phoneNumber']) is None:
        return Response({'message': 'Please enter a valid phone number'}, status=status.HTTP_400_BAD_REQUEST)
    else:    
        profile = Profile.objects.get(user=request.user)
        profile.name = request.data['name']
        profile.surname = request.data['surname']
        profile.sex = request.data['sex']
        profile.phoneNumber = request.data['phoneNumber']
        profile.age = request.data['age']

        profile.save()

        return Response(UpdateProfileSerializer(profile, many=False).data, status=status.HTTP_200_OK)
    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfiles(request):
    if request.method == 'OPTIONS':
        return Response(status=status.HTTP_200_OK)
    return Response(ProfilesSerializer(Profile.objects.all(), many=True).data, status=status.HTTP_200_OK)
