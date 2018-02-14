from datetime import datetime, date, timedelta
import json
import uuid
import logging

import requests
import jwt

from event_bus.utils import guess_timezone


class Requestor:
    log = logging.getLogger('event_bus')

    def __init__(self, host, jwt_secret, jwt_issuer, jwt_exp_delta_seconds):
        self.host = host
        self.jwt_secret = jwt_secret
        self.jwt_issuer = jwt_issuer
        self.jwt_exp_delta_seconds = jwt_exp_delta_seconds
        self.session = requests.sessions.Session()

    def post(self, path, body):
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer %s' % self._jwt_token()
        }
        data = json.dumps(body, cls=PayloadSerializer)
        res = self.session.post(self._url(path), data=data, headers=headers)

        try:
            res.raise_for_status()
        except requests.exceptions.HTTPError:
            self.log.debug('received response: %s', res.text)
            raise APIError(res.status_code, res.text)

        return res

    def _url(self, path):
        return '{0}/{1}'.format(self.host, path)

    def _jwt_token(self):
        exp = datetime.utcnow() + timedelta(seconds=self.jwt_exp_delta_seconds)

        return jwt.encode(
            {
                'iss': self.jwt_issuer,
                'exp': exp
            },
            self.jwt_secret,
            algorithm='HS256').decode()


class APIError(Exception):
    def __init__(self, status, message):
        self.message = message
        self.status = status

    def __str__(self):
        return '[event-bus] {0}: {1}'.format(self.status, self.message)


class PayloadSerializer(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return guess_timezone(obj).isoformat()
        if isinstance(obj, date):
            return obj.isoformat()
        if isinstance(obj, uuid.UUID):
            return str(obj)

        return json.JSONEncoder.default(self, obj)
