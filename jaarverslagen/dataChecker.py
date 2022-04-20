import pandas as pd
import numpy as np

ar = pd.read_csv("jaarverslagen/results.csv", delimiter=';', encoding="ISO-8859-1")

print(ar.columns)

print('='*50)

print(ar.head())

print('='*50)

# aantallen omzetten naar '0' + integer
#filter = ar['aantal'].str.contains('None')
#ar[filter] = ar[filter].replace('None', 0)
#ar['aantal'] = ar['aantal'].astype('int')


# balanstotalen omzetten naar '0' + integer
#filter = ar['balanstotaal'].str.contains('a-zA-Z', regex=True, na=False)
#print(ar[filter])
#filter = ar['balanstotaal'].str.contains('None', na=False) | ar['balanstotaal'].str.contains('a-zA-Z', na=False)
#ar[filter] = ar[filter].replace('None', 0)
#ar['balanstotaal'] = ar['balanstotaal'].astype('object') # integer te lang?

# omzet omzetten naar '0' + integer
#filter = ar['omzet'].str.contains('a-zA-Z', regex=True, na=False)
#print(ar[filter])
#filter = ar['omzet'].str.contains('None', na=False) | ar['omzet'].str.contains('a-zA-Z', na=False)
#ar[filter] = ar[filter].replace('None', 0)
#ar['omzet'] = ar['omzet'].astype('float') 

#print(ar['sector'].value_counts())

#ar.to_csv('jaarverslagen/results.csv', sep=';', index=False)