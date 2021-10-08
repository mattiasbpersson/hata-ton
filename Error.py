from Event import Event, EventField


class Error(Event):
    topic = 'ErrorEvents'

    def __init__(self, error_message: EventField, **kwargs):
        super().__init__(**kwargs)
        self.error_message = error_message
