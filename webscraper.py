#Gebruik voor de bulk van web scraping.
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
    provincies = ['Oost-Vl', 'West-Vl', 'Antwerpen', 'Limburg',  'Vl-Brabant']
    f = open("websites.txt", "w+")
    for prov in provincies:
        file = prov + '.csv'
        df = pd.read_csv(file)
        lijst = df["Web adres"].tolist()
        
        for rij in lijst:
            if isinstance(rij, str) and rij.startswith('www') :
                f.write(rij + "\n")




# Alle informatie van één website (inclusief alle resterende webpages) opslaan in een tekstbestand.
def saveAsFile(naam, gold):
    try: 
        # Opslaan onder /contents/
        path = "C:/DEPGroep1/contents/"
        file = naam + '.txt'
        
        with open(os.path.join(path,file), "a+") as file_object:
            # Move read cursor to the start of file.
            file_object.seek(0)

            # If file is not empty then append '\n'
            data = file_object.read(100)
            if len(data) > 0 :
                file_object.write("\n")

            # Append text at the end of file
            file_object.write(gold)
    except:
        # Niet gelukt om bestand op te slaan
        print(f'Niet gelukt om bestand voor {naam} aan te maken.')
    
    # Pauze van drie seconden.
    time.sleep(3)



# Welke tags sluiten we uit bij het scrapen?
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
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

def siteScraper(adres, og, arr=set(), visited=set()):
    try:
        naam = og.split('.')[1]
        # Op het einde van de rit
        # Resultaten opslaan in een tekstbestand;
        if len(arr) == len(visited) and len(visited) != 0:
            naam = og.split('.')[1]
            print(f'Alles doorlopen van site {naam}')

        # Niet meer dan 20 sites bezoeken.
        elif len(visited) > 20:
            naam = og.split('.')[1]
            print(f'Limiet bereikt voor {naam}')
            # Naar volgende site gaan!!

        else:
            #Huidige site op 'bezoekt' plaatsen
            visited.add(adres)

            #Pagina ophalen en soup aanmaken.
            page = req.get(adres, headers=useragent, timeout=10)
            soup = BeautifulSoup(page.text, 'html.parser')

            #Alle links ophalen
            for link in soup.select('a[href]'):        
                parsed_url = urlparse(link.get('href')).scheme
                
                #mail-links uitsluiten
                if link.get('href').startswith('mailto'):
                    pass
                #Correct formaat?
                elif parsed_url:
                    if compareSite(adres, link.get('href')):
                        arr.add(link.get('href'))
                #
                else:
                    link = og + link.get('href')
                    arr.add(link)

            soup = BeautifulSoup(page.text, 'html.parser')
            texts = soup.findAll(text=True)
            visible_texts = filter(tag_visible, texts)  
            collectedData = " ".join(t.strip() for t in visible_texts)
            saveAsFile(naam, collectedData)

            #data = soup.html.findAll()
            #for tag in data:
            #    tagSearch = str(tag)
            #    if zoekterm in tagSearch:
            #        print(tag.get_text().strip())

            #Alle P-tags ophalen
            #ptag = "".join([p.text for p in soup.find_all('p')])
            #print(ptag.strip())

            #Alle mails van de site ophalen.
            #mailtos = soup.select('a[href^=mailto]')
            #for mail in mailtos:
            #    mailadres = mail.get_text().strip()
            #    print(mailadres)

            #Extra opmerking: niet zo relevant
            #Alle telefoonnummers van de site ophalen.
            #data = soup.html.findAll()
            #for tag in data:
            #    tagSearch = str(tag)
            #    if '+32' in tagSearch:
            #        print(tag.get_text().strip())

            #Volgende site doorlopen
            for site in arr:
                if site not in visited:                
                    #print(f'Starten met: {site}')
                    siteScraper(site, og, arr, visited)
                    
    except:
        pass
        print(f"Site '{adres}' failed")


#################################################################################################################
#################################################################################################################
#################################################################################################################

tekstbestandUitschrijven()

# Bij start tweemaal de site meegeven
lines = open('websites.txt', 'r').readlines()

for site in lines:
    adres = 'https://' + site.strip()
    siteScraper(adres, adres, set(), set())
    time.sleep(1)
    

    


