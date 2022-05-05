gendergelijkheid = ["geslacht", "gendergelijkheid", "man/vrouw verhouding",
                    "ratio man/vrouw", "salaris man/vrouw", "discriminatie", "genderneutraal"]
implementatie_werknemersrechten = ["duurzaamheidscommissie", "rechten van werknemers", "arbeisrechten",
                                   "rechten en plichten van werknemers", "arbeidsomstandigheden", "algemene rechten en plichten", "mensenrechten", "recht op vrijheid"]
sociale_relaties = ["sociale relaties", "werkvloer",
                    "solidair gedrag",  "betrokkenheid van werknemers"]
werkgelegenheid = ["rekrutering", "rekruteringsbeleid", "rekruteringsverloop", "rekruteringstijd", "arbeidsovereenkomst", "werknemer", "werknemers", "diversiteitsbeleid", "loopbaan", "carrière",
                   "carrièreontwikkeling", "groei opportuniteiten", "groeikansen", "doorstroommogelijkheden", "promotie", "demografisch", "personeelsbestand", "human resources", "HR", "personeelsbeleid"]
organisatie_op_het_werk = ["vergoeding", "beloning", "bonus", "stabiliteit van werknemers", "stabiliteit", "bedrijfscultuur", "loyaliteit van werknemers", "personeelsbehoud", "retentie personeel", "loyaliteitsbonus",
                           "personeelsverloop", "leeftijdsstructuur", "afwezigheid", "afwezigheidsratio", "tevredenheid op het werk", "opvolgingsbeheer", "prestatiebeleid", "prestatie", "ziekte", "verzuim", "aanwezigheid", "aanwezigheidsratio"]
gezondheid_en_veiligheid = ["preventie", "pesterij", "ongewenst gedrag", "klacht", "gezondheid van werknemers", "welzijn van werknemers", "managers", "arbeiders",
                            "bedienden", "medewerkers", "incidenten op het werk", "incidenten", "discriminatie", "gezondheid en veiligheid op het werk", "intimidatie", "intimiderend gedrag", "vakbond"]
opleidingsbeleid = ["opleidingsbeleid", "training", "opleiding", "vaardigheden van werknemers", "kennis van werknemers",
                    "werknemersvaardigheden", "competenties van werknemer", "werknemercompetenties", "talent", "vakbekwaamheid"]
SDG = ["kinderarbeid", "goede gezondheid en welzijn", "gender-gelijkheid", "waardig werk en economische groei",
       "ongelijkheid verminderen", "vrede", "veiligheid en sterke publieke diensten"]

gebruik_van_energiebronnen = ["energiebron", "energie vermindering",
                              "energie reductie", "energie-intensiteit", "energiegebruik"]
gebruik_van_waterbronnen = ["waterverbruik", "waterbron", "wateronttrekking",
                            "waterafvoer", "watergebruik", "afvalwater", "grondwater"]
emissies_van_broeikasgassen = ["broeikasgas", "CO2", "CO²"]
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


menselijk_kapitaal = {"Gender equality/equality of treatment": gendergelijkheid,
                      "Implementation of (inter)national conventions on employeerights": implementatie_werknemersrechten, "Social dialogue/social relations (of personnel)": sociale_relaties, "Employment": werkgelegenheid, "Organisation of work": organisatie_op_het_werk, "Health and safety": gezondheid_en_veiligheid, "Training policy": opleidingsbeleid, "SDG": SDG}

natuurlijk_kapitaal = {"The use of energy resources": gebruik_van_energiebronnen, "The use of water resources": gebruik_van_waterbronnen, "Emissions of greenhouse gases": emissies_van_broeikasgassen, "Polluting emissions": vervuilende_uitstoot,
                       "Impact on the environment": milieu_impact, "Impact on health and security": impact_op_gezondheid_en_veiligheid, "Further requirements on specific items": verdere_eisen_over_bepaalde_onderwerpen, "Environmental policy": milieu_beleid, "SDG": SDGs}

duurzaamheid = {"Sustainability": ["duurzaamheidsdoelstelling(en)", "ontwikkelingsdoelen",
                "ontwikkelingsdoelstelling", "duurzaamheidsrapportering"]}

coding_tree = [menselijk_kapitaal, natuurlijk_kapitaal, duurzaamheid]
