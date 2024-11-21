from django.urls import path
from sleeper import views as sleeper_views


# URL Patterns
urlpatterns = [
    path('user/fetch/', sleeper_views.SleeperUserFetchView.as_view(), name='sleeper-user-fetch'),
    path('user/create/', sleeper_views.SleeperUserCreateView.as_view(), name='sleeper-user-create'),
    path('leagues/<str:league_id>/champion/', sleeper_views.SleeperLeagueChampionView.as_view(), name='sleeper-league-champion'),
    path('leagues/champion/', sleeper_views.SleeperTestView.as_view(), name='sleeper-test'),
]
