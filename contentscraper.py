from os import listdir
from os.path import isfile, join
from collections import Counter

# globaal variabele voor de directory
DIR = 'C:/DEPGroep1/contents/'

# alle bestandsnamen ophalen en in een array steken
contents = [f for f in listdir(DIR) if isfile(join(DIR, f))]

for file in contents:
    # naam van onderneming ophalen
    bedrijf = file.split('.')[0]

    # bestand wordt geopend en alle tekst wordt opgeslaan in een var
    f = open(DIR+file)
    tekst = f.read().lower().split()

    # onnodige whitespace verwijderen
    # opm: wordt al gedaan in webscraper.py
    #tekst = ' '.join(tekst.split())

    # occurrences checken
    
    dict = Counter(tekst)
    print(dict)
    
    


