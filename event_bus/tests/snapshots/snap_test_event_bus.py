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
