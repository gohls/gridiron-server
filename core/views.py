from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import SignUpSerializer, LoginSerializer

from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from knox.views import LogoutView as KnoxLogoutView
from knox.views import LogoutAllView as KnoxLogoutAllView


class SignUpView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer

    def create(self, request, *args, **kwargs):
        print(request)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        instance, token = AuthToken.objects.create(user)

        return Response({
            "message": "User sign up successfully",
            "user": {
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
            },
            "token": token,
        }, status=status.HTTP_201_CREATED)


class LoginView(KnoxLoginView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            return super().post(request, format=None)


class LogoutView(KnoxLogoutView):
    pass

class LogoutAllView(KnoxLogoutAllView):
    pass
  
class AuthStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'isAuthenticated': True}, status=status.HTTP_200_OK)
