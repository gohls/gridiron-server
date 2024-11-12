from django.db import models
from core.models import PlatformUser


class SleeperUser(models.Model):
    """
    Represents a user on the Sleeper app
    
    Related to:
    - PlatformUser via a ForeignKey (a user on this platform corresponding sleeper user)
    """
    platform_user = models.ForeignKey(PlatformUser, on_delete=models.CASCADE, related_name='sleeper_users')
    user_id = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)

    def __str__(self):
        return self.display_name


class SleeperLeague(models.Model):
    """
    Represents a fantasy league on the Sleeper app

    Related to:
    - SleeperUser through SleeperUserLeague (many users can be in this league)
    - SleeperUserLeagueRoster (many rosters belong to this league)
    - SleeperLeagueRulebook (one rulebook per league)
    """
    league_id = models.CharField(max_length=50, unique=True)
    previous_league_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    name = models.CharField(max_length=100, help_text="Name of the league")
    total_rosters = models.IntegerField(null=True, blank=True, help_text="Total number of rosters/teams in league")
    season = models.CharField(max_length=50, help_text="Year e.g. 2018, 2019, 2020, etc.")
    sport = models.CharField(max_length=50, help_text="nfl") # only support "nfl" right now

    def __str__(self):
        return self.name


class SleeperUserLeague(models.Model):
    """
    Represents a user's membership in a particular league

    Related to:
    - SleeperUser through a ForeignKey (a user can belong to multiple leagues).
    - SleeperLeague through a ForeignKey (a league can have multiple users).
    """
    user = models.ForeignKey(SleeperUser, on_delete=models.CASCADE)
    league = models.ForeignKey(SleeperLeague, on_delete=models.CASCADE)
    metadata = models.JSONField(blank=True, null=True, help_text="Additional user league information like team_name")

    def __str__(self):
        return f"{self.user.display_name} in {self.league.name}"
    
    class Meta:
        unique_together = ('user', 'league') 


class SleeperUserLeagueRoster(models.Model):
    """
    Represents a roster associated with a user in a particular league
    
    Related to:
    - SleeperLeague through a ForeignKey (a league can have multiple rosters)
    - SleeperUser through a ForeignKey (a user can have multiple rosters in different leagues)
    """
    owner = models.ForeignKey(SleeperUser, on_delete=models.CASCADE, related_name="rosters")
    league = models.ForeignKey(SleeperLeague, on_delete=models.CASCADE, related_name="rosters")
    roster_id = models.IntegerField()
    
    def __str__(self):
        return f"Roster {self.roster_id} for {self.owner.display_name} in {self.league.name}"

    class Meta:
        unique_together = ('league', 'roster_id')


class SleeperLeagueRulebook(models.Model):
    """
    Represents the rulebook for a particular league, containing the rules

    Related to:
    - SleeperLeague via a OneToOneField (each league can have only one rulebook)
    """
    league = models.OneToOneField(SleeperLeague, on_delete=models.CASCADE, related_name="rulebook")
    name = models.CharField(max_length=100, help_text="Name of the rulebook")
    description = models.TextField(help_text="A description of the rulebook", blank=True, null=True)

    def __str__(self):
        return f"Rulebook for {self.league.name}"


class SleeperRulebookRule(models.Model):
    """
    Represents an individual rule within a league's rulebook

    Related to:
    - SleeperLeagueRulebook via ForeignKey (each rule belongs to a specific rulebook)
    - SleeperRulebookRuleSubsection through a related name (a rule can have multiple subsections)
    """
    rulebook = models.ForeignKey(SleeperLeagueRulebook, on_delete=models.CASCADE, related_name="rules")
    rule_title = models.CharField(max_length=200, help_text="Title of the rule")
    rule_description = models.TextField(help_text="Detailed description of the rule")
    ordering = models.IntegerField(default=0, help_text="Order of the rule within the rulebook")

    def __str__(self):
        return self.rule_title

    class Meta:
        ordering = ['ordering']
        constraints = [
            models.UniqueConstraint(fields=['rulebook', 'ordering'], name='unique_ordering_within_rulebook')
        ]


class SleeperRulebookRuleSubsection(models.Model):
    """
    Represents a subsection of a specific rule within a rulebook.

    Related to:
    - SleeperRulebookRule via ForeignKey (each subsection belongs to a specific rule).
    """
    rule = models.ForeignKey(SleeperRulebookRule, on_delete=models.CASCADE, related_name="subsections")
    subsection_title = models.CharField(max_length=200, help_text="Title of the subsection")
    subsection_content = models.TextField(help_text="Content of the subsection")
    ordering = models.IntegerField(default=0, help_text="Order of the subsection within the rule")

    def __str__(self):
        return f"{self.subsection_title} (Subsection of {self.rule.rule_title})"

    class Meta:
        ordering = ['ordering']
        constraints = [
            models.UniqueConstraint(fields=['rule', 'ordering'], name='unique_ordering_within_rule')
        ]
