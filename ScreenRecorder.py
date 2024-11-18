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

#setarile videoclipului
resolution = (1920, 1080)
codec = cv2.VideoWriter_fourcc(*'mp4v')
fps = 20.0

#crearea clasei de screen record
class ScreenRecorder:
    #constructorul clasei care creaza un fisier/videoclipul
    def __init__(self, filename):
        self.out = cv2.VideoWriter(filename, codec, fps, resolution)

    #functia pentru crearea thread-ului ce va face handle la partea de recording
    def start_recording(self, duration):
        thread = threading.Thread(target=self.record_for_duration, name='Video Recorder Thread', args=(duration,))
        return thread

    #functia pentru inregistrarea videoclipului pentru o durata anume de timp
    def record_for_duration(self, duration): #parametrul duration reprezinta lungimea videocliului
        finish_time = time.time() + duration #timpul curent plus durata aleasa
        current_time = last_screenshot_time = time.time() #initializarea parametrilor
        print("starting screen recording")
        while current_time <= finish_time: #cat timp timpul curent este mai mic decat timpul la care trebuie sa se termine inregistrarea
            #daca diferenta de timp dintre timpul curent si ultimul screenshot este mai mare decat timpul calculat dintre doua screenshot-uri
            #se va face un nou screenshot
            if current_time - last_screenshot_time >= (1.0 / fps): #* 0.95: # pentru a face screenshotul putin mai devreme si a ii da o marja de eroare, scadem perioada cu 5%
                last_screenshot_time = current_time #se aloca timpul noului screenshot
                img = pyautogui.screenshot() #crearea screenshot-ului
                frame = np.array(img) #face imaginea un array
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #convertim din bgr in rgb
                self.out.write(frame) #scriem poza in fisierul/videoclipul creat in constructor
            current_time = time.time() #actualizam timpul curent
        self.out.release() #finalizarea videoclipului
        print("done screen recording")