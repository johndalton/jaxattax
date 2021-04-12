import os

import dj_database_url

from .base import *  # noqa: F401 F403
from .base import BASE_DIR, INSTALLED_APPS, WAGTAIL_SITE_NAME

DATABASES = {
    'default': dj_database_url.config(conn_max_age=600, ssl_require=True),
}


SECRET_KEY = os.environ['SECRET_KEY']


INSTALLED_APPS = [
    'scout_apm.django',
    *INSTALLED_APPS,
]


# Static file handling
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = BASE_DIR / 'staticfiles'
os.makedirs(STATIC_ROOT, exist_ok=True)


# Heroku makes up all sorts of names
ALLOWED_HOSTS = ['*']


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

# General AWS integration settings
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']


# Upload media files to s3
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_STORAGE_BUCKET_NAME = 'jaxewin-media'
AWS_S3_REGION_NAME = 'ap-southeast-2'
AWS_S3_FILE_OVERWRITE = False


# Redirect users to HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True


# Scout settings
SCOUT_MONITOR = True
SCOUT_NAME = WAGTAIL_SITE_NAME


# Email sending
EMAIL_BACKEND = 'django_amazon_ses.EmailBackend'
DEFAULT_FROM_EMAIL = os.environ['DEFAULT_FROM_EMAIL']
