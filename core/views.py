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

from core.serializers import SignUpSerializer, SignInSerializer


class SignUpView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)
        _, token = AuthToken.objects.create(user)

        return Response({
            "message": "User sign up successfully",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            "token": token,
        }, status=status.HTTP_201_CREATED)


class SignInView(KnoxLoginView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = SignInSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return super(SignInView, self).post(request, format=None)
        else:
            return Response(serializer.errors, status=status.HTTP_400)

class SignOutView(KnoxLogoutView):
    pass

class SignOutAllView(KnoxLogoutAllView):
    pass

class AuthStatusView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        return Response({
            'isAuthenticated': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
        }, status=status.HTTP_200_OK)