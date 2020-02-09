import re
import logging

from eventful_django.models import Event as eventful_Event

logging.basicConfig()
logger = logging.getLogger(__name__)


def parse_str_to_timedelta(timedelta_str):
    if 'day' in timedelta_str:
        exp = re.compile(
            r'^(?P<days>[-\d]+) day[s]*, (?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d[\.\d+]*)$')
    else:
        exp = re.compile(r'^(?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d[\.\d+]*)$')
    matched = exp.match(timedelta_str)
    return {key: float(val) for key, val in matched.groupdict().items()}


def fire_action_pubsub(event, payload):
    logger.info(f"Firing event {event} payload {payload}")
    try:
        eventful_Event.dispatch(event, payload)
    except Exception as e:
        logger.error(f"Error {e} while dispatching event {event} with payload {payload}")
