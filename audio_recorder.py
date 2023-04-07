import pyaudio
import math
import struct
import wave
import time
import os

Threshold = 10

SHORT_NORMALIZE = (1.0 / 32768.0)
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
width = 2

should_listen = True

TIMEOUT_LENGTH = 1

f_name_directory = os.getcwd()


class Recorder:

    @staticmethod
    def rms(frame):
        count = len(frame) / width
        file_format = "%dh" % count
        shorts = struct.unpack(file_format, frame)

        sum_squares = 0.0
        for sample in shorts:
            n = sample * SHORT_NORMALIZE
            sum_squares += n * n
        rms = math.pow(sum_squares / count, 0.5)

        return rms * 1000

    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  output=True,
                                  frames_per_buffer=chunk)

    def record(self):
        print('Noise detected, recording beginning')
        rec = []
        current = time.time()
        end = time.time() + TIMEOUT_LENGTH

        while current <= end:

            data = self.stream.read(chunk)
            if self.rms(data) >= Threshold: end = time.time() + TIMEOUT_LENGTH

            current = time.time()
            rec.append(data)
        self.write(b''.join(rec))

    def write(self, recording):
        filename = "recording_output.wav"

        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(recording)
        wf.close()
        print('Written to file: {}'.format(filename))
        global should_listen
        should_listen = False

    def listen(self):
        print("Listening...")
        while should_listen:
            audio_input = self.stream.read(chunk)
            rms_val = self.rms(audio_input)
            if rms_val > Threshold:
                self.record()


def start():
    a = Recorder()
    global should_listen
    should_listen = True
    a.listen()
