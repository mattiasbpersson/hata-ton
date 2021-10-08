import audioop
import tempfile
import wave

import pyaudio

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from playsound import playsound

from Client import Client, QualityOfService
from Wav import Wav


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def record_audio():
    _audio = pyaudio.PyAudio()
    # prepare recording stream
    RATE = 16000
    CHUNK = 1024

    # number of seconds to allow to establish threshold
    THRESHOLD_TIME = 1

    stream = _audio.open(format=pyaudio.paInt16,
                              channels=1,
                              rate=RATE,
                              input=True,
                              frames_per_buffer=CHUNK)




def passiveListen(PERSONA):
    _audio = pyaudio.PyAudio()
    """
    Listens for PERSONA in everyday sound. Times out after LISTEN_TIME, so
    needs to be restarted.
    """

    THRESHOLD_MULTIPLIER = 1.8
    RATE = 16000
    CHUNK = 1024

    # number of seconds to allow to establish threshold
    THRESHOLD_TIME = 1

    # number of seconds to listen before forcing restart
    LISTEN_TIME = 2

    # prepare recording stream
    stream = _audio.open(format=pyaudio.paInt16,
                              channels=1,
                              rate=RATE,
                              input=True,
                              frames_per_buffer=CHUNK)

    # stores the audio data
    frames = []

    # stores the lastN score values
    lastN = [i for i in range(30)]

    # calculate the long run average, and thereby the proper threshold
    for i in range(0, int(RATE / CHUNK * THRESHOLD_TIME)):
        data = stream.read(CHUNK)
        frames.append(data)

        # save this data point as a score
        lastN.pop(0)
        lastN.append(getScore(data))
        average = sum(lastN) / len(lastN)

    # this will be the benchmark to cause a disturbance over!
    THRESHOLD = average * THRESHOLD_MULTIPLIER

    # save some memory for sound data
    frames = []

    # flag raised when sound disturbance detected
    didDetect = False

    # start passively listening for disturbance above threshold
    for i in range(0, int(RATE / CHUNK * LISTEN_TIME)):

        data = stream.read(CHUNK)
        frames.append(data)
        score = getScore(data)

        if score > THRESHOLD:
            didDetect = True


    # no use continuing if no flag raised
    if not didDetect:
        print("No disturbance detected")
        stream.stop_stream()
        stream.close()
        return (None, None)
    else:
        print("Distubance detected")
    # cutoff any recording before this disturbance was detected
    #frames = frames[-20:]

    # otherwise, let's keep recording for few seconds and save the file
    DELAY_MULTIPLIER = 1
    for i in range(0, int(RATE / CHUNK * DELAY_MULTIPLIER)):
        data = stream.read(CHUNK)
        frames.append(data)

    # save the audio data
    stream.stop_stream()
    stream.close()

    client = Client("producer", quality_of_service=QualityOfService.DELIVER_AT_MOST_ONE)
    client.emit_event(Wav(frames), quality_of_service=QualityOfService.DELIVER_AT_MOST_ONE)


def getScore(data):
    rms = audioop.rms(data, 2)
    score = rms / 3
    return score
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    while True:
        passiveListen("NILS")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


