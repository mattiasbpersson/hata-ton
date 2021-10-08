import uuid
from datetime import datetime
from typing import Union

EventField = Union[str, int, float, bytes]


class Event:
    topic = None

    def __init__(self, id=None, timestamp=None):
        if id:
            self.id = id
        else:
            self.id = str(uuid.uuid1())

        if timestamp:
            self.timestamp = timestamp
        else:
            self.timestamp = datetime.now().astimezone().isoformat()
