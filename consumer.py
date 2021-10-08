import wave

import pyaudio

from Client import Client, QualityOfService
from EventHandler import EventHandler
from Wav import Wav

def playWav(client, event: Wav):
    CHUNK = 512
    RATE = 44100
    with open('test.wav', 'w+b') as f:

        wav_fp = wave.open(f, 'wb')
        wav_fp.setnchannels(1)
        wav_fp.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
        wav_fp.setframerate(RATE*1.3)
        wav_fp.writeframes(b''.join(event.wav_blob))
        wav_fp.close()
    
    wf = wave.open('test.wav', 'rb')
    p = pyaudio.PyAudio()

    # open stream (2)
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # read data
    data = wf.readframes(CHUNK)

    # play stream (3)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)

    # stop stream (4)
    stream.stop_stream()
    stream.close()

    # close PyAudio (5)
    p.terminate()

if __name__ == '__main__':
    eventHandler = EventHandler(Wav, playWav)
    client = Client("consumer", [eventHandler], quality_of_service=QualityOfService.DELIVER_AT_MOST_ONE)
    client.listen()

