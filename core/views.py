from django.contrib.auth import login
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from knox.views import LogoutView as KnoxLogoutView
from knox.views import LogoutAllView as KnoxLogoutAllView
from knox.auth import TokenAuthentication

from core.serializers import PlatformUserSerializer, SignUpSerializer, SignInSerializer


class SignUpView(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            _, token = AuthToken.objects.create(user)

            user_data = SignUpSerializer(user).data

            return Response({
                "isAuthenticated": True,
                "user": user_data,
                "token": token,
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)



class SignInView(KnoxLoginView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = SignInSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            _, token = AuthToken.objects.create(user)

            user_data = PlatformUserSerializer(user).data

            return Response({
                "isAuthenticated": True,
                "user": user_data,
                "token": token,
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "isAuthenticated": False,
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class SignOutView(KnoxLogoutView):
    pass


class SignOutAllView(KnoxLogoutAllView):
    pass


class AuthStatusView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        _, token = AuthToken.objects.create(user)
        user_data = PlatformUserSerializer(user).data

        return Response({
            'isAuthenticated': True,
            'user': user_data,
            "token": token,
        }, status=status.HTTP_200_OK)