from django.shortcuts import render
from typing import Any
import requests
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from sleeper import constants


'''
    CURRENTLY THESE ARE BASICALLY JUST WRAPPER APIS TO GET SLEEPER DATA
    I.E. IT DOES ADD ANY LOGIC AND JUST RETURNS THE SAME DATA AS MAKING THE
    REQUEST TO SLEEPER API DIRECTLY

    THIS WILL BE UPDATED AS WE FIGURE OUT WHAT DATA WE NEED AND WHAT CALCULATION 
    WE NEED TO MAKE

    HOWEVER, THESE IS GOOD ENOUGH TO GET STARTED ON SOME END-TO-END WORK
'''
class SleeperLeagueAPI(APIView):
    def get(self, request: Request, league_id: str) -> Response:
        url: str = constants.SLEEPER_LEAGUE_URL.format(league_id=league_id)
        return self.make_request(url)

class SleeperLeagueMatchupsAPI(APIView):
    def get(self, request: Request, league_id: str, week: int) -> Response:
        url: str = constants.SLEEPER_LEAGUE_MATCHUPS_URL.format(league_id=league_id, week=week)
        return self.make_request(url)

class SleeperLeagueUsersAPI(APIView):
    def get(self, request: Request, league_id: str) -> Response:
        url: str = constants.SLEEPER_LEAGUE_USERS_URL.format(league_id=league_id)
        return self.make_request(url)

class SleeperLeagueRostersAPI(APIView):
    def get(self, request: Request, league_id: str) -> Response:
        url: str = constants.SLEEPER_LEAGUE_ROSTERS_URL.format(league_id=league_id)
        return self.make_request(url)

class SleeperLeagueTradesAPI(APIView):
    def get(self, request: Request, league_id: str, week: int) -> Response:
        url: str = constants.SLEEPER_LEAGUE_TRADES_URL.format(league_id=league_id, week=week)
        return self.make_request(url)

class SleeperLeagueDraftsAPI(APIView):
    def get(self, request: Request, league_id: str) -> Response:
        url: str = constants.SLEEPER_LEAGUE_DRAFTS_URL.format(league_id=league_id)
        return self.make_request(url)

class SleeperPlayerAPI(APIView):
    def get(self, request: Request, player_id: str) -> Response:
        url: str = constants.SLEEPER_PLAYER_URL.format(player_id=player_id)
        return self.make_request(url)

class SleeperPlayersAPI(APIView):
    def get(self, request: Request) -> Response:
        url: str = constants.SLEEPER_PLAYERS_URL
        return self.make_request(url)

class SleeperPlayerNewsAPI(APIView):
    def get(self, request: Request) -> Response:
        url: str = constants.SLEEPER_PLAYER_NEWS_URL
        return self.make_request(url)

class SleeperUserAPI(APIView):
    def get(self, request: Request, user_id: str) -> Response:
        url: str = constants.SLEEPER_USER_URL.format(user_id=user_id)
        return self.make_request(url)

class SleeperUserLeaguesAPI(APIView):
    def get(self, request: Request, user_id: str, season: str) -> Response:
        url: str = constants.SLEEPER_USER_LEAGUES_URL.format(user_id=user_id, season=season)
        return self.make_request(url)

class SleeperDraftAPI(APIView):
    def get(self, request: Request, draft_id: str) -> Response:
        url: str = constants.SLEEPER_DRAFT_URL.format(draft_id=draft_id)
        return self.make_request(url)

class SleeperDraftPicksAPI(APIView):
    def get(self, request: Request, draft_id: str) -> Response:
        url: str = constants.SLEEPER_DRAFT_PICKS_URL.format(draft_id=draft_id)
        return self.make_request(url)

class SleeperDraftTradesAPI(APIView):
    def get(self, request: Request, draft_id: str) -> Response:
        url: str = constants.SLEEPER_DRAFT_TRADES_URL.format(draft_id=draft_id)
        return self.make_request(url)

class SleeperRosterAPI(APIView):
    def get(self, request: Request, roster_id: str) -> Response:
        url: str = constants.SLEEPER_ROSTER_URL.format(roster_id=roster_id)
        return self.make_request(url)

class SleeperStateNFLAPI(APIView):
    def get(self, request: Request) -> Response:
        url: str = constants.SLEEPER_STATE_NFL_URL
        return self.make_request(url)

class APIView:
    def make_request(self, url: str) -> Response:
        try:
            response: requests.Response = requests.get(url)
            if response.status_code == 200:
                data: Any = response.json()
                return Response(data, status=status.HTTP_200_OK)
            return Response({"error": "Unable to fetch data"}, status=response.status_code)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
