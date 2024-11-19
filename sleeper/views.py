from typing import Any

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from knox.auth import TokenAuthentication

from core.models import PlatformUser
from sleeper.api_clients import sleeper_api
from sleeper.models import SleeperUser
from sleeper.serializers import SleeperUserSerializer


class SleeperUserSetupView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, username: str) -> Response:
        platform_user = get_object_or_404(PlatformUser, user=request.user)

        # Check if the SleeperUser already exists
        sleeper_user = SleeperUser.objects.filter(username=username).first()
        if sleeper_user:
            serializer = SleeperUserSerializer(sleeper_user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # If not found, call the Sleeper API
        sleeper_use_data = sleeper_api.get_user(username)
        # If no sleeper user 
        if not sleeper_use_data:
            return Response(tatus=status.HTTP_204_NO_CONTENT)

        sleeper_use_data['platform_user'] = platform_user.id  # Add platform_user to the data
        
        # Validate and save the new data
        serializer = SleeperUserSerializer(data=sleeper_use_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class SleeperLeagueSetupView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, league_id: str) -> Response:
       
        return Response(status=status.HTTP_200_OK)
    
class SleeperLeagueSetupView(APIView):
    def post(self, request, league_id: str) -> Response:
       
        return Response(status=status.HTTP_200_OK)
    
class SleeperLeagueChampionView(APIView):
    def get(self, request, league_id: str) -> Response:
        # Get league data the contains the latest winner roster id
        league_data = sleeper_api.get_league(league_id)
        latest_winner_roster_id = league_data.get("metadata", {}).get("latest_league_winner_roster_id")
        
        # From the league rosters we can check againts the roster id to get the owner id
        rosters = sleeper_api.get_league_rosters(league_id)
        champ_id = None
        for roster in rosters:
            if roster["roster_id"] == int(latest_winner_roster_id):
                champ_id = roster["owner_id"]

        # Finally we can grab the user data we want to display from the league users
        users = sleeper_api.get_league_users()
        champ_data = None
        for user in users:
            if user["user_id"] == champ_id:
                champ_data = roster["owner_id"]

        return Response(champ_data, status=status.HTTP_200_OK)

    
class SleeperTestView(APIView):
    # for testing purposes
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def get(self, request) -> Response:
        data = {}
        data['username'] = 'Joe Schmo'
        data['display_name'] = 'The Ringer'
        return Response(data, status=status.HTTP_200_OK)

