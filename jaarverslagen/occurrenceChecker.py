import pandas as pd
import numpy as np

ar = pd.read_csv("jaarverslagen/occurrences.csv", delimiter=';', encoding="ISO-8859-1")

print(ar.columns)

print('='*50)

print(ar.head())

print('='*50)