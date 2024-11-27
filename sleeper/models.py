import uuid

from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import gettext_lazy as _

from core.models import LeagueRulebook, PlatformUser


class SleeperUser(models.Model):
    platform_user = models.OneToOneField(PlatformUser, on_delete=models.CASCADE, related_name='sleeper_user')
    user_id = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)
    avatar = models.CharField(max_length=100, help_text="Avatar id of the user")

    def __str__(self):
        return self.display_name
    

class LeagueStatus(models.IntegerChoices):
    PRE_DRAFT = 1, _('Pre-Draft')
    DRAFTING = 2, _('Drafting')
    IN_SEASON = 3, _('In Season')
    COMPLETE = 4, _('Complete')

STATUS_MAP = {
    'pre_draft': LeagueStatus.PRE_DRAFT,
    'drafting': LeagueStatus.DRAFTING,
    'in_season': LeagueStatus.IN_SEASON,
    'complete': LeagueStatus.COMPLETE
}


class SleeperLeague(models.Model):
    league_id = models.CharField(max_length=50, unique=True)
    previous_league_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    name = models.CharField(max_length=100, help_text="Name of the league")
    avatar = models.CharField(max_length=100, help_text="Avatar id of the league") 
    total_rosters = models.IntegerField(null=True, blank=True, help_text="Total number of rosters/teams in league")
    status = models.IntegerField(choices=LeagueStatus.choices, default=LeagueStatus.PRE_DRAFT, help_text="Current status of the league")
    season = models.CharField(max_length=50, help_text="Year e.g. 2018, 2019, 2020, etc.")
    sport = models.CharField(max_length=50, help_text="nfl") # only support "nfl" right now
    rulebook = models.OneToOneField(LeagueRulebook, on_delete=models.CASCADE, related_query_name="sleeper_league")

    def __str__(self):
        return self.name
    
    class Meta:
        indexes = [
            models.Index(fields=['league_id']),
        ]
    
    
class SleeperLeagueTeam(models.Model):
    owner = models.ForeignKey(SleeperUser, on_delete=models.CASCADE)
    league = models.ForeignKey(SleeperLeague, on_delete=models.CASCADE)
    metadata = models.JSONField(blank=True, null=True, help_text="Additional user league information like team_name")

    def __str__(self):
        return f"{self.owner.display_name} in {self.league.name}"
    
    class Meta:
        unique_together = ('owner', 'league') 
        indexes = [
            models.Index(fields=['owner', 'league']),
            models.Index(fields=['league', 'owner']),
        ]


class SleeperLeagueTeamRoster(models.Model):
    league = models.ForeignKey(SleeperLeague, on_delete=models.CASCADE)
    team = models.OneToOneField(SleeperLeagueTeam, on_delete=models.CASCADE, related_name='roster', null=True, blank=True)
    roster_id = models.IntegerField()
    
    def __str__(self):
        return f"Roster {self.roster_id} for {self.team.owner.display_name} in {self.league.name}"

    class Meta:
        unique_together = ('league', 'roster_id')


