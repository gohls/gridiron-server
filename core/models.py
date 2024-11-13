from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _


class PlatformUser(AbstractUser):
    # Override the email field to make it required
    ## Dont want to make this required while developing atm
    #email = models.EmailField(unique=True, blank=False, null=False)

    def __str__(self):
        return self.username


class FantasyApp(models.IntegerChoices):
    SLEEPER = 1, _('Sleeper')
    UNDERDOG = 2, _('Underdog')
    ESPN = 3, _('Espn')


class UserFantasyApp(models.Model):
    user = models.ForeignKey(PlatformUser, on_delete=models.CASCADE, related_name='fantasy_apps')
    app = models.CharField(max_length=4, choices=FantasyApp.choices)
    
    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'app'], name='unique_user_app')
        ]


class LeagueRulebook(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    league = GenericForeignKey("content_type", "object_id")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['content_type', 'object_id'], name='unique_league_rulebook')
        ]


class Rule(models.Model):
    rulebook = models.ForeignKey(LeagueRulebook, on_delete=models.CASCADE, related_name='rules')
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']
        constraints = [
            UniqueConstraint(fields=['rulebook', 'order'], name='unique_rulebook_rule')
        ]


class RuleSubsection(models.Model):
    rule = models.ForeignKey(Rule, on_delete=models.CASCADE, related_name='subsections')
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']
        constraints = [
            UniqueConstraint(fields=['rulebook', 'order'], name='unique_rule_subsection')
        ]
