from django.db import models
from core.models import PlatformUser


class SleeperUser(models.Model):
    platform_user = models.ForeignKey(PlatformUser, on_delete=models.CASCADE, related_name='sleeper_users')
    user_id = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)

    def __str__(self):
        return self.display_name

class SleeperLeague(models.Model):
    league_id = models.CharField(max_length=50, unique=True)
    previous_league_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    name = models.CharField(max_length=100)
    season = models.CharField(max_length=50)
    sport = models.CharField(max_length=10) # only support "nfl" right now
    num_teams = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

class SleeperUserLeague(models.Model):
    user = models.ForeignKey(SleeperUser, on_delete=models.CASCADE)
    league = models.ForeignKey(SleeperLeague, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'league')  # ensures a user can only be in a league once

    def __str__(self):
        return f"{self.user.display_name} in {self.league.name}"


class SleeperTeam(models.Model):
    user = models.ForeignKey(SleeperUser, on_delete=models.CASCADE, related_name="sleeper_teams")
    league = models.ForeignKey(SleeperLeague, on_delete=models.CASCADE, related_name="sleeper_teams")
    team_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.team_name} in {self.league.name}"

    class Meta:
        unique_together = ('user', 'league') # ensures that a user can only have one team in a league