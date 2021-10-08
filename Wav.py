from Event import Event, EventField


class Wav(Event):
    topic = 'WavEvents'

    def __init__(self, wav_blob: EventField, **kwargs):
        super().__init__(**kwargs)
        self.wav_blob = wav_blob
