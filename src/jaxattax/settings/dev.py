from jaxattax.settings.base import *

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
