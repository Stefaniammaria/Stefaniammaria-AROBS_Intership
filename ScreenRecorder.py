import time
import threading
import os
import wave
import pyaudio
import pyautogui
import cv2
import numpy as np
import pyscreeze
from trio import current_time

resolution = (1920, 1080)
codec = cv2.VideoWriter_fourcc(*'XVID')
filename = "Recording.avi"
fps = 20.0


class ScreenRecorder:
    def __init__(self):
        self.out = cv2.VideoWriter(filename, codec, fps, resolution)

    def start_recording(self, duration):
        thread = threading.Thread(target=self.record_for_duration, name='Video Recorder Thread', args=(duration,))
        thread.start()
        return thread

    def record_for_duration(self, duration):
        finish_time = time.time() + duration
        current_time = last_screenshot_time = time.time()
        print("starting screen recording")
        numberOfSS = 0
        while current_time <= finish_time:
            if current_time - last_screenshot_time > (1.0 / fps):
                last_screenshot_time = current_time
                img = pyautogui.screenshot()
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.out.write(frame)
                numberOfSS += 1
            current_time = time.time()
        self.out.release()
        print("done screen recording" + str(numberOfSS))