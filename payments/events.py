from dataclasses import dataclass


@dataclass(frozen=True)
class Event:
    id: str
    type: str
    data: dict


class EventBus:
    """Records every event and passes it to each subscriber, in order."""

    def __init__(self):
        self._subscribers = []
        self.history = []

    def subscribe(self, handler):
        self._subscribers.append(handler)

    def publish(self, event_type, data):
        event = Event(f"evt_{len(self.history) + 1}", event_type, dict(data))
        self.history.append(event)
        for handler in self._subscribers:
            handler(event)
        return event
