from rest_framework import serializers
from .models import SleeperUser

class SleeperUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SleeperUser
        fields = ['id', 'platform_user', 'user_id', 'username', 'display_name', 'avatar']