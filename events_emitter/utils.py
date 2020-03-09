import re
import logging
import requests

from eventful_django.models import Event as eventful_Event
from events_emitter.models import EventsDependencies, UserSubscriptoins

logging.basicConfig()
logger = logging.getLogger(__name__)


def parse_str_to_timedelta(timedelta_str):
    logger.debug(f"timedelta str {timedelta_str}")
    if 'day' in timedelta_str:
        exp = re.compile(
            r'^(?P<days>[-\d]+) day[s]*, (?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d[\.\d+]*)$')
    else:
        exp = re.compile(r'^(?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d[\.\d+]*)$')
    matched = exp.match(timedelta_str)
    return {key: float(val) for key, val in matched.groupdict().items()}


def fire_user_subscriptions(expression_id):
    try:
        exp_inst = EventsDependencies.objects.get(id=expression_id)
        event_name = exp_inst.name
        users = exp_inst.users_set.all()
        for user in users:
            subs = UserSubscriptoins.objects.filter(user_id=user.name, event_id=expression_id)
            for subscription in subs:
                send_notification_request(subscription, event_name)

    except Exception as e:
        logger.exception(f'expression I-{expression_id} failed to publish event to subscribers due to: {e}')


def send_notification_request(subscription, event_name):
    try:
        response = requests.request(
            'POST',
            subscription.webhook_url,
            json={
                "event": event_name,
            },
            headers=eval(subscription.headers or '{}'),
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        logger.error(error)


def fire_action_pubsub(event, payload):
    logger.info(f"Firing event {event} payload {payload}")
    try:
        eventful_Event.dispatch(event, payload)
    except Exception as e:
        logger.error(f"Error {e} while dispatching event {event} with payload {payload}")
