from django.urls import path
from sleeper import views as sleeper_views


# URL Patterns
urlpatterns = [
    path('user/setup/', sleeper_views.SleeperUserSetupView.as_view(), name='sleeper-user-setup'),
    path('leagues/<str:league_id>/setup/', sleeper_views.SleeperLeagueChampionView.as_view(), name='sleeper-league-setup'),

    path('leagues/<str:league_id>/champion/', sleeper_views.SleeperLeagueChampionView.as_view(), name='sleeper-league-champion'),
    path('leagues/champion/', sleeper_views.SleeperTestView.as_view(), name='sleeper-test'),
]
