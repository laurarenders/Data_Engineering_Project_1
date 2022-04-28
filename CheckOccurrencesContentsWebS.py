# directories + delay
import os
import time

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
SDG = ["kinderarbeid", "goede gezondheid en welzijn", "gender-gelijkheid", "waardig werk en economische groei",
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


# Gevonden gegevens opslaan in een CSV-bestand. 
# Meegegeven -- ondernemingsnummer en array met daarin alle info 'gold'.
def saveAsFile(data):
    try: 
        # Opslaan onder /contents/
        path = "C:/DEPGroep1/scores/"
        file = 'VoorkomensWeb.csv'

        path = path + file

        #print(path)
        
        with open(path, "a+") as file_object:

            occData = ';'.join(str(x) for x in data[1])

            voorkomens = [str(data[0].split('.')[0]), str(occData)]

            # Duurzaamheid
            text = ";".join(voorkomens) + '\n'

            # Append text at the end of file
            file_object.write(text)
        
    except:
        # Niet gelukt om bestand op te slaan
        print(f'Niet gelukt om de uitslag aan het bestand toe te voegen.')
    # Pauze van drie seconden.
    time.sleep(3)

def giveScore(ondnr, text):
    textArr = text.split(' ')
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

    for keyword in SDG:
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

    return([ondnr, data])

path = "c:/DEPGroep1/contents/"
os.chdir(path)

for file in os.listdir():
    if file.endswith(".txt"):
        file_path = f"{path}\{file}"
        with open(file_path, 'r') as f:
            score = giveScore(file, f.read())
            #print(score)
            saveAsFile(score)