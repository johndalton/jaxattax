"""
ASGI config for jaxattax project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    raise RuntimeError("Set DJANGO_SETTINGS_MODULE to start this app")

application = get_asgi_application()
