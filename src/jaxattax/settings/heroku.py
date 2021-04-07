import os

import django_heroku

from .base import *
from .base import INSTALLED_APPS, WAGTAIL_SITE_NAME

django_heroku.settings(locals())


INSTALLED_APPS = [
    'scout_apm.django',
    *INSTALLED_APPS,
]


# From: https://docs.djangoproject.com/en/3.1/topics/logging/
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}


# Upload media files to s3
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'jaxewin-media'
AWS_S3_REGION_NAME = 'ap-southeast-2'
AWS_S3_FILE_OVERWRITE = False


# Redirect users to HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True


# Scout settings
SCOUT_MONITOR = True
SCOUT_KEY = os.getenv('SCOUT_KEY')
SCOUT_NAME = WAGTAIL_SITE_NAME
