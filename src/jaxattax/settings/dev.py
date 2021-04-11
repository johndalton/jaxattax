from .base import *  # noqa: F401 F403
from .base import BASE_DIR

LOCAL_ROOT = BASE_DIR / "local"

ASSETS_ROOT = LOCAL_ROOT / "assets"
STATIC_ROOT = ASSETS_ROOT / "static"
MEDIA_ROOT = ASSETS_ROOT / "media"

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'database',
        'NAME': 'jaxattax',
        'USER': 'jaxattax',
        'PASSWORD': 'dev-password',
    }
}

SECRET_KEY = 'shhh not very secret'

ALLOWED_HOSTS = ['*']

EMAIL_HOST = 'mail'
DEFAULT_FROM_EMAIL = 'jaxattax@example.com'
