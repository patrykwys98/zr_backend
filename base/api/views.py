from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from base.models import User
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import RegisterSerializer, ChangePasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse
import jwt
from django.conf import settings


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["email"] = user.email
        token['id'] = user.id
        token['is_verified'] = user.is_verified
        token['message'] = 'You have successfully logged in.'

        return token

    def validate(self, attrs):
        credentials = {
            'email': '',
            'password': attrs.get("password")
        }

        user_obj = User.objects.filter(email=attrs.get("email")).first(
        )
        if user_obj:
            credentials['email'] = user_obj.email

        return super().validate(credentials)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = User.objects.get(email=serializer.data['email'])


        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ChangePasswordView(generics.UpdateAPIView):
    
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):

        if request.method == 'OPTIONS':
            return Response(status=status.HTTP_200_OK)

        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"message": ["Wrong password old password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
