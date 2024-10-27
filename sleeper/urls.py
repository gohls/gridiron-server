from django.urls import path
from sleeper import views as sleeper_views

# URL Patterns
urlpatterns = [
    path('league/<str:league_id>/', sleeper_views.SleeperLeagueAPI.as_view(), name='sleeper-league'),
    path('league/<str:league_id>/matchups/<int:week>/', sleeper_views.SleeperLeagueMatchupsAPI.as_view(), name='sleeper-league-matchups'),
    path('league/<str:league_id>/users/', sleeper_views.SleeperLeagueUsersAPI.as_view(), name='sleeper-league-users'),
    path('league/<str:league_id>/rosters/', sleeper_views.SleeperLeagueRostersAPI.as_view(), name='sleeper-league-rosters'),
    path('league/<str:league_id>/transactions/<int:week>/', sleeper_views.SleeperLeagueTradesAPI.as_view(), name='sleeper-league-trades'),
    path('league/<str:league_id>/drafts/', sleeper_views.SleeperLeagueDraftsAPI.as_view(), name='sleeper-league-drafts'),
    path('player/<str:player_id>/', sleeper_views.SleeperPlayerAPI.as_view(), name='sleeper-player'),
    path('players/nfl/', sleeper_views.SleeperPlayersAPI.as_view(), name='sleeper-players'),
    path('players/nfl/news/', sleeper_views.SleeperPlayerNewsAPI.as_view(), name='sleeper-player-news'),
    path('user/<str:user_id>/', sleeper_views.SleeperUserAPI.as_view(), name='sleeper-user'),
    path('user/<str:user_id>/leagues/nfl/<str:season>/', sleeper_views.SleeperUserLeaguesAPI.as_view(), name='sleeper-user-leagues'),
    path('draft/<str:draft_id>/', sleeper_views.SleeperDraftAPI.as_view(), name='sleeper-draft'),
    path('draft/<str:draft_id>/picks/', sleeper_views.SleeperDraftPicksAPI.as_view(), name='sleeper-draft-picks'),
    path('draft/<str:draft_id>/traded_picks/', sleeper_views.SleeperDraftTradesAPI.as_view(), name='sleeper-draft-trades'),
    path('roster/<str:roster_id>/', sleeper_views.SleeperRosterAPI.as_view(), name='sleeper-roster'),
    path('state/nfl/', sleeper_views.SleeperStateNFLAPI.as_view(), name='sleeper-state-nfl'),
]
