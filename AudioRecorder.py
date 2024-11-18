import audioop
import math
import time
import threading
import wave
import pyaudio

#setarile pentru inregistrarea audio
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 10
STEREO_MIXER_INDEX = 2

#clasa pentru audio recorder
class AudioRecorder:
    #constructorul clasei
    def __init__(self, filename):
        self.filename = filename
        self.p_audio = pyaudio.PyAudio()
        self.stream = self.p_audio.open(format=FORMAT,
                             channels=CHANNELS,
                             rate=RATE,
                             input=True,
                             input_device_index=STEREO_MIXER_INDEX,
                             frames_per_buffer=CHUNK)
        self.last_file_average_decibels = 0

    #functia ce creaza thread-ul ce va face handle la partea de inregistrare audio
    def start_recording(self, duration):
        thread = threading.Thread(target=self.record_for_duration, name='Audio Recorder Thread', args=(duration,))
        return thread

    #functia pentru inregistrarea audio pentru o durata anume de timp
    def record_for_duration(self, duration):
        average_rms = 0
        chunk_count = 0
        frames = []
        finishing_time = time.time() + duration #calculam timpul la care trebuie sa se termine inregistrarea
        print("starting audio recording")
        #cat timp timpul curent este mai mic decat timpul la care trebuie sa se opreasca din inregistrat
        while time.time() < finishing_time:
            data = self.stream.read(CHUNK)
            frames.append(data)
            # adunam la totalul rms-ului valoarea chunkului, pentru calcularea mediei
            average_rms += audioop.rms(data, 2)
            chunk_count += 1

        # calculam rms mediu
        average_rms /= chunk_count
        # convertim din rms in dB si salvam rezultatul in proprietatea "last_file_average_decibels" a obiectului
        self.last_file_average_decibels = 20 * math.log10(average_rms)

        #inchiderea stream-ului si scrierea in fisier a datelor
        self.stream.stop_stream()
        self.stream.close()
        self.p_audio.terminate()
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p_audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        print("done audio recording")