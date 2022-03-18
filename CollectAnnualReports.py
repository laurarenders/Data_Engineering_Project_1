import os
from googlesearch import *
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import glob
import os
import shutil
import PyPDF2

# ################# #
# Global variables #
# ################ #

provincies = ['Oost-Vl', 'West-Vl', 'Antwerpen', 'Limburg',  'Vl-Brabant']
url = 'https://cri.nbb.be/bc9/web/catalog?execution=e1s1'

# ########## #
# Functions #
# ######### #

def xlsxToCSV():
    for prov in provincies:
        read_file = pd.read_excel (r'prioriteitenlijst.xlsx', sheet_name=prov)
        read_file.to_csv (r'{}.csv'.format(prov), index=None, header=True)

def findCompanyNr():
  for prov in provincies:
    file = prov + '.csv'
    df = pd.read_csv(file)
    ls = df['Ondernemingsnummer'].tolist()
    
  return ls

def download_pdf(companyNr):
  delay = 10

  # br = webdriver.Chrome(service = Service(ChromeDriverManager().install()))
  br = webdriver.Chrome(executable_path='./chromedriver.exe')
  br.get(url)

  try:
    WebDriverWait(br, delay).until(EC.presence_of_element_located((By.ID, "page_searchForm:j_id3:generated_number_2_component"))) # To make sure the page is loaded before going further

    input_field = br.find_element(By.ID, "page_searchForm:j_id3:generated_number_2_component")
    input_field.send_keys(companyNr)

    br.find_element(By.NAME, "page_searchForm:actions:0:button").click()
    
    xPath = '/html/body/div[2]/div[1]/div/div/div/div/div[1]/div/div/form/div[3]/div[2]/div/div/div[2]'
    xPath_download = '/html/body/div[2]/div[1]/div/div/div/div/div[1]/div/div/form/div[3]/div[2]/div/div/div[2]/table/tbody/tr[1]/td[7]/a'

    WebDriverWait(br, delay).until(EC.presence_of_element_located((By.XPATH, xPath)))

    myTable = br.find_element(By.XPATH, xPath)
    for row in myTable.find_elements(By.XPATH, ".//tr"):
      count = 0
      for cell in row.find_elements(By.TAG_NAME, 'td'):
        if count == 1:
          if '/2020' in cell.text:
            br.find_element(By.XPATH, xPath_download).click()
        count += 1

  except Exception as e:
    print(e)
    print('Failed...')

  finally:
    br.quit()

def move_file():
  try:
    list_of_files = glob.glob("..\..\..\..\..\Downloads\*.pdf")
    latest_file = max(list_of_files, key = os.path.getmtime)
    shutil.move(latest_file, "./annualReports")
  except shutil.Error as se:
    delete_file()
    move_file()

def delete_file():
  to_be_deleted = max(glob.glob(f"./annualReports/*"), key = os.path.getmtime)
  print(to_be_deleted)
  os.remove(to_be_deleted)

# Gevonden gegevens opslaan in een CSV-bestand. 
# Meegegeven -- ondernemingsnummer en array met daarin alle info 'gold'.
def saveAsFile(ondnr, gold):
    try: 
        # Opslaan onder /contents/
        path = "C:/DEPGroep1/jaarverslagen/"
        file = 'results.csv'
        
        with open(os.path.join(path,file), "a+") as file_object:
            # Move read cursor to the start of file.
            file_object.seek(0)

            # If file is not empty then append '\n'
            data = file_object.read(100)
            if len(data) > 0 :
                file_object.write("\n")

            arr = [str(ondnr), str(gold[0]), str(gold[1])]

            text = ";".join(arr)

            # Append text at the end of file
            file_object.write(text)
    except:
        # Niet gelukt om bestand op te slaan
        print(f'Niet gelukt om de uitslag aan het bestand toe te voegen.')
    
    # Pauze van drie seconden.
    time.sleep(3)


# Geeft een array met 
def scrape_jaarverslag():

    try:
      #list_of_files = glob.glob("..\..\..\..\..\Downloads\*.pdf") #og
      list_of_files = glob.glob("C:/Users/dylan/Downloads/*.pdf")
      latest_file = max(list_of_files, key = os.path.getmtime)
      read_pdf = PyPDF2.PdfFileReader(latest_file)

      # get number of pages
      NumPages = read_pdf.getNumPages()
    except:
      print('Failed..')

    # define keyterms
    # keytermsGenderGelijkheid = ["geslacht", "gendergelijkheid", "man/vrouw verhouding", "ratio man/vrouw", "salaris man/vrouw", "discriminatie", "genderneutraal"]

    data = [None]*2 # Array met twee plaatsen maken; kan uitgebreid worden

    # Tekst ophalen
    for i in range(0, NumPages):

        try:
          PageObj = read_pdf.getPage(i)
          Text = PageObj.extractText()
          Text.replace('\n', ' ')
        
        except:
          print(f'Failed reading page {i}')

        try:
          # Omzet ophalen
          if data[1] == None and i in [6,7,8] and 'Omzet' in Text:
            arr = Text.split('\n')
            index = arr.index('Omzet')
            omzet = arr[index + 3]
            data[1] = omzet
        except:
          print('Error: Omzet')

        # Aantal werknemers ophalen.
        try:  
          if data[0] == None and 'Aantal werknemers' in Text:
            arr = Text.split('\n')
            index = arr.index('Aantal werknemers')
            aantal = int(arr[index + 2]) + int(arr[index + 3])
            data[0] = aantal
        except:
          print('Error: Aantal werknemers')


        try:  
          if data[0] == None and i in [38,39,40] and 'Aantal werknemers' in Text:
            arr = Text.split('\n')
            index = arr.index('Aantal werknemers')
            aantal = int(arr[index + 2]) + int(arr[index + 3])
            data[0] = aantal
        except:
          print('Error: Aantal werknemers')
    
    return data

# ######################## #
# Start van het programma #
# ######################## #

#xlsxToCSV()

companyNumbers = findCompanyNr() # bedrijfsnummers ophalen

for nr in companyNumbers:
  download_pdf(nr.replace(" ", ""))
  time.sleep(3) # Om zeker te zijn dat de file gedownload is alvorens we ze gaan verplaatsen, anders verplaatsen we een verkeerde.
  data = scrape_jaarverslag() # Data van de scraper opslaan
  
  saveAsFile(nr, data) # Naar bestand schrijven.

  print(f'{nr} bekeken')
  time.sleep(3)
  
  #move_file()
  delete_file() # Uncomment dit om ruimte te besparen op je HDD, maar zorg dat je eerst scrapet.
