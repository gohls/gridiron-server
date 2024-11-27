from rest_framework import serializers
from django.contrib.auth import authenticate
from core.models import (
    PlatformUser, 
)


class PlatformUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformUser
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    
class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformUser
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = PlatformUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class SignInSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return {'user': user}
        raise serializers.ValidationError("Incorrect Credentials")

