from django.conf import settings

def setting(suffix, default):
    return getattr(settings, 'DIRECTED_EDGE_%s' % suffix, default)

ENABLED = setting('ENABLED', True)
USERNAME = setting('USERNAME', None)
PASSWORD = setting('PASSWORD', None)
