#!/bin/sh

set -x

if [ "$1" = "events_emitter" ]; then
    echo "==================="
    echo "Running events_emitter"
    echo "==================="
    echo
    python manage.py migrate
    gunicorn events_emitter.wsgi --bind 0.0.0.0:9000 -k eventlet --log-level $LOG_LEVEL

elif [ "$1" = "eventful_worker" ]; then
    echo "==================="
    echo "Running eventful worker"
    echo "==================="
    echo
    celery worker -A eventful_django.eventful_tasks --loglevel=INFO --broker=$EVENTFUL_BROKER_URL

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

elif [ "$1" = "monitoring" ]; then
  echo "Running celery prometheus exporter"
  export BROKER_URL=`env | grep CELERY_BROKER_URL | sed 's/.*=//g'`
  export CELERY_METRICS_URL=`env | grep CELERY_METRICS_URL | sed 's/.*=//g'`
  celery-prometheus-exporter --enable-events --broker=$BROKER_URL --addr=$CELERY_METRICS_URL
fi