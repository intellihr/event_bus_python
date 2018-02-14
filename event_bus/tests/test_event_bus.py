import jwt
import datetime
import uuid

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
        assert_jwt_token(adapter.last_request.headers)


@pytest.mark.freeze_time('2018-02-14')
def test_emit(snapshot):
    with requests_mock.mock() as m:
        adapter = m.post(
            'http://test_event_bus.local/event-bus/events/emit', {})

        user_id = uuid.UUID('edef2965-0ffe-445b-9e45-f7ff11f389a6')
        shard_id = uuid.UUID('d458a514-85c6-42fb-99f3-bc9bf3a1fb78')
        event_bus.emit('test_event',
                       tenant='test_tenant',
                       user_id=user_id,
                       timestamp=datetime.datetime(2018, 1, 3),
                       data=dict(a=0, c=3),
                       meta=dict(shard_id=shard_id), a=1, b=2)

        snapshot.assert_match(adapter.last_request.json())
        assert_jwt_token(adapter.last_request.headers)


@pytest.mark.freeze_time('2018-02-14')
def test_complex_emit(snapshot):
    with requests_mock.mock() as m:
        adapter = m.post(
            'http://test_event_bus.local/event-bus/events/emit', {})

        user_id = uuid.UUID('edef2965-0ffe-445b-9e45-f7ff11f389a6')
        shard_id = uuid.UUID('d458a514-85c6-42fb-99f3-bc9bf3a1fb78')
        event_bus.emit('test_event',
                       tenant='test_tenant',
                       user_id=user_id,
                       timestamp=datetime.datetime(2018, 1, 3),
                       data=dict(a=0, c=3, d=dict(
                           time=datetime.datetime.now())),
                       meta=dict(shard_id=shard_id),
                       a=1, b=2,
                       e=[1, datetime.datetime.now(), 'test'])

        snapshot.assert_match(adapter.last_request.json())
        assert_jwt_token(adapter.last_request.headers)


def test_emit_without_event():
    with pytest.raises(AssertionError):
        event_bus.emit(None, tenant='test_tenant',
                       timestamp=datetime.datetime(2018, 1, 3),
                       data=dict(a=0, c=3), a=1, b=2)


def test_emit_with_service_error():
    with requests_mock.mock() as m:
        m.post('http://test_event_bus.local/event-bus/events/emit',
               status_code=500, json=dict(msg='service error'))
        with pytest.raises(event_bus.request.APIError):
            event_bus.emit('test_event', tenant='test_tenant',
                           timestamp=datetime.datetime(2018, 1, 3),
                           data=dict(a=0, c=3), a=1, b=2)


def test_subscribe(snapshot):
    with requests_mock.mock() as m:
        adapter = m.post(
            'http://test_event_bus.local/event-bus/events/subscribers', {})

        event_bus.subscribe('https://my-test-service.local/hook',
                            'test_event_1', 'test_event_2')

        snapshot.assert_match(adapter.last_request.json())
        assert_jwt_token(adapter.last_request.headers)


def test_unsubscribe(snapshot):
    with requests_mock.mock() as m:
        adapter = m.post(
            'http://test_event_bus.local/event-bus/events/subscribers/delete',
            {})

        event_bus.unsubscribe('test_event_1', 'test_event_2')

        snapshot.assert_match(adapter.last_request.json())
        assert_jwt_token(adapter.last_request.headers)


def assert_jwt_token(headers):
    token = headers['Authorization'].replace('Bearer ', '')
    decoded = jwt.decode(token, event_bus.jwt_secret, algorithms=['HS256'])

    assert decoded['iss'] == event_bus.service
    assert decoded['exp'] > 0
