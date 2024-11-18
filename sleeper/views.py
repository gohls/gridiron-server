from typing import Any

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from knox.auth import TokenAuthentication

from sleeper.api_clients import sleeper_api


class SleeperLeagueChampionAPI(APIView):
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

    
class SleeperTestAPI(APIView):
    # for testing purposes
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request) -> Response:
        data = {}
        data['username'] = 'Joe Schmo'
        data['display_name'] = 'The Ringer'
        return Response(data, status=status.HTTP_200_OK)

