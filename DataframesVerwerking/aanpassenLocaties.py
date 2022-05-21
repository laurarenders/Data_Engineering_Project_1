import pandas as pd

all = pd.read_csv('refinedWebData4.csv', delimiter=';')
loc = pd.read_csv('c:/DEPGroep1/CSV/uniekeGemeenten.csv',delimiter=';')

loc = loc.rename(columns={'Gemeente':'Locatie'})
all = all.rename(columns={'Adres':'Locatie'})

merged = pd.merge(all, loc, on='Locatie',how='outer')

merged['Locatie'] = merged['Unnamed: 0']
merged['SectorID'] = merged['SectorID'].fillna(7)
merged['SectorID'] = merged['SectorID'].astype(int)

merged.drop(columns={'Unnamed: 0', 'Postcode'}, inplace=True, axis=1)
merged = merged.drop_duplicates(subset=["Ondernemingsnummer"], keep=False)
#merged.to_csv('refinedWebData5.csv', sep=';', index=False)