import os
from googlesearch import *
from matplotlib.pyplot import text
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
import glob
import os
import shutil
import PyPDF2

# gebruiken voor het ophalen van de sector
from bs4 import BeautifulSoup
import requests as req

# ################# #
# Global variables #
# ################ #

url = 'https://consult.cbso.nbb.be/'

def findCompanyNr():
  file = 'CSV/all.csv'
  df = pd.read_csv(file)
  ls = df['Ondernemingsnummer'].tolist()
  return ls


def download_pdf(companyNr):
  delay = 10

  data = [None]

  # br = webdriver.Chrome(service = Service(ChromeDriverManager().install()))
  br = webdriver.Chrome(executable_path='./chromedriver.exe')
  br.get(url)

  try:
    
    WebDriverWait(br, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ui-tabpanel-0"]/app-search-by-enterprise-number/div/div[1]/div/input'))) # To make sure the page is loaded before going further

    ondNrTextBox = '//*[@id="ui-tabpanel-0"]/app-search-by-enterprise-number/div/div[1]/div/input'
    ondNrButton = '/html/body/app-root/div/main/div/app-deposit-search/div/p-tabview/div/div/p-tabpanel[1]/div/app-search-by-enterprise-number/div/div[2]/button'

    br.find_element_by_xpath(ondNrTextBox).send_keys(companyNr)
    br.find_element_by_xpath(ondNrButton).click()

    xpathDeelTwee = '/html/body/app-root/div/main/div/app-search-result/div/div[2]/app-deposit-list/div/div[3]/app-deposit-item[1]'
    xpathPDFDownload = '/html/body/app-root/div/main/div/app-search-result/div/div[2]/app-deposit-list/div/div[3]/app-deposit-item[1]/div/div[5]/app-download-deposit-pdf-button'


    WebDriverWait(br, delay).until(EC.presence_of_element_located((By.XPATH, xpathDeelTwee)))

    br.find_element_by_xpath(xpathPDFDownload).click()

    time.sleep(5)

  except Exception as e:
    print(e)
    print('Failed...')

  finally:
    br.quit()

nummers = findCompanyNr()
teller = 0

print(len(nummers))

for nr in nummers:
  if teller > 0 and teller < 5000:
    scrapeteInfo = download_pdf(nr.replace(" ", ""))
    time.sleep(1) # Om zeker te zijn dat de file gedownload is alvorens we ze gaan verplaatsen, anders verplaatsen we een verkeerde.

    print(f'{nr} bekeken')

    #move_file()
    #delete_file() # Uncomment dit om ruimte te besparen op je HDD, maar zorg dat je eerst scrapet.
    print(teller)
  
  teller += 1
