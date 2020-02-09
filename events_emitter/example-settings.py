"""
Django settings for events_emitter project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from django.utils.log import DEFAULT_LOGGING

import environ

getenv = os.getenv
ENV = getenv('ENVIRONMENT', 'development')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = environ.Path(__file__) - 3
APPS_DIR = ROOT_DIR.path('events_emitter')
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'a_va9!658xfz86o*k-51o5)9_za)6=ou5curj0d@+=395zz@_x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'events_emitter',
    'django_celery_results',
    'django_celery_beat',
    'eventful_django',
]

MIDDLEWARE = [
    'events_emitter.middleware.HealthCheckMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'events_emitter.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'events_emitter.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

(
    DB_ENGINE,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_PORT,
    TEST_DB_NAME,
) = {
    'production': (
        getenv('DB_ENGINE', 'django_prometheus.db.backends.mysql'),
        getenv('DB_NAME'),
        getenv('DB_USER'),
        getenv('DB_PASSWORD'),
        getenv('DB_HOST'),
        getenv('DB_PORT'),
        getenv('DB_NAME_TESTS'),
    ),
    'development': (
        getenv('DB_ENGINE', 'django_prometheus.db.backends.mysql'),
        getenv('DB_NAME', 'events_emitter_testing'),
        getenv('DB_USER', 'root'),
        getenv('DB_PASSWORD', ''),
        getenv('DB_HOST', '127.0.0.1'),
        getenv('DB_PORT', '3306'),
        getenv('DB_NAME_TESTS', 'events_emitter_tests'),
    )
}.get(ENV)

# Celery Broker
(
    CELERY_BROKER_URL,
    CELERY_RESULT_BACKEND,
    CELERY_ACCEPT_CONTENT,
    CELERY_TASK_SERIALIZER,
    CELERY_RESULT_SERIALIZER,
    CELERY_IGNORE_RESULT,
) = {
    "production": (
        getenv('CELERY_BROKER_URL'),
        getenv('CELERY_RESULT_BACKEND', 'django-db'),
        getenv('CELERY_ACCEPT_CONTENT', ['json']),
        getenv('CELERY_TASK_SERIALIZER', 'json'),
        getenv('CELERY_RESULT_SERIALIZER', 'json'),
        getenv('CELERY_IGNORE_RESULT', False),
    ),
    "development": (
        getenv('CELERY_BROKER_URL', 'redis://localhost:6379/'),
        getenv('CELERY_RESULT_BACKEND', 'django-db'),
        getenv('CELERY_ACCEPT_CONTENT', ['json']),
        getenv('CELERY_TASK_SERIALIZER', 'json'),
        getenv('CELERY_RESULT_SERIALIZER', 'json'),
        getenv('CELERY_IGNORE_RESULT', False),
    )
}.get(ENV)

DATABASES = {
    'default': {
        'ENGINE': DB_ENGINE,
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        'TEST': {
            'NAME': TEST_DB_NAME,
            'CHARSET': 'utf8',
            'COLLATION': 'utf8_general_ci',
        },
        'OPTIONS': {
            'connect_timeout': 3,
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'
TABLE_NAME = getenv('TABLE_NAME')
EVENTS_EMITTER_QUEUE = getenv('EVENTS_EMITTER_QUEUE', 'events_emitter')
TIME_SERIES_TYPE = getenv('TIME_SERIES_TYPE')

# logging configuration
LOGLEVEL = getenv('LOGLEVEL', default='info').upper()
LOGGING_CONFIG = None
handlers_list = ['console']
log_dict = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            # exact format is not important, this is the minimum information
            'format': '%(levelname)s %(asctime)s [%(name)s:%(lineno)s] '
                      '%(process)d %(thread)d %(message)s',
        },
        'django.server': DEFAULT_LOGGING['formatters']['django.server'],
    },
    'handlers': {
        # console logs to stderr
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        'django.server': DEFAULT_LOGGING['handlers']['django.server'],
    },
    'loggers': {
        # default for all undefined Python modules
        '': {
            'level': 'WARNING',
            'handlers': handlers_list,
        },
        # Our application code
        'events_emitter': {
            'level': LOGLEVEL,
            'handlers': handlers_list,
            # Avoid double logging because of root logger
            'propagate': False,
        },
        'django.server': DEFAULT_LOGGING['loggers']['django.server'],
    },
}
