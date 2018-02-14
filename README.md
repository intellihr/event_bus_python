# Event Bus

Intellihr event bus python client


## Purpose
Make event emitting and subscription simple


## Installation
`pip install git+git://github.com/intellihr/event_bus_python.git`


## Usage
The library is meant to be a singleton used throughout an application.

```python
import event_bus

event_bus.host = 'http://test_event_bus.local'
event_bus.jwt_secret = 'test_secret'
event_bus.service = 'test_service'

# emit `test_event` with data {"a"=1} (timestamp default to current time)
event_bus.emit('test_event', a=1)

# emit `test_event` and override timestamp
event_bus.emit('test_event', timestamp=datetime.datetime.now())

# emit `test_event` with existing event body
event_data = {
  'a': 1
}

event_bus.emit('test_event', data=event_data)
```


## Test

```sh
docker-compose run --rm local make test
```
