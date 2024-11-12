from rest_framework import serializers
from django.db import transaction
from sleeper.models import (
    SleeperLeague, 
    SleeperLeagueRulebook, 
    SleeperRulebookRule, 
    SleeperRulebookRuleSubsection
)


class SleeperRulebookRuleSubsectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SleeperRulebookRuleSubsection
        fields = ['id', 'subsection_title', 'subsection_content', 'ordering']

class SleeperRulebookRuleSerializer(serializers.ModelSerializer):
    subsections = SleeperRulebookRuleSubsectionSerializer(many=True)

    class Meta:
        model = SleeperRulebookRule
        fields = ['id', 'rule_title', 'rule_description', 'ordering', 'subsections']

class SleeperLeagueRulebookSerializer(serializers.ModelSerializer):
    rules = SleeperRulebookRuleSerializer(many=True)
    league_id = serializers.PrimaryKeyRelatedField(queryset=SleeperLeague.objects.all(), source='league')

    class Meta:
        model = SleeperLeagueRulebook
        fields = ['id', 'league_id', 'name', 'description', 'rules']

    @transaction.atomic
    def create(self, validated_data):
        league = validated_data.pop('league_id')
        rules_data = validated_data.pop('rules', [])
        
        rulebook, _ = SleeperLeagueRulebook.objects.update_or_create(
            league=league,
            defaults=validated_data
        )
        
        self._create_or_update_rules(rulebook, rules_data)
        return rulebook

    @transaction.atomic
    def update(self, instance, validated_data):
        rules_data = validated_data.pop('rules', [])
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        self._create_or_update_rules(instance, rules_data)
        return instance

    def _create_or_update_rules(self, rulebook, rules_data):
        rulebook.rules.all().delete()
        for rule_data in rules_data:
            subsections_data = rule_data.pop('subsections', [])
            rule = SleeperRulebookRule.objects.create(rulebook=rulebook, **rule_data)
            SleeperRulebookRuleSubsection.objects.bulk_create([
                SleeperRulebookRuleSubsection(rule=rule, **subsection_data)
                for subsection_data in subsections_data
            ])