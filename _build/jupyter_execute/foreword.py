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
# Das Ziel dieses Projekts war es, Daten zu sammeln und die notwendige Infrastruktur zu entwickeln, um die Zusammensetzung und Häufigkeit von anthropogenem Material entlang ausgewählter Schweizer Flüsse und Seen genau zu bewerten und diese Ergebnisse in einem konsolidierten, webbasierten Bericht zu präsentieren.
# 
# Die Ergebnisse dieser Erhebungen werden genutzt, um andere Methoden zur Ermittlung von Akkumulationszonen zu erforschen.
# 
# __Erkennung von Akkumulation und Leckage mit Spearmans Rho__, [Repository](https://hammerdirt-analyst.github.io/landuse/titlepage.html), *Zusammenarbeit mit Louise Schreyers, [Wageningen University and Research](https://www.wur.nl/).   Christian Ludwig, [_Paul Scherer Institute_](https://www.psi.ch/en)/[_EPFL_](https://www.epfl.ch/en/). Montserrat Filella, [_Department F.-A. Forel, University of Geneva_](https://www.unige.ch/forel/fr/).*
# 
# __Die Wahrscheinlichkeit, ein Objekt zu finden__, [Repository](https://github.com/hammerdirt-analyst/finding-one-object), *Zusammenarbeit mit Romain Tramoy, Laboratoire Eau Environment et Systèmes Urbains [LEESU](https://www.leesu.fr/), Bhavish Patel, [_Paul Scherrer Institute_](https://www.psi.ch/en), Montserrat Filella, [_Department F.-A. Forel, University of Geneva_](https://www.unige.ch/forel/fr/).* 
# 
# __Überwachung von Müll mit der nächsten Generation von Umweltingenieuren 2016-2021__, [Repository](https://github.com/hammerdirt-analyst/swe), *Zusammenarbeit mit Bhavish Patel, [_Paul Scherrer Institute_](https://www.psi.ch/en), Christian Ludwig, [_Paul Scherer Institute_](https://www.psi.ch/en)/[_EPFL_](https://www.epfl.ch/en/).* 
# 
# ## Bewertungsmethode
# 
# Im Jahr 2008 wurde der erste internationale Leitfaden zur Überwachung von Abfallobjekten am Strand vom Umweltprogramm der Vereinten Nationen (UNEP) und der Zwischenstaatlichen Ozeanographischen Kommission (IOC) veröffentlicht {cite}`unepseas`. Diese Methode wurde 2010 von der OSPAR-Kommission aufgegriffen {cite}`ospard10`. Im Jahr 2013 veröffentlichte die EU einen Leitfaden zur Überwachung von marinen Abfallobjekten in den europäischen Meeren (The guide) {cite}`mlwguidance`. Die Schweiz ist Mitglied von OSPAR und hat über 1.400 Proben nach den im Leitfaden beschriebenen Methoden genommen. 
# 
# 
# ```{card}
# :class-card: sd-text-black
# :img-top: resources/images/titlepage/conferencepresim.jpg
# :margin: auto
# +++
# *Eine Strand-Abfallaufkommen Untersuchung ist die Erfassung von sichtbarem anthropogenem Material, das in einem abgegrenzten Gebiet identifiziert wurde, das auf einer Seite von einem See, Fluss oder Meer begrenzt wird.*
# ```
# <br/>
# 
# 
# * Standorte werden durch ihre GPS-Punkte definiert 
# * Länge und Breite werden für jeden Erhebungsbereich gemessen 
# * Sichtbare anthropogene Materialien im Untersuchungsgebiet werden gesammelt, klassifiziert, gezählt und gewogen 
# * Alle Artikel werden anhand der im Leitfaden enthaltenen Code-Definitionen klassifiziert.
# 
# Um Objekte von regionalem Interesse zu identifizieren, wurden zusätzliche Codes hinzugefügt. So wurden beispielsweise Codes für Gegenstände wie Pheromon-Köderbehälter und Skistöcke entwickelt, um das Vorkommen dieser Gegenstände in bestimmten Regionen zu berücksichtigen. Die Identifizierung und Quantifizierung von Gegenständen ermöglicht es Forschern und Interessenvertretern, wahrscheinliche Quellen zu bestimmen und Strategien zur Reduzierung bestimmter Gegenstände zu definieren.  
# 
# Für weitere Informationen: [Code-Gruppen](codegroups).
# 
# ## Metrische Bewertung
# 
# Der Medianwert (50. Perzentil) der Datenerhebungen Ergebnisse wird als die Anzahl der Objekte pro 100m (p/100m) der Küstenlinie angegeben. Dies ist die Methode, die in EU Marine Beach Abfallobjekte Baselines{cite}`eubaselines` beschrieben ist und die in diesem Bericht als Standard verwendet wird. Der in der Meeresumwelt verwendete 100-Meter-Standard ist für die Küstenregionen des europäischen Kontinents geeignet. Die Verstädterung und die Topographie stellen jedoch eine besondere Herausforderung bei der Auswahl von Standorten dar, die für die sichere Durchführung von ganzjährigen Datenerhebungen von Abfallobjekten an der Uferzone geeignet sind. 
# 
# Eine Beschränkung der Datenerhebungen auf 100 Meter exponierte Uferlinie hätte die Anzahl der verfügbaren Messstellen sowie die Verwendung bereits vorhandener Daten drastisch reduziert. Daher spiegelt das IQAASL die lokale Topographie mit einer mittleren Erhebungslänge von 45 m und einem Durchschnitt von 51 m wider. Datenerhebungen, die kürzer als 10 m sind, wurden bei der Basisanalyse nicht berücksichtigt. Die Datenerhebungen Ergebnisse werden in p/100m umgerechnet, indem das Ergebnis der Erhebung mit 100 multipliziert wird. 
# 
# __Sammeln von Daten__ 
# 
# Eine Strand-Abfallaufkommen Untersuchung kann jederzeit von jedem durchgeführt werden. Wenn die Untersuchung nach der im Leitfaden {cite}`mlwguidance` beschriebenen Methode oder nach den [Basiswerte für Abfallobjekte an Gewässern](threshhold) kann das Ergebnis direkt mit den Tabellen in diesem Bericht verglichen werden. Es ist nicht notwendig, die Daten in das System einzugeben, um die Ergebnisse zu vergleichen.
# 
# Das Sammeln von Daten für den Bericht (oder den nächsten Bericht) erfordert eine gewisse Einarbeitung und eine Bewertung. Es dauert in der Regel 3-5 Datenerhebungen, um eine Person an die Aufgabe zu gewöhnen. Die meiste Zeit wird damit verbracht, Objekte zu identifizieren und zu lernen, wie wichtig es ist, ein Feldnotizbuch zu führen. Der Vorteil der Datenübermittlung besteht darin, dass das Berichtsverfahren automatisiert ist und man jederzeit Zugriff auf die Ergebnisse hat.
# 
# ---
# 
# ## Erklärung zur Verwendung dieses Berichts 
# 
# Es ist wichtig, den Unterschied zwischen dem _Median_ {cite}`mediandef` und dem _Durchschnitt_ {cite}`meandeff` zu verstehen, wenn Sie die Ergebnisse interpretieren. Mit Ausnahme der monatlichen Ergebnisse werden die Datenerhebungen Ergebnisse als Median p/100m für den jeweiligen Standort angegeben. 
# 
# Betrachten Sie als Beispiel den Median der Datenerhebungen für die häufigsten Objekte am Thuner- und Brienzersee. 

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
# __Oben__: _Interpretation der Datenerhebungen Ergebnisse. Die aggregierten Ergebnisse aus allen Erhebungsgebieten befinden sich in der Spalte ganz rechts, vor den aggregierten Ergebnissen aus dem Thunersee und dem Brienzersee. Die ersten sechs Spalten sind die Gemeinden, in denen die Proben genommen wurden. Dieser Standard wird im gesamten Dokument beibehalten. Die Zahl stellt den Medianwert der Erhebung für dieses Objekt dar. Wenn dieses Objekt in mindestens der Hälfte der Datenerhebungen nicht gefunden wird, ist der Medianwert gleich Null. Der Medianwert ist eine vernünftige Schätzung der Anzahl der Objekte, die bei einer Wiederholung einer Abfallobjekte-Erhebung wahrscheinlich gefunden werden._ 
# 

# Die Ergebnisse für Bauschutt aus Kunststoffen zeigen, dass dieser in Bönigen (4,5p/100m) und Unterseen (1,5p/100m) häufiger vorkommt als in den anderen Gemeinden, wo der Medianwert bei Null liegt. Industriefolien und Zigaretten wurden jedoch in allen Gemeinden in mindestens 1/2 der Datenerhebungen festgestellt. 
# 
# Praktisch gesehen war die Wahrscheinlichkeit, am Strand von Bönigen und Unterseen Bauschutt aus Kunststoff zu finden, größer als in den anderen Gemeinden. Die Wahrscheinlichkeit, Industriefolien zu finden, war jedoch überall ungefähr gleich hoch, am höchsten war sie jedoch in rine (67p/100m). 
# 
# Das Kapitel [Schlüsselindikatoren](keyindicators) enthält eine genaue Definition jeder der grundlegenden Statistiken, die aus den Datenerhebungen abgeleitet werden können, und wie sie zur Identifizierung von Akkumulationszonen und signifikanten Ereignissen verwendet werden. Die Methoden zur Berechnung der verschiedenen Umweltvariablen werden in [_Das Landnutzungsprofil_](luseprofile) erläutert. Die Codes und Beschreibungen, die zur Identifizierung der Objekte verwendet werden, sowie die verschiedenen wirtschaftlichen Gruppierungen werden in [_Codegruppen_](codegroups). detailliert behandelt. Wie Proben gesammelt werden und die Methoden zur Identifizierung von Extremwerten und zur Berechnung von Basiswerten für eine Region finden Sie unter [_Geteilte Verantwortung_](transport). 
# 
# ---

# (italiano_intro_de)=
# ## Prefazione
# 
# Il presente progetto mira a raccogliere dati e a sviluppare l’infrastruttura necessaria per valutare accuratamente la composizione e l’abbondanza di materiale antropogenico lungo fiumi e laghi svizzeri selezionati nonché a presentare questi risultati in un rapporto consolidato basato su web.
# 
# I risultati di queste indagini saranno utilizzati per esplorare altri metodi per rilevare le zone di accumulo.
# 
# __Rilevamento dell'accumulo e della perdita con il Rho di Spearman__,  [Repository](https://hammerdirt-analyst.github.io/landuse/titlepage.html), *collaborazione con Louise Schreyers, [Wageningen University and Research](https://www.wur.nl/).   Christian Ludwig, [_Paul Scherer Institute_](https://www.psi.ch/en)/[_EPFL_](https://www.epfl.ch/en/). Montserrat Filella, [_Department F.-A. Forel, University of Geneva_](https://www.unige.ch/forel/fr/).*
# 
# __La probabilità di trovare un oggetto__, *collaborazione con Romain Tramoy, Laboratoire Eau Environment et Systèmes Urbains [LEESU](https://www.leesu.fr/), Bhavish Patel, [_Paul Scherrer Institute_](https://www.psi.ch/en), Montserrat Filella, [_Department F.-A. Forel, University of Geneva_](https://www.unige.ch/forel/fr/).* [Repository](https://github.com/hammerdirt-analyst/finding-one-object)
# 
# __Monitoraggio dei rifiuti con la prossima generazione di ingegneri ambientali 2016-2021__, *collaborazione con Bhavish Patel, [_Paul Scherrer Institute_](https://www.psi.ch/en), Christian Ludwig, [_Paul Scherer Institute_](https://www.psi.ch/en)/[_EPFL_](https://www.epfl.ch/en/).* [Repository](https://github.com/hammerdirt-analyst/swe)
# 
# ## Metodo di valutazione
# 
# Nel 2008 è stata pubblicata la prima guida internazionale per il monitoraggio del beach litter dal Programma delle Nazioni Unite per l’ambiente (UNEP) e dalla Commissione oceanografica intergovernativa (COI) {cite}`unepseas`. Questo metodo è stato riprodotto dalla Commissione OSPAR nel 2010 {cite}`ospard10`.  Nel 2013 l’UE ha pubblicato una guida sul monitoraggio dei rifiuti marini nei mari europei (La guida) {cite}`mlwguidance`. La Svizzera è membro di OSPAR e ha più di 1.400 campioni che utilizzano i metodi descritti in tale guida. 
# 
# 
# ```{card}
# :class-card: sd-text-black
# :img-top: resources/images/titlepage/conferencepresim.jpg
# :margin: auto
# +++
# *Con un’indagine di beach litter si conta il materiale antropogenico visibile identificato all’interno di un’area delimitata che confina su un lato con un lago, un fiume o un oceano.*
# ```
# <br/>
# 
# 
# * Le posizioni sono definite dai loro punti GPS. 
# * La lunghezza e la larghezza sono misurate per ogni area d’indagine. 
# * Le sostanze inquinanti visibili all'interno dell’area d’indagine vengono raccolte, classificate, contate e pesate. 
# * Tutti gli articoli sono classificati in base alle definizioni dei codici inclusi nella guida. 
# 
# Per identificare oggetti di interesse regionale sono stati aggiunti codici supplementari. Per esempio, sono stati sviluppati codici per oggetti come contenitori di esche a feromoni e bastoncini da sci per rendere conto della presenza di questi oggetti quando identificati in determinate regioni. Identificare e quantificare gli oggetti permette ai ricercatori e alle parti interessate di determinare le probabili fonti e definire strategie di riduzione mirate a oggetti specifici.  
# 
# Per maggiori informazioni: [Gruppi di codici -tedesco](codegroups).
# 
# ## Metrica di valutazione
# 
# Il valore mediano (50ºpercentile) dei risultati dell’indagine viene riportato come numero di oggetti per 100 m (p/100 m) di costa. Questo è il metodo descritto in EU Marine Beach Litter Baselines (Linee guida sui rifiuti ritrovati sulle spiagge marine) {cite}`eubaselines` ed è lo standard usato in questo rapporto. Lo standard di 100 metri di costa usato nell’ambiente marino è appropriato per le regioni costiere del continente europeo. Tuttavia, l’urbanizzazione e la topografia presentano sfide particolari se si tratta di selezionare luoghi adatti a condurre in modo sicuro indagini annuali sui rifiuti costieri. 
# 
# Limitare le indagini a 100 metri di costa esposta avrebbe ridotto drasticamente il numero di luoghi d’indagine disponibili e l’uso di dati preesistenti. Pertanto, l’IQAASL riflette la topografia locale con una lunghezza mediana di sondaggio di 45 m e una media di 51 m. I sondaggi inferiori a 10 m non sono stati considerati nell’analisi di base. I risultati dei sondaggi vengono convertiti in p/100 m moltiplicando il risultato del sondaggio per 100. 
# 
# ### Raccolta di dati
# 
# Un’indagine sul beach litter può essere condotta da chiunque in qualsiasi momento. Se l’indagine viene condotta secondo il metodo descritto nella guida {cite}`mlwguidance` o nel [valori di riferimento -tedesco](threshhold) il risultato può essere confrontato direttamente con i grafici di questo rapporto. Non è necessario inserire i dati nel sistema per confrontare i risultati.  
# 
# __La raccolta di dati__ per il rapporto (o il prossimo rapporto) richiede un po’ di addestramento e una valutazione. Di solito sono necessari 3-5 rilevamenti per comprendere adeguatamente il compito. La maggior parte del tempo viene spesa per identificare gli oggetti e l’importanza di mantenere un taccuino da campo. Il vantaggio di contribuire ai dati è che la procedura di reporting è automatizzata e si ha sempre accesso ai risultati.  
# 
# ##  Usare questo rapporto 
# 
# È importante capire la differenza tra la _mediana_ {cite}`mediandef` e la _media_ {cite}`meandeff` quando si interpretano i risultati. Tranne che per i risultati mensili, i risultati dell’indagine sono dati come la mediana p/100 m per la località in questione. 
# 
# Come esempio, prendiamo in considerazione il risultato __mediano__ del sondaggio per gli oggetti più comuni ritrovati sul Lago di Thun e sul Lago di Brienz. 

# ```{glue:figure} t_b_it
# ```
# __In alto:__ _Interpretazione dei risultati dell’indagine. I risultati aggregati di tutte le aree d’indagine sono nella colonna all’estrema destra,  preceduti dai risultati aggregati del Lago di Thun e del Lago di Brienz. Le prime sei colonne sono i comuni da cui sono stati prelevati i campioni. Questo standard è mantenuto in tutto il documento. Il numero rappresenta il valore mediano del sondaggio per quell’oggetto. Se quell’oggetto non viene trovato in almeno la metà delle indagini, allora il valore mediano sarà zero. Il valore mediano è una stima ragionevole del numero di oggetti che probabilmente verrebbero trovati se si ripetesse un’indagine sui rifiuti._

# I risultati per i rifiuti edili in plastica mostrano che erano più diffusi a Bönigen (4,5 p/100 m) e Unterseen (1,5 p/100 m) rispetto agli altri comuni dove il valore mediano è zero. Tuttavia lamiere industriali e sigarette sono state identificate in tutti i comuni in almeno 1/2 delle indagini.  
# 
# In termini pratici c’erano più possibilità di trovare rifiuti edili in plastica sulla spiaggia a Bönigen e Unterseen che negli altri comuni. Tuttavia le possibilità di trovare teli industriali erano all’incirca uguali ovunque ma il massimo si poteva trovare a Brienz (67 p/100 m). 
# 
# Il capitolo degli [Indicatori chiave -tedesco ](keyindicators) dà una definizione precisa di ciascuna delle statistiche di base che si possono ricavare dai risultati dell’indagine e come vengono usate per identificare zone di accumulo ed eventi significativi. I metodi usati per calcolare le diverse variabili ambientali sono spiegati in [Il profilo dell’uso del suolo -tedesco](luseprofile). I codici e le descrizioni usati per identificare gli elementi e i diversi raggruppamenti economici sono trattati in dettaglio in [Gruppi di codici -tedesco](codegroups). Come si raccolgono i campioni e i metodi per identificare i valori estremi e calcolare le linee di base per una regione si trovano in [_Beach litter baselines -tedesco_](threshhold).
# 
# I risultati per ogni comune indicano il lago o il fiume a cui appartengono. Si può produrre un rapporto più dettagliato per ogni comune in questo documento.  
# 
# ### Contribuire a questo rapporto 
# 
# Questo rapporto indica la versione quindi è molto facile inviare articoli o analisi che correggono, chiariscono o migliorano il contenuto. Per contribuire, basta inviare una richiesta di pull a [fine repo di campionamento](https://github.com/hammerdirt-analyst/IQAASL-End-0f-Sampling-2021). Si accettano richieste redatte in tutte le lingue nazionali ufficiali svizzere.

# (francais_intro_de)=
# ## Avant-propos
# 
# L'objectif de ce projet était de collecter des données et de développer l'infrastructure nécessaire pour évaluer avec précision la composition et l'abondance des matières anthropogènes le long de certains lacs et rivières suisses et de présenter ces résultats dans un rapport consolidé basé sur le Web. 
# 
# Les résultats de ces inventaires sont utilisés pour explorer d'autres méthodes de détection des zones d'accumulation.
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
# En 2008, le premier guide international de surveillance des déchets de plage a été publié par le Programme des Nations Unies pour l'environnement (PNUE) et la Commission océanographique intergouvernementale (COI) {cite}`unepseas`. Cette méthode a été reproduite par la Commission OSPAR en 2010 {cite}`ospard10`. En 2013, l'UE a publié un guide sur la surveillance des déchets marins dans les mers européennes (le guide) {cite}`mlwguidance`. La Suisse est membre d'OSPAR et dispose de plus de 1 400 inventaires utilisant les méthodes décrites dans Le guide. 
# 
# 
# ```{card}
# :class-card: sd-text-black
# :img-top: resources/images/titlepage/conferencepresim.jpg
# :margin: auto
# +++
# *Un __inventaire de déchets__ de plage consiste à comptabiliser les matériaux anthropogènes visibles identifiés dans une zone délimitée qui est bordée d'un côté par un lac, une rivière ou un océan.*
# ```
# <br/>
# * Les emplacements sont définis par leurs points GPS 
# * La longueur et la largeur sont mesurées pour chaque inventaire 
# * Les polluants visibles dans la zone d'étude sont collectés, classés, comptés et pesés. 
# * Tous les articles sont classés en fonction des définitions de code incluses dans Le guide.  
# 
# Afin d'identifier les objets d'intérêt régional, des codes supplémentaires ont été ajoutés. Par exemple, des codes ont été développés pour des objets tels que les conteneurs d'appâts à phéromones et les bâtons de ski afin de tenir compte de l'occurrence de ces objets lorsqu'ils sont identifiés dans certaines régions. L'identification et la quantification des objets permettent aux chercheurs et aux parties prenantes de déterminer les sources probables et de définir des stratégies de réduction ciblant des objets spécifiques.   
# 
# Pour plus d'informations: [Groupes de codes -allemand](codegroups).
# 
# ## Mesure d'évaluation 
# 
# La valeur médiane ( 50e percentile) des résultats des inventaires est rapportée comme le nombre d'objets par 100m (p/100m) de rivage. C'est la méthode décrite dans le document EU Marine Beach Litter Baselines [HG19] et c'est la norme utilisée dans ce rapport. La norme de 100 mètres de rivage utilisée dans le milieu marin est appropriée pour les régions côtières du continent européen. Cependant, l'urbanisation et la topographie présentent des défis uniques lors de la sélection de lieux adaptés. La sécurité et l'accès tout au long de l'année doivent être pris en considération.  
# 
# La valeur médiane ( 50e percentile) des résultats des inventaires est rapportée comme le nombre d'objets par 100m (p/100m) de rivage. C'est la méthode décrite dans le document EU Marine Beach Litter Baselines [HG19] et c'est la norme utilisée dans ce rapport. La norme de 100 mètres de rivage utilisée dans le milieu marin est appropriée pour les régions côtières du continent européen. Cependant, l'urbanisation et la topographie présentent des défis uniques lors de la sélection de lieux adaptés. La sécurité et l'accès tout au long de l'année doivent être pris en considération.  
# 
# ### Collecte des données
# 
# Un inventaire de déchets de plage peut être menée par n'importe qui, à tout moment. Si l'inventaire est menée selon la méthode décrite dans le Guide {cite}`mlwguidance`  ou les [valeurs de reference -allemand](threshhold) le résultat peut être comparé directement aux graphiques de ce rapport. Il n'est pas nécessaire de saisir les données dans le système pour comparer les résultats.   
# 
# La collecte de données pour le rapport (ou le rapport suivant) nécessite une certaine formation sur le tas et une évaluation. Il faut généralement 3 à 5 enquêtes pour acclimater une personne à la tâche. La majeure partie du temps est consacrée à l'identification des objets et à l'importance de tenir un carnet de terrain. L'avantage  de contribuer aux données est que la procédure de rapport est automatisée et qu'il est toujours possible d'accéder aux résultats. 
# 
# ##  Utilisation de ce rapport 
# 
# Il est important de comprendre la différence entre la médiane {cite}`mediandef` et la moyenne {cite}`meandeff` lors de l'interprétation des résultats. À l'exception des résultats mensuels, les résultats des inventaires sont donnés comme la médiane p/100m pour l'emplacement en question.  
# 
# À titre d'exemple, considérons le résultat médian des inventaires pour les objets les plus courants sur Thunersee et le Brienzersee.  

# ```{glue:figure} t_b_fr
# ```
# __Ci-dessus:__ _Interprétation des résultats de l'inventaire. Les résultats agrégés de toutes les zones d'enquêtes figurent dans la colonne d'extrême droite, précédés des résultats agrégés de Thunersee et Brienzersee. Les six premières colonnes correspondent aux municipalités où les échantillons ont été prélevés. Cette norme est maintenue tout au long du document. Le chiffre représente la valeur médiane de l' inventaire pour cet objet. Si cet objet n'est pas trouvé dans au moins la moitié des inventaires, la valeur médiane sera de zéro. La valeur médiane est une estimation raisonnable du nombre d'objets susceptibles d'être trouvés si un inventaire de déchets sauvages était répétée._

# Les résultats pour les déchets de construction en plastique indiquent qu'ils étaient plus répandus à Bönigen (4,5p/100m) et Unterseen (1,5p/100m) par rapport aux autres municipalités où la valeur médiane est de zéro. Cependant, la bâche industrielle et les cigarettes ont été identifiées dans toutes les municipalités dans au moins la moitié des inventaires.  
# 
# Concrètement, il y avait plus de chances de trouver des déchets de construction en plastique sur la plage à Bönigen et Unterseen que dans les autres communes. En revanche, les chances de trouver des bâches industrielles étaient à peu près égales partout, mais c'est à Brienz que l'on pouvait en trouver le plus (67p/100m). 
# 
# Le chapitre sur les [indicateurs clés -allemand](keyindicators) donne une définition précise de chacune des statistiques de base qui peuvent être dérivées des résultats de l' inventaire et de la manière dont elles sont utilisées pour identifier les zones d'accumulation et les événements significatifs. Les méthodes utilisées pour calculer les différentes variables environnementales sont expliquées dans [Le profil d'utilisation des sols -allemand](luseprofile). Les codes et les descriptions utilisés pour identifier les éléments ainsi que les différents groupements économiques sont traités en détail dans [Groupes de codes. -allemand](codegroups). La manière dont les échantillons sont collectés et les méthodes d'identification des valeurs extrêmes et de calcul des lignes de base pour une région se trouvent dans [_valeurs de reference_ -allemand](threshhold).
# 
# Les résultats de chaque municipalité sont inclus avec le lac ou la rivière à laquelle ils appartiennent. Un rapport plus détaillé peut être produit pour n'importe quelle municipalité dans ce document.    
# 
# ### Contribuer à ce rapport 
# 
# Ce rapport est versionné, il est donc très facile de soumettre des articles ou des analyses qui corrigent, clarifient ou améliorent le contenu. Pour contribuer, envoyez une demande de retrait à [repo de fin d'échantillonnage](https://github.com/hammerdirt-analyst/IQAASL-End-0f-Sampling-2021). Les soumissions sont acceptées dans toutes les langues nationales officielles de la Suisse. 

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

