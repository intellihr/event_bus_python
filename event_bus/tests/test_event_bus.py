import requests_mock
import pytest

import event_bus

event_bus.host = 'http://test_event_bus.local'
event_bus.jwt_secret = 'test_secret'
event_bus.service = 'test_service'


@pytest.mark.freeze_time('2018-02-14')
def test_simple_emit(snapshot):
    with requests_mock.mock() as m:
        adapter = m.post(
            'http://test_event_bus.local/event-bus/events/emit', {})
        event_bus.emit('test_event', a=1)

        snapshot.assert_match(adapter.last_request.json())
