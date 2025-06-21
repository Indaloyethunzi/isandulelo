"""
Settings module for Isandulelo.

Automatically loads the appropriate settings based on the DJANGO_SETTINGS_MODULE
environment variable or defaults to development settings.
"""
import os
from decouple import config

# Determine which settings to use
ENVIRONMENT = config('DJANGO_ENVIRONMENT', default='development')

if ENVIRONMENT == 'production':
    from .production import *
elif ENVIRONMENT == 'testing':
    from .testing import *
else:
    from .development import *