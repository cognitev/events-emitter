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
    event_name = models.CharField(max_length=200, null=False)
