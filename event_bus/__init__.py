from event_bus.version import VERSION
from event_bus.client import Client

__version__ = VERSION

host = None
jwt_secret = None
service = None
debug = False
default_client = None


def emit(*args, **kwargs):
    _proxy('emit', *args, **kwargs)


def subscribe(*args, **kwargs):
    _proxy('subscribe', *args, **kwargs)


def unsubscribe(*args, **kwargs):
    _proxy('unsubscribe', *args, **kwargs)


def _proxy(method, *args, **kwargs):
    global default_client
    if not default_client:
        default_client = Client(
            service=service, host=host, jwt_secret=jwt_secret, debug=debug)

    fn = getattr(default_client, method)
    fn(*args, **kwargs)
