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
    name = models.CharField(max_length=100, help_text="Year e.g. 2018, 2019, 2020, etc.")
    season = models.CharField(max_length=50, help_text="nfl")
    sport = models.CharField(max_length=50) # only support "nfl" right now
    num_teams = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

class SleeperUserLeague(models.Model):
    user = models.ForeignKey(SleeperUser, on_delete=models.CASCADE)
    league = models.ForeignKey(SleeperLeague, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.display_name} in {self.league.name}"
    
    class Meta:
        unique_together = ('user', 'league')  # ensures a user can only be in a league once

class SleeperTeam(models.Model):
    user = models.ForeignKey(SleeperUser, on_delete=models.CASCADE, related_name="sleeper_teams")
    league = models.ForeignKey(SleeperLeague, on_delete=models.CASCADE, related_name="sleeper_teams")
    team_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.team_name} in {self.league.name}"

    class Meta:
        unique_together = ('user', 'league') # ensures that a user can only have one team in a league


class SleeperLeagueRulebook(models.Model):
    league = models.OneToOneField(SleeperLeague, on_delete=models.CASCADE, related_name="rulebook")
    name = models.CharField(max_length=100, help_text="Name of the rulebook")
    description = models.TextField(help_text="A description of the rulebook", blank=True, null=True)

    def __str__(self):
        return f"Rulebook for {self.league.name}"

class SleeperRulebookRule(models.Model):
    rulebook = models.ForeignKey(SleeperLeagueRulebook, on_delete=models.CASCADE, related_name="rules")
    rule_title = models.CharField(max_length=200, help_text="Title of the rule")
    rule_description = models.TextField(help_text="Detailed description of the rule")
    created_at = models.DateTimeField(auto_now_add=True)
    ordering = models.IntegerField(default=0, help_text="Order of the rule within the rulebook")

    def __str__(self):
        return self.rule_title

    class Meta:
        ordering = ['ordering'] # ensure rules are ordered by 'ordering'
        constraints = [
            models.UniqueConstraint(fields=['rulebook', 'ordering'], name='unique_ordering_within_rulebook')
        ]

class SleeperRulebookRuleSubsection(models.Model):
    rule = models.ForeignKey(SleeperRulebookRule, on_delete=models.CASCADE, related_name="subsections")
    subsection_title = models.CharField(max_length=200, help_text="Title of the subsection")
    subsection_content = models.TextField(help_text="Content of the subsection")
    ordering = models.IntegerField(default=0, help_text="Order of the subsection within the rule")

    def __str__(self):
        return f"{self.subsection_title} (Subsection of {self.rule.rule_title})"

    class Meta:
        ordering = ['ordering']  # ensure subsections are ordered by 'ordering'
        constraints = [
            models.UniqueConstraint(fields=['rule', 'ordering'], name='unique_ordering_within_rule')
        ]
