# Event Bus Python Client

Intellihr event bus python client


## Purpose
Make event emitting and subscription simple


## Installation
`pip install git+git://github.com/intellihr/event_bus_python.git`


## Usage
The library is meant to be a singleton used throughout an application.


### Setup

```python
import event_bus

event_bus.host = 'http://test_event_bus.local'
event_bus.jwt_secret = 'test_secret'
event_bus.service = 'test_service'
```


### Emit Events

```python
# emit `test_event` with data {"a"=1} (timestamp default to current time)
event_bus.emit('test_event', a=1)

# emit `test_event` and override timestamp
event_bus.emit('test_event', timestamp=datetime.datetime.now())

# emit `test_event` with existing event body
event_data = {
  'a': 1
}

event_bus.emit('test_event', data=event_data)

# emit `test_event` with existing event body and meta
# the following shows the expected event:
#   {
#     "event": "test_event", "user_id": "uuid-123",
#     "timestamp": "2018-02-14T00:00:00+00:00",
#     "data": {
#       "a": 1, "b": 2
#     },
#     "meta": {"x": 1}
#   }
#
event_data = {
  'a': 1
}

event_bus.emit('test_event', user_id='uuid-123',
               data=event_data, meta=dict(x=1), b=2)
```


### Subscribe Events with Web Hook

```python
# subscribe `test_service` to 'test_event_1' and 'test_event_2' with
# target url `https://my-test-service.local/hook`
event_bus.subscribe('https://my-test-service.local/hook',
                    'test_event_1', 'test_event_2')
```

### Unsubscribe Events

```python
# unsubscribe `test_service` to 'test_event_1' and 'test_event_2'
event_bus.unsubscribe('https://my-test-service.local/hook',
                      'test_event_1', 'test_event_2')
```


## Test

```sh
docker-compose run --rm local make test
```
