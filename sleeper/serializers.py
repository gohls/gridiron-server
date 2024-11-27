from rest_framework import serializers
from sleeper.models import STATUS_MAP, LeagueStatus, SleeperUser, SleeperLeague, SleeperLeagueTeam


class SleeperUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SleeperUser
        fields = ['id', 'platform_user', 'user_id', 'username', 'display_name', 'avatar']


class SleeperLeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = SleeperLeague
        fields = ['league_id', 'previous_league_id', 'name', 'status', 'total_rosters', 'season', 'sport']

    def validate_status(self, value):
        if isinstance(value, str):
            return STATUS_MAP.get(value.lower(), LeagueStatus.PRE_DRAFT)
        if value not in LeagueStatus.values:
            raise serializers.ValidationError(f"Invalid status. Must be one of: {LeagueStatus.values}")
        return value

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['status'] = LeagueStatus(instance.status).label
        return ret


class SleeperLeagueTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = SleeperLeagueTeam
        fields = ['owner', 'league', 'metadata']