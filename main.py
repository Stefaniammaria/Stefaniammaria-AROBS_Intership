from contextlib import nullcontext

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service #setarea path-ului
from selenium.webdriver.common.by import By #acces la cautare dupa proprietati
from selenium.webdriver.common.keys import Keys #ne da acces la taste precum ESC, Space, Enter etc
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Specifică calea către ChromeDriver
service = Service('C:\\Users\\marac\\AppData\\Local\\Programs\\Common\\chromedriver.exe')  # Asigură-te că această cale este corectă

# Inițializează driverul Chrome
driver = webdriver.Chrome(service=service)

# Deschide site-ul dorit (in cazul nostru YouTube)
driver.get("https://www.youtube.com")
print("Opening " + driver.title) #trebuie transformat in scrierea log-urilor in fisier
time.sleep(3) #timp pentru a accepta pop-up-ul de cookies pentru a nu crapa programul
#insert pop-up handle here

#Cautarea unui videoclip

#search_query = "name"-ul elementului cu care vrem sa lucram, il gasim dand click dreapta pe un element si inspect
#in cazul nostru bara de search a YouTube-ului

searchedItem = nullcontext

try:
    consentButton = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Accept all"]'))
    )

    searchedItem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "search_query"))
    )
except TimeoutException:
    driver.quit()

#searchedItem = driver.find_element(By.NAME, "search_query")
searchedItem.send_keys("Coldplay - Fix You") #trimitem textul pe care vrem sa il cautam pe YouTube
searchedItem.send_keys(Keys.RETURN) #actionam tasta Enter

time.sleep(2) #timp pentru a vedea rezultatele

link = driver.find_element(By.PARTIAL_LINK_TEXT, "Coldplay - Fix You (Official Video)") #cauta elementul care contine acest text

time.sleep(3) #timp pentru a gasi elementul

link.click() #click pe elementul gasit

#handle reclame din timpul videoclipului

time.sleep(5) #timp de asteptare inainte de inchiderea paginii pentru a putea vedea rezultatele

#driver.close() #inchide tab-ul
driver.quit() #inchide browser-ul