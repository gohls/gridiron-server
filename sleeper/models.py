import uuid

from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from core.models import LeagueRulebook, PlatformUser


class SleeperUser(models.Model):
    platform_user = models.OneToOneField(PlatformUser, on_delete=models.CASCADE, related_name='sleeper_user')
    user_id = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)

    def __str__(self):
        return self.display_name
    

class SleeperLeague(models.Model):
    league_id = models.CharField(max_length=50, unique=True)
    previous_league_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    name = models.CharField(max_length=100, help_text="Name of the league")
    total_rosters = models.IntegerField(null=True, blank=True, help_text="Total number of rosters/teams in league")
    season = models.CharField(max_length=50, help_text="Year e.g. 2018, 2019, 2020, etc.")
    sport = models.CharField(max_length=50, help_text="nfl") # only support "nfl" right now
    rulebook = models.OneToOneField(LeagueRulebook, on_delete=models.CASCADE, related_query_name="sleeper_league")

    def __str__(self):
        return self.name
    
    
class SleeperLeagueTeam(models.Model):
    owner = models.ForeignKey(SleeperUser, on_delete=models.CASCADE)
    league = models.ForeignKey(SleeperLeague, on_delete=models.CASCADE)
    metadata = models.JSONField(blank=True, null=True, help_text="Additional user league information like team_name")

    def __str__(self):
        return f"{self.owner.display_name} in {self.league.name}"
    
    class Meta:
        unique_together = ('owner', 'league') 


class SleeperLeagueTeamRoster(models.Model):
    league = models.ForeignKey(SleeperLeague, on_delete=models.CASCADE)
    team = models.OneToOneField(SleeperLeagueTeam, on_delete=models.CASCADE, related_name='roster', null=True, blank=True)
    roster_id = models.IntegerField()
    
    def __str__(self):
        return f"Roster {self.roster_id} for {self.team.owner.display_name} in {self.league.name}"

    class Meta:
        unique_together = ('league', 'roster_id')


