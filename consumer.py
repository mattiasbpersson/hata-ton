import wave

import pyaudio
from playsound import playsound

from Client import Client, QualityOfService
from EventHandler import EventHandler
from Wav import Wav

def playWav(client, event: Wav):
    RATE = 16000
    with open('test.wav', 'w+b') as f:

        wav_fp = wave.open(f, 'wb')
        wav_fp.setnchannels(1)
        wav_fp.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
        wav_fp.setframerate(RATE*1.3)
        wav_fp.writeframes(b''.join(event.wav_blob))
        wav_fp.close()


    playsound('test.wav')

if __name__ == '__main__':
    eventHandler = EventHandler(Wav, playWav)
    client = Client("consumer", [eventHandler], quality_of_service=QualityOfService.DELIVER_AT_MOST_ONE)
    client.listen()

