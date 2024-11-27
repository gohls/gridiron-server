from typing import Any
from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from knox.auth import TokenAuthentication

from sleeper.api_clients import sleeper_api
from sleeper.models import SleeperLeague, SleeperUser
from sleeper.serializers import SleeperLeagueSerializer, SleeperLeagueTeamSerializer, SleeperUserSerializer


class SleeperUserFetchView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request) -> Response:
        username = request.data.get('username')

        if not username:
            return Response({"error": "Username is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            sleeper_user = request.user.sleeper_user
            serializer = SleeperUserSerializer(sleeper_user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except SleeperUser.DoesNotExist:
            sleeper_user_data = sleeper_api.get_user(username)

            if not sleeper_user_data:
                return Response({"error": "Sleeper user not found in the Sleeper API."}, status=status.HTTP_404_NOT_FOUND)

            sleeper_user_data['platform_user'] = request.user.id
            serializer = SleeperUserSerializer(data=sleeper_user_data)
            serializer.is_valid(raise_exception=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SleeperUserCreateView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        username = request.data.get('username')
        if not username:
            return Response({"error": "Username is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            sleeper_user = request.user.sleeper_user
            serializer = SleeperUserSerializer(sleeper_user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except SleeperUser.DoesNotExist:
            sleeper_user_data = sleeper_api.get_user(username)
            if not sleeper_user_data:
                return Response({"error": "User not found in Sleeper API."}, status=status.HTTP_404_NOT_FOUND)

            sleeper_user_data['platform_user'] = request.user.id
            serializer = SleeperUserSerializer(data=sleeper_user_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class SleeperUserLeaguesFetchView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def post(self, request) -> Response:
        try:
            sleeper_user = request.user.sleeper_user
            user_leagues = SleeperLeague.objects.filter(sleeperleagueteam__owner=sleeper_user)
            serializer = SleeperLeagueSerializer(user_leagues, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except SleeperUser.DoesNotExist:
            sleeper_user_leagues_data = sleeper_api.get_user_leagues(request.user.platform_user.sleeper_user.user_id)
            if not sleeper_user_leagues_data:
                return Response({"error": "User leagues not found in Sleeper API."}, status=status.HTTP_404_NOT_FOUND)

            saved_leagues = []
            with transaction.atomic():
                for league_data in sleeper_user_leagues_data:
                    
                    league_serializer = SleeperLeagueSerializer(data=league_data)
                    if league_serializer.is_valid():
                        league = league_serializer.save()
                        
                        team_data = {
                            'owner': sleeper_user.id,
                            'league': league.id,
                            'metadata': league_data.get('metadata', {})
                        }
                        team_serializer = SleeperLeagueTeamSerializer(data=team_data)
                        if team_serializer.is_valid():
                            team_serializer.save()
                        
                        saved_leagues.append(league_serializer.data)
                    else:
                        # Raising an exception will cause a rollback
                        raise ValueError(f"Validation error for league: {league_serializer.errors}")

            return Response(saved_leagues, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
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

