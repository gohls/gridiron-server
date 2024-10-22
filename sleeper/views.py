from django.shortcuts import render
from typing import Any
import requests
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from sleeper import constants


class SleeperLeagueAPI(APIView):
    def get(self, request: Request, league_id: str) -> JsonResponse:
        url: str = constants.SLEEPER_LEAGUE_URL.format(league_id=league_id)

        try:
            response: requests.Response = requests.get(url)
            if response.status_code == 200:
                data: Any = response.json()
                return Response(data, status=status.HTTP_200_OK)
            return Response({"error": "Unable to fetch data"}, status=response.status_code)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

