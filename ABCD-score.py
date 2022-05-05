import csv
import  pandas as pd
import numpy as np

df = pd.read_csv("scores/voorkomensWEBUniek.csv", sep=';')
df2 = pd.read_csv("scores/voorkomensPDF.csv", sep=';')

cols = ['gendergelijkheid', 'implementatie_werknemersrechten', 'sociale_relaties', 'werkgelegenheid', 'organisatie_op_het_werk', 'gezondheid_en_veiligheid', 'opleidingsbeleid', 'gebruik_van_energiebronnen', 'gebruik_van_waterbronnen', 'emissies_van_broeikasgassen', 'vervuilende_uitstoot', 'milieu_impact', 'impact_op_gezondheid_en_veiligheid', 'verdere_eisen_over_bepaalde_onderwerpen', 'milieu_beleid', 'SDGs']

df["totWEB"] = df[cols].sum(axis=1) 
df["totPDF"] = df2[cols].sum(axis=1) 

df["totAlles"] = df['totWEB'] + df['totPDF']

df["perc"] = round(df["totAlles"]/110*100)
df[" "] = '    '

conditions = [
    (df['perc'] < 25),
    (df['perc'] >= 25) & (df['perc'] < 50),
    (df['perc'] >= 50) & (df['perc'] < 75),
    (df['perc'] >= 75)
    ]

values = ['D', 'C', 'B', 'A']

df['score'] = np.select(conditions, values)


print(df[['ondnr', ' ', 'perc', ' ', 'score']])

df[['ondnr', ' ', 'perc', ' ', 'score']].to_csv (r'/Users/laurarenders/DEPGroep1-2/ABCDscore.csv', index = False, header=True)
