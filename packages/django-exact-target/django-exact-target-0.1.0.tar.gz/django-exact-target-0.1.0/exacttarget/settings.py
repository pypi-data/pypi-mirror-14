from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

def overridable(name, default=None, required=False):
    if required:
        if not hasattr(settings, name) or not getattr(settings, name):
            raise ImproperlyConfigured("%s must be defined in Django settings" % name)
    return getattr(settings, name, default)


EXACT_TARGET_CLIENT_ID = overridable('EXACT_TARGET_CLIENT_ID', required=True)
EXACT_TARGET_CLIENT_SECRET = overridable('EXACT_TARGET_CLIENT_SECRET', required=True)
