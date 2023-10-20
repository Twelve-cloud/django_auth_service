"""
Django settings for car_salon_activities project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""


import os
from typing import Optional
from pathlib import Path


# -------------------------- MAIN SETTINGS ------------------------------------

BASE_DIR: Path = Path(__file__).resolve().parent.parent

SECRET_KEY: Optional[str] = os.getenv('SECRET_KEY')

DEBUG: Optional[str] = os.getenv('DEBUG')

ALLOWED_HOSTS: Optional[list] = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')

DEFAULT_CHARSET: str = 'utf8'

ROOT_URLCONF: str = 'car_salon_activities.urls'

AUTH_USER_MODEL: str = 'jauth.User'

# -------------------------- INSTALLED APPS -----------------------------------

INSTALLED_APPS: list = [
    'jauth.apps.JauthConfig',
    'salon.apps.SalonConfig',
    'rest_framework',
]

# -------------------------- MIDDLEWARES --------------------------------------

MIDDLEWARE: list = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ---------------------------- DATABASES --------------------------------------

DATABASES: dict = {
    'master': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'CONN_MAX_AGE': 0,
    },
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'CONN_MAX_AGE': 0,
    },
}

# ------------------------- LANGUAGE SETTINGS ---------------------------------

LANGUAGE_CODE: str = 'en-us'

USE_I18N: bool = False

USE_L10N: bool = False

TIME_ZONE: str = 'Europe/Minsk'

USE_TZ: bool = True

# --------------------------- DRF SETTINGS ------------------------------------

REST_FRAMEWORK: dict = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'jauth.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'UNAUTHENTICATED_USER': None,
    'UNAUTHENTICATED_TOKEN': None,
    'UNICODE_JSON': False,
    'COMPACT_JSON': False,
    'STRICT_JSON': True,
}

# -------------------------- JWT SETTINGS -------------------------------------

JWT_TOKEN: dict = {
    'ACCESS_TOKEN_LIFETIME_MINUTES': 15,
    'REFRESH_TOKEN_LIFETIME_DAYS': 30,
    'TOKEN_TYPE': 'Bearer',
    'ENCODE_ALG': 'HS256',
    'DECODE_ALGS': ['HS256'],
    'HEADER_NAME': 'HTTP_AUTHORIZATION',
}

# ----------------------- DJANGO EMAIL SETTINGS -------------------------------

EMAIL_BACKEND: str = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL: Optional[str] = os.getenv('DEFAULT_FROM_EMAIL')
EMAIL_HOST: Optional[str] = os.getenv('EMAIL_HOST')
EMAIL_PORT: Optional[str] = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER: Optional[str] = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD: Optional[str] = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS: bool = False
EMAIL_USE_SSL: bool = False
EMAIL_USE_LOCALTIME: bool = False
EMAIL_TIMEOUT: None = None

# ------------------------ RABBITMQ SETTINGS -----------------------------------

RABBITMQ: dict = {
    'PROTOCOL': 'amqp',
    'HOST': os.getenv('RABBITMQ_HOST'),
    'PORT': os.getenv('AMQP_RABBITMQ_PORT'),
    'USER': os.getenv('RABBITMQ_DEFAULT_USER'),
    'PASS': os.getenv('RABBITMQ_DEFAULT_PASS'),
}

# ------------------------- REDIS SETTINGS -------------------------------------

REDIS: dict = {
    'PROTOCOL': 'redis',
    'HOST': os.getenv('REDIS_HOST'),
    'PORT': os.getenv('REDIS_PORT'),
    'PASSWORD': os.getenv('REDIS_PASS'),
    'DB_NUMBER': os.getenv('REDIS_DB_NUMBER'),
}

# ------------------------- CELERY SETTINGS ------------------------------------

CELERY_ENABLE_UTC: bool = True
CELERY_TIMEZONE: str = 'Europe/Minsk'

CELERY_BROKER_URL: str = (
    f"{RABBITMQ['PROTOCOL']}://{RABBITMQ['USER']}:"
    f"{RABBITMQ['PASS']}@{RABBITMQ['HOST']}:{RABBITMQ['PORT']}"
)

CELERY_BROKER_TRANSPORT_OPTIONS: dict = {'visibility_timeout': 3600}
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP: bool = True
CELERY_BROKER_CONNECTION_MAX_RETRIES: int = 200
CELERY_BROKER_USE_SSL: bool = False

CELERY_RESULT_BACKEND: str = (
    f"{REDIS['PROTOCOL']}://:{REDIS['PASSWORD']}@"
    f"{REDIS['HOST']}:{REDIS['PORT']}/{REDIS['DB_NUMBER']}"
)

CELERY_RESULT_BACKEND_TRANSPORT_OPTIONS: dict = {'visibility_timeout': 3600}
CELERY_RESULT_CACHE_MAX: bool = False
CELERY_REDIS_BACKEND_HEALTH_CHECK_INTERVAL: None = None
CELERY_REDIS_BACKEND_USE_SSL: bool = False

CELERY_BEAT_SCHEDULE: dict = {}

# -------------------------- OTHER SETTINGS ------------------------------------

WSGI_APPLICATION: str = 'car_salon_activities.wsgi.application'

DEFAULT_AUTO_FIELD: str = 'django.db.models.BigAutoField'
