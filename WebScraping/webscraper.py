#Gebruik voor de bulk van web scraping.
from base64 import decode
from bs4 import BeautifulSoup
from bs4 import Comment

# Gebruik van wiskundige berekening voor gelijkenissen in web-URLs.
from numpy import mean

# Gebruik van ophalen van webpagina's.
import requests as req

# Gebruik voor testen van website-URLs.
from urllib.parse import urlparse

# Gebruik voor omzetten van CSV-files.
import pandas as pd

# Gebruik voor timer
import time

# Gebruik voor pad
import os

# Generatie van willekeurige waarden (merendeel testen)
import random
import re

contentDIR = "C:/DEPGroep1/contents/"

#################################################################################################################
#################################################################################################################
#################################################################################################################



# Useragent aanmaken
useragent = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0'}

# CSV-bestanden aanmaken op basis van het Excel-bestand
def xlsxToCSV():
    provincies = ['Oost-Vl', 'West-Vl', 'Antwerpen', 'Limburg',  'Vl-Brabant']
    for prov in provincies:
        read_file = pd.read_excel (r'prioriteitenlijst.xlsx', sheet_name=prov)
        read_file.to_csv (r'{}.csv'.format(prov), index=None, header=True)




# Alle websites ophalen uit het CSV-bestand
def tekstbestandUitschrijven():
    oldpwd=os.getcwd()

    path = "c:/DEPGroep1/CSV/"
    os.chdir(path)
    
    df = pd.DataFrame()

    for file in os.listdir():
        if file.endswith('.csv'):
            aux=pd.read_csv(file, error_bad_lines=False, delimiter=',')
            df=df.append(aux)
    
    os.chdir(oldpwd)

    df.to_csv(f"all.csv")
    
    f = open("websites.txt", "w+")
    file = 'all.csv'
    df = pd.read_csv(file)

    cols = ['Ondernemingsnummer', 'Web adres']
    df = df[cols]
    filter = df['Web adres'].notnull()

    df = df[filter]

    df.to_csv('websites.csv', index=False)




# Alle informatie van één website (inclusief alle resterende webpages) opslaan in een tekstbestand.
def saveAsFile(naam, gold):
    try: 
        # Opslaan onder /contents/
        path = contentDIR
        file = naam + '.txt'

        print(file)

        # sommige tekens kunnen niet in een tekstbestand gestoken worden
        # speciale tekens eruit halen
        gold = re.sub('[^a-zA-Z0-9 \n\.]', '', gold)
        
        with open(os.path.join(path,file), "a+") as file_object:
            # Move read cursor to the start of file.
            file_object.seek(0)

            # If file is not empty then append '\n'
            data = file_object.read(100)
            if len(data) > 0 :
                file_object.write("\n")

            # Append text at the end of file
            file_object.write(str(gold))
    except:
        # Niet gelukt om bestand op te slaan
        print(f'Niet gelukt om bestand voor {naam} aan te maken.')
    
    # Pauze van drie seconden.
    time.sleep(3)



# Welke tags sluiten we uit bij het scrapen?
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]', 'nav']:
        return False
    if isinstance(element, Comment):
        return False
    return True


# Functie om te tonen hoe gelijkaardig twee URL's zijn    
def compareSite(adres1, adres2):
    n = mean(len(adres1) + len(adres2))
    t = 0
    for a, b in zip(adres1, adres2):
        if a == b:
            t += 1
    return t/n > 0.4

def siteScraper(adres, og, ondnr, arr=set(), visited=set()):
    try:
        naam = og.split('.')[1]

        print(adres)

        # Op het einde van de rit
        # Resultaten opslaan in een tekstbestand;
        if len(arr) == len(visited) and len(visited) != 0:
            naam = og.split('.')[1]
            #print(f'Alles doorlopen van site {naam}')
        elif len(visited) > 20:
            pass
        else:
            #Huidige site op 'bezoekt' plaatsen
            visited.add(adres)

            #Pagina ophalen en soup aanmaken.
            page = req.get(adres, headers=useragent, timeout=10)
            soup = BeautifulSoup(page.content, 'html.parser')

            links = soup.select('a[href]')

            #Alle links ophalen
            for link in links:    
                parsed_url = urlparse(link.get('href')).scheme
                
                #mail-links uitsluiten
                if parsed_url:
                    if compareSite(adres, link.get('href')):
                        arr.add(link.get('href'))
                else:
                    link = og + link.get('href')
                    arr.add(link)

            soup = BeautifulSoup(page.content, 'html.parser')
            
            texts = soup.body.findAll(text=True)
            visible_texts = filter(tag_visible, texts)  
            collectedData = " ".join(t.strip() for t in visible_texts)
            collectedData = ' '.join(collectedData.split())
            
            saveAsFile(ondnr.replace(' ', ''), collectedData)

            #Volgende site doorlopen
            for site in arr:
                if site not in visited:                
                    #print(f'Starten met: {site}')
                    siteScraper(site, og, ondnr, arr, visited)
                    
    except:
        pass
        print(f"Site '{adres}' failed")


#################################################################################################################
###########################                 Applicatie             ##############################################
#################################################################################################################

tekstbestandUitschrijven()

# Bij start tweemaal de site meegeven
lines = open('websites.csv', 'r').readlines()

for site in lines:
    ondnr = site.split(',')[0].replace(' ', '').strip()
    adres = 'https://' + site.split(',')[1].strip()
    siteScraper(adres, adres, ondnr, set(), set())
    time.sleep(1)
    

    


