from __future__ import absolute_import, unicode_literals
from events_emitter.utils import parse_str_to_timedelta
from events_emitter.utils import fire_action_pubsub, fire_user_subscriptions
from events_emitter.apis import subscribe_user, unsubscribe_user
from django.test import TestCase
from events_emitter.tasks import proccess_expression, proccess_rule
from events_emitter.models import EventsDependencies, BusinessRules, UserSubscriptoins, Users
import mock
from datetime import datetime, timedelta


class APIUtils(TestCase):
    def test_subscribe_unsubscribe_user(self):
        username = 'kareem_test2255'
        br = BusinessRules.objects.create(event_type='test_type22',
                                          state='ABSENT',
                                          duration=timedelta(days=20, hours=10))
        expression = EventsDependencies.objects.create(name='expression_test222',
                                                       dependency_experssion=f'id{br.id}')
        test_user = Users.objects.create(name=username)
        subscription_res = subscribe_user(username, 'https://test.com', '', expression.id)

        self.assertEquals(subscription_res.webhook_url, 'https://test.com')
        self.assertEquals(test_user.events.count(), 1)

        unsubscribe_user(username, subscription_res.webhook_url, expression.id)

        self.assertEquals(test_user.events.count(), 0)
        self.assertEquals(UserSubscriptoins.objects.filter(id=subscription_res.id).count(), 0)

    def test_get_user_subscriptios(self):
        pass


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

    def test_fire_user_subscriptions_should_silently_fail(self):
        fake_id = 52427
        fire_user_subscriptions(fake_id)

    @mock.patch("events_emitter.utils.send_notification_request", return_value={})
    def test_fire_user_subscriptions(self, notification_mock):
        br = BusinessRules.objects.create(event_type='test_type',
                                          state='ABSENT',
                                          duration=timedelta(days=20, hours=10))
        expression = EventsDependencies.objects.create(name='expression_test',
                                                       dependency_experssion=f'id{br.id}')
        username = 'kareem_test'
        expression.users_set.create(name=username)
        user_sub = UserSubscriptoins.objects.create(event_id=expression.id,
                                                    user_id=username,
                                                    webhook_url='https://test.com')

        fire_user_subscriptions(expression.id)

        self.assertEquals(notification_mock.call_count, 1)
        self.assertEquals(notification_mock.call_args[0][0], user_sub)
        self.assertEquals(notification_mock.call_args[0][1], expression.name)


class TestCeleryTasks(TestCase):
    @mock.patch("events_emitter.tasks.fire_action_pubsub")
    def test_proccess_expression(self, pubsub_mock):
        proccess_expression('id1 or id2', 'event_name', 1, {'id1': True, 'id2': False})
        self.assertEqual(pubsub_mock.call_count, 1)

        proccess_expression('id1 and id2', 'event_name', 1, {'id1': True, 'id2': False})
        self.assertEqual(pubsub_mock.call_count, 1)

        proccess_expression('id1 and id2', 'event_name', 1, {'id1': True, 'id2': True})
        self.assertEqual(pubsub_mock.call_count, 2)

    @mock.patch(
        "events_emitter.events_factory.bigquery_time_series.BigQueryTimeSeries.get_event_last_creation",
        return_value=[])
    def test_process_rule(self, bigquery_mock):
        rule = {'id': 1, 'event_type': 'event ay 7aga', 'state': 'PRESENT', 'duration': '0:20:0'}
        event_result = proccess_rule(rule)
        expected_result = {'id1': False}
        self.assertEqual(event_result, expected_result)

        bigquery_mock.return_value = [{'created_at': datetime.now()}]
        expected_result = {'id1': True}
        event_result = proccess_rule(rule)
        self.assertEqual(event_result, expected_result)
