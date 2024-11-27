# Generated by Django 5.1.2 on 2024-11-27 20:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("core", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="SleeperLeague",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("league_id", models.CharField(max_length=50, unique=True)),
                (
                    "previous_league_id",
                    models.CharField(
                        blank=True, max_length=255, null=True, unique=True
                    ),
                ),
                (
                    "name",
                    models.CharField(help_text="Name of the league", max_length=100),
                ),
                (
                    "avatar",
                    models.CharField(
                        help_text="Avatar id of the league", max_length=100
                    ),
                ),
                (
                    "total_rosters",
                    models.IntegerField(
                        blank=True,
                        help_text="Total number of rosters/teams in league",
                        null=True,
                    ),
                ),
                (
                    "status",
                    models.IntegerField(
                        choices=[
                            (1, "Pre-Draft"),
                            (2, "Drafting"),
                            (3, "In Season"),
                            (4, "Complete"),
                        ],
                        default=1,
                        help_text="Current status of the league",
                    ),
                ),
                (
                    "season",
                    models.CharField(
                        help_text="Year e.g. 2018, 2019, 2020, etc.", max_length=50
                    ),
                ),
                ("sport", models.CharField(help_text="nfl", max_length=50)),
                (
                    "rulebook",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_query_name="sleeper_league",
                        to="core.leaguerulebook",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SleeperLeagueTeam",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "metadata",
                    models.JSONField(
                        blank=True,
                        help_text="Additional user league information like team_name",
                        null=True,
                    ),
                ),
                (
                    "league",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="sleeper.sleeperleague",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SleeperLeagueTeamRoster",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("roster_id", models.IntegerField()),
                (
                    "league",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="sleeper.sleeperleague",
                    ),
                ),
                (
                    "team",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="roster",
                        to="sleeper.sleeperleagueteam",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SleeperUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_id", models.CharField(max_length=100, unique=True)),
                ("username", models.CharField(max_length=100)),
                ("display_name", models.CharField(max_length=100)),
                (
                    "avatar",
                    models.CharField(help_text="Avatar id of the user", max_length=100),
                ),
                (
                    "platform_user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sleeper_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="sleeperleagueteam",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="sleeper.sleeperuser"
            ),
        ),
        migrations.AddIndex(
            model_name="sleeperleague",
            index=models.Index(
                fields=["league_id"], name="sleeper_sle_league__111bed_idx"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="sleeperleagueteamroster",
            unique_together={("league", "roster_id")},
        ),
        migrations.AddIndex(
            model_name="sleeperleagueteam",
            index=models.Index(
                fields=["owner", "league"], name="sleeper_sle_owner_i_1c91ea_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="sleeperleagueteam",
            index=models.Index(
                fields=["league", "owner"], name="sleeper_sle_league__246778_idx"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="sleeperleagueteam",
            unique_together={("owner", "league")},
        ),
    ]
