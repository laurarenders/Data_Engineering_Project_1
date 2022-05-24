import pandas as pd
import numpy as np

"""
Dataframe inlezen.
De kolom ondernemingsnummer aanpassen en enkel het ondernemingsnummer en de gescrapeteData behouden.
"""
web = pd.read_csv('scores/data.csv', delimiter=';')
web.rename({'Ondernemingsnummer_all': 'Ondernemingsnummer'})
webKolommen = ['Ondernemingsnummer', 'gescrapeteData']

web = web[webKolommen]
web['Ondernemingsnummer'] = web['Ondernemingsnummer'].astype('int64')

all = pd.read_csv('all.csv', delimiter=',')

allKolommen = ['Ondernemingsnummer', 'Naam', 'Gemeente']
all['Ondernemingsnummer'] = all['Ondernemingsnummer'].str.replace(' ', '').astype('int64')
all = all[allKolommen]

# merged = pd.join(all, lsuffix='_pdf', rsuffix='_all')
merged = pd.merge(all, web, on='Ondernemingsnummer', how='outer')

sector = pd.read_csv('CSV/ondSector.csv', delimiter=';')
sector['Ondernemingsnummer'] = sector['Ondernemingsnummer'].astype('int64')
merged = pd.merge(merged, sector, how='outer', on='Ondernemingsnummer')


# Deel van Organisatorische Kenmerken
orgken = pd.read_csv('CSV/orgKenFixed.csv', delimiter=';')
orgken = orgken.rename(columns={'ondnr':'Ondernemingsnummer'})
merged = pd.merge(merged, orgken, how='outer', on='Ondernemingsnummer')

merged.to_csv('refinedWebData.csv', sep=';', index=False)
#pdf.to_csv('correctFormat.csv', sep=';')


"""""
De data uit de prioriteitenlijst gaan we samenvoegen met de organisatorische kenmerken.
Het resultaat is een dataframe met daarin alle ondernemingsnummers met hun organisatorische kenmerken, adresgegevens en gescrapete data.
"""""

all = pd.read_csv('refinedWebData5.csv',delimiter=';')
orgKen = pd.read_csv('scores/orgKenmerkenPar7.csv', delimiter=';')
all = pd.merge(all, orgKen, on='Ondernemingsnummer', how='outer')
all = all.drop_duplicates(subset=["Ondernemingsnummer"], keep=False)


"""
Lege velden opvullen na de join en de waarden ervan overschrijven naar de gebruikte kolom.
"""

all['AantalWerknemers_x'] = all['AantalWerknemers_x'].fillna(all['AantalWerknemers_y'])
all['Omzet_x'] = all['Omzet_x'].fillna(all['Omzet_y'])
all['Balanstotaal_x'] = all['Balanstotaal_x'].fillna(all['Balanstotaal_y'])
all['B2_x'] = all['B2_x'].fillna(all['B2_y'])
all['Framework_x'] = all['Framework_x'].fillna(all['Framework_y'])


"""""
Het mergen leidde tot extra kolommen. Deze gaan we droppen. De overgebleven kolommen met een 'x' gaan we hernoemen.
"""""

all.drop(columns={'AantalWerknemers_y', 'Omzet_y', 'Balanstotaal_y', 'B2_y', 'Framework_y'}, inplace=True, axis=0)
all = all.rename(columns={'AantalWerknemers_x':'AantalWerknemers', 'Omzet_x':'Omzet', 'Balanstotaal_x':'Balanstotaal', 'B2_x':'B2', 'Framework_x':'Framework'})

print(all.head())

all.to_csv('finalRefinedWebData.csv',sep=';',index=False)