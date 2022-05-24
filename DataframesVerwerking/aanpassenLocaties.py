import pandas as pd

"""""
We hebben twee dataframes. 
Een dataframe met de unieke gemeenten en een locatieID. 
Een dataframe met alle gegevens van de ondernemingen.
"""""

all = pd.read_csv('refinedWebData4.csv', delimiter=';')
loc = pd.read_csv('c:/DEPGroep1/CSV/uniekeGemeenten.csv',delimiter=';')

loc = loc.rename(columns={'Gemeente':'Locatie'})
all = all.rename(columns={'Adres':'Locatie'})

"""""
We voeren een merge uit tussen de twee dataframes. Deze outer join voeren we uit op de locatie.
De bedoeling is dat we de gegeven locatie bijvoorbeeld 'Antwerpen' gaan vervangen door het passende locatieID dat we bijhouden in de databank.
Het ID houden we bij als integer.

Extra opmerking:
Er werden lege sectorIDs opgemerkt. Deze IDs gaan we opvullen en plaatsen onder 'Overige ...'.
"""""

merged = pd.merge(all, loc, on='Locatie',how='outer')

merged['Locatie'] = merged['Unnamed: 0']
merged['SectorID'] = merged['SectorID'].fillna(7)
merged['SectorID'] = merged['SectorID'].astype(int)


"""""
Onnodige kolommen gaan we droppen.
Eventuele duplicates gaan we verwerpen.
Het dataframe gaan we omzetten naar een csv-bestand.
"""""

merged.drop(columns={'Unnamed: 0', 'Postcode'}, inplace=True, axis=1)
merged = merged.drop_duplicates(subset=["Ondernemingsnummer"], keep=False)
#merged.to_csv('refinedWebData5.csv', sep=';', index=False)