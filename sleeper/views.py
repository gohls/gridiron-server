from django.shortcuts import render
from typing import Any
from rest_framework.views import APIView
from rest_framework.response import Response

from sleeper.api_clients import sleeper_api


class SleeperLeagueChampionAPI(APIView):
    def get(self, request, league_id: str) -> Response:
        data = sleeper_api.get_league(league_id)
        if "error" in data:
            return Response(data, status=400)
        return Response(data, status=200)
