# Base Sleeper API URL
SLEEPER_API_BASE_URL = 'https://api.sleeper.app/v1'

# League-related URLs
SLEEPER_LEAGUE_URL = f'{SLEEPER_API_BASE_URL}/league/{{league_id}}'
SLEEPER_LEAGUE_MATCHUPS_URL = f'{SLEEPER_API_BASE_URL}/league/{{league_id}}/matchups/{{week}}'
SLEEPER_LEAGUE_USERS_URL = f'{SLEEPER_API_BASE_URL}/league/{{league_id}}/users'
SLEEPER_LEAGUE_ROSTERS_URL = f'{SLEEPER_API_BASE_URL}/league/{{league_id}}/rosters'
SLEEPER_LEAGUE_TRADES_URL = f'{SLEEPER_API_BASE_URL}/league/{{league_id}}/transactions/{{week}}'
SLEEPER_LEAGUE_DRAFTS_URL = f'{SLEEPER_API_BASE_URL}/league/{{league_id}}/drafts'

# Player-related URLs
SLEEPER_PLAYER_URL = f'{SLEEPER_API_BASE_URL}/player/{{player_id}}'
SLEEPER_PLAYERS_URL = f'{SLEEPER_API_BASE_URL}/players/nfl'
SLEEPER_PLAYER_NEWS_URL = f'{SLEEPER_API_BASE_URL}/players/nfl/news'

# User-related URLs
SLEEPER_USER_URL = f'{SLEEPER_API_BASE_URL}/user/{{user_id}}'
SLEEPER_USER_LEAGUES_URL = f'{SLEEPER_API_BASE_URL}/user/{{user_id}}/leagues/nfl/{{season}}'

# Draft-related URLs
SLEEPER_DRAFT_URL = f'{SLEEPER_API_BASE_URL}/draft/{{draft_id}}'
SLEEPER_DRAFT_PICKS_URL = f'{SLEEPER_API_BASE_URL}/draft/{{draft_id}}/picks'
SLEEPER_DRAFT_TRADES_URL = f'{SLEEPER_API_BASE_URL}/draft/{{draft_id}}/traded_picks'

# Roster-related URLs
SLEEPER_ROSTER_URL = f'{SLEEPER_API_BASE_URL}/roster/{{roster_id}}'

# State-related URLs
SLEEPER_STATE_NFL_URL = f'{SLEEPER_API_BASE_URL}/state/nfl'
