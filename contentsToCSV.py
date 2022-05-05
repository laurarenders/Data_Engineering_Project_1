import os
import re


def saveAsFile(ondnr, data):
    try: 
        # Opslaan onder /scores/
        path = "C:/DEPGroep1/scores/"
        file = 'data.csv'

        path = path + file

        #print(path)
        
        with open(path, "a+") as file_object:

            text = ["", "", "", "", ""]

            text[0] = ondnr
            text[3] = ondnr
            text[4] = data

            text = ";".join(text)         

            # Append text at the end of file
            file_object.write(text)
            file_object.write('\n')
        
    except:
        # Niet gelukt om bestand op te slaan
        print(f'Niet gelukt om de uitslag aan het bestand toe te voegen.')

dir = os.listdir('contents')

writeTo = open

for file in dir:
    filename = 'contents/' + file
    bestand = open(filename, 'r')

    text = bestand.read()
    text = text.lower()
    woorden = text.split()
    woorden = [word.strip('.,!;()[]') for word in woorden]

    unique = []
    for word in woorden:
        if word not in unique:
            unique.append(word)
    
    saveAsFile(file.split('.')[0], " ".join(unique))
