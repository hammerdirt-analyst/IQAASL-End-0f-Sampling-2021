#!/usr/bin/env python
# coding: utf-8

# In[11]:


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
import reportlab
from reportlab.platypus.flowables import Flowable
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle

# the module that has all the methods for handling the data
import resources.featuredata as featuredata
from resources.featuredata import makeAList, small_space, large_space, aSingleStyledTable, smallest_space
from resources.featuredata import caption_style, subsection_title, title_style, block_quote_style
from resources.featuredata import figureAndCaptionTable, tableAndCaption, aStyledTableWithTitleRow
from resources.featuredata import sectionParagraphs, section_title, addToDoc, makeAParagraph, bold_block

# the module that has all the methods for handling the data
import resources.featuredata as featuredata
from resources.featuredata import makeAList

# home brew utitilties
import resources.chart_kwargs as ck
import resources.sr_ut as sut

# images and display
from PIL import Image as PILImage
from IPython.display import Markdown as md
from myst_nb import glue

# chart style
sns.set_style("whitegrid")

# colors for gradients
cmap2 = ck.cmap2
colors_palette = ck.colors_palette

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

# Changing these variables produces different reports
# Call the map image for the area of interest
bassin_map = "resources/maps/bielersee_city_labels.jpeg"

# the label for the aggregation of all data in the region
top = "Alle Erhebungsgebiete"

# define the feature level and components
# the feature of interest is the Aare (aare) at the river basin (river_bassin) level.
# the label for charting is called 'name'
this_feature = {'slug':'bielersee', 'name':"Bielersee", 'level':'water_name_slug'}

# the lake is in this survey area
this_bassin = "aare"
# label for survey area
bassin_label = "Erhebungsgebiet Aare"

# these are the smallest aggregated components
# choices are water_name_slug=lake or river, city or location at the scale of a river bassin 
# water body or lake maybe the most appropriate
this_level = 'city'

# the doctitle is the unique name for the url of this document
doc_title = "bielersee_de"

# identify the lakes of interest for the survey area
lakes_of_interest = ["bielersee"]    


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
    "these_features": this_feature['slug'], 
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
    "these_features": this_feature['slug'],
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

# collects the summarized values for the feature data
# use this to generate the summary data for the survey area
# and the section for the rivers
admin_kwargs = {
    "data":fd,
    "dims_data":dfDims,
    "label": this_feature["name"],
    "feature_component": this_level,
    "date_range":start_end,
    **{"dfBeaches":dfBeaches}
}
admin_details = featuredata.AdministrativeSummary(**admin_kwargs)
admin_summary = admin_details.summaryObject()

# update the admin kwargs with river data to make the river summary
admin_kwargs.update({"data":fdr.feature_data})
admin_r_details = featuredata.AdministrativeSummary(**admin_kwargs)
admin_r_summary = admin_r_details.summaryObject()

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
pdf_link = f'resources/pdfs/key_indicators_de.pdf'
pdfcomponents = []


# (keyindicators)=
# # Statistische Schlüsselindikatoren
# 
# 
# {Download}`Download </resources/pdfs/key_indicators_de.pdf>`

# Die Schlüsselindikatoren sind einfach zu berechnen und werden direkt aus den Erhebungsergebnissen entnommen. Sie sind für die Identifizierung von Akkumulationszonen im Wassereinzugsgebiet unerlässlich. Wenn sie im Rahmen eines Abfallüberwachungsprogramms verwendet und mit spezifischen Kenntnissen über die Umgebung kombiniert werden, helfen die Schlüsselindikatoren, potenzielle Abfallquellen zu identifizieren. {cite}`mlwguidance`
# 
# Auswertungen von Untersuchungen des Strand-Abfallaufkommens beschreiben den Ort, die Häufigkeit und die Zusammensetzung der gefundenen Objekte {cite}`eubaselines`. Die Schlüsselindikatoren beantworten die folgenden Fragen:
# 
# * Welche Objekte werden gefunden?
# * Wie viel wird gefunden? (Gesamtgewichte und Anzahl der Artikel)
# * Wie oft werden diese Objekte gefunden?
# * Wo sind diese Objekte in den grössten Konzentrationen zu finden?
# 
# Ähnlich wie bei der Zählung von Vögeln oder Wildblumen muss eine Person die Erhebung durchführen, um die Zielobjekte zu finden und dann zu identifizieren. Dieser Prozess ist gut dokumentiert und wurde unter vielen Bedingungen getestet.{cite}`ryan2015` {cite}`Rech`
# 
# ## Indikatoren für die am häufigsten gestellten Fragen
# 
# Die Schlüsselindikatoren geben Antworten auf die am häufigsten gestellten Fragen zum Zustand der Abfälle in der natürlichen Umwelt. Die Schlüsselindikatoren sind:
# 
# * Anzahl der Erhebungen
# * Bestehens- und Misserfolgsquote (Häufigkeitsrate)
# * Anzahl der Objekte pro Meter (p/m oder p/m²)
# * Zusammensetzung (prozentualer Anteil an der Gesamtmenge)
# 
# ### Annahmen zu den Schlüsselindikatoren
# 
# Die Zuverlässigkeit dieser Indikatoren beruht auf den folgenden Annahmen:
# 
# * Je mehr Abfallobjekte auf dem Boden liegen, desto grösser ist die Wahrscheinlichkeit, dass eine Person sie findet.
# * Die gefundenen Objekte stellen die Mindestmenge an Abfallobjekten an diesem Erhebungsort dar.
# * Die Erhebenden befolgen das Protokoll und zeichnen die Ergebnisse genau auf.
# * Für jede Datenerhebung: Das Auffinden eines Artikels hat keinen Einfluss auf die Wahrscheinlichkeit, einen anderen zu finden.{cite}`iid`
# 
# ### Verwendung der Schlüsselindikatoren
# 
# Die Schlüsselindikatoren der häufigsten Objekte werden mit jeder Datenzusammenfassung auf jeder Aggregationsebene angegeben. Wenn die vorherigen Annahmen beibehalten werden, sollte die Anzahl der Proben in der Region von Interesse immer als Mass für die Unsicherheit betrachtet werden. Je mehr Proben innerhalb definierter geografischer und zeitlicher Grenzen liegen, desto grösser ist das Vertrauen in die numerischen Ergebnisse, die aus Ergebnissen innerhalb dieser Grenzen gewonnen werden.
# 
# ## Definition: Die am häufigsten gefundenen Objekte
# 
# Die am häufigsten vorkommenden Objekte haben eine Häufigkeitsrate von mindestens 50% und/oder befinden sich in einem bestimmten geografischen Gebiet unter den Top Ten nach Menge oder Stückzahl/m.
# 
# ## Die wichtigsten Indikatoren

# In[12]:


# pdf title and map
pdfcomponents = []
pdf_title = Paragraph("Statistische Schlüsselindikatoren", style=title_style)

p1 = [
    "Die Schlüsselindikatoren sind einfach zu berechnen und werden direkt aus den Erhebungsergebnissen entnommen. ",
    "Sie sind für die Identifizierung von Akkumulationszonen im Wassereinzugsgebiet unerlässlich. Wenn sie im Rahmen ",
    "eines Abfallüberwachungsprogramms verwendet und mit spezifischen Kenntnissen über die Umgebung kombiniert werden, ",
    "helfen die Schlüsselindikatoren, potenzielle Abfallquellen zu identifizieren.",
    '<a href="#Han13" color="blue">(Han13)</a>'
]

p2 = [
    "Auswertungen von Untersuchungen des Strand-Abfallaufkommens beschreiben den Ort, die Häufigkeit und die ",
    'Zusammensetzung der gefundenen Objekte <a href="#HG19" color="blue">(HG19)</a>. Die Schlüsselindikatoren beantworten ',
    "die folgenden Fragen:"
]

p1_2 = sectionParagraphs([p1, p2], smallspace=smallest_space)
first_list = [
    "Welche Objekte werden gefunden?",
    "Wie viel wird gefunden? (Gesamtgewichte und Anzahl der Artikel)",
    "Wie oft werden diese Objekte gefunden?",
    "Wo sind diese Objekte in den grössten Konzentrationen zu finden?"
]

first_list = makeAList(first_list)

p3 = [
    "Ähnlich wie bei der Zählung von Vögeln oder Wildblumen muss eine Person die Erhebung durchführen, um ",
    "die Zielobjekte zu finden und dann zu identifizieren. Dieser Prozess ist gut dokumentiert und wurde ",
    "unter vielen Bedingungen getestet.",
    '<a href="#Rya15" color="blue">(Rya15)</a><a href="#RMCP+15" color="blue">(RMCP+15)</a>'
]

p3 = makeAParagraph(p3)

section_one = Paragraph("Indikatoren für die am häufigsten gestellten Fragen", style=section_title)

p4 = [
    "Die Schlüsselindikatoren geben Antworten auf die am häufigsten gestellten Fragen zum ",
    "Zustand der Abfälle in der natürlichen Umwelt. Die Schlüsselindikatoren sind:"
]

p4 = makeAParagraph(p4)

second_list = [
    "Anzahl der Erhebungen",
    "Bestehens- und Misserfolgsquote (Häufigkeitsrate)",
    "Anzahl der Objekte pro Meter (p/m oder p/m²)",
    "Zusammensetzung (prozentualer Anteil an der Gesamtmenge)"
]

second_list = makeAList(second_list)

subsection_one = Paragraph("Annahmen zu den Schlüsselindikatoren:", style=subsection_title)

p5 = [
    "Die Zuverlässigkeit dieser Indikatoren beruht auf den folgenden Annahmen:"
]

p5 = makeAParagraph(p5)

third_list =[
    "Je mehr Abfallobjekte auf dem Boden liegen, desto grösser ist die Wahrscheinlichkeit, dass eine Person sie findet.",
    "Die gefundenen Objekte stellen die Mindestmenge an Abfallobjekten an diesem Erhebungsort dar.",
    "Die Erhebenden befolgen das Protokoll und zeichnen die Ergebnisse genau auf.",
    'Für jede Datenerhebung: Das Auffinden eines Artikels hat keinen Einfluss auf die Wahrscheinlichkeit, einen anderen zu finden. <a href="#Sta21a" color="blue">(Sta21a)</a>'
]

third_list = makeAList(third_list)

subsection_2 = Paragraph("Verwendung der Schlüsselindikatoren", style=subsection_title)

p6 = [
    "Die Schlüsselindikatoren der häufigsten Objekte werden mit jeder Datenzusammenfassung auf ",
    "jeder Aggregationsebene angegeben. Wenn die vorherigen Annahmen beibehalten werden, sollte die ",
    "Anzahl der Proben in der Region von Interesse immer als Mass für die Unsicherheit betrachtet werden. ",
    "Je mehr Proben innerhalb definierter geografischer und zeitlicher Grenzen liegen, desto grösser ",
    "ist das Vertrauen in die numerischen Ergebnisse, die aus Ergebnissen innerhalb dieser Grenzen gewonnen werden."
]

p6 = makeAParagraph(p6)

subsection_3 = Paragraph("Definition: Die am häufigsten gefundenen Objekte", style=subsection_title)

p7 = [
    "Die am häufigsten vorkommenden Objekte haben eine Häufigkeitsrate von mindestens 50% und/oder ",
    "befinden sich in einem bestimmten geografischen Gebiet unter den Top Ten nach Menge oder Stückzahl/m."
]

p7 = makeAParagraph(p7)

section_2 = Paragraph("Die wichtigsten Indikatoren", style=section_title)

o_w, o_h = convertPixelToCm("resources/maps/aare_city_labels.jpeg")
caption_one = [
    "Im Zeitraum von März 2020 und bis Mai 2021 wurden bei 140 Erhebungen im Aare-Erhebungsgebiet 13 847 Objekte gesammelt."
]

caption_one = makeAParagraph(caption_one, style=caption_style)

figure_kwargs = {
    "image_file":"resources/maps/aare_city_labels.jpeg",
    "caption": None, 
    "original_width":o_w,
    "original_height":o_h,
    "desired_width": 13,
    "caption_height":1,
    "hAlign": "CENTER",
}

first_figure = figureAndCaptionTable(**figure_kwargs)

Han13 = [
    '<a name="Han13"/>Han13: <i>George Hanke</i>. Guidance on monitoring of marine litter in european seas. Joint Research Centre of the European Commission, 2013.'
]

HG19 = [
    '<a name="HG19" />HG19: <i> Van Loon W. Hanke G., Walvoort D.</i> Eu marine beach litter baselines. Publications Office of the European Union, 2019. doi:10.2760/16903.'
]

Sta21a = [
    '<a name="Sta21a" />Sta21a: <i>StackExcahnge.</i> What does independent observations mean? URL: https://stats.stackexchange.com/questions/116355/what-does-independent-observations-mean.'
]

rya15 = [
    '<a name="Rya15" />Rya15: <i>Peter G. Ryan.</i> A Brief History of Marine Litter Research. Springer International Publishing, 2015. : URL: https://doi.org/10.1007/978-3-319-16510-3_1, doi:10.1007/978-3-319-16510-3_1.'
]

rmcp = [
    '<a name="RMCP+15" />RMCP+15: <i>Sabine Rech, Vivian Macaya-Caquilpán, Jose Pantoja, Marcelo Rivadeneira, C Campodónico, and Martin Thiel.</i> Sampling of riverine litter with citizen scientists—findings and recommendations. Environmental monitoring and assessment, 187:4473, 06 2015. doi:10.1007/s10661-015-4473-y.'
]

cp17 = [
    '<a name="CP17" />CP17: <i>Mehran Sahami Chris Piech</i> Parameter estimation. 2017. URL: https://web.stanford.edu/class/archive/cs/cs109/cs109.1192/reader/11%20Parameter%20Estimation.pdf'
]

references = [Paragraph("Bibliographie", style=section_title)]

for citation in [Han13, HG19, Sta21a, rya15, rmcp, cp17]:
    references.append(smallest_space)
    references.append(makeAParagraph(citation))

new_components = [
    pdf_title,    
    small_space,
    *p1_2,
    first_list,
    smallest_space,
    p3,
    small_space,
    section_one,
    small_space,
    p4,
    smallest_space,
    second_list,
    small_space,
    subsection_one,
    small_space,
    p5,
    smallest_space,
    third_list,
    small_space,
    subsection_2,
    small_space,
    p6,
    small_space,
    subsection_3,
    small_space,
    p7,
    PageBreak(),
    section_2,
    small_space,
    first_figure    
]
    

pdfcomponents = addToDoc(new_components, pdfcomponents)


# ```{figure} resources/maps/aare_city_labels.jpeg
# ---
# name: key_indicator_map
# ---
# ` `
# ```
# {numref}`Abbildung %s: <key_indicator_map>` Im Zeitraum von März 2020 und bis Mai 2021 wurden bei 140 Erhebungen im Aare-Erhebungsgebiet 13 847 Objekte gesammelt.

# ```{figure} resources/output/key_indicators_data.jpeg
# ---
# name: key_indicators_data
# ---
# ` `
# ```
# {numref}`Abbildung %s: <key_indicators_data>` Die Resultate des Erhebungsgebiets Aare, mit Ausschnitt Biel/Bienne und Monatsmedian. links: Zusammenfassende Statistik für das Erhebungsgebiet Aare. Rechts: Zusammenfassende Statistik Biel/Bienne.

# In[13]:


o_w, o_h = convertPixelToCm("resources/output/key_indicators_data.jpeg")
caption_two = [
    "Im Zeitraum von März 2020 und bis Mai 2021 wurden bei 140 Erhebungen im Aare-Erhebungsgebiet 13 847 Objekte gesammelt."
]

caption_two = makeAParagraph(caption_two, style=caption_style)

figure_kwargs = {
    "image_file":"resources/output/key_indicators_data.jpeg",
    "caption": caption_two, 
    "original_width":o_w,
    "original_height":o_h,
    "desired_width": 13,
    "caption_height":1,
    "hAlign": "CENTER",
}

second_figure = figureAndCaptionTable(**figure_kwargs)

new_components = [
    small_space,
    second_figure,
    PageBreak()
]
pdfcomponents = addToDoc(new_components, pdfcomponents)


# ### Die Anzahl der Proben
# 
# Die Anzahl der Proben bezieht sich auf die Anzahl der Proben innerhalb eines geografischen und zeitlichen Bereichs. Wie bereits erwähnt, kann den Ergebnissen der Analyse umso mehr Vertrauen geschenkt werden, je mehr Proben innerhalb eines bestimmten Gebiets und Zeitraums vorhanden sind.
# 
# ### Die Häufikeitsrate
# Die Häufigkeitsrate ist die Anzahl der Fälle, in denen ein Objekt mindestens einmal gefunden wurde, geteilt durch die Anzahl der Datenerhebungen.
# 
# __Was bedeutet das?__ Die Häufigkeitsrate beschreibt den Prozentsatz der Fälle, in denen eine Kategorie im Verhältnis zur Anzahl der durchgeführten Datenerhebungen identifiziert wurde. __Hinweis:__ Die Häufigkeitsrate gibt keinen Hinweis auf die Menge.
# 
# Die Häufigkeitsrate ist zu verwenden, um festzustellen, wie häufig ein Objekt innerhalb eines geografischen Bereichs gefunden wurde. Objekte können nach Häufigkeitsrate unterschieden werden. Die Häufigkeitsrate und p/m ist zu verwenden, um Objekte zu identifizieren, die nur selten, aber in grossen Mengen gefunden werden.
# 
# __Unterschiedliche Häufigkeitsraten auf verschiedenen Ebenen__
# 
# Die Häufigkeitsrate wird auf jeder Aggregationsebene berechnet. Daher ändert sich die Häufigkeitsrate für ein bestimmtes Objekt je nach den geografischen Grenzen, die die Aggregationsebene definieren. Für das Erhebungsgebiet Aare sind alle Objekte mit einer Häufigkeitsrate von mindestens 50 % zu betrachten.

# ```{figure} resources/output/fail_rate_key_i.jpeg
# ---
# name: fail_rate_key_i
# ---
# ` `
# ```
# {numref}`Abbildung %s: <fail_rate_key_i>` Die Häufigkeitsraten der am meisten gefundenen Objekte aus dem Erhebungsgebiet Aare bei verschiedenen Aggregationsstufen.

# In[14]:


subsection_4 = Paragraph("Die Anzahl der Proben", style=subsection_title)

p8 = [
    "Die Anzahl der Proben bezieht sich auf die Anzahl der Proben innerhalb eines ",
    "geografischen und zeitlichen Bereichs. Wie bereits erwähnt, kann den Ergebnissen ",
    "der Analyse umso mehr Vertrauen geschenkt werden, je mehr Proben innerhalb eines ",
    "bestimmten Gebiets und Zeitraums vorhanden sind."
]

p8 = makeAParagraph(p8)

subsection_5 = Paragraph("Die Häufikeitsrate", style=subsection_title)

p9 = [
    "Die Häufigkeitsrate ist die Anzahl der Fälle, in denen ein Objekt mindestens ",
    "einmal gefunden wurde, geteilt durch die Anzahl der Datenerhebungen."
]

p10 = [
    "<b>Was bedeutet das?</b> Die Häufigkeitsrate beschreibt den Prozentsatz der Fälle, ",
    "in denen eine Kategorie im Verhältnis zur Anzahl der durchgeführten Datenerhebungen identifiziert wurde. ",
    "<b>Hinweis:</b> Die Häufigkeitsrate gibt keinen Hinweis auf die Menge"
]

p11 = [
    "Die Häufigkeitsrate ist zu verwenden, um festzustellen, wie häufig ein Objekt innerhalb ",
    "eines geografischen Bereichs gefunden wurde. Objekte können nach Häufigkeitsrate unterschieden ",
    "werden. Die Häufigkeitsrate und p/m ist zu verwenden, um Objekte zu identifizieren, die nur ",
    "selten, aber in grossen Mengen gefunden werden."
]

p9_11 = sectionParagraphs([p9, p10, p11], smallspace=smallest_space)
p12 = [
    "Unterschiedliche Häufigkeitsraten auf verschiedenen Ebenen"
]

p12 = makeAParagraph(p12, style=bold_block)

p13 = [
    "Die Häufigkeitsrate wird auf jeder Aggregationsebene berechnet. Daher ändert sich die Häufigkeitsrate ",
    "für ein bestimmtes Objekt je nach den geografischen Grenzen, die die Aggregationsebene definieren. Für ",
    "das Erhebungsgebiet Aare sind alle Objekte mit einer Häufigkeitsrate von mindestens 50 % zu betrachten."
]

p13 = makeAParagraph(p13)

o_w, o_h = convertPixelToCm("resources/output/fail_rate_key_i.jpeg")
caption_3 = [
    "Die Häufigkeitsraten der am meisten gefundenen Objekte aus dem Erhebungsgebiet Aare bei verschiedenen Aggregationsstufen."
]

caption_3 = makeAParagraph(caption_3, style=caption_style)

figure_kwargs = {
    "image_file":"resources/output/fail_rate_key_i.jpeg",
    "caption": caption_3, 
    "original_width":o_w,
    "original_height":o_h,
    "desired_width": 8.4,
    "caption_height":1,
    "hAlign": "CENTER",
}

figure_3 = figureAndCaptionTable(**figure_kwargs)

new_components = [
    subsection_4,
    small_space,
    p8,
    small_space,
    subsection_5,
    small_space,
    *p9_11,
    # p12,
    smallest_space,
    p13,
    small_space,
    figure_3,
   
]
pdfcomponents = addToDoc(new_components, pdfcomponents)


# Mit Ausnahme von Industriefolien und Kunststofffragmenten war die Häufigkeitsrate in Biel/Bienne höher als in allen anderen Untersuchungsgebieten. Das bedeutet, dass die Wahrscheinlichkeit, diese Objekte zu finden, in Biel pro Untersuchung grösser war als an den meisten anderen Orten.
# 
# Die Häufigkeitsrate ist die wahrscheinlichste Schätzung (MLE) der Wahrscheinlichkeit, mindestens ein Objekt zu finden {cite}`mle`. Wenn das Objekt in allen vorherigen Stichproben identifiziert wurde und sich Präventionsmassnahmen nicht geändert haben, kann man davon ausgehen, dass auch in den folgenden Stichproben mindestens ein Objekt zu finden sein wird.
# 
# 
# 
# ### Objekte pro Meter
# 
# Objekte pro Meter (p/m) ist die Anzahl der bei jeder Untersuchung gefundenen Objekte geteilt durch die Länge der untersuchten Uferlinie.
# 
# __Was bedeutet das?__ p/m beschreibt die Menge eines Objekts, das pro Meter gefunden wurde. Es handelt sich um eine Methode zur Normalisierung der Daten aus allen Vermessungen, damit sie verglichen werden können.
# 
# P/m ist zu verwenden um die Objekte zu finden, die in den grössten Mengen gefunden wurden. Mit p/m können Zonen der Anhäufung identifiziert werden.
# 
# Warum nicht die Fläche verwenden? Der EU-Standard empfiehlt, die Ergebnisse als Anzahl der Objekte pro Länge der untersuchten Küstenlinie anzugeben, normalerweise 100 Meter {cite}`eubaselines`. Die Fläche wurde für 99 % aller Erhebungen in IQAASL berechnet. Die Ergebnisse für diese Analyse werden in p/m angegeben.

# ```{figure} resources/output/pcs_m_key_i.jpeg
# ---
# name: pcs_m_key_i
# ---
# ` `
# ```
# {numref}`Abbildung %s: <pcs_m_key_i>` Der Median (p/m) der häufigsten Objekte im Erhebungsgebiet Aare.

# In[15]:


p14 = [
    "Mit Ausnahme von Industriefolien und Kunststofffragmenten war die Häufigkeitsrate in ",
    "Biel/Bienne höher als in allen anderen Untersuchungsgebieten. Das bedeutet, dass die Wahrscheinlichkeit, ",
    "diese Objekte zu finden, in Biel pro Untersuchung grösser war als an den meisten anderen Orten."
]

p15 = [
    "Die Häufigkeitsrate ist die wahrscheinlichste Schätzung (MLE) der Wahrscheinlichkeit, mindestens ein Objekt ",
    'zu finden <a href="#CP17">(CP17)</a>. Wenn das Objekt in allen vorherigen Stichproben identifiziert wurde und sich Präventionsmassnahmen ',
    "nicht geändert haben, kann man davon ausgehen, dass auch in den folgenden Stichproben mindestens ein Objekt zu finden ",
    "sein wird."
]


p14_16 = sectionParagraphs([p14, p15], smallspace=smallest_space)

subsection_6 = Paragraph("Objekte pro Meter", style=subsection_title)

p17 = [
    "Objekte pro Meter (p/m) ist die Anzahl der bei jeder Untersuchung gefundenen Objekte geteilt durch die ",
    "Länge der untersuchten Uferlinie."
]

p18 = [
    "<b>Was bedeutet das?</b> p/m beschreibt die Menge eines Objekts, das pro Meter gefunden wurde. Es handelt ",
    "sich um eine Methode zur Normalisierung der Daten aus allen Vermessungen, damit sie verglichen werden können."
]

p19 = [
    "P/m ist zu verwenden um die Objekte zu finden, die in den grössten Mengen gefunden wurden. Mit p/m können ",
    "Zonen der Anhäufung identifiziert werden."
]

p20 = [
    "Warum nicht die Fläche verwenden? Der EU-Standard empfiehlt, die Ergebnisse als Anzahl der Objekte pro Länge der ",
    'untersuchten Küstenlinie anzugeben, normalerweise 100 Meter <a href="#HG19" color="blue">(HG19)</a>. Die Fläche wurde für 99 % aller Erhebungen in ',
    "IQAASL berechnet. Die Ergebnisse für diese Analyse werden in p/m angegeben."
]

p17_20 = sectionParagraphs([p17, p18, p19, p20], smallspace=smallest_space)

o_w, o_h = convertPixelToCm("resources/output/pcs_m_key_i.jpeg")
caption_4 = [
    "Der Median (p/m) der häufigsten Objekte im Erhebungsgebiet Aare."
]

caption_4 = makeAParagraph(caption_4, style=caption_style)

figure_kwargs = {
    "image_file":"resources/output/pcs_m_key_i.jpeg",
    "caption": caption_4, 
    "original_width":o_w,
    "original_height":o_h,
    "desired_width": 8.4,
    "caption_height":1,
    "hAlign": "CENTER",
}

figure_4 = figureAndCaptionTable(**figure_kwargs)

new_components = [
    *p14_16,
    smallest_space,
    subsection_6,
    small_space,
    *p17_20,
    small_space,
    figure_4,
   
]
pdfcomponents = addToDoc(new_components, pdfcomponents)


# Der angegebene Wert ist der Median der Erhebungsergebnisse für diese Aggregationsebene und dieses Objekt. Ein Medianwert von Null bedeutet, dass das Objekt in weniger als 1/2 der Erhebungen für diese Aggregationsebene identifiziert wurde. Betrachten wir zum Beispiel die Ergebnisse für Dämmstoffe, einschliesslich Spritzschäumen: Der Medianwert für das Erhebungsgebiet Aare ist gleich Null. Betrachtet man jedoch nur die Ergebnisse vom Bielersee oder jene aus Biel/Bienne, ist der Medianwert grösser als Null. Dies deutet darauf hin, dass am Bielersee und speziell in Biel/Bienne mehr Dämmstoffe gefunden wurden als im übrigen Aaregebiet.
# 
# ### Prozentsatz der Gesamtmenge
# 
# Der prozentuale Anteil an der Gesamtzahl ist die Menge eines gefundenen Objekts geteilt durch die Gesamtzahl aller gefundenen Objekte für eine(n) bestimmte(n) Ort/Region und einen bestimmten Datumsbereich.
# 
# __Was bedeutet das?__ Der prozentuale Anteil an der Gesamtmenge beschreibt die Zusammensetzung der gefundenen Abfallobjekte.
# 
# Der prozentuale Anteil an der Gesamtmenge ist zu verwenden, um die wichtigsten Abfallobjekten zu definieren. Mit dem prozentualen Anteil können Prioritäten auf regionaler Ebene ermittelt werden.
# 
# Ähnlich wie bei den Objekten pro Meter ist ein Objekt mit einer niedrigen Häufigkeitsrate und einem hohen Prozentsatz an der Gesamtzahl ein Signal dafür, dass Objekte möglicherweise in unregelmässigen Abständen in grossen Mengen deponiert werden: Verklappung oder Unfälle.

# ```{figure} resources/output/percent_total_i.jpeg
# ---
# name: percent_total_i
# ---
# ` `
# ```
# {numref}`Abbildung %s: <percent_total_i>` Die häufigsten Objekte im Erhebungsgebiet Aare machen rund 66 % (2022) der Gesamtzahl der erfassten Objekte (3067) an den drei Erhebungsorten in Biel/Bienne aus.

# In[16]:


p21 = [
    "Der angegebene Wert ist der Median der Erhebungsergebnisse für diese Aggregationsebene und dieses Objekt. Ein Medianwert ",
    "von Null bedeutet, dass das Objekt in weniger als 1/2 der Erhebungen für diese Aggregationsebene identifiziert wurde. ",
    "Betrachten wir zum Beispiel die Ergebnisse für Dämmstoffe, einschliesslich Spritzschäumen: Der Medianwert für das ",
    "Erhebungsgebiet Aare ist gleich Null. Betrachtet man jedoch nur die Ergebnisse vom Bielersee oder jene aus Biel/Bienne, ",
    "ist der Medianwert grösser als Null. Dies deutet darauf hin, dass am Bielersee und speziell in Biel/Bienne mehr Dämmstoffe ",
    "gefunden wurden als im übrigen Aaregebiet."
]

p21 = makeAParagraph(p21)

subsection_7 = Paragraph("Prozentsatz der Gesamtmenge", style=subsection_title)

p22 = [
    "Der prozentuale Anteil an der Gesamtzahl ist die Menge eines gefundenen Objekts geteilt durch die Gesamtzahl aller ",
    "gefundenen Objekte für eine(n) bestimmte(n) Ort/Region und einen bestimmten Datumsbereich."
]

p23 = [
    "<b>Was bedeutet das?</b> Der prozentuale Anteil an der Gesamtmenge beschreibt die Zusammensetzung der gefundenen Abfallobjekte "
]

p24 = [
    "Der prozentuale Anteil an der Gesamtmenge ist zu verwenden, um die wichtigsten Abfallobjekten zu definieren. Mit dem ",
    "prozentualen Anteil können Prioritäten auf regionaler Ebene ermittelt werden."
]

p25 = [
    "Ähnlich wie bei den Objekten pro Meter ist ein Objekt mit einer niedrigen Häufigkeitsrate und einem hohen Prozentsatz ",
    "an der Gesamtzahl ein Signal dafür, dass Objekte möglicherweise in unregelmässigen Abständen in grossen Mengen deponiert ",
    "werden: Verklappung oder Unfälle."
]

p22_25 = sectionParagraphs([p22, p23, p24, p25], smallspace=smallest_space)


o_w, o_h = convertPixelToCm("resources/output/percent_total_i.jpeg")
caption_5 = [
    "Die häufigsten Objekte im Erhebungsgebiet Aare machen rund 66 % (2022) der Gesamtzahl der erfassten Objekte (3067) an den drei Erhebungsorten in Biel/Bienne aus."
]

caption_5 = makeAParagraph(caption_5, style=caption_style)

figure_kwargs = {
    "image_file":"resources/output/percent_total_i.jpeg",
    "caption": caption_5, 
    "original_width":o_w,
    "original_height":o_h,
    "desired_width": 8,
    "caption_height":1,
    "hAlign": "CENTER",
}

figure_5 = figureAndCaptionTable(**figure_kwargs)
    

new_components = [
    p21,
    small_space,
    subsection_7,
    small_space,
    *p22_25,
    figure_5,
]
pdfcomponents = addToDoc(new_components, pdfcomponents)


# ## Diskussion
# 
# Zwischen April 2020 und Mai 2021 wurden 16 Datenerhebungen an 3 verschiedenen Orten in Biel/Bienne durchgeführt, bei denen 3067 Objekte identifiziert werden konnten. Die häufigsten Objekte aus dem Erhebungsgebiet Aare machen 66 % aller in Biel identifizierten Objekte aus. Objekte, die in direktem Zusammenhang mit dem Konsum stehen (Lebensmittel, Getränke, Tabak), werden in einer Häufigkeit gefunden, die über dem Median des Erhebungsgebiets liegt, den diese Objekte stellen rund 34 % der gesammelten Abfallobjekte in Biel/Bienne dar, im Vergleich zu 25 % für alle Untersuchungsgebiete.
# 
# Objekte, die nicht direkt mit Konsumverhalten in Verbindung stehen, wie zerbrochene Kunststoffe, Industriefolien, expandiertes Polystyrol oder Industriepellets, werden in grösseren Mengen gefunden als im übrigen Erhebungsgebiet Aare. Expandiertes Polystyrol wird als äussere Isolierhülle für Gebäude (Neubauten und Renovierungen) und zum Schutz von Bauteilen beim Transport verwendet. Biel hat eine starke industrielle Basis und eine aktive Bau- und Produktionsbasis. Zusammengenommen machen diese Objekte 30 % der insgesamt gesammelten Objekte aus.
# 
# ### Anwendung
# 
# Bei den Schlüsselindikatoren handelt es sich um einfache Kennzahlen, die direkt aus den Erhebungsergebnissen übernommen wurden. Änderungen in der Grössenordnung dieser Verhältnisse signalisieren Änderungen in der relativen Menge bestimmter Objekte. Wenn die Schlüsselindikatoren im Rahmen eines Überwachungsprogramms verwendet werden, ermöglichen sie die Identifizierung wahrscheinlicher Anreicherungszonen.
# 
# ### Praktische Übung
# 
# Industrielle Kunststoffgranulate (GPI) sind das wichtigste Material zur Herstellung von Kunststoffgegenständen, die in der Schweiz in grossem Umfang verwendet werden. Sie sind scheiben- oder pelletförmig und haben einen Durchmesser von ungefähr 5 mm.
# 
# Beantworten Sie anhand der folgenden Erhebungsergebnisse, der Karte mit den Erhebungsorten und unter Beibehaltung der zu Beginn dieses Artikels dargestellten Annahmen die folgenden Fragen:
# 
# * Wo besteht die grösste Wahrscheinlichkeit, mindestens ein Vorkommen des Abfallobjekts zu finden?
# * Wie gross ist die wahrscheinliche Mindestmenge an Pellets, die Sie bei einer Untersuchung von 50 Metern finden würden?
# * Warum haben Sie sich für diesen Ort oder diese Orte entschieden? Wie sicher sind Sie sich bei Ihrer Wahl?

# In[17]:


section_3 = Paragraph("Diskussion", style=section_title)

p26 = [
    "Zwischen April 2020 und Mai 2021 wurden 16 Datenerhebungen an 3 verschiedenen Orten in Biel/Bienne durchgeführt, ",
    "bei denen 3067 Objekte identifiziert werden konnten. Die häufigsten Objekte aus dem Erhebungsgebiet Aare machen ",
    "66 % aller in Biel identifizierten Objekte aus. Objekte, die in direktem Zusammenhang mit dem Konsum stehen ",
    "(Lebensmittel, Getränke, Tabak), werden in einer Häufigkeit gefunden, die über dem Median des Erhebungsgebiets ",
    "liegt, den diese Objekte stellen rund 34 % der gesammelten Abfallobjekte in Biel/Bienne dar, im Vergleich ",
    "zu 25 % für alle Untersuchungsgebiete."
]

p27 = [
    "Objekte, die nicht direkt mit Konsumverhalten in Verbindung stehen, wie zerbrochene Kunststoffe, Industriefolien, ",
    "expandiertes Polystyrol oder Industriepellets, werden in grösseren Mengen gefunden als im übrigen Erhebungsgebiet ",
    "Aare. Expandiertes Polystyrol wird als äussere Isolierhülle für Gebäude (Neubauten und Renovierungen) und zum Schutz ",
    "von Bauteilen beim Transport verwendet. Biel hat eine starke industrielle Basis und eine aktive Bau- und Produktionsbasis. ",
    "Zusammengenommen machen diese Objekte 30 % der insgesamt gesammelten Objekte aus."
]

p26_27 = sectionParagraphs([p26, p27], smallspace = smallest_space)

subsection_8 = Paragraph("Anwendung", style=subsection_title)

p28 = [
    "Bei den Schlüsselindikatoren handelt es sich um einfache Kennzahlen, die direkt aus den Erhebungsergebnissen übernommen ",
    "wurden. Änderungen in der Grössenordnung dieser Verhältnisse signalisieren Änderungen in der relativen Menge bestimmter ",
    "Objekte. Wenn die Schlüsselindikatoren im Rahmen eines Überwachungsprogramms verwendet werden, ermöglichen sie die ",
    "Identifizierung wahrscheinlicher Anreicherungszonen."
]

p28 = makeAParagraph(p28)

subsection_9 = Paragraph("Praktische Übung", style=subsection_title)

p29 = [
    "Industrielle Kunststoffgranulate (GPI) sind das wichtigste Material zur Herstellung von Kunststoffgegenständen, die ",
    "in der Schweiz in grossem Umfang verwendet werden. Sie sind scheiben- oder pelletförmig und haben einen Durchmesser von ungefähr 5 mm."
]

p30 = [
    "Beantworten Sie anhand der folgenden Erhebungsergebnisse, der Karte mit den Erhebungsorten und unter Beibehaltung der ",
    "zu Beginn dieses Artikels dargestellten Annahmen die folgenden Fragen:"
]

p29_30 = sectionParagraphs([p29, p30], smallspace=smallest_space)

last_list = [
    "Wo besteht die grösste Wahrscheinlichkeit, mindestens ein Vorkommen des Abfallobjekts zu finden?",
    "Wie gross ist die wahrscheinliche Mindestmenge an Pellets, die Sie bei einer Untersuchung von 50 Metern finden würden?",
    "Warum haben Sie sich für diesen Ort oder diese Orte entschieden? Wie sicher sind Sie sich bei Ihrer Wahl?"
]

last_list = makeAList(last_list)


new_components = [
    PageBreak(),
    section_3,
    small_space,
    *p26_27,
    subsection_8,
    small_space,
    p28,
    PageBreak(),
    subsection_9,
    small_space,
    *p29_30,
    last_list,
    smallest_space,
]
pdfcomponents = addToDoc(new_components, pdfcomponents)


# In[18]:


aggs = {'loc_date':'nunique', 'fail':'sum', 'pcs_m':'mean', "quantity":"sum"}
new_col_names = {"loc_date":"Anzahl Proben", "fail":"Anzahl der Fälle", "pcs_m":"Median p/m", "quantity":"Gefunden"}

biel_g95 = fd[(fd.water_name_slug == 'bielersee')&(fd.code == 'G112')].groupby(['location']).agg(aggs)
biel_g95.rename(columns=new_col_names, inplace=True)
biel_g95["Median p/m"] = biel_g95["Median p/m"].round(3)
biel_g95.index.name = None

dims_table_caption = [
    ""
]

# pdf table out
dims_table_caption = ''.join(dims_table_caption)
col_widths = [4.2*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm]

dims_pdf_table = featuredata.aSingleStyledTable(biel_g95, colWidths=col_widths, style=featuredata.default_table_style)
dims_pdf_table_caption = Paragraph(dims_table_caption, style=caption_style)

pdf_table_and_caption = featuredata.tableAndCaption(dims_pdf_table, dims_pdf_table_caption,col_widths)

header_row = {'selector': 'th:nth-child(1)', 'props': f'background-color: #FFF;'}
even_rows = {"selector": 'tr:nth-child(even)', 'props': f'background-color: rgba(139, 69, 19, 0.08);'}
odd_rows = {'selector': 'tr:nth-child(odd)', 'props': 'background: #FFF;'}
table_font = {'selector': 'tr', 'props': 'font-size: 12px;'}
table_css_styles = [even_rows, odd_rows, table_font, header_row]

formatter = {
    "median pcs/m": lambda x: featuredata.replaceDecimal(round(x,3), "de"),
   
}

mcc = biel_g95.style.format(formatter).set_table_styles(table_css_styles)
mcc


# ```{figure} resources/maps/practical_excercise.jpeg
# ---
# name: practical_excercise
# ---
# ` `
# ```
# {numref}`Abbildung %s: <practical_excercise>` Die häufigsten Objekte im Erhebungsgebiet Aare machen rund 66 % (2022) der Gesamtzahl der erfassten Objekte (3067) an den drei Erhebungsorten in Biel/Bienne aus.

# In[19]:


o_w, o_h = convertPixelToCm("resources/maps/practical_excercise.jpeg")

figure_kwargs = {
    "image_file":"resources/maps/practical_excercise.jpeg",
    "caption": None, 
    "original_width":o_w,
    "original_height":o_h,
    "desired_width": 14,
    "caption_height":1,
    "hAlign": "CENTER",
}

figure_6 = figureAndCaptionTable(**figure_kwargs)

new_components = [
    pdf_table_and_caption,
    small_space,
    figure_6,
    PageBreak(),  
    *references
]
pdfcomponents = addToDoc(new_components, pdfcomponents)


# In[20]:


doc = SimpleDocTemplate(pdf_link, pagesize=A4, leftMargin=2.5*cm, rightMargin=1.5*cm, topMargin=3*cm, bottomMargin=1.5*cm)

page_info = "IQAASL: Statistische Schlüsselindikatoren"

def myLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Italic',9)
    canvas.drawString(1*cm, 1*cm, "S.%d %s" % (doc.page, page_info))
    canvas.restoreState()
    
doc.build(pdfcomponents,  onFirstPage=myLaterPages, onLaterPages=myLaterPages)


# In[ ]:





# In[ ]:





# In[ ]:




