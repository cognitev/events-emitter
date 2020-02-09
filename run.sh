#!/bin/sh

set -x

if [ "$1" = "events_emitter" ]; then
    echo "==================="
    echo "Running events_emitter"
    echo "==================="
    echo
    python manage.py migrate
    python manage.py runserver 0.0.0.0:9000

elif [ "$1" = "eventful_worker" ]; then
    echo "==================="
    echo "Running eventful worker"
    echo "==================="
    echo
    celery worker -A eventful_django.eventful_tasks --loglevel=INFO

elif [ "$1" = "worker" ]; then
    echo "==================="
    echo "Running events_emitter worker"
    echo "==================="
    echo
    celery worker -A events_emitter --loglevel=INFO -Q $EVENTS_EMITTER_QUEUE

elif [ "$1" = "beat" ]; then
    echo "==================="
    echo "Running celery beat"
    echo "==================="
    echo
    celery beat -A events_emitter --loglevel=INFO -S django

fi