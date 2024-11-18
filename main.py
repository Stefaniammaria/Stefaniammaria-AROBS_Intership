from selenium import webdriver
from selenium.common import TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service #setarea path-ului
from selenium.webdriver.common.by import By #acces la cautare dupa proprietati
from selenium.webdriver.common.keys import Keys #ne da acces la taste precum ESC, Space, Enter etc
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from AudioRecorder import AudioRecorder
from Logger import Logger
from ScreenRecorder import ScreenRecorder
from VideoAudioMerger import VideoAudioMerger

RECORDING_LENGTH = 120

logger = Logger()

# Specifică calea către ChromeDriver
service = Service('C:\\Users\\marac\\AppData\\Local\\Programs\\Common\\chromedriver.exe')
logger.log_message("Specified the path to the Chrome driver.")

# Inițializează driverul Chrome
driver = webdriver.Chrome(service=service)
logger.log_message("Initialized the Chrome driver.")

try:
    # Deschide site-ul dorit (in cazul nostru YouTube)
    # Verificam daca site-ul se deschide
    driver.get("https://www.youtube.com")
    logger.log_message("Opening " + driver.title + ".")

    try:
        #cautarea butonului de "Accept All" folosind XPATH
        logger.log_message("Searching for the \"Accept All\" button to accept and close the cookies pop-up.")
        consentButton = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'Accept all')]]"))
        )
        consentButton.click()  # acceptam cookie-urile YouTube-ului
        logger.log_message("Accepted the cookies from YouTube, the pop-up is closing.")
    except TimeoutException:
        logger.log_message("Timed out waiting for consent button. Maybe there is no consent required...")

    #cautam un element ce exista mereu pe pagina de YouTube indiferent de unde navighezi in aplicatie pentru a vedea daca s-a incarcat pagina
    #cautam bara de sus a aplicatiei ce contine logo-ul de la Youtube, bara de search, butonul de profil si multe altele
    consentButton = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "masthead"))
    )

    time.sleep(2)  # timp pentru a inchide modalul de consent
    # search_query = "name"-ul elementului cu care vrem sa lucram, il gasim dand click dreapta pe un element si inspect
    # in cazul nostru bara de search a YouTube-ului
    logger.log_message("Searching for the search bar of Youtube.")
    searchedItem = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.NAME, "search_query"))
    )

    logger.log_message("The search bar was found, now tipping the name of the desired video.")
    # Cautarea unui videoclip
    searchedItem.send_keys("Coldplay - Fix You")  # trimitem textul pe care vrem sa il cautam pe YouTube
    searchedItem.send_keys(Keys.RETURN)  # actionam tasta Enter
    logger.log_message("Pressing search, finding results...")
    link = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Coldplay - Fix You (Official Video)"))
    )
    link.click()  # click pe elementul gasit
    logger.log_message("Results found, clicking on the desired video.")

    # cautarea butonului pentru a face videoclipul fullscreen
    # youtube_video = WebDriverWait(driver, 30).until(
    #     EC.element_to_be_clickable((By.XPATH, "//button[@aria-keyshortcuts='f']"))
    # )
    # youtube_video.click()  # click pe elementul gasit

    #cream instante ale claselor si pornim thread-urile
    audio_recorder = AudioRecorder("temp_audio.wav")
    audio_recorder_thread = audio_recorder.start_recording(RECORDING_LENGTH)
    logger.log_message("Created the audio recorder instance and thread.")
    video_recorder = ScreenRecorder("temp_video.mp4")
    video_recorder_thread = video_recorder.start_recording(RECORDING_LENGTH)
    logger.log_message("Created the video recorder instance and thread.")

    audio_recorder_thread.start()
    logger.log_message("Strated the audio recorder thread.")
    time.sleep(1.5) #timp pentru sincronizarea video-audio
    video_recorder_thread.start()
    logger.log_message("Started the video recorder thread.")

    try:
        logger.log_message("Waiting to see if the add is skippable or not.")
        # cautarea butonului de "Skip" folosind XPATH
        skipButton = WebDriverWait(driver, RECORDING_LENGTH).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//div[contains(text(), 'Skip')]]"))
        )
        skipButton.click()  # apasa butonul de skip la reclama
        logger.log_message("Button found, skipping video.")
    except TimeoutException:
        logger.log_message("Timed out waiting for skip button. Maybe there is no skip required...")

    #avem nevoie de join pentru a opri executia codului in acest punct pana la terminarea thread-urilor de recording
    audio_recorder_thread.join()
    video_recorder_thread.join()
    logger.log_message("Waiting for the audio and video recorder threads to finish.")

    logger.log_message("Calculating the avarage number of dB. The average number of dB is: " + str(audio_recorder.last_file_average_decibels))
    logger.log_message("Quiting YouTube, closing the window.")
    driver.quit()

    logger.log_message("Merging the audio and video recorders...")
    av_merger = VideoAudioMerger("temp_video.mp4", "temp_audio.wav")
    av_merger.merge_video_with_audio("result.mp4")
    logger.log_message("The audio and video merger was completed, the file is found in the project's folder.")
    av_merger.remove_original_source_files()
    logger.log_message("Removing the original source files used in the merger.")
    logger.close_file()

except TimeoutException:
    driver.quit()
    logger.log_message("An exception occurred, quiting the window.")
except WebDriverException:
    logger.log_message("The page didn't load, maybe there's no internet connection...")
    driver.quit()
    exit()