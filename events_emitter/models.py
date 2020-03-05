import re
from django.db import models

RULE_STATES = [
    ('PRESENT', 'PRESENT'),
    ('ABSENT', 'ABSENT'),
]


class BusinessRules(models.Model):
    event_type = models.CharField(max_length=80, null=False)

    state = models.CharField(
        max_length=10,
        choices=RULE_STATES,
        null=False
    )

    duration = models.DurationField()


class EventsDependencies(models.Model):
    dependency_experssion = models.CharField(max_length=250, null=False)
    name = models.CharField(max_length=200, null=False)

    def validate_expression(self):
        event_dependency_exp = self.dependency_experssion
        boolean_expression = eval(re.sub('id[0-9]+', 'True', event_dependency_exp))
        business_rules_ids = re.findall('id[0-9]+', event_dependency_exp)

        for business_rule_id in business_rules_ids:
            BusinessRules.objects.get(id=business_rule_id.replace('id', ''))

        return boolean_expression

    def save(self, *args, **kwargs):
        self.validate_expression()
        super(EventsDependencies, self).save(*args, **kwargs)


class Users(models.Model):
    name = models.CharField(max_length=80, primary_key=True)
    events = models.ManyToManyField(EventsDependencies)


class UserSubscriptoins(models.Model):
    webhook_url = models.URLField(max_length=200)
    headers = models.TextField('Request Headers', null=True)
    event_id = models.IntegerField(null=False)
    user_id = models.IntegerField(null=False)
