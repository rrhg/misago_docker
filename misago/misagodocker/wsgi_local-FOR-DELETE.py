"""
WSGI config for misagodocker project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application


# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "misagodocker.settings_local")

application = get_wsgi_application()

print('*****  test for logs: . Printed from misago/misagodocker/wsgi_local.py ***************')