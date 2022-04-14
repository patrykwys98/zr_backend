from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Profile
from base.models import User
from .serializers import ProfileSerializer, ProfilesSerializer


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
    user = request.user
    profile = Profile.objects.get(user=user)
    serializer = ProfileSerializer(profile, many=False)

    data = request.data
    profile.name = data['name']
    profile.surname = data['surname']
    profile.email = data['email']
    profile.sex = data['sex']
    profile.phoneNumber = data['phoneNumber']
    profile.age = data['age']

    profile.save()

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfiles(request):
    profile = Profile.objects.all()
    serializer = ProfilesSerializer(profile, many=True)
    return Response(serializer.data)
