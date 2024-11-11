from contextlib import nullcontext

import pyaudio
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service #setarea path-ului
from selenium.webdriver.common.by import By #acces la cautare dupa proprietati
from selenium.webdriver.common.keys import Keys #ne da acces la taste precum ESC, Space, Enter etc
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import wave

from AudioRecorder import AudioRecorder
from ScreenRecorder import ScreenRecorder

# Specifică calea către ChromeDriver
service = Service('C:\\Users\\marac\\AppData\\Local\\Programs\\Common\\chromedriver.exe')

# Inițializează driverul Chrome
driver = webdriver.Chrome(service=service)

# Deschide site-ul dorit (in cazul nostru YouTube)
driver.get("https://www.youtube.com")
print("Opening " + driver.title) #trebuie transformat in scrierea log-urilor in fisier

try:
    try:
        #cautarea butonului de "Accept All" folosind XPATH
        consentButton = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'Accept all')]]"))
        )
        consentButton.click()  # acceptam cookie-urile YouTube-ului
    except TimeoutException:
        print("Timed out waiting for consent button. Maybe there is no consent required...")

    time.sleep(2)  # timp pentru a inchide modalul de consent
    # search_query = "name"-ul elementului cu care vrem sa lucram, il gasim dand click dreapta pe un element si inspect
    # in cazul nostru bara de search a YouTube-ului
    searchedItem = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.NAME, "search_query"))
    )

    # Cautarea unui videoclip
    searchedItem.send_keys("Coldplay - Fix You")  # trimitem textul pe care vrem sa il cautam pe YouTube
    searchedItem.send_keys(Keys.RETURN)  # actionam tasta Enter
    link = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Coldplay - Fix You (Official Video)"))
    )
    link.click()  # click pe elementul gasit

    youtube_video = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@aria-keyshortcuts='f']"))
    )
    youtube_video.click()  # click pe elementul gasit

    audio_recorder = AudioRecorder()
    audio_recorder_thread = audio_recorder.start_recording(10)
    video_recorder = ScreenRecorder()
    video_recorder_thread = video_recorder.start_recording(10)

    audio_recorder_thread.join()
    video_recorder_thread.join()

    time.sleep(5000)  # timp de asteptare inainte de inchiderea paginii pentru a putea vedea rezultatele
except TimeoutException:
    driver.quit()

#driver.close() #inchide tab-ul
driver.quit() #inchide browser-ul