from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Profile
from base.models import User
from .serializers import ProfileSerializer, ProfilesSerializer
from rest_framework import status
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import phonenumbers

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfile(request):

    if request.method == 'OPTIONS':
        return Response(status=status.HTTP_200_OK)

    return Response(ProfileSerializer(Profile.objects.get(user=request.user), many=False).data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateProfile(request):

    if request.method == 'OPTIONS':
        return Response(status=status.HTTP_200_OK)
    
    if request.data['name'] == '':
        return Response({'message': 'You cannot send empty name'}, status=status.HTTP_400_BAD_REQUEST)
    if request.data['surname'] == '':
        return Response({'message': 'You cannot send empty surname'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        validate_email(request.data['email'])
    except ValidationError:
        return Response({'message': 'Please enter a valid email address'}, status=status.HTTP_400_BAD_REQUEST)

    print(request.data['sex'])
    
    if request.data['sex'] == '':
        return Response({'message': 'You cannot send empty sex'}, status=status.HTTP_400_BAD_REQUEST)
    
    if request.data['age'] == "" and type(request.data['age'])!=int:
        return Response({'message': 'Please enter a valid age'}, status=status.HTTP_400_BAD_REQUEST)



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

    if request.method == 'OPTIONS':
        return Response(status=status.HTTP_200_OK)
        
    return Response(ProfilesSerializer(Profile.objects.all(), many=True).data, status=status.HTTP_200_OK)
