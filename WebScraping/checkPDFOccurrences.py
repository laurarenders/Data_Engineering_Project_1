"""""
Alle imports
"""""

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
import numpy as np


"""""
Globale variabelen.

Het pad moet aangepast worden naar het lokale pad van de computer.
De termen en sleutelwoorden worden bijgehouden in libraries. Deze worden nadien aangehaald bij het tellen van het aantal voorkomens.
"""""

path = 'C:/Users/Dylan/Downloads'
scores = "C:/DEPGroep1/scores/"

# termen en sleutelwoorden #######
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



"""""
Het ondernemingsnummer en het aantal voorkomens (in arrayvorm) wordt doorgestuurd naar deze methode.
Als het ondernemingsnummer geen getal is wordt de methode afgebroken en commandline gelogd.
"""""

def saveAsFile(data, ondnr):
    try: 
        
        # Opslaan onder /contents/
        path = scores
        file = 'VoorkomensPDF.csv'

        path = path + file

        if ondnr.isdigit():
        
          with open(path, "a+") as file_object:

            voorkomens = np.hstack(([ondnr], data))

            # 
            text = ";".join(voorkomens) + '\n'

            # Append text at the end of file
            file_object.write(text)
        else:
          print(f' {ondnr} geen getal')
        
    except:
        # Niet gelukt om bestand op te slaan
        print(f'Niet gelukt om de uitslag aan het bestand toe te voegen.')


"""""
De input van de methode is een array van woorden. Dit zijn alle woorden die op het jaarverslag terug te vinden waren.
Voor ieder sleutelwoord wordt er in het gehele tekstbestand gekeken naar het aantal unieke voorkomens.
Een eenmalig voorkomen van een woord telt mee als een voorkomen. De voorkomens worden opgeteld en opgeslaan in een array.
De methode geeft een array aan voorkomens terug.
"""""


def countKeywordOccurrences(textArr):
    
    textArr = textArr.split(' ')

    data = [0]*17

    for keyword in gendergelijkheid:
      if keyword in textArr:
        data[0] += 1

    for keyword in implementatie_werknemersrechten:
      if keyword in textArr:
        data[1] += 1

    for keyword in sociale_relaties:
      if keyword in textArr:
        data[2] += 1

    for keyword in werkgelegenheid:
      if keyword in textArr:
        data[3] += 1

    for keyword in organisatie_op_het_werk:
      if keyword in textArr:
        data[4] += 1

    for keyword in gezondheid_en_veiligheid:
      if keyword in textArr:
        data[5] += 1

    for keyword in opleidingsbeleid:
      if keyword in textArr:
        data[6] += 1

    for keyword in SDg:
      if keyword in textArr:
        data[7] += 1

    for keyword in gebruik_van_energiebronnen:
      if keyword in textArr:
        data[8] += 1

    for keyword in gebruik_van_waterbronnen:
      if keyword in textArr:
        data[9] += 1

    for keyword in emissies_van_broeikasgassen:
      if keyword in textArr:
        data[10] += 1

    for keyword in vervuilende_uitstoot:
      if keyword in textArr:
        data[11] += 1
    
    for keyword in milieu_impact:
      if keyword in textArr:
        data[12] += 1

    for keyword in impact_op_gezondheid_en_veiligheid:
      if keyword in textArr:
        data[13] += 1

    for keyword in verdere_eisen_over_bepaalde_onderwerpen:
      if keyword in textArr:
        data[14] += 1
    
    for keyword in milieu_beleid:
      if keyword in textArr:
        data[15] += 1

    for keyword in SDGs:
      if keyword in textArr:
        data[16] += 1

    return data


"""""
Applicatie.

De glob dient om alle pdf's uit de huidige map op te halen. Pas het 'path'-variabele aan bij globale variabelen naar de gewenste werkmap.
Iedere PDF wordt doorlopen. Fouten worden opgevangen.
Onnodige speciale tekens worden uit de arrays gehaald, zo blijft enkel bruikbare lowercase woorden over.
Alle tekst uit een jaarverslag wordt samengevoegd. De tekst in arrayvorm wordt doorgestuurd naar 'countOccurrences'.
"""""

os.chdir(path)
for file in glob.glob("*.pdf"):
    read_pdf = PyPDF2.PdfFileReader(file)
    NumPages = read_pdf.getNumPages()

    allText = ["."]*NumPages
    ondnr = None

    for i in range(0, NumPages):
        try:
            PageObj = read_pdf.getPage(i)
            Text = PageObj.extractText().replace('\n', ' ').lower()
            if ondnr == None:
                if 'ondernemingsnummer' in Text:
                    arr = Text.split(' ')
                    index = arr.index('ondernemingsnummer')
                    ondnr = arr[index + 2].replace('.','')

            allText[i] = Text
        except:
            print(f'PDF {file} kon niet gelezen worden.')
    
    data = countKeywordOccurrences(" ".join(allText))

    saveAsFile(data, ondnr)