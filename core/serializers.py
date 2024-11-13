from rest_framework import serializers
from core.models import (
    PlatformUser, 
)

class PlatformUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformUser
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

