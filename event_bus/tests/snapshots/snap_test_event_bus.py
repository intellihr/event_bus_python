# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_simple_emit 1'] = {
    'data': {
        'a': 1
    },
    'event': 'test_event',
    'service': 'test_service',
    'timestamp': '2018-02-14T00:00:00+00:00'
}

snapshots['test_emit 1'] = {
    'data': {
        'a': 1,
        'b': 2,
        'c': 3
    },
    'event': 'test_event',
    'meta': {
        'shard_id': 'd458a514-85c6-42fb-99f3-bc9bf3a1fb78'
    },
    'service': 'test_service',
    'tenant': 'test_tenant',
    'timestamp': '2018-01-03T00:00:00+00:00',
    'user_id': 'edef2965-0ffe-445b-9e45-f7ff11f389a6'
}

snapshots['test_subscribe 1'] = [
    {
        'event': 'test_event_1',
        'service': 'test_service',
        'target_url': 'https://my-test-service.local/hook'
    },
    {
        'event': 'test_event_2',
        'service': 'test_service',
        'target_url': 'https://my-test-service.local/hook'
    }
]

snapshots['test_unsubscribe 1'] = [
    {
        'event': 'test_event_1',
        'service': 'test_service'
    },
    {
        'event': 'test_event_2',
        'service': 'test_service'
    }
]

snapshots['test_complex_emit 1'] = {
    'data': {
        'a': 1,
        'b': 2,
        'c': 3,
        'd': {
            'time': '2018-02-14T00:00:00+00:00'
        },
        'e': [
            1,
            '2018-02-14T00:00:00+00:00',
            'test'
        ]
    },
    'event': 'test_event',
    'meta': {
        'shard_id': 'd458a514-85c6-42fb-99f3-bc9bf3a1fb78'
    },
    'service': 'test_service',
    'tenant': 'test_tenant',
    'timestamp': '2018-01-03T00:00:00+00:00',
    'user_id': 'edef2965-0ffe-445b-9e45-f7ff11f389a6'
}
