import logging
from datetime import datetime

from six import string_types

from event_bus.request import Requestor

JWT_EXP_DELTA_SECONDS = 300


class Client:
    log = logging.getLogger('event_bus')

    def __init__(self, service=None, host=None, jwt_secret=None, debug=False):
        _require('service', service, string_types)
        _require('host', host, string_types)
        _require('jwt_secret', jwt_secret, string_types)
        self.service = service
        self.debug = debug
        self.requestor = Requestor(
            host, jwt_secret, service, JWT_EXP_DELTA_SECONDS)

        if debug:
            self.log.setLogger(logging.DEBUG)

    def emit(self, event, tenant=None, user_id=None, timestamp=None, data=None,
             meta=None, **kwargs):
        _require('event', event, string_types)

        if data:
            data = data.copy()
            data.update(kwargs)
        else:
            data = kwargs

        msg = {
            'event': event,
            'service': self.service,
            'timestamp': timestamp or datetime.now(),
            'data': data
        }

        if tenant:
            msg['tenant'] = tenant
        if user_id:
            msg['user_id'] = user_id
        if meta and isinstance(meta, dict):
            msg['meta'] = meta

        self.requestor.post('event-bus/events/emit', msg)

    def subscribe(self, target_url, *events):
        _require('target_url', target_url, string_types)
        payload = [
            dict(event=_require('event', event, string_types),
                 service=self.service,
                 target_url=target_url) for event in events]

        if payload:
            self.requestor.post('event-bus/events/subscribers', payload)

        self.log.info('{0} subscriptions created for {1}'.format(
            len(payload), self.service))

    def unsubscribe(self, *events):
        payload = [
            dict(event=_require('event', event, string_types),
                 service=self.service) for event in events]

        if payload:
            self.requestor.post('event-bus/events/subscribers/delete', payload)

        self.log.info('{0} subscriptions deleted for {1}'.format(
            len(payload), self.service))


def _require(name, field, data_type):
    if not isinstance(field, data_type) or not field:
        msg = '{0} must have {1}, got: {2}'.format(name, data_type, field)
        raise AssertionError(msg)

    return field
