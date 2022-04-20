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

provincies = ['Oost-Vl', 'West-Vl', 'Antwerpen', 'Limburg',  'Vl-Brabant']
url = 'https://cri.nbb.be/bc9/web/catalog?execution=e1s1'


# termen en sleutelwoorden
gendergelijkheid = ["geslacht", "gendergelijkheid", "man/vrouw verhouding",
                    "ratio man/vrouw", "salaris man/vrouw", "discriminatie", "genderneutraal"]
implementatie_werknemersrechten = ["duurzaamheidscommissie", "rechten van werknemers", "arbeisrechten",
                                   "rechten en plichten van werknemers", "arbeidsomstandigheden", "algemene rechten en plichten", "mensenrechten", "recht op vrijheid"]
sociale_relaties = ["sociale relaties", "werkvloer",
                    "solidair gedrag",  "betrokkenheid van werknemers"]
werkgelegenheid = ["rekrutering", "rekruteringsbeleid", "rekruteringsverloop", "rekruteringstijd", "arbeidsovereenkomst", "werknemer", "werknemers", "diversiteitsbeleid", "loopbaan", "carrière",
                   "carrièreontwikkeling", "groei opportuniteiten", "groeikansen", "doorstroommogelijkheden", "promotie", "demografisch", "personeelsbestand", "promotie", "human resources", "HR", "personeelsbeleid"]
organisatie_op_het_werk = ["vergoeding", "beloning", "bonus", "stabiliteit van werknemers", "stabiliteit", "bedrijfscultuur", "loyaliteit van werknemers", "personeelsbehoud", "retentie personeel", "loyaliteitsbonus",
                           "personeelsverloop", "leeftijdsstructuur", "afwezigheid", "afwezigheidsratio", "tevredenheid op het werk", "opvolgingsbeheer", "prestatiebeleid", "prestatie", "ziekte", "verzuim", "aanwezigheid", "aanwezigheidsratio"]
gezondheid_en_veiligheid = ["preventie", "pesterij", "ongewenst gedrag", "klacht", "gezondheid van werknemers", "welzijn van werknemers", "managers", "arbeiders",
                            "bedienden", "medewerkers", "incidenten op het werk", "incidenten", "discriminatie", "gezondheid en veiligheid op het werk", "intimidatie", "intimiderend gedrag", "vakbond"]
opleidingsbeleid = ["opleidingsbeleid", "training", "opleiding", "vaardigheden van werknemers", "kennis van werknemers",
                    "werknemersvaardigheden", "competenties van werknemer", "werknemercompetenties", "talent", "vakbekwaamheid"]
SDg = ["kinderarbeid", "goede gezondheid en welzijn", "gender-gelijkheid", "waardig werk en economische groei",
       "ongelijkheid verminderen", "vrede", "veiligheid en sterke publieke diensten"]

gebruik_van_energiebronnen = ["energiebron", "energie vermindering",
                              "energie reductie", "energie-intensiteit", "energiegebruik", "energieverbruik"]
gebruik_van_waterbronnen = ["waterverbruik", "waterbron", "wateronttrekking",
                            "waterafvoer", "watergebruik", "afvalwater", "grondwater"]
emissies_van_broeikasgassen = ["broeikasgas", "CO2", "CO²", "CO2"]
vervuilende_uitstoot = ["emissie", "uitstoot", "vervuiling", "zure regen", "uitstoot", "fijnstof",
                        "fijn stof", "vervuilende stof", "filtertechniek", "luchtzuiverheid", "zuiveringstechnologie"]
milieu_impact = ["impact", "milieu-impact", "impact op het milieu", "milieu impact", "milieu", "mobiliteit", "vervoer", "verplaatsing", "fiets",
                 "auto", "staanplaatsen", "parking", "openbaar vervoer", "klimaatimpact", "impact op het klimaat", "klimaatsverandering", "green deal"]
impact_op_gezondheid_en_veiligheid = [
    "gezondheid", "reclyclage", "recycleren", "biodiversiteit", "afval", "afvalproductie", "vervuiling"]
verdere_eisen_over_bepaalde_onderwerpen = [
    "klimaat", "klimaatsverandering", "klimaatopwarming", "opwarming", "scope"]
milieu_beleid = ["milieubeleid", "hernieuwbare energie", "verspilling",
                 "milieucriteria", "planeet", "klimaatsbeleid", "milieunormen"]
SDGs = ["schoon water en sanitair", "betaalbare en duurzame energie", "duurzame steden en gemeenschappen",
        "verantwoorde consumptie en productie", "klimaatactie", "leven in het water", "leven op het land"]

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

  data = [None]

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

    cels = br.find_elements_by_xpath('//td')

    arr = []

    for cel in cels:
      arr.append(cel.text)
    
    data[0] = arr[25].split('-')[1].strip()
    
    return data

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
  try:
    list_of_files = glob.glob("C://Users/Dylan/Downloads/*")
    latest_file = max(list_of_files, key = os.path.getmtime)
    os.remove(latest_file)
  except:
    print('Niet gelukt om bestand te verwijderen.')
  
# Gevonden gegevens opslaan in een CSV-bestand. 
# Meegegeven -- ondernemingsnummer en array met daarin alle info 'gold'.
def saveAsFile(ondnr, dataPDF, goldNBB):
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
                
            # null-waarden vermijden
            if dataPDF[1] == 'None':
              dataPDF[1] == 0

            if dataPDF[2] == 'None':
              dataPDF[2] == 0

            if dataPDF[3] == 'None':
              dataPDF[3] == 0

            arr = [str(ondnr).replace(' ', ''), str(dataPDF[0]), str(dataPDF[1]).replace('.',''), str(dataPDF[2]).replace('.',''), str(dataPDF[3]), str(dataPDF[4]), str(goldNBB[0]).replace(';', ',')]

            text = ";".join(arr)

            # Append text at the end of file
            file_object.write(text)
    except:
        # Niet gelukt om bestand op te slaan
        print(f'Niet gelukt om de uitslag aan het bestand toe te voegen.')
    # Pauze van drie seconden.
    time.sleep(3)

def countKeywordOccurrences(textArr):
    textArr = textArr.split(' ')

    data = [0]*17

    for keyword in gendergelijkheid:
        data[0] += textArr.count(keyword)

    for keyword in implementatie_werknemersrechten:
        data[1] += textArr.count(keyword)

    for keyword in sociale_relaties:
        data[2] += textArr.count(keyword)

    for keyword in werkgelegenheid:
        data[3] += textArr.count(keyword)

    for keyword in organisatie_op_het_werk:
        data[4] += textArr.count(keyword)

    for keyword in gezondheid_en_veiligheid:
        data[5] += textArr.count(keyword)

    for keyword in opleidingsbeleid:
        data[6] += textArr.count(keyword)

    for keyword in SDg:
        data[7] += textArr.count(keyword)

    for keyword in gebruik_van_energiebronnen:
        data[8] += textArr.count(keyword)

    for keyword in gebruik_van_waterbronnen:
        data[9] += textArr.count(keyword)

    for keyword in emissies_van_broeikasgassen:
        data[10] += textArr.count(keyword)

    for keyword in vervuilende_uitstoot:
        data[11] += textArr.count(keyword)
    
    for keyword in milieu_impact:
        data[12] += textArr.count(keyword)

    for keyword in impact_op_gezondheid_en_veiligheid:
        data[13] += textArr.count(keyword)

    for keyword in verdere_eisen_over_bepaalde_onderwerpen:
        data[14] += textArr.count(keyword)
    
    for keyword in milieu_beleid:
        data[15] += textArr.count(keyword)

    for keyword in SDGs:
        data[16] += textArr.count(keyword)

    return data

def saveOccurrencesKeywords(ondnr, occData):
  try: 
        # Opslaan onder /contents/
        path = "C:/DEPGroep1/scores/"
        file = 'voorkomensPDF.csv'

        
        with open(os.path.join(path,file), "a+") as file_object:

            # Move read cursor to the start of file.
            file_object.seek(0)

            # If file is not empty then append '\n'
            data = file_object.read(100)
            if len(data) > 0 :
                file_object.write("\n")

            occData.insert(0, ondnr.replace(' ', ''))

            text = ';'.join(str(x) for x in occData)

            print(text)

            # Append text at the end of file
            file_object.write(text)
  except:
        # Niet gelukt om bestand op te slaan
        print(f'Niet gelukt om de termen op te slaan.')
        # Pauze van drie seconden.
        time.sleep(3)


# Geeft een array met 
def scrape_jaarverslag(ondnr):
    try:
      #list_of_files = glob.glob("..\..\..\..\..\Downloads\*.pdf") #og
      list_of_files = glob.glob("C:/Users/dylan/Downloads/*.pdf")
      latest_file = max(list_of_files, key = os.path.getmtime)
      read_pdf = PyPDF2.PdfFileReader(latest_file)

      # get number of pages
      NumPages = read_pdf.getNumPages()
    except:
      print('Failed..')

    data = [None]*5 # Array met vijf plaatsen maken; kan uitgebreid worden
    voorkomens = [0]*17

    try:
      # Tekst ophalen
      for i in range(0, NumPages):

          try:
            PageObj = read_pdf.getPage(i)
            Text = PageObj.extractText()
            Text.replace('\n', ' ').lower()

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
              # Omzet ophalen
              if data[1] == None and 'Omzet' in Text:
                arr = Text.split('\n')
                index = arr.index('Omzet')
                omzet = arr[index + 3].replace('.','')
                data[1] = omzet
                if balanstotaal.isdecimal():
                  data[2] = balanstotaal
                else:
                  data[2] = 0
            except:
              print('Error: Omzet')

          # balanstotaal ophalen
            try:  
              if data[2] == None and 'TOTAAL VAN DE ACTIVA' in Text:
                arr = Text.split('\n')
                index = arr.index('TOTAAL VAN DE ACTIVA')
                balanstotaal = arr[index + 2].replace('.','')
                if balanstotaal.isdecimal():
                  data[2] = balanstotaal
                else:
                  data[2] = 0
            except:
              print('Error: Balanstotaal')

            try:
              results = countKeywordOccurrences(Text)
              
              for i in range (0, 16):
                voorkomens[i] += results[i]

            except:
              print('Error: Tellen niet gelukt.')

          except:
            print(f'Failed reading page {i}')
          
          # framework voor duurzaamheidsrapportering
          # ja of nee? indien ja --> GRI, IIRC, ISO
          if  ' GRI ' in Text:
            data[3] = 'GRI'
          elif ' IIRC ' in Text:
            data[3] = 'IIRC'
          elif ' ISO ' in Text:
            data[3] = 'ISO'
          else:
            if i == (NumPages-1):
              data[3] = 'Nee'

          
          # B2B of B2C -- woord
          if 'B2C' in Text:
            data[4] = 'B2C'
          elif 'B2B' in Text:
            data[4] = 'B2B'
          else:
            if i == (NumPages-1):
              data[3] = 'Niet vermeld'

    except:
      print('niet gelukt om pagina te lezen')

    return [data,voorkomens]

# ######################## #
# Start van het programma #
# ######################## #

#xlsxToCSV()

companyNumbers = findCompanyNr() # bedrijfsnummers ophalen

for nr in companyNumbers:
  scrapeteInfo = download_pdf(nr.replace(" ", ""))
  time.sleep(3) # Om zeker te zijn dat de file gedownload is alvorens we ze gaan verplaatsen, anders verplaatsen we een verkeerde.
  data = scrape_jaarverslag(nr) # Data van de scraper opslaan
  
  saveAsFile(nr, data[0], scrapeteInfo) # Naar bestand schrijven.

  saveOccurrencesKeywords(nr, data[1])

  print(f'{nr} bekeken')
  time.sleep(3)
  
  #move_file()
  delete_file() # Uncomment dit om ruimte te besparen op je HDD, maar zorg dat je eerst scrapet.
