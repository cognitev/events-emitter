from __future__ import absolute_import, unicode_literals
from events_emitter.utils import parse_str_to_timedelta, fire_action_pubsub # noqa
from django.test import TestCase
from events_emitter.tasks import proccess_expression, proccess_rule
import mock
from datetime import datetime


class TestUtils(TestCase):

    def test_parse_str_to_timedelta(self):
        parsed_timedelta = parse_str_to_timedelta('50 days, 30:20:1')
        expected_output = {'days': 50, 'hours': 30, 'minutes': 20, 'seconds': 1}
        self.assertEqual(parsed_timedelta, expected_output)

        parsed_timedelta = parse_str_to_timedelta('30:20:1')
        expected_output = {'hours': 30, 'minutes': 20, 'seconds': 1}
        self.assertEqual(parsed_timedelta, expected_output)

    @mock.patch("eventful_django.models.Event.dispatch")
    def test_fire_action_pubsub(self, eventful_mock):
        fire_action_pubsub('some_event', {})
        self.assertEqual(eventful_mock.call_count, 1)
        eventful_mock.assert_called_with('some_event', {})


class TestCeleryTasks(TestCase):
    @mock.patch("events_emitter.tasks.fire_action_pubsub")
    def test_proccess_expression(self, pubsub_mock):
        proccess_expression('id1 or id2', 'event_name', {'id1': True, 'id2': False})
        self.assertEqual(pubsub_mock.call_count, 1)

        proccess_expression('id1 and id2', 'event_name', {'id1': True, 'id2': False})
        self.assertEqual(pubsub_mock.call_count, 1)

        proccess_expression('id1 and id2', 'event_name', {'id1': True, 'id2': True})
        self.assertEqual(pubsub_mock.call_count, 2)

    @mock.patch("events_emitter.events_factory.bigquery_time_series.BigQueryTimeSeries.get_event_last_creation", return_value=[]) # noqa
    def test_process_rule(self, bigquery_mock):
        rule = {'id': 1, 'event_type': 'event ay 7aga', 'state': 'PRESENT', 'duration': '0:20:0'}
        event_result = proccess_rule(rule)
        expected_result = {'id1': False}
        self.assertEqual(event_result, expected_result)

        bigquery_mock.return_value = [{'created_at': datetime.now()}]
        expected_result = {'id1': True}
        event_result = proccess_rule(rule)
        self.assertEqual(event_result, expected_result)
