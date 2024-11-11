import time
import threading
import os
import wave
import pyaudio

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "audioOut.wav"
STEREO_MIXER_INDEX = 2


class AudioRecorder:
    def __init__(self):
        self.p_audio = pyaudio.PyAudio()
        self.stream = self.p_audio.open(format=FORMAT,
                             channels=CHANNELS,
                             rate=RATE,
                             input=True,
                             input_device_index=STEREO_MIXER_INDEX,
                             frames_per_buffer=CHUNK)

    def start_recording(self, duration):
        thread = threading.Thread(target=self.record_for_duration, name='Audio Recorder Thread', args=(duration,))
        thread.start()
        return thread

    def record_for_duration(self, duration):
        frames = []
        starting_time = time.time()
        print("starting audio recording")
        while time.time() < starting_time + duration:
            data = self.stream.read(CHUNK)
            frames.append(data)

        self.stream.stop_stream()
        self.stream.close()
        self.p_audio.terminate()
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p_audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        print("done audio recording")