from cv2 import merge
import pandas as pd
import numpy as np

all = pd.read_csv('all.csv',delimiter=',')

web = pd.read_csv('finalRefinedWebData.csv',delimiter=';')

all.rename(columns={'ondnr':'Ondernemingsnummer'})
columns = ['Ondernemingsnummer', 'Adres']
all = all[columns]

all['Ondernemingsnummer'] = all['Ondernemingsnummer'].dropna().str.replace(' ','').astype('int')
web['Ondernemingsnummer'] = web['Ondernemingsnummer'].astype('int')

new = pd.merge(web, all, on='Ondernemingsnummer')

new.to_csv('refinedWebData6.csv',sep=';',index=False)