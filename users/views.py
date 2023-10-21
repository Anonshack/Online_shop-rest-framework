from datetime import datetime, timedelta
import jwt
from django.contrib.auth import logout
from rest_framework.authtoken.models import Token
from .serializers import PasswordChangeSerializer 
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import generics
from django.contrib.auth.forms import PasswordChangeForm
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import UserRegSerializer, UserSerializer, UsersListSerializer, UserUpdateSerializer
from .filters import UsersFilterBackend
from django.contrib.auth import get_user_model


class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserRegSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserLoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = User.objects.filter(username=username, is_active=True).first()
        if user is None:
            raise AuthenticationFailed('Login yoki parol xato, iltimos tekshirib qaytadan kiriting')
        if not user.check_password(password):
            raise AuthenticationFailed('Login yoki parol xato, iltimos tekshirib qaytadan kiriting')

        payload = {
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(minutes=100),
            'iat': datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.data = {
            'token': token
        }

        return response


class UserDetailView(APIView):
    def get(self, request):
        try:
            token = request.META['HTTP_TOKEN']
        except:
            raise AuthenticationFailed('Iltimos, avval tizimga kiring')

        if not token:
            raise AuthenticationFailed('Token yaroqsiz, iltimos tizimga qayta kiring')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Sessiya muddati o\'tgan, iltimos, qayta kiring')
        except:
            raise AuthenticationFailed('Sessiya muddati o\'tgan, iltimos, qayta kiring')

        user = User.objects.filter(username=payload['username']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


def checkUserToken(token):
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except:
        return False

    user = User.objects.filter(username=payload['username']).first()
    if user:
        return user
    return False


class PasswordChangeView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordChangeSerializer  

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password1']

            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                return Response({'detail': 'Password has been changed successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsersListView(ListAPIView):
    serializer_class = UsersListSerializer
    queryset = User.objects.all()
    filter_backends = (UsersFilterBackend,)


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logout(request)
        return Response({"Message": "You are logged out successfully"}, status=status.HTTP_200_OK)


# Ro'yhatdan o'tgan userlar o'zgartira oladi
class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user