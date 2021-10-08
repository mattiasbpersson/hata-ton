import wave

import pyaudio
from playsound import playsound

from Client import Client, QualityOfService
from EventHandler import EventHandler
from Wav import Wav

def playWav(client, event: Wav):
    RATE = 44100
    CHUNK = 512

    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=RATE,
                    input_device_index=3,
                    output=True)

    stream.write(b''.join(event.wav_blob))
    #data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()

    p.terminate()

if __name__ == '__main__':
    eventHandler = EventHandler(Wav, playWav)
    client = Client("consumer", [eventHandler], quality_of_service=QualityOfService.DELIVER_AT_MOST_ONE)
    client.listen()

