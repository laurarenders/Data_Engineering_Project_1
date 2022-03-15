try:
  from googlesearch import *
  import os
  import time
  from urllib.error import HTTPError
  import pandas as pd
  from bs4 import BeautifulSoup as bs
  import requests as req
  import re
except Exception as e:
  print(e)

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
      
  return found == 1

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
