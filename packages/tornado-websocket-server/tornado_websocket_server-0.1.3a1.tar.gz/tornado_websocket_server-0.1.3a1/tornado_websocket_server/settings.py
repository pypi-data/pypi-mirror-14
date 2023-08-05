import sys

WEBSOCKET_SERVER_PORT = 9000
WEBSOCKET_SERVER_ADDR = "http://localhost"

REDIS_SERVER = "localhost"
REDIS_SERVER_PORT = "6379"

try:
    from django.conf import settings as django_settings
    settings = sys.modules[__name__]
    defaults = [item for item in dir(settings) if not item.startswith("__")]
    for item in defaults:
        try:
            django_value = getattr(django_settings, item)
            if django_value is not None:
                setattr(settings, item, django_value)
        except AttributeError:
            pass

except Exception:
    pass