"""
WSGI config for firstAnyLearn project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'firstAnyLearn.settings')
os.environ["DJANGO_SETTINGS_MODULE"] = "firstAnyLearn.settings"

sys.path.append('/home/ubuntu/project_django/firstAnyLearn')
sys.path.append('/home/ubuntu/project_django/firstAnyLearn/firstAnyLearn')

application = get_wsgi_application()
