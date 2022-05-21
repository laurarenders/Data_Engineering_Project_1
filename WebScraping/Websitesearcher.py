try:
  # Ophalen van websites waarvoor er geen link verkregen is
  from googlesearch import *
  import re

  #Gebruik voor de bulk van web scraping.
  from bs4 import BeautifulSoup
  from bs4 import BeautifulSoup as bs
  from bs4 import Comment

  # Gebruik van wiskundige berekening voor gelijkenissen in web-URLs.
  from numpy import mean

  # Gebruik van ophalen van webpagina's.
  import requests as req

  # Gebruik voor testen van website-URLs.
  from urllib.parse import urlparse
  from urllib.error import HTTPError

  # Gebruik voor omzetten van CSV-files.
  import pandas as pd

  # Gebruik voor timer
  import time

  # Gebruik voor pad
  import os

except Exception as e:
  print(e)


#################################################################################################################
#################################################################################################################
#################################################################################################################

provencies = ["Antwerpen", "Limburg", "Oost-Vl", "Vl-Brabant", "West-Vl"] # , "Limburg", "Oost-Vlaanderen", "Vl-Brabant", "West-Vlaanderen"
companyName = []
companyAddress = []
websites = []
withWebsite = []
withoutWebsite = []
useragent = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0'}

def dataOphalen(prov):
  
  file = open(f"{prov}.csv")

  df = pd.read_csv(file)
  ls_sites = df['Web adres'].tolist()
  ls_naam = df['Naam'].tolist()
  ls_adres = df["Adres"].tolist()
  ls_gemeente = df["Gemeente"].tolist()
  
  zipped = list(zip(ls_adres, ls_gemeente))

  for index in range(len(ls_naam)):
    if not isinstance(ls_sites[index], str):
      withWebsite.append(ls_naam[index])
      websites.append("N/A")
    else:
      withWebsite.append(ls_naam[index])
      websites.append(ls_sites[index])
    companyName.append(ls_naam[index])
    companyAddress.append([zipped[index][0], zipped[index][1]])

def checkCorrectWebsite(soup, companyName, companyAddress, url):
  found = 0
  if (re.search("[0-9]{3,}", url) or "facebook" in url or "wiki" in url):
    return found == 1
  for elem in soup.find_all():
    companyNameLs = companyName.split(' ')
    for cn in companyNameLs:
      if cn in str(elem).upper() or companyAddress.upper() in str(elem).upper():
        found = 1
        break
    if found == 1:
      break
      
  return found
  

# Functie voor sitescraping. 
# Gaat filteren op basis van welke tags er genegeerd mogen worden.
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

# Functie voor sitescraping. 
# Gaat de gevonden links gaan filteren op basis van likeliness (vb Facebook/Twitter/ander bedrijf negeren). Niet buiten de site gaan.
def compareSite(adres1, adres2):
    # Hoe gelijkaardig zijn de twee URL's?
    n = mean(len(adres1) + len(adres2))
    t = 0
    for a, b in zip(adres1, adres2):
        if a == b:
            t += 1
    return t/n > 0.4

  

def websitesOphalenViaNaam():
  for index in range(len(companyName)):
    print(f'{index+1}: {companyName[index]}')

    try:
      time.sleep(1)
      if websites[index] == "N/A":
        for url in search(companyName[index], num=1, stop=1, pause=2): # pause solves the problem of getting your IP blocked in google -- HERE IS ERROR
          response = req.get(url, headers=useragent, timeout=10)
          soup = bs(response.text, 'html.parser')

          # Kijken of naam van bedrijf in website staat. Zoniet, bedrijf opzoeken via adres
          if checkCorrectWebsite(soup, companyName[index], companyAddress[index][0], url):
            websites[index] = url
            print(f'Website: {websites[index]}')
            
          elif not checkCorrectWebsite(soup, companyName[index], companyAddress[index][0], url):
            print(f'{companyName[index]} searching via address\n')
            websiteOphalenViaAddress(index)
      else:
        print(f'Website: {websites[index]}')

    except Exception as e:
      print(f'{companyName[index]} could NOT be found due to the exception below')
      print(f'exception:\n\t{e}\n')

def websiteOphalenViaAddress(index):
  address = companyAddress[index][0] + " " + companyAddress[index][1]
  name = companyName[index]
  print(f'{name} is located at {address}')

  for url in search(address, num=1, stop=1, pause=2): # pause solves the problem of getting your IP blocked in google -- HERE IS ERROR
    response = req.get(url, headers=useragent, timeout=10)
    soup = bs(response.text, 'html.parser')
    if checkCorrectWebsite(soup, name, address, url):
      websites[index] = url
      print(f'Website: {websites[index]}')
    elif not checkCorrectWebsite(soup, name, address, url):
      print(f'Website NOT found...')
      websites.pop(index)
      withWebsite.pop(index)
      withoutWebsite.append(name)
      print(f"Without website: {withoutWebsite}")






# Alle informatie van één website (inclusief alle resterende webpages) opslaan in een tekstbestand.
def saveAsFile(naam, data):
    try: 
        # Opslaan onder /contents/
        path = "C:/web_scraper/contents/"
        file = naam + '.txt'
        f = open(os.path.join(path,file), "w")
        f.write("\n".join(data))
        f.close()
    except:
        # Niet gelukt om bestand op te slaan
        print(f'Niet gelukt om bestand voor {naam} aan te maken.')
    # Pauze van drie seconden.
    time.sleep(3)




def siteScraper(adres, og, arr=set(), visited=set(), data=[]):
    try:
        # Op het einde van de rit
        # Resultaten opslaan in een tekstbestand;
        if len(arr) == len(visited) and len(visited) != 0:
            naam = og.split('.')[1]
            saveAsFile(naam, data)
            print(f'Alles doorlopen van site {naam}')

        # Niet meer dan 50 sites bezoeken.
        elif len(visited) > 50:
            naam = og.split('.')[1]
            saveAsFile(naam, data)
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

            #Alle tekst ophalen en verzamelen in een array.
            collect = soup.html.findAll(text=True)
            rdb = filter(tag_visible, collect)
            data.append("".join(t.strip() for t in rdb))

            #Volgende site doorlopen
            for site in arr:
                if site not in visited:                
                    #print(f'Starten met: {site}')
                    siteScraper(site, og, arr, visited, data)
                    
    except:
        pass
        print(f"Site '{adres}' failed")

for prov in provencies:
  dataOphalen(prov)
  websitesOphalenViaNaam()

  # writing websites to file
  print('\nWriting websites to file\n')
  file = open('websitesOfAllCompanies.txt', 'a+')
  badCompanies = open('companiesWithoutWebsite.txt', 'a+')
  for w1, w2 in zip(websites, withWebsite):
    if w1 != "N/A":
      file.write(f"{w2}\n\t{w1}\n")

  for noWebsite in withoutWebsite:
    badCompanies.write(noWebsite + "\n")
    
  file.close()

# Eerst haalt hij de data op van de csv's via dataOphalen(). Vervolgens gaat hij kijken of er een website opgegeven was.
# Is er een website opgegeven, dan gaat hij deze meteen in de array stoppen; is er geen website, dan gaat hij zoeken via de naam.
# Om te verifiëren of de correcte website werd opgehaald, wordt er gekeken of de naam (of het adres) van het bedrijf uit de excel voorkomt in de website.
# Staat deze erin, dan wordt deze in de array gestoken, komt deze niet voor, dan zoeken we via het adres. Als daar de naam
# in voorkomt, dan steken we deze site in de array, anders zeggen we dat deze niet is gevonden en blijft de waarde op "N/A" staan.

# Probleem: soms een timeout en mogelijks soms verkeerde website nemen


## App: Sites scrapen op basis van tekstbestand. 
## OPM: Moet hier dus twee maal gebeuren? Eén keer voor de gegeven websites en daarna nog een keer voor de gevonden websites?

# Gekende sites doorlopen. Bij start tweemaal de site meegeven
lines = open('websitesOfAllCompanies.txt', 'r').readlines()

for site in lines:
    adres = 'https://' + site.strip()
    siteScraper(adres, adres)


# Niet-gekende sites doorlopen.
lines = open('websitesOfAllCompanies.txt', 'r').readlines()
for site in lines:
    adres = 'https://' + site.strip()
    siteScraper(adres, adres)