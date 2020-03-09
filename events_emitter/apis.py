from events_emitter.models import UserSubscriptoins, Users


def subscribe_user(user_name, subscription_webhook, headers, event_id):
    user_obj = Users.objects.get(name=user_name)
    user_obj.events.add(event_id)
    user_sub = UserSubscriptoins.objects.create(event_id=event_id,
                                                user_id=user_name,
                                                webhook_url=subscription_webhook,
                                                headers=headers)

    return user_sub


def unsubscribe_user(user_name, subscription_webhook, event_id):
    user_obj = Users.objects.get(name=user_name)
    user_obj.events.remove(event_id)
    return UserSubscriptoins.objects.filter(event_id=event_id, user_id=user_name).delete()


def get_user_subscriptions(user_name):
    return UserSubscriptoins.objects.filter(user_id=user_name)
