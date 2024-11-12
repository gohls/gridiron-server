from typing import Any

from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response

from sleeper.serializers import SleeperLeagueRulebookSerializer
from sleeper.api_clients import sleeper_api
from sleeper.models import SleeperLeagueRulebook


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
    def get(self, request) -> Response:
        data = {}
        data['username'] = 'Joe Schmo'
        data['display_name'] = 'The Ringer'
        return Response(data, status=status.HTTP_200_OK)


class SleeperLeagueRulebookAPIView(APIView):
    def get_queryset(self):
        return SleeperLeagueRulebook.objects.prefetch_related('rules__subsections')

    def get(self, request, league_id: str):
        if league_id:
            rulebook = get_object_or_404(self.get_queryset(), league_id=league_id)
            serializer = SleeperLeagueRulebookSerializer(rulebook)
        else: # while developing, we just get all rulebooks
            rulebooks = self.get_queryset()
            serializer = SleeperLeagueRulebookSerializer(rulebooks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SleeperLeagueRulebookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, league_id: str):
        rulebook = get_object_or_404(self.get_queryset(), league_id=league_id)
        serializer = SleeperLeagueRulebookSerializer(rulebook, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, league_id):
        rulebook = get_object_or_404(self.get_queryset(), league_id=league_id)
        serializer = SleeperLeagueRulebookSerializer(rulebook, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, league_id):
        rulebook = get_object_or_404(self.get_queryset(), league_id=league_id)
        rulebook.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)