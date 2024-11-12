from django.urls import path
from sleeper import views as sleeper_views


# URL Patterns
urlpatterns = [
    path('league/<str:league_id>/champion/', sleeper_views.SleeperLeagueChampionAPI.as_view(), name='sleeper-league-champion'),
    path('league/<str:league_id>/rulebook/', sleeper_views.SleeperLeagueRulebookAPIView.as_view(), name='sleeper-league-rulebook'),
]
