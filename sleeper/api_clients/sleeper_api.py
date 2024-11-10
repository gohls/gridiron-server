import requests
from . import constants

def make_request(url: str) -> dict:
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Unable to fetch data", "status_code": response.status_code}
    except Exception as e:
        return {"error": str(e), "status_code": 500}


def get_league(league_id: str) -> dict:
    url = constants.SLEEPER_LEAGUE_URL.format(league_id=league_id)
    return make_request(url)

def get_league_matchups(league_id: str, week: int) -> dict:
    url = constants.SLEEPER_LEAGUE_MATCHUPS_URL.format(league_id=league_id, week=week)
    return make_request(url)

def get_league_users(league_id: str) -> dict:
    url = constants.SLEEPER_LEAGUE_USERS_URL.format(league_id=league_id)
    return make_request(url)

def get_league_rosters(league_id: str) -> dict:
    url = constants.SLEEPER_LEAGUE_ROSTERS_URL.format(league_id=league_id)
    return make_request(url)

def get_league_trades(league_id: str, week: int) -> dict:
    url = constants.SLEEPER_LEAGUE_TRADES_URL.format(league_id=league_id, week=week)
    return make_request(url)

def get_league_drafts(league_id: str) -> dict:
    url = constants.SLEEPER_LEAGUE_DRAFTS_URL.format(league_id=league_id)
    return make_request(url)

def get_player(player_id: str) -> dict:
    url = constants.SLEEPER_PLAYER_URL.format(player_id=player_id)
    return make_request(url)

def get_players() -> dict:
    url = constants.SLEEPER_PLAYERS_URL
    return make_request(url)

def get_player_news() -> dict:
    url = constants.SLEEPER_PLAYER_NEWS_URL
    return make_request(url)

def get_user(user_id: str) -> dict:
    url = constants.SLEEPER_USER_URL.format(user_id=user_id)
    return make_request(url)

def get_user_leagues(user_id: str, season: str) -> dict:
    url = constants.SLEEPER_USER_LEAGUES_URL.format(user_id=user_id, season=season)
    return make_request(url)

def get_draft(draft_id: str) -> dict:
    url = constants.SLEEPER_DRAFT_URL.format(draft_id=draft_id)
    return make_request(url)

def get_draft_picks(draft_id: str) -> dict:
    url = constants.SLEEPER_DRAFT_PICKS_URL.format(draft_id=draft_id)
    return make_request(url)

def get_draft_trades(draft_id: str) -> dict:
    url = constants.SLEEPER_DRAFT_TRADES_URL.format(draft_id=draft_id)
    return make_request(url)

def get_roster(roster_id: str) -> dict:
    url = constants.SLEEPER_ROSTER_URL.format(roster_id=roster_id)
    return make_request(url)

def get_state_nfl() -> dict:
    url = constants.SLEEPER_STATE_NFL_URL
    return make_request(url)

