from django.db.models.signals import pre_save
from django.dispatch import receiver
from events_emitter.models import EventsDependencies, BusinessRules
import logging
logger = logging.getLogger(__name__)


@receiver(pre_save, sender=EventsDependencies)
def insta_campaign_update_status(sender, **kwargs):
    event_dependency_exp = kwargs['instance'].dependency_experssion
    for or_experssion in event_dependency_exp.split('&'):
        for business_event_id in or_experssion.split('||'):
            business_event_id = int(business_event_id)
            BusinessRules.objects.get(id=business_event_id)

    return event_dependency_exp