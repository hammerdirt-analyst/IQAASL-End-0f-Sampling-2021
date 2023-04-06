#!/usr/bin/env python
# coding: utf-8

# In[1]:


# -*- coding: utf-8 -*-
# This is a report using the data from IQAASL.
# IQAASL was a project funded by the Swiss Confederation
# It produces a summary of litter survey results for a defined region.
# These charts serve as the models for the development of plagespropres.ch
# The data is gathered by volunteers.
# Please remember all copyrights apply, please give credit when applicable
# The repo is maintained by the community effective January 01, 2022
# There is ample opportunity to contribute, learn and teach
# contact dev@hammerdirt.ch

# Dies ist ein Bericht, der die Daten von IQAASL verwendet.
# IQAASL war ein von der Schweizerischen Eidgenossenschaft finanziertes Projekt.
# Es erstellt eine Zusammenfassung der Ergebnisse der Littering-Umfrage für eine bestimmte Region.
# Diese Grafiken dienten als Vorlage für die Entwicklung von plagespropres.ch.
# Die Daten werden von Freiwilligen gesammelt.
# Bitte denken Sie daran, dass alle Copyrights gelten, bitte geben Sie den Namen an, wenn zutreffend.
# Das Repo wird ab dem 01. Januar 2022 von der Community gepflegt.
# Es gibt reichlich Gelegenheit, etwas beizutragen, zu lernen und zu lehren.
# Kontakt dev@hammerdirt.ch

# Il s'agit d'un rapport utilisant les données de IQAASL.
# IQAASL était un projet financé par la Confédération suisse.
# Il produit un résumé des résultats de l'enquête sur les déchets sauvages pour une région définie.
# Ces tableaux ont servi de modèles pour le développement de plagespropres.ch
# Les données sont recueillies par des bénévoles.
# N'oubliez pas que tous les droits d'auteur s'appliquent, veuillez indiquer le crédit lorsque cela est possible.
# Le dépôt est maintenu par la communauté à partir du 1er janvier 2022.
# Il y a de nombreuses possibilités de contribuer, d'apprendre et d'enseigner.
# contact dev@hammerdirt.ch

# sys, file and nav packages:
import datetime as dt
from datetime import date, datetime, time
from babel.dates import format_date, format_datetime, format_time, get_month_names
import locale

# math packages:
import pandas as pd
import numpy as np
from math import pi

# charting:
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import ticker
from matplotlib.ticker import MultipleLocator
import seaborn as sns
from matplotlib import colors as mplcolors

# build report
from reportlab.platypus.flowables import Flowable
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, KeepTogether
from reportlab.lib.pagesizes import A4
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

# the module that has all the methods for handling the data
import resources.featuredata as featuredata
from resources.featuredata import makeAList

# home brew utitilties
# import resources.chart_kwargs as ck
import resources.sr_ut as sut

# images and display
from PIL import Image as PILImage
from IPython.display import Markdown as md
from myst_nb import glue

# chart style
sns.set_style("whitegrid")

# border and row shading for tables
a_color = "saddlebrown"
table_row = "saddlebrown"

# a place to save figures and a 
# method to choose formats
save_fig_prefix = "resources/output/"

# the arguments for formatting the image
save_figure_kwargs = {
    "fname": None,
    "dpi": 300.0,
    "format": "jpeg",
    "bbox_inches": None,
    "pad_inches": 0,
    "bbox_inches": 'tight',
    "facecolor": 'auto',
    "edgecolor": 'auto',
    "backend": None,
}

## !! Begin Note book variables !!

# There are two language variants: german and english
# change both: date_lang and language
date_lang =  'de_DE.utf8'
locale.setlocale(locale.LC_ALL, date_lang)

# the date format of the survey data is defined in the module
date_format = featuredata.date_format

# the language setting use lower case: en or de
# changing the language may require changing the unit label
language = "de"
unit_label = "p/100 m"

# the standard date format is "%Y-%m-%d" if your date column is
# not in this format it will not work.
# these dates cover the duration of the IQAASL project
start_date = "2020-03-01"
end_date ="2021-05-31"
start_end = [start_date, end_date]

# the fail rate used to calculate the most common codes is
# 50% it can be changed:
fail_rate = 50

# # Changing these variables produces different reports
# # Call the map image for the area of interest
# bassin_map = "resources/maps/thunerseebrienzersee_city_labels.jpeg"

# the label for the aggregation of all data in the region
top = "Alle Erhebungsgebiete"

# define the feature level and components
# the feature of interest is the Aare (aare) at the river basin (river_bassin) level.
# the label for charting is called 'name'
this_feature = {'slug':'thunerseebrienzersee', 'name':"Thunersee/Brienzersee", 'level':'water_name_slug'}

# the lake is in this survey area
this_bassin = "aare"
# label for survey area
bassin_label = "Erhebungsgebiet Aare"

# these are the smallest aggregated components
# choices are water_name_slug=lake or river, city or location at the scale of a river bassin 
# water body or lake maybe the most appropriate
this_level = 'city'

# the doctitle is the unique name for the url of this document
doc_title = "thunerseebrienzersee"

# identify the lakes of interest for the survey area
lakes_of_interest = ["thunersee","brienzersee"]   


# !! End note book variables !!
## data
# Survey location details (GPS, city, land use)
dfBeaches = pd.read_csv("resources/beaches_with_land_use_rates.csv")
# set the index of the beach data to location slug
dfBeaches.set_index("slug", inplace=True)

# Survey dimensions and weights
dfDims = pd.read_csv("resources/corrected_dims.csv")

# code definitions
dxCodes = pd.read_csv("resources/codes_with_group_names")
dxCodes.set_index("code", inplace=True)

# columns that need to be renamed. Setting the language will automatically
# change column names, code descriptions and chart annotations
columns={"% to agg":"% agg", "% to recreation": "% recreation", "% to woods":"% woods", "% to buildings":"% buildings", "p/100m":"p/100 m"}

# !key word arguments to construct feature data
# !Note the water type allows the selection of river or lakes
# if None then the data is aggregated together. This selection
# is only valid for survey-area reports or other aggregated data
# that may have survey results from both lakes and rivers.
fd_kwargs ={
    "filename": "resources/checked_sdata_eos_2020_21.csv",
    "feature_name": this_feature['slug'], 
    "feature_level": this_feature['level'], 
    "these_features": ["thunersee","brienzersee"],
    "component": this_level, 
    "columns": columns, 
    "language": 'de', 
    "unit_label": unit_label, 
    "fail_rate": fail_rate,
    "code_data":dxCodes,
    "date_range": start_end,
    "water_type": None,    
}

fdx = featuredata.Components(**fd_kwargs)

# call the reports and languages
fdx.adjustForLanguage()
fdx.makeFeatureData()
fdx.locationSampleTotals()
fdx.makeDailyTotalSummary()
fdx.materialSummary()
fdx.mostCommon()
fdx.codeGroupSummary()

# !this is the feature data!
fd = fdx.feature_data

# !keyword args to build period data
# the period data is all the data that was collected
# during the same period from all the other locations
# not included in the feature data. For a survey area
# or river bassin these_features = feature_parent and 
# feature_level = parent_level
period_kwargs = {
    "period_data": fdx.period_data,
    "these_features": ["thunersee","brienzersee"],
    "feature_level":this_feature['level'],
    "feature_parent":this_bassin,
    "parent_level": "river_bassin",
    "period_name": bassin_label,
    "unit_label": unit_label,
    "most_common": fdx.most_common.index
}
period_data = featuredata.PeriodResults(**period_kwargs)

# the rivers are considered separately
# select only the results from rivers
# this can be done by updating the fd_kwargs
fd_rivers = fd_kwargs.update({"water_type":"r"})
fdr = featuredata.Components(**fd_kwargs)
fdr.makeFeatureData()

# this defines the css rules for the note-book table displays
header_row = {'selector': 'th:nth-child(1)', 'props': f'background-color: #FFF;'}
even_rows = {"selector": 'tr:nth-child(even)', 'props': f'background-color: rgba(139, 69, 19, 0.08);'}
odd_rows = {'selector': 'tr:nth-child(odd)', 'props': 'background: #FFF;'}
table_font = {'selector': 'tr', 'props': 'font-size: 12px;'}
table_css_styles = [even_rows, odd_rows, table_font, header_row]

def convertPixelToCm(file_name: str = None):
    im = PILImage.open(file_name)
    width, height = im.size
    dpi = im.info.get("dpi", (72, 72))
    width_cm = width / dpi[0] * 2.54
    height_cm = height / dpi[1] * 2.54
    
    return width_cm, height_cm


# pdf download is an option 
# reportlab is used to produce the document
# the arguments for the document are captured at run time
# capture for pdf content
pdf_link = f'resources/pdfs/foreword.pdf'
pdfcomponents = []

# pdf title and map
pdf_title = Paragraph(this_feature["name"], featuredata.title_style)
# map_image =  Image(bassin_map, width=cm*19, height=20*cm, kind="proportional", hAlign= "CENTER")


pdfcomponents = featuredata.addToDoc([
    pdf_title,    
    featuredata.small_space,
   
], pdfcomponents)


# (foreword)=
# # Vorwort
# 
# | [Italiano](italiano_intro_de) | [Francais](francais_intro_de) |
# 
# Ziel des vorliegenden Projekts «Identification, quantification and analysis of anthropogenic Swiss litter» (Identifizierung, Quantifizierung und Analyse von anthropogenem Abfall in der Schweiz, IQAASL) war es, Daten zu erheben und die erforderliche Infrastruktur aufzubauen, um die Zusammensetzung und die Häufigkeit von anthropogenem Material an ausgewählten Schweizer Fliessgewässern und Seen zu evaluieren. Zudem sollen die Ergebnisse in einem konsolidierten, webbasierten Bericht dargestellt werden.
# 
# Gegenwärtig werden mindestens drei Manuskripte vorbereitet, die Daten aus diesem Bericht verwenden oder Techniken daraus erforschen:
# 
# __Erkennung von Akkumulation und Leckage mit Spearmans Rho__, [Repository](https://hammerdirt-analyst.github.io/landuse/titlepage.html), *Zusammenarbeit mit Louise Schreyers, [Wageningen University and Research](https://www.wur.nl/).   Christian Ludwig, [_Paul Scherer Institute_](https://www.psi.ch/en)/[_EPFL_](https://www.epfl.ch/en/). Montserrat Filella, [_Department F.-A. Forel, University of Geneva_](https://www.unige.ch/forel/fr/).*
# 
# __Die Wahrscheinlichkeit, ein Objekt zu finden__, [Repository](https://github.com/hammerdirt-analyst/finding-one-object), *Zusammenarbeit mit Romain Tramoy, Laboratoire Eau Environment et Systèmes Urbains [LEESU](https://www.leesu.fr/), Bhavish Patel, [_Paul Scherrer Institute_](https://www.psi.ch/en), Montserrat Filella, [_Department F.-A. Forel, University of Geneva_](https://www.unige.ch/forel/fr/).* 
# 
# __Überwachung von Müll mit der nächsten Generation von Umweltingenieuren 2016-2021__, [Repository](https://github.com/hammerdirt-analyst/swe), *Zusammenarbeit mit Bhavish Patel, [_Paul Scherrer Institute_](https://www.psi.ch/en), Christian Ludwig, [_Paul Scherer Institute_](https://www.psi.ch/en)/[_EPFL_](https://www.epfl.ch/en/).* 
# 
# ## Bewertungsmethode
# 
# 2008 veröffentlichten das Umweltprogramm der Vereinten Nationen (UNEP) und die Zwischenstaatliche Ozeanografische Kommission (IOC) den ersten internationalen Leitfaden zur Überwachung von Strandabfällen {cite}`unepseas`. Diese Methode wurde vom OSPAR-Ausschuss im Jahr 2010 übernommen {cite}`ospard10`. IIm Jahr 2013 gab die EU dann Leitlinien für die Überwachung von Abfällen in den europäischen Meeren (Guidance on Monitoring of Marine Litter in European Seas) heraus {cite}`mlwguidance`. Die Schweiz ist OSPAR-Mitglied. Im Rahmen des IQAASL-Projekts und früherer Probenahmen wurden über 1’400 Proben gesammelt und kategorisiert, wobei die in diesen Leitlinien beschriebenen Methoden - die ursprünglich für Abfallerhebungen an Meeresküsten entwickelt wurden - für Seen und Fliessgewässer angepasst wurden. {cite}`mlwguidance`
# 
# 
# ```{card}
# :class-card: sd-text-black
# :img-top: resources/images/titlepage/conferencepresim.jpg
# :margin: auto
# +++
# *Bei einer Untersuchung von Strandabfällen wird das sichtbare anthropogene Material erhoben, das in einem abgegrenzten Gebiet identifiziert wird, das auf einer Seite von einem See, einem Fliessgewässer oder dem Meer begrenzt ist.*
# ```
# <br/>
# 
# * Die Standorte werden anhand ihrer GPS-Koordinaten definiert.
# * Für jedes Erhebungsgebiet werden Länge und Breite gemessen.
# * Sichtbare Schadstoffe im Erhebungsgebiet werden gesammelt, klassifiziert, gezählt und gewogen.
# * Alle Gegenstände werden anhand der Codes der Leitlinien klassifiziert.
# 
# Für Gegenstände von regionalem Interesse wurden zusätzliche Codes vorgesehen. So wurden etwa Codes definiert für Gegenstände wie Pheromon-Lockstoff-Behälter und Skistöcke, damit diese Objekte in gewissen Gebieten entsprechend erfasst werden können. Durch das Identifizieren und Quantifizieren von Gegenständen können Forschende und Stakeholder wahrscheinliche Quellen ermitteln und Strategien definieren, mit denen dafür gesorgt werden kann, dass bestimmte Gegenstände in der Umwelt weniger häufig vorkommen. Weitere Informationen: [Code-Gruppen](codegroups).
# 
# ## Bewertungsparameter
# 
# Der Medianwert (50. Perzentil) der Erhebungsergebnisse gibt die Anzahl Gegenstände pro 100 m (p/100 m) Küstenlinie resp. Uferlinie an. Diese Methode wird in den EU Marine Beach Litter Baselines {cite}`eubaselines` beschrieben und in diesem Bericht als Standard verwendet. Der in Meeresgebieten angewandte Standard von 100 Metern Küstenlinie eignet sich für die Küstengebiete des europäischen Kontinents. Die Urbanisierung und die Topografie stellen jedoch bei der Auswahl geeigneter Standorte für langjährige Abfallerhebungen an Küsten resp. Ufern besondere Herausforderungen dar.
# 
# Wären die Untersuchungen auf Uferlinien mit einer Länge von 100 Metern beschränkt worden, hätte dies die Anzahl der möglichen Standorte sowie die Verwendung bereits bestehender Daten drastisch eingeschränkt. Daher wird beim IQAASL-Projekt (Identification, Quantification and Analysis of Swiss Litter) die lokale Topografie mit einer mittleren Erhebungslänge von 45 m (Median) und einem Durchschnitt von 51 m widergespiegelt. Erhebungen von Abschnitten mit einer Länge von weniger als 10 m wurden in der Analyse der Erhebungsergebnisse nicht berücksichtigt. Die Ergebnisse der Erhebung werden in p/100 m umgerechnet, indem sie mit dem Faktor 100 multipliziert werden.
# 
# ### Datenerhebung
# 
# Jede Person kann jederzeit eine Strandabfallerhebung durchführen. Wird die Erhebung gemäss der Methode der Leitlinien {cite}`mlwguidance` oder den [Basiswerte für Abfallobjekte an Gewässern](threshhold) vorgenommen, kann das Ergebnis direkt mit den Abbildungen in diesem Bericht verglichen werden.
# 
# Das Sammeln von Daten für den Bericht (oder den nächsten Bericht) erfordert eine gewisse Einarbeitung und eine Bewertung. Es dauert in der Regel 3-5 Datenerhebungen, um eine Person an die Aufgabe zu gewöhnen. Die meiste Zeit wird damit verbracht, Objekte zu identifizieren und zu lernen, wie wichtig es ist, ein Feldnotizbuch zu führen. Der Vorteil der Datenübermittlung besteht darin, dass das Berichtsverfahren automatisiert ist und man jederzeit Zugriff auf die Ergebnisse hat.
# 
# ---
# 
# ### Verwendung dieses Berichts
# 
# Bei der Interpretation der Ergebnisse ist es wichtig, den Unterschied zwischen dem _Median_ {cite}`mediandef` und dem _Durchschnitt_ {cite}`meandeff` zu verstehen. Mit Ausnahme der monatlichen Resultate werden die Erhebungsergebnisse als Median p/100 m für den betreffenden Standort angegeben.
# 
# In der folgenden Abbildung wird beispielsweise der Median der Erhebungsergebnisse für die am häufigsten vorgefundenen Gegenstände an Thuner- und Brienzersee dargestellt.

# In[2]:


# calling componentsMostCommon gets the results for the most common codes
# at the component level
components = fdx.componentMostCommonPcsM()

# pivot that and quash the hierarchal column index that is created when the table is pivoted
mc_comp = components[["item", unit_label, "city"]].pivot(columns="city", index="item")
mc_comp.columns = mc_comp.columns.get_level_values(1)

# the aggregated total of the feature is taken from the most common objects table
mc_feature = fdx.most_common[unit_label]
mc_feature = featuredata.changeSeriesIndexLabels(mc_feature, {x:fdx.dMap.loc[x] for x in mc_feature.index})

# aggregated totals of the parent this is derived from the arguments in kwargs
mc_parent = period_data.parentMostCommon(parent=True)
mc_parent = featuredata.changeSeriesIndexLabels(mc_parent, {x:fdx.dMap.loc[x] for x in mc_parent.index})

# the aggregated totals of all the period data
mc_period = period_data.parentMostCommon(parent=False)
mc_period = featuredata.changeSeriesIndexLabels(mc_period, {x:fdx.dMap.loc[x] for x in mc_period.index})

# add the feature, bassin_label and period results to the components table
mc_comp[this_feature["name"]]= mc_feature
mc_comp[bassin_label] = mc_parent
mc_comp[top] = mc_period

mc_comp_de = mc_comp.copy()
mc_comp_it = mc_comp.copy()
mc_comp_fr = mc_comp.copy()

ital = {
    "Cigarette filters": "Filtri di sigarette" ,
    "Fragmented plastics":"Plastica frammentata",
    "Expanded polystyrene": "Polistirolo espanso",
    "Food wrappers; candy, snacks":"Incarti di cibo; caramelle, snack",
    "Industrial sheeting": "Telo industriale",
    "Glass drink bottles, pieces":"Bottiglie per bevande in vetro, pezzi",
    "Industrial pellets (nurdles)":"Pellet industriali (nurdles)",
    "Insulation foams": "Schiume isolanti",
    "Cotton bud/swab sticks":"Bastoncini di cotton fioc/ tampone",
    "Expanded foams < 5mm":"Schiume espanse < 5mm",
    "Plastic construction waste":"Rifiuti plastici da costruzione",
    "Metal bottle caps and lids":"Tappi e coperchi di bottiglia in metallo",
    "Packaging films nonfood or unknown":"Pellicole da imballaggio non alimentari o sconosciute"
}

ital = {
    'Zigarettenfilter': "Filtri di sigarette" ,
    'Fragmentierte Kunststoffe':"Plastica frammentata",
    'Expandiertes Polystyrol': "Polistirolo espanso",
    'Snack-Verpackungen':"Incarti di cibo; caramelle, snack",
    "Industriefolie (Kunststoff)": "Telo industriale",
    ' Getränkeflaschen aus Glas, Glasfragmente':"Bottiglie per bevande in vetro, pezzi",
    'Industriepellets (Nurdles)':"Pellet industriali (nurdles)",
    'Schaumstoffverpackungen/Isolierung': "Schiume isolanti",
    'Wattestäbchen/Tupfer':"Bastoncini di cotton fioc/ tampone",
    "Expanded foams < 5mm":"Schiume espanse < 5mm",
    'Kunststoff-Bauabfälle':"Rifiuti plastici da costruzione",
    "Metal bottle caps and lids":"Tappi e coperchi di bottiglia in metallo",
    "Verpackungsfolien, nicht für Lebensmittel":"Pellicole da imballaggio non alimentari o sconosciute",
    "Industriefolie (Kunststoff)": "Telo industriale",
}


fren = {
    'Zigarettenfilter': "Filtres à cigarettes",  
    'Fragmentierte Kunststoffe': "Plastiques fragmentés",
    'Expandiertes Polystyrol': "Polystyrène expansé",
    'Snack-Verpackungen':"Emballages alimentaires, bonbons",
    'Industriefolie (Kunststoff)':"film plastique épais",
    ' Getränkeflaschen aus Glas, Glasfragmente':"Bouteilles pour boissons, morceaux",
    'Industriepellets (Nurdles)':"Granules Plastique industriels (GPI)",
    'Schaumstoffverpackungen/Isolierung':"Isolation : y compris les mousses en spray",
    'Wattestäbchen/Tupfer':"Bâtonnets de coton-tige",
    'Kunststoff-Bauabfälle':"Déchets plastiques de construction",
    'Verpackungsfolien, nicht für Lebensmittel':"Films d'emballage non alimentaires ou inconnus",
}

mc_comp_it.index = [ital[x] for x in mc_comp_it.index]
mc_comp_fr.index = [fren[x] for x in mc_comp_fr.index]

mc_comp_it_caption = [
    "Interpretazione dei risultati dell’indagine. I risultati aggregati di tutte le aree d’indagine sono nella colonna all’estrema destra, ",
    "preceduti dai risultati aggregati del Lago di Thun e del Lago di Brienz. Le prime sei colonne sono i comuni da cui sono stati prelevati ",
    "i campioni. Questo standard è mantenuto in tutto il documento. Il numero rappresenta il valore mediano del sondaggio per quell’oggetto. ",
    "Se quell’oggetto non viene trovato in almeno la metà delle indagini, allora il valore mediano sarà zero. Il valore mediano è una stima ",
    "ragionevole del numero di oggetti che probabilmente verrebbero trovati se si ripetesse un’indagine sui rifiuti."
]

mc_comp_fr_caption = [
    "Interprétation des résultats de l'inventaire. Les résultats agrégés de toutes les zones d'enquêtes figurent dans la colonne d'extrême droite, ",
    "précédés des résultats agrégés de Thunersee et Brienzersee. Les six premières colonnes correspondent aux municipalités où les échantillons ont ",
    "été prélevés. Cette norme est maintenue tout au long du document. Le chiffre représente la valeur médiane de l' inventaire pour cet objet. Si cet ",
    "objet n'est pas trouvé dans au moins la moitié des inventaires, la valeur médiane sera de zéro. La valeur médiane est une estimation raisonnable du ",
    "nombre d'objets susceptibles d'être trouvés si un inventaire de déchets sauvages était répétée."
]

mc_comp_de_caption = [
    "Interpretation der Datenerhebungen Ergebnisse. Die aggregierten Ergebnisse aus allen Erhebungsgebieten befinden sich in der Spalte ganz rechts, vor den ",
    "aggregierten Ergebnissen aus dem Thunersee und dem Brienzersee. Die ersten sechs Spalten sind die Gemeinden, in denen die Proben genommen wurden. Dieser ",
    "Standard wird im gesamten Dokument beibehalten. Die Zahl stellt den Medianwert der Erhebung für dieses Objekt dar. Wenn dieses Objekt in mindestens der ",
    "Hälfte der Datenerhebungen nicht gefunden wird, ist der Medianwert gleich Null. Der Medianwert ist eine vernünftige Schätzung der Anzahl der Objekte, die bei ",
    "einer Wiederholung einer Abfallobjekte-Erhebung wahrscheinlich gefunden werden."
]

col_widths=[4.5*cm, *[1.2*cm]*(len(mc_comp.columns)-1)]
it_cap = featuredata.makeAParagraph(mc_comp_it_caption, style=featuredata.caption_style)
it_table = featuredata.aSingleStyledTable(mc_comp_it, vertical_header=True, colWidths=col_widths, gradient=True)
it_pdf_heat_map = featuredata.tableAndCaption(it_table, it_cap, col_widths)

fr_cap = featuredata.makeAParagraph(mc_comp_fr_caption, style=featuredata.caption_style)
fr_table = featuredata.aSingleStyledTable(mc_comp_fr, vertical_header=True, colWidths=col_widths, gradient=True)
fr_pdf_heat_map = featuredata.tableAndCaption(fr_table, fr_cap, col_widths)

de_cap = featuredata.makeAParagraph(mc_comp_de_caption, style=featuredata.caption_style)
de_table = featuredata.aSingleStyledTable(mc_comp, vertical_header=True, colWidths=col_widths, gradient=True)
de_pdf_heat_map = featuredata.tableAndCaption(de_table, de_cap, col_widths)
    
# notebook display style de
aformatter = {x: featuredata.replaceDecimal for x in mc_comp.columns}
mcd = mc_comp.style.format(aformatter).set_table_styles(table_css_styles)
mcd = mcd.background_gradient(axis=None, vmin=mc_comp.min().min(), vmax=mc_comp.max().max(), cmap="YlOrBr")

# remove the index name and column name labels
mcd.index.name = None
mcd.columns.name = None

# rotate the text on the header row
# the .applymap_index method in the
# df.styler module is used for this
mcd = mcd.applymap_index(featuredata.rotateText, axis=1)

# notebook display style it
aformatter_i = {x: featuredata.replaceDecimal for x in mc_comp_it.columns}
mcdi = mc_comp_it.style.format(aformatter_i).set_table_styles(table_css_styles)
mcdi = mcdi.background_gradient(axis=None, vmin=mc_comp_it.min().min(), vmax=mc_comp_it.max().max(), cmap="YlOrBr")

# remove the index name and column name labels
mcdi.index.name = None
mcdi.columns.name = None

# rotate the text on the header row
# the .applymap_index method in the
# df.styler module is used for this
mcdi = mcdi.applymap_index(featuredata.rotateText, axis=1)

# notebook display style fr
aformatter_f = {x: featuredata.replaceDecimal for x in mc_comp_fr.columns}
mcdf = mc_comp_fr.style.format(aformatter_f).set_table_styles(table_css_styles)
mcdf = mcdf.background_gradient(axis=None, vmin=mc_comp_fr.min().min(), vmax=mc_comp_fr.max().max(), cmap="YlOrBr")

# remove the index name and column name labels
mcdf.index.name = None
mcdf.columns.name = None

# rotate the text on the header row
# the .applymap_index method in the
# df.styler module is used for this
mcdf = mcdf.applymap_index(featuredata.rotateText, axis=1)



glue('t_b_de', mcd, display=False)
glue('t_b_it', mcdi, display=False)
glue('t_b_fr', mcdf, display=False)


# ```{glue:figure} t_b_de
# ```
# Abbildung: _Interpretation der Erhebungsergebnisse. Die aggregierten Ergebnisse aller Erhebungsgebiete und des Aare-Erhebungsgebietes befinden sich in den beiden Spalten ganz rechts, in der Spalte links daneben sind die aggregierten Ergebnisse von Thuner- und Brienzersee angegeben. Die ersten sechs Spalten beziehen sich auf die Gemeinden, in denen die Proben genommen wurden. Dieser Standard wird im gesamten Dokument beibehalten. Die Zahl entspricht dem mittleren Erhebungswert für den betreffenden Gegenstand. Wurde dieser Gegenstand nicht in mindestens der Hälfte der Erhebungen festgestellt, beträgt der Medianwert null. Der Medianwert stellt eine angemessene Schätzung der Anzahl Gegenstände dar, die bei einer Wiederholung der Abfallerhebung wahrscheinlich gefunden werden würde._ 
# 

# Die Ergebnisse zeigen, dass Bauabfälle aus Kunststoff in Bönigen (4,5 p/100 m) und Unterseen (1,5 p/100 m) im Vergleich zu den anderen Gemeinden, die einen Medianwert von null aufweisen, häufiger vorzufinden waren. Industriefolien und Zigaretten wurden jedoch in allen Gemeinden in mindestens der Hälfte der Erhebungen festgestellt. 
# 
# Das bedeutet, dass die Wahrscheinlichkeit, Bauabfälle aus Kunststoff zu finden, in den Uferzonen in Bönigen und Unterseen grösser war als in den anderen Gemeinden. Demgegenüber war es praktisch überall gleich wahrscheinlich, auf Industriefolien zu stossen, wobei in Brienz der grösste Anteil davon gefunden werden dürfte (67 p/100 m).
# 
# Im Kapitel [Schlüsselindikatoren](keyindicators) werden alle grundlegenden Statistiken, die sich aus den Erhebungsergebnissen ableiten lassen, genau definiert. Ausserdem wird angegeben, wie sie für die Identifikation von Akkumulationszonen und signifikanten Ereignissen verwendet werden können. Die Methoden zur Berechnung der verschiedenen Umweltvariablen werden im Kapitel [_Das Landnutzungsprofil_](luseprofile) erläutert. Im Teil [_Codegruppen_](codegroups) werden die Codes und die Beschreibungen, die zur Identifizierung der Gegenstände dienen, sowie die wirtschaftlichen Gruppierungen im Detail vorgestellt. Im Kapitel [_Geteilte Verantwortung_](transport) wiederum wird dargelegt, wie Proben gesammelt werden, und welche Methoden zur Feststellung von Extremwerten und zur Berechnung von Basiswerten für eine Region angewandt werden.
# 
# ---

# (italiano_intro_de)=
# ## Prefazione
# 
# Scopo del presente progetto IQAASL (Identification, quantification and analysis of anthropogenic Swiss litter) è quello di raccogliere dati e sviluppare l’infrastruttura necessaria per valutare accuratamente la composizione e la quantità del materiale antropogenico presente lungo fiumi e laghi selezionati della Svizzera. I risultati sono poi presentati in un rapporto basato sul web.
# 
# I risultati di queste indagini saranno utilizzati per esplorare altri metodi per rilevare le zone di accumulo.
# 
# __Detecting accumulation and leakage with Spearman’s Rho (Rilevamento dell’accumulo e della perdita con il rho di Spearman)__,  [Repository](https://hammerdirt-analyst.github.io/landuse/titlepage.html), *collaborazione con Louise Schreyers, [Wageningen University and Research](https://www.wur.nl/).   Christian Ludwig, [_Paul Scherer Institute_](https://www.psi.ch/en)/[_EPFL_](https://www.epfl.ch/en/). Montserrat Filella, [_Department F.-A. Forel, University of Geneva_](https://www.unige.ch/forel/fr/).*
# 
# __The probability of finding an object (La probabilità di trovare un oggetto)__, *collaborazione con Romain Tramoy, Laboratoire Eau Environment et Systèmes Urbains [LEESU](https://www.leesu.fr/), Bhavish Patel, [_Paul Scherrer Institute_](https://www.psi.ch/en), Montserrat Filella, [_Department F.-A. Forel, University of Geneva_](https://www.unige.ch/forel/fr/).* [Repository](https://github.com/hammerdirt-analyst/finding-one-object)
# 
# __Monitoring trash with the next generation of Solid waste engineers 2016-2021 (Monitoraggio dei rifiuti con la nuova generazione di ingegneri ambientali 2016-2021)__, *collaborazione con Bhavish Patel, [_Paul Scherrer Institute_](https://www.psi.ch/en), Christian Ludwig, [_Paul Scherer Institute_](https://www.psi.ch/en)/[_EPFL_](https://www.epfl.ch/en/).* [Repository](https://github.com/hammerdirt-analyst/swe)
# 
# ## Metodo di valutazione
# 
# Nel 2008, la prima guida internazionale per il monitoraggio dell’accumulo di rifiuti spiaggiati (c.d. «beach litter») {cite}`unepseas`. è stata pubblicata dal Programma delle Nazioni Unite per l’ambiente (UNEP) e dalla Commissione oceanografica intergovernativa (COI) dell’UNESCO. Questo metodo è stato in seguito ripreso dalla Commissione OSPAR nel 2010 {cite}`ospard10`.  Nel 2013 l’UE ha pubblicato una Guida sul monitoraggio dei rifiuti marini nei mari europei (Guidance on Monitoring of Marine Litter in European Seas – la Guida) {cite}`mlwguidance`. La Svizzera è membro della Convenzione OSPAR. Nell’ambito del progetto IQAASL e dei rilevamenti precedenti, oltre 1400 campioni sono stati raccolti e catalogati adattando i metodi descritti nella Guida – concepita appunto per la costa marittima – a un rilevamento condotto lungo laghi e fiumi. 
# 
# 
# ```{card}
# :class-card: sd-text-black
# :img-top: resources/images/titlepage/conferencepresim.jpg
# :margin: auto
# +++
# *Nell’ambito di un’indagine sui rifiuti spiaggiati viene censito il materiale antropogenico visibile individuato all’interno di un’area delimitata bagnata da un lago, un fiume o un mare.*
# ```
# <br/>
# 
# * Le posizioni sono definite mediante rispettivi punti GPS
# * Per ogni area d’indagine vengono misurate lunghezza e larghezza
# * Gli inquinanti visibili all’interno dell’area d’indagine vengono raccolti, classificati, contati e pesati
# * Tutti gli articoli sono classificati in base alle definizioni dei codici stabiliti nella Guida
# 
# Per identificare oggetti di rilevanza regionale sono stati aggiunti codici supplementari. Per esempio, sono stati creati codici per oggetti quali contenitori di esche a feromoni e bastoni da sci per rendere conto della presenza di questi oggetti ove individuati in determinate regioni. L’individuazione e la quantificazione degli oggetti permettono ai ricercatori e alle parti coinvolte di determinare le probabili fonti inquinanti e definire così strategie di riduzione mirate a oggetti specifici.
# 
# Per maggiori informazioni: [Gruppi di codici -deutsch](codegroups).
# 
# ## Parametri di valutazione
# 
# Il valore mediano (50° percentile) dei risultati dell’indagine viene riportato come numero di oggetti per 100 metri lineari (p/100 m) di riva. Questo metodo è descritto nelle EU Marine Beach Litter Baselines (Linee guida sui rifiuti ritrovati sulle spiagge marine) {cite}`eubaselines` e costituisce lo standard adottato nel presente rapporto. Lo standard di 100 metri lineari di costa usato nell’ambiente marino è pertinente per le regioni costiere del continente europeo. Tuttavia, l’urbanizzazione e la topografia presentano sfide specifiche per quanto concerne la selezione di luoghi adatti a condurre indagini annuali sui rifiuti spiaggiati.
# 
# Una limitazione delle indagini a 100 metri lineari di riva, rispettivamente di costa, esposta avrebbe tuttavia ridotto drasticamente il numero di luoghi d’indagine disponibili e l’uso dei dati preesistenti. Il progetto IQAASL (Identificazione, quantificazione e analisi dei rifiuti antropogenici in Svizzera) rispecchia pertanto la topografia locale con una lunghezza mediana di indagine di 45 m e una media di 51 m. Le indagini con lunghezze inferiori a 10 m non sono state invece considerate nell’analisi di baseline. I risultati delle indagini vengono convertiti in p/100 m rapportando i dati su base 100.
# 
# 
# ### Raccolta di dati
# 
# Un’indagine sul beach litter può essere condotta da chiunque in qualsiasi momento. Se l’indagine viene condotta secondo il metodo descritto nella guida {cite}`mlwguidance` o nel [valori di riferimento -deutsch](threshhold) il risultato può essere confrontato direttamente con i grafici di questo rapporto. 
# 
# ## Utilizzo del rapporto
# 
# Quando si interpretano i risultati è importante capire la differenza tra *mediana* {cite}`mediandef` e la *media* {cite}`meandeff`. Tranne che per i dati mensili, i risultati delle indagini sono espressi come la mediana del parametro p/100m per quanto concerne l’ubicazione in questione.
# 
# A titolo di esempio, si consideri il risultato **mediano** dell’indagine per gli oggetti più comuni reperiti sulle sponde del lago di Thun e del lago di Brienz. 

# ```{glue:figure} t_b_it
# ```
# __In alto:__ _I Interpretazione dei risultati dell’indagine. I risultati aggregati di tutte le aree d’indagine come pure dell’area di indagine dell’Aare sono riportati nelle ultime due colonne all’estrema destra, preceduti dai risultati aggregati del lago di Thun e del lago di Brienz. Le prime sei colonne sono i comuni da cui sono stati prelevati i campioni. Questo standard è mantenuto nell’intero documento. Il numero rappresenta il valore mediano dell’indagine per uno specifico oggetto. Se tale oggetto non viene trovato in almeno la metà delle indagini, il valore mediano risulterà pari a zero. Il valore mediano è una stima ragionevole del numero di oggetti che probabilmente verrebbero trovati se si ripetesse un’indagine sui rifiuti spiaggiati._

# I risultati per i rifiuti edili in plastica mostrano che questa tipologia presentava una prevalenza maggiore a Bönigen (4,5 p/100 m) e Unterseen (1,5 p/100 m) rispetto agli altri comuni, dove il valore mediano è zero. Teli industriali e sigarette sono stati tuttavia censiti in tutti i comuni in almeno la metà delle indagini.
# 
# In termini pratici, sulle rive dei comuni di Bönigen e Unterseen sussistevano probabilità di reperire rifiuti edili in plastica maggiori che negli altri comuni. Tuttavia le possibilità di trovare teli industriali sono state all’incirca uguali ovunque, sebbene il picco massimo sia individuabile a Brienz (67 p/100 m).
# 
# Il capitolo degli [Indicatori chiave -deutsch ](keyindicators) fornisce una definizione precisa di ciascuna delle statistiche di base ricavabili dai risultati dell’indagine e sul modo in cui esse vengono usate per individuare zone di accumulo ed eventi significativi. I metodi impiegati per calcolare le diverse variabili ambientali sono illustrati nella sezione [Il profilo dell’uso del suolo -deutsch](luseprofile). II codici e le descrizioni utilizzati per individuare gli elementi e i diversi raggruppamenti economici sono trattati in dettaglio nel capitolo [Gruppi di codici -deutsch](codegroups). Le modalità di raccolta dei campioni e i metodi per individuare i valori estremi e calcolare le baseline per una regione sono esposti nella sezione [_Beach litter baselines -deutsch_](threshhold).
# 
# ### Contribuire a questo rapporto 
# 
# l presente rapporto viene continuamente aggiornato e saluta con favore l’invio di articoli o analisi che ne rettificano, chiariscono o migliorano il contenuto. Il modo più semplice per contribuire è inviare una richiesta alla [fine repo di campionamento](https://github.com/hammerdirt-analyst/IQAASL-End-0f-Sampling-2021). Vengono accettati i contributi redatti in tutte le lingue nazionali svizzere.

# (francais_intro_de)=
# ## Avant-propos
# 
# L’objectif du présent projet IQAASL (Identification, quantification and analysis of anthropogenic Swiss litter) est de collecter des données et de développer l’infrastructure nécessaire pour évaluer la composition et la quantité de matériaux d’origine anthropique ayant échoué sur les rivages de certains lacs et cours d’eau suisses. Les résultats de cette étude se présentent sous la forme d’un e-rapport disponible en ligne.
# 
# Au moins trois ouvrages utilisant les données ou explorant les techniques développées dans l’élaboration du présent projet sont en cours d’élaboration :
# 
# __Détection de l'accumulation et des fuites avec Spearman's Rho__, [Repository](https://hammerdirt-analyst.github.io/landuse/titlepage.html), *collaboration avec Louise Schreyers, [Wageningen University and Research](https://www.wur.nl/).   Christian Ludwig, [_Paul Scherer Institute_](https://www.psi.ch/en)/[_EPFL_](https://www.epfl.ch/en/). Montserrat Filella, [_Department F.-A. Forel, University of Geneva_](https://www.unige.ch/forel/fr/).*
# 
# 
# __La probabilité de trouver un objet__ *collaboration avec Romain Tramoy, Laboratoire Eau Environment et Systèmes Urbains [LEESU](https://www.leesu.fr/), Bhavish Patel, [_Paul Scherrer Institute_](https://www.psi.ch/en), Montserrat Filella, [_Department F.-A. Forel, University of Geneva_](https://www.unige.ch/forel/fr/).* [Repository](https://github.com/hammerdirt-analyst/finding-one-object)
# 
# __Surveillance des déchets avec la prochaine génération d'ingénieurs écologues 2016-2021__ *collaboration avec Bhavish Patel, [_Paul Scherrer Institute_](https://www.psi.ch/en), Christian Ludwig, [_Paul Scherer Institute_](https://www.psi.ch/en)/[_EPFL_](https://www.epfl.ch/en/).* [Repository](https://github.com/hammerdirt-analyst/swe)
# 
# ## Méthode d'évaluation
# 
# En 2008, le Programme des Nations Unies pour l’environnement (PNUE) et la Commission océanographique intergouvernementale (COI) {cite}`unepseas`. ont publié les premières lignes directrices relatives à la surveillance des déchets marins (Guidelines on Survey and Monitoring of Marine Litter). Cette méthode a ensuite été reprise en 2010 par la Commission OSPAR {cite}`ospard10` avant que l’UE ne publie à son tour un Guide sur la surveillance des déchets marins dans les mers européennes {cite}`mlwguidance` en 2013. La Suisse est membre d’OSPAR. Dans le cadre du projet IQAASL et des prélèvements antérieurs, plus de 1400 échantillons ont été récoltés et répertoriés en adaptant les méthodes décrites dans ce guide – pensé pour les côtes maritimes – à une application aux lacs et cours d’eau.
# 
# 
# ```{card}
# :class-card: sd-text-black
# :img-top: resources/images/titlepage/conferencepresim.jpg
# :margin: auto
# +++
# __Figure 1:__ *Réaliser un inventaire de déchets sauvages consiste à comptabiliser les matériaux d’origine anthropique visibles qui ont été identifiés dans une zone de rive délimitée d’un lac, d’un cours d’eau ou d’un océan.*
# ```
# <br/>
# 
# * Les zones de relevé sont définies par leurs coordonnées GPS.
# * La longeur et la largeur de chaque zone de relevé sont mesurées.
# * Les déchets visibles dans la zone de relevé sont collectés, classés, comptés et pesés.
# * Tous les objets sont catégorisés en fonction des codes définis dans le guide susmentionné.
# 
# Afin d’identifier les objets d’intérêt régional, des codes supplémentaires ont été ajoutés, par exemple pour les conteneurs d’appâts à phéromones ou les bâtons de ski afin de tenir compte de leur occurrence dans certaines régions. Les procédures de catégorisation et de quantification permettent aux chercheurs ainsi qu’aux parties prenantes de déterminer l’origine probable des articles collectés et de définir des stratégies de réduction spécifiques.   
# 
# Pour plus d'informations: [Groupes de codes -allemand](codegroups).
# 
# ## Périmetètre d’évaluation 
# 
# La valeur médiane (50e percentile) des résultats est définie comme étant le nombre d’éléments (pieces) collectés par transect de 100 m (p/100m). Il s’agit de la méthode décrite dans le document EU Marine Beach Litter Baselines {cite}`eubaselines` et du standard adopté dans le présent rapport. La norme de 100 m de rivage utilisée dans le milieu marin convient pour les régions côtières du continent européen. Cependant, l’urbanisation et la topographie présentent des défis spécifiques lorsqu’il s’agit de sélectionner des sites permettant d’inventorier de manière fiable tout au long de l’année les déchets polluant les abords des lacs et des cours d’eau.
# 
# Limiter les inventaires à 100 m de rivage aurait considérablement restreint le nombre de zones de relevé disponibles ainsi que l’utilisation des données préexistantes. Les longueurs médiane et moyenne de respectivement 45 m et 51 m utilisées dans le projet IQAASL (Identification, quantification and analysis of anthropogenic Swiss litter) reflètent par conséquent la topographie locale. Les données relevées sur moins de 10 m n’ont pas été prises en compte dans l’analyse de base. Les résultats de des inventaires ont été convertis en p/100 m en divisant les valeurs obtenues en mètre linéaire et en les multipliant ensuite par 100. 
# 
# ### Collecte des données
# 
# Un inventaire des déchets retrouvés sur les plages peut être dressé à tout moment par tout un chacun. Si la collecte de données est effectuée selon la méthode décrite dans le guide susmentionné {cite}`mlwguidance`  ou au chapitre [valeurs de reference -allemand](threshhold) le résultat peut être comparé directement aux graphiques présentés ici.   
# 
# ##  Utilisation du présent rapport
# 
# Lors de l’interprétation des résultats, il est important de distinguer valeur médiane {cite}`mediandef` et valeur moyenne {cite}`meandeff` lors de l'interprétation des résultats. À l’exception des résultats mensuels, les résultats indiqués correspondent à la valeur médiane p/100m pour le site considéré.  
# 
# Examinons, à titre d’exemple, le résultat médian des inventaires des objets les plus fréquemment rencontrés sur les bords des lacs de Thoune et de Brienz.  

# ```{glue:figure} t_b_fr
# ```
# __Figure 2:__ _Interprétation des résultats de l’inventaire. Les résultats agrégés de toutes les zones de relevé et du périmètre d’étude de l’Aar figurent dans les deux colonnes à droite et sont précédés par les résultats agrégés des lacs de Thoune et de Brienz. Les six premières colonnes correspondent aux communes dans lesquelles des échantillons ont été prélevés. Ce modèle est appliqué à l’ensemble du document. Le chiffre indiqué représente la valeur médiane relative à chaque objet considéré. Si un objet n’a pas été identifié dans au moins 50 % des inventaires, la valeur médiane sera nulle. La valeur médiane constitue une estimation fiable de la quantité de déchets susceptible d’être trouvée si un inventaire était à nouveau réalisé._

# Les résultats montrent ici que les déchets plastiques issus du secteur de la construction étaient plus fréquents à Bönigen (4,5p/100m) et à Unterseen (1,5p/100m) que dans les autres communes, pour lesquelles la valeur médiane est nulle. Les résultats concernant les films plastiques industriels et les filtres de cigarettes font apparaître que ces objets ont été identifiés sur tous les sites étudiés dans au moins 50 % des inventaires réalisés.
# 
# Concrètement, la probabilité de trouver des déchets plastiques issus du secteur de la construction était plus élevée sur les plages de Bönigen et d’Unterseen que dans les autres localités. En revanche, bien que plus répandus à Brienz (67p/100m), les films plastiques industriels présentaient un taux d’occurrence presque égal sur tous les sites étudiés.  
# 
# Le chapitre dédié aux [Indicateurs statistiques clés -allemand](keyindicators) donne une définition précise des statistiques de base qui peuvent être élaborées à partir des résultats et explique de quelle manière elles peuvent être utilisées pour identifier les lieux de concentration et les événements significatifs. Les méthodes appliquées afin de calculer les différentes variables environnementales sont exposées dans le [Profil d’utilisation des sols -allemand](luseprofile). Les codes et les descriptions utilisés pour identifier les éléments ainsi que les différents groupements économiques sont traités en détail dans [Groupes de codes. -allemand](codegroups). La manière dont les échantillons sont collectés et les méthodes d'identification des valeurs extrêmes et de calcul des lignes de base pour une région se trouvent dans [Beach litter baselines -allemand](threshhold).
# 
# Les résultats de chaque municipalité sont inclus avec le lac ou la rivière à laquelle ils appartiennent. Un rapport plus détaillé peut être produit pour n’importe quelle municipalité dans ce document.    
# 
# ### Contribuer à ce rapport 
# 
# Ce rapport étant dynamique, il est très facile de soumettre des articles ou des analyses qui corrigent, clarifient ou améliorent son contenu. Ceci peut être effectué via une requête Pull au [repo de fin d'échantillonnage](https://github.com/hammerdirt-analyst/IQAASL-End-0f-Sampling-2021). Les soumissions sont acceptées dans toutes les langues officielles suisses.

# In[3]:


doc = SimpleDocTemplate(pdf_link, pagesize=A4, leftMargin=1*cm, rightMargin=1*cm, topMargin=1*cm, bottomMargin=1*cm)
report_url = f'https this will be a link to the url of {doc_title} dot html'
report_name = f"Bericht IQAASL: {this_feature['name']} {start_date} bis {end_date}"

page_info = f'{report_name}; {report_url}'

def myLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Italic',9)
    canvas.drawString(.5*cm, 0.5*cm, "S.%d %s" % (doc.page, page_info))
    canvas.restoreState()
    
doc.build(pdfcomponents,  onFirstPage=myLaterPages, onLaterPages=myLaterPages)

