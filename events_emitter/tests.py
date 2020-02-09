from __future__ import absolute_import, unicode_literals
from events_emitter.utils import parse_str_to_timedelta, fire_action_pubsub # noqa
from django.test import TestCase
import mock


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
    def test_proccess_expression(self):
        pass
