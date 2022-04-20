# Wordt pas gedaan na het uitvoeren van zowel scoreBerekenen.py en contentscraper.py
# Overloopt de twee bestanden

# imports
import pandas as pd
import numpy as np


pdf = pd.read_csv("scores/VoorkomensPDF.csv", delimiter=';', encoding="ISO-8859-1")
web = pd.read_csv("scores/VoorkomensWeb.csv", delimiter=';', encoding="ISO-8859-1")

df = pd.concat([pdf,web], axis=1)

print(df.head())
