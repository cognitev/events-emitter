from __future__ import absolute_import
import logging


from celery import group, shared_task, chain
from datetime import datetime, timedelta
from django.conf import settings

from events_emitter.models import BusinessRules, EventsDependencies
from events_emitter.utils import parse_str_to_timedelta, fire_action_pubsub
from events_emitter.events_factory.factory_event import FactoryEvent

logging.basicConfig()
logger = logging.getLogger(__name__)
"""
                          -                 -
                         -- proccess rule 1 --
                        ---                 ---
Get business rules --> ---- proccess rule 2 ---- --> evaluate rules result with exprissions
                        ---                 ---
                         -- proccess rule 3 --
                          -                 -
"""
@shared_task
def proccess_business_rules(*args, **kwargs):
    rules = BusinessRules.objects.all() # noqa
    logger.info("start proccess business rules")
    proccess_rule_list = []
    for rule in rules:
        logger.info(f"business rule {rule.event_type} with duration {rule.duration} and state {rule.state}")
        curr_rule = {
            'id': rule.id,
            'event_type': rule.event_type,
            'duration': str(rule.duration),
            'state': rule.state
        }
        proccess_rule_list.append(proccess_rule.s(curr_rule))

    proccess_rules_group = chain(group(proccess_rule_list), proccess_rules_res.s())
    proccess_rules_group.apply_async(queue=settings.EVENTS_EMITTER_QUEUE)


@shared_task
def proccess_rule(rule, *args, **kwargs):
    logger.info(f"start evaluate rule {rule.get('event_type')}")
    rule_res = False
    try:
        time_series_type = FactoryEvent().create_event_class(settings.TIME_SERIES_TYPE)
        result = time_series_type.get_event_last_creation(rule.get('event_type'))
        for row in result:
            event_last_time = datetime.now() - row['created_at']
            event_duration = timedelta(**parse_str_to_timedelta(rule.get('duration')))
            rule_res = (rule.get('state') == 'ABSENT'
                        and event_last_time >= event_duration) or (rule.get('state') == 'PRESENT' # noqa
                                                                   and event_last_time <= event_duration) # noqa
        logger.info(f"finish evaluate rule {rule.get('event_type')} with result {rule_res}")
    except Exception as e:
        logger.error(f"can't evaluate rule {rule.get('event_type')} with error {e}")

    return {f"id{rule.get('id')}": rule_res}


@shared_task
def proccess_rules_res(result):
    logger.info(f"get rules result {result} and start proccess exprissions")
    result = {k: v for rule_res in result for k, v in rule_res.items()}
    expressions = EventsDependencies.objects.all() # noqa
    proccess_expression_list = [
        proccess_expression.s(expression.dependency_experssion, expression.name, result) for expression in expressions # noqa
    ]
    proccess_expressions_group = group(proccess_expression_list)
    proccess_expressions_group.apply_async(queue=settings.EVENTS_EMITTER_QUEUE)


@shared_task(ignore_result=True)
def proccess_expression(expression, event_name, rules_res):
    logger.info(f"start evaluate expression '{expression}' ")
    try:
        eval_expression = eval(expression, rules_res)
        if(eval_expression):
            fire_action_pubsub(event_name, {"event": event_name})
            logger.info(f"finish evaluate expression '{expression}' with result {eval_expression}")
    except Exception as e:
        logger.error(f"can't evaluate expression '{expression}' with error {e}")
