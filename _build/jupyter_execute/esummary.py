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
import scipy.stats as stats

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
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

from reportlab.platypus.flowables import Flowable
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle

# the module that has all the methods for handling the data
import resources.featuredata as featuredata
from resources.featuredata import makeAList, small_space, large_space, aSingleStyledTable, smallest_space
from resources.featuredata import caption_style, subsection_title, title_style, block_quote_style, makeBibEntry
from resources.featuredata import figureAndCaptionTable, tableAndCaption, aStyledTableWithTitleRow
from resources.featuredata import sectionParagraphs, section_title, addToDoc, makeAParagraph, bold_block
from resources.featuredata import makeAList

# home brew utitilties
import resources.chart_kwargs as ck
import resources.sr_ut as sut

# images and display
import IPython
from IPython.display import Markdown as md
from IPython.display import HTML
from PIL import Image as PILImage
from myst_nb import glue

def convertPixelToCm(file_name: str = None):
    im = PILImage.open(file_name)
    width, height = im.size
    dpi = im.info.get("dpi", (72, 72))
    width_cm = width / dpi[0] * 2.54
    height_cm = height / dpi[1] * 2.54
    
    return width_cm, height_cm


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
bassin_map = "resources/maps/all_survey_areas_summary.jpeg"

# the label for the aggregation of all data in the region
top = "Alle Erhebungsgebiete"

# define the feature level and components
# the feature of interest is the all (all) at the river basin (river_bassin) level.
# the label for charting is called 'name'
this_feature = {'slug':'all', 'name':"Alle Erhebungsgebiete", 'level':'all'}

# these are the smallest aggregated components
# choices are water_name_slug=lake or river, city or location at the scale of a river bassin 
# water body or lake maybe the most appropriate
this_level = 'river_bassin'

# the doctitle is the unique name for the url of this document
doc_title = "lakes_rivers"


# # identify the lakes of interest for the survey area
# lakes_of_interest = ["neuenburgersee", "thunersee", "bielersee", "brienzersee"]   

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
    "feature_parent":this_feature['slug'],
    "parent_level": this_feature['level'],
    "period_name": top,
    "unit_label": unit_label,
    "most_common": fdx.most_common.index
}
period_data = featuredata.PeriodResults(**period_kwargs)

# the rivers are considered separately
# select only the results from rivers
fd_kwargs.update({"water_type":"r"})
fdr = featuredata.Components(**fd_kwargs)
fdr.makeFeatureData()
fdr.adjustForLanguage()
fdr.makeFeatureData()
fdr.locationSampleTotals()
fdr.makeDailyTotalSummary()
fdr.materialSummary()
fdr.mostCommon()

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


# pdf download is an option 
# the .pdf output is generated in parallel
# this is the same as if it were on the backend where we would
# have a specific api endpoint for .pdf requests. 
# reportlab is used to produce the document
# the components of the document are captured at run time
# the pdf link gives the name and location of the future doc
pdf_link = f'resources/pdfs/esummary.pdf'

# the components are stored in an array and collected as the script runs
pdfcomponents = []

# pdf title and map
# pdf_title = Paragraph(this_feature["name"], featuredata.title_style)
# map_image =  Image(bassin_map, width=cm*19, height=20*cm, kind="proportional", hAlign= "CENTER")

map_caption = [
    "Karte der Erhebungsstandorte März 2020–August 2021. Die rot dargestellten Standorte betreffen Erhebungen an Fliessgewässern oder Seen, ",
    "die violetten Punkte sind die Standorte in den Alpen und im Jura."
]
f1cap = makeAParagraph(map_caption, featuredata.caption_style),


def convertPixelToCm(file_name: str = None):
    im = PILImage.open(file_name)
    width, height = im.size
    dpi = im.info.get("dpi", (72, 72))
    width_cm = width / dpi[0] * 2.54
    height_cm = height / dpi[1] * 2.54
    
    return width_cm, height_cm

astyle = "'display:flex; align-content:center; flex-flow:column no-wrap; flex-direction:column; width80%;  box-shadow: 0px 0px 3px #d2d9db'"


def cardFigure(html_table: str=None, table_caption: str=None, style: str=astyle):
    
    
    figure_in_a_card = f"""
    <div style={style}>
        <div style='padding:10px;'>
            {html_table}
        </div>
        <div style='border-top: 1px solid #d2d9db;'>
            <p style='margin:10px'><i>{table_caption}</i></p>
        </div>
    </div>
                    """
    
    return figure_in_a_card


# In[2]:


glue('esummary_map_caption', map_caption, display=False)

o_w, o_h = convertPixelToCm("resources/maps/esummary_map.jpeg")

figure_kwargs = {
    "image_file":"resources/maps/esummary_map.jpeg",
    "caption": f1cap, 
    "original_width":o_w,
    "original_height":o_h,
    "desired_width": 14,
    "caption_height":1,
    "hAlign": "CENTER",
}

f1 = figureAndCaptionTable(**figure_kwargs)


# # Kurzfassung
# 
# {Download}`Download </resources/pdfs/esummary.pdf>`
# 
# 
# | [Italiano](italiande)| [Français](francaisde) |
# 
# Beim Projekt «Identification, quantification and analysis of anthropogenic Swiss litter» (Identifizierung, Quantifizierung und Analyse von anthropogenem Abfall in der Schweiz, IQAASL) handelt es sich um ein vom Bundesamt für Umwelt (BAFU) in Auftrag gegebenes Projekt zur Erhebung von Daten über sichtbare Schadstoffe an Schweizer Seen und Flüssen. Mit Hilfe von Datenerhebungen wurden Abfallobjekte gesammelt und identifiziert, alle weggeworfenen Materialien wurden eingesammelt. Das Projekt wurde auf 20 Standorte in den Alpen und im Jura ausgeweitet, insgesamt wurden 406 Erhebungen von 163 Standorten in 95 Gemeinden genommen. 
#     
# In diesem Bericht werden die vom März 2020 bis August 2021 durchgeführten Abfallerhebungen sowie die in der Schweiz angewandten Methoden zusammengefasst und analysiert. Diese Erhebungsphase überschneidet sich mit dem Erhebungszeitraum des Swiss Litter Reports (SLR) {cite}`slr`, dessen Erhebungen von April 2017 bis März 2018 durchgeführt worden sind. Der SLR war das erste nationale Projekt, bei dem das Standardprotokoll gemäss dem Leitfaden zur Überwachung von Strandabfällen  {cite}`mlwguidance` oder eine andere vergleichbare Methode angewandt wurde. Diese Überschneidung der Erhebungsphasen ermöglicht es, die Ergebnisse der vorliegenden Studie mit denen des SLR zu vergleichen. 
# 
# ```{card}
# :class-card: sd-text-black
# :img-top: resources/maps/esummary_map.jpeg
# +++
# Figure : Karte der Erhebungsstandorte März 2020–August 2021. Die rot dargestellten Standorte betreffen Erhebungen an Fliessgewässern oder Seen, die violetten Punkte sind die Standorte in den Alpen und im Jura.
# ```
# Gesamtwerte der Erhebungen nach Datum.
# {numref}`Abbildung %s: <esummarymap_de>` Karte der Erhebungsstandorte März 2020–August 2021. Die rot dargestellten Standorte betreffen Erhebungen an Fliessgewässern oder Seen, die violetten Punkte sind die Standorte in den Alpen und im Jura.
# 
# ##  Seen und Flüsse 
# 
# Die Proben an Seen und Fliessgewässern wurden vom März 2020 bis Mai 2021 entnommen. Im Rahmen von 386 Erhebungen wurden insgesamt 54’744 Gegenstände eingesammelt und klassifiziert. Die Erhebungsstandorte wurden für die regionale Analyse zu Erhebungsgebieten zusammengefasst und durch die Flüsse Aare, Rhone, Ticino und Linth/Limmat definiert. Die Erhebungen fanden an 143 verschiedenen Standorten in 77 Gemeinden statt. Insgesamt wurde eine lineare Strecke von 20 km mit einer Fläche von 9 Hektaren und einer Gesamtbevölkerung von 1,7 Millionen Personen untersucht.
# 
# Die meisten Erhebungen wurden an Seeufern durchgeführt (331 Proben), da Seen im Vergleich zu Fliessgewässern einen beständigeren und sichereren ganzjährigen Zugang bieten. Des Weiteren besitzen Seen grosse Flächen mit verringerter Fliessgeschwindigkeit, die von verschiedenen Flüssen, Bächen und Entwässerungssystemen gespeist werden. Damit sind sie ideale Standorte, um die Vielfalt der Gegenstände in und rund um die Gewässer zu beurteilen. Die insgesamt 316 Proben stammten aus sieben grossen Seen in drei grossen Einzugsgebieten. Zwanzig Standorte wurden für eine monatliche Probenahme während zwölf Monaten ausgewählt, mit Ausnahme des Lago Maggiore, der alle drei Monate beprobt wurde. Auch am Luganersee, am Vierwaldstättersee, am Brienzersee und am Zugersee wurden Erhebungen durchgeführt. Darüber hinaus fanden 55 Erhebungen an 16 Fliessgewässern statt.
# 
# Seestandorte mit monatlichen Probenahmen:
# 
# * Erhebungsgebiet Aare
#   * Thunersee: Spiez, Unterseen
#   * Bielersee: Biel/Bienne, Vinelz
#   * Neuenburgersee: Neuenburg, Cheyres-Châbles, Yverdon-les-Bains
# 
# * Erhebungsgebiet Linth/Limmat
#   * Zürichsee: Zürich, Küsnacht (ZH), Rapperswil-Jona, Richterswil
#   * Walensee: Walenstadt, Weesen
# 
# * Erhebungsgebiet Rhone
#   * Genfersee: Vevey, Saint-Gingolph, Genf, Préverenges, La Tour-de-Peilz
# 
# * Erhebungsgebiet Ticino
#   * Lago Maggiore: Ascona, Gambarogno (dreimonatlich)

# In[3]:


# start pdf
pdf_title = Paragraph("Kurzfassung", featuredata.title_style)

p1 = [
    "Identifikation, Quantifizierung und Analyse von anthropogenem Abfall in der Schweiz (IQAASL) ist ein vom Bundesamt für Umwelt (BAFU) in ",
    "Auftrag gegebenes Projekt zur Erhebung von Daten über sichtbare Schadstoffe an Schweizer Seen und Flüssen. Mit Hilfe von Datenerhebungen ",
    "wurden Abfallobjekte gesammelt und identifiziert, alle weggeworfenen Materialien wurden eingesammelt. Das Projekt wurde auf 20 Standorte in ",
    "den Alpen und im Jura ausgeweitet, insgesamt wurden 406 Erhebungen von 163 Standorten in 95 Gemeinden genommen." 
]

p2 = [
    "In diesem Bericht werden die vom März 2020 bis August 2021 durchgeführten Abfallerhebungen sowie die in der Schweiz angewandten Methoden zusammengefasst ",
    "und analysiert. Diese Erhebungsphase überschneidet sich mit dem Erhebungszeitraum des Swiss Litter Reports ",
    '<a href="#Bla18" color="blue">(SLR)</a>, ',
    "dessen Erhebungen von April 2017 bis März 2018 durchgeführt worden sind. Der SLR war das erste nationale Projekt, bei dem das Standardprotokoll ",
    "gemäss dem Leitfaden zur Überwachung von Strandabfällen ", 
    '<a href="#Han13" color="blue">(Han13)</a> ',
    "oder eine andere vergleichbare Methode angewandt wurde. Diese Überschneidung der Erhebungsphasen ermöglicht es, die Ergebnisse der vorliegenden ",
    "Studie mit denen des SLR zu vergleichen."
]

sec1 = Paragraph("Seen und Fliessgewässer", style=section_title)

p3 = [
    "Die Proben an Seen und Fliessgewässern wurden vom März 2020 bis Mai 2021 entnommen. Im Rahmen von 386 Erhebungen wurden insgesamt ",
    "54’744 Gegenstände eingesammelt und klassifiziert. Die Erhebungsstandorte wurden für die regionale Analyse zu Erhebungsgebieten zusammengefasst ",
    "und durch die Flüsse Aare, Rhone, Ticino und Linth/Limmat definiert. Die Erhebungen fanden an 143 verschiedenen Standorten in 77 Gemeinden statt. ",
    "Insgesamt wurde eine lineare Strecke von 20 km mit einer Fläche von 9 Hektaren und einer Gesamtbevölkerung von 1,7 Millionen Personen untersucht."
]
p1_2 = sectionParagraphs([p1, p2], smallspace=smallest_space)

p4 = [
    "Die meisten Erhebungen wurden an Seeufern durchgeführt (331 Proben), da Seen im Vergleich zu Fliessgewässern einen beständigeren und sichereren ganzjährigen ",
    "Zugang bieten. Des Weiteren besitzen Seen grosse Flächen mit verringerter Fliessgeschwindigkeit, die von verschiedenen Flüssen, Bächen und Entwässerungssystemen ",
    "gespeist werden. Damit sind sie ideale Standorte, um die Vielfalt der Gegenstände in und rund um die Gewässer zu beurteilen. Die insgesamt 316 Proben stammten ",
    "aus sieben grossen Seen in drei grossen Einzugsgebieten. Zwanzig Standorte wurden für eine monatliche Probenahme während zwölf Monaten ausgewählt, mit Ausnahme ",
    "des Lago Maggiore, der alle drei Monate beprobt wurde. Auch am Luganersee, am Vierwaldstättersee, am Brienzersee und am Zugersee wurden Erhebungen durchgeführt. "
    "Darüber hinaus fanden 55 Erhebungen an 16 Fliessgewässern statt."
]


p3_4 = sectionParagraphs([p3, p4], smallspace=smallest_space)

p5 = Paragraph("Seestandorte mit monatlichen Probenahmen:", style=bold_block)

p6 = Paragraph("Erhebungsgebiet Aare", style=bold_block)

l1 = [
    "Thunersee: Spiez, Unterseen",
    "Bielersee: Biel/Bienne, Vinelz",
    "Neuenburgersee: Neuenburg, Cheyres-Châbles, Yverdon-les-Bains"
]

l1 = makeAList(l1)
p7 = Paragraph("Erhebungsgebiet Linth/Limmat", style=bold_block)

l2 = [
    "Zürichsee: Zürich, Küsnacht (ZH), Rapperswil-Jona, Richterswil",
    "Walensee: Walenstadt, Weesen",
]
l2 = makeAList(l2)

p8 = Paragraph("Erhebungsgebiet Rhone", style=bold_block)

l3 = [
    "Genfersee: Vevey, Saint-Gingolph, Genf, Préverenges, La Tour-de-Peilz",
]
l3 = makeAList(l3)

p9 = Paragraph("Erhebungsgebiet Ticino", style=bold_block)
l4 = [
    "Lago Maggiore: Ascona, Gambarogno (dreimonatlich)"
]
l4 = makeAList(l4)

new_components = [
     pdf_title,    
    small_space,
    f1,
    smallest_space,
    *p1_2,
    small_space,
    sec1,
    small_space,
    *p3_4,
    smallest_space,
    p5,
    smallest_space,
    p6,
    smallest_space,
    l1,
    smallest_space,
    p7,
    smallest_space,
    l2,
    smallest_space,
    p8,
    smallest_space,
    l3,
    smallest_space,
    p9,
    smallest_space,
    l4
    
]
# add those sections
pdfcomponents = addToDoc(new_components, pdfcomponents)


# In[4]:


# the bibiliography entries for the article:

def aBibEntry(name, team, pub):
    # formats the bib entries according to the
    # original version
    return makeAParagraph(makeBibEntry(name=name, team=team, pub=pub))

name = "Han13"
team = "George Hanke."
pub = "Guidance on monitoring of marine litter in european seas. Joint Research Centre of the European Commission, 2013. URL: https://indicit-europa.eu/cms/wp-content/uploads/2017/05/guidance_monitoring_marine_litter_2013.pdf."
han13 = aBibEntry(name, team, pub)

name = "Kuh"
team = "Gabrielle Kuhl."
kuh = "Stop plastic polution switzerland. URL: http://stoppp.org/."
kuh = aBibEntry(name, team, pub)

name = "Fun"
team = "World Wildlife Fund."
pub = "World wildlife fund switzerland. URL: https://www.wwf.ch/fr."
fun = aBibEntry(name, team, pub)

name = "Bla18"
team = "Pascal Blarer.",
pub = "The swiss litter report. 2018. URL: http://stoppp.org/researchvalue."
bla18 = aBibEntry(name, team, pub)

name = "vEV21"
team = "T.H.M. van Emmerik and P. Vriend."
pub = "Roadmap litter monitoring in dutch rivers. Wageningen University, Report., 2021. doi:10.18174/537439."
vev21 = aBibEntry(name, team, pub)

HG19 = [
    '<a name="HG19" />HG19: <i> Van Loon W. Hanke G., Walvoort D.</i> Eu marine beach litter baselines. Publications Office of the European Union, 2019. doi:10.2760/16903.'
]

hg19 = makeAParagraph(HG19)

references = [
    han13,
    smallest_space,
    kuh,
    smallest_space,
    fun,
    smallest_space,
    bla18,
    smallest_space,
    vev21,
    smallest_space,
    hg19
]


# ### Medianwert der Erhebungen
# 
# Die Ergebnisse werden in der Einheit Abfallobjekte (pieces) pro 100 Meter (p/100 m) angegeben. Der Median der Erhebungsergebnisse aller Daten lag bei rund 189 p/100 m. Der höchste verzeichnete Wert betrug 6617 p/100 m (Erhebungsgebiet Rhone) und der tiefste Wert 2 p/100 m (Erhebungsgebiet Aare). Das Erhebungsgebiet Rhone wies von allen Erhebungen mit 442 p/100 m den höchsten Medianwert auf. Dies kann zum Teil durch die im Vergleich zu den anderen Erhebungsgebieten hohe Anzahl städtischer Erhebungsstandorte sowie durch die Ablagerung von fragmentierten Kunststoffen und Schaumstoffen am Ausfluss der Rhone im oberen Seebereich erklärt werden.
# 
# Weiter wurde ein Referenzwert berechnet, bei dem die Ergebnisse von Proben von Uferabschnitten mit einer Länge von weniger als 10 m und Gegenständen kleiner als 2,5 cm ausgeschlossen wurden. Diese in den Marine Beach Litter Baselines der EU {cite}`eubaselines` beschriebene Methode wurde verwendet, um die Referenz- und Schwellenwerte für alle europäischen Strände für die Jahre 2015 und 2016 zu berechnen. In Anwendung dieser Methode resultierte ein Medianwert von 131 p/100 m. Die Ergebnisse des europäischen Basiswerts liegen ausserhalb des Konfidenzintervalls (KI) von 95 % von 147–213 p/100 m, das anhand der IQAASL-Daten ermittelt wurde.
# 
# Die Erhebungen in der Schweiz waren im Durchschnitt kleinräumiger als in Meeresgebieten sowie an Standorten, die unter den meisten Umständen als städtisch eingestuft würden. Bisher werden See und Fliessgewässer flussaufwärts von Küstenregionen auf dem europäischen Kontinent noch nicht flächendeckend überwacht. Allerdings gibt es gemeinsame Bestrebungen einer Gruppe von Organisationen in der Schweiz und in Frankreich, um ein gemeinsames Überwachungs- und Datenaustauschprotokoll für das Rhonebecken einzuführen. Ausserdem setzt die Universität Wageningen für die Analyse von im Maas-Rhein-Delta erhobenen Daten seit Kurzem ähnliche Protokolle wie bei IQAASL ein. {cite}`meuserhine`
# 
# ### Die am häufigsten gefundenen Gegenstände
# 
# Als die am häufigsten gefundenen Gegenstände gelten Objekte, die in mindestens der Hälfte aller Erhebungen festgestellt wurden und/oder die zu den zehn mengenmässig am häufigsten vorkommenden Gegenständen gehören. Diese häufigsten Gegenstände stellen als Gruppe 68 Prozent aller im Probezeitraum identifizierten Objekte dar. Von den häufigsten Gegenständen fallen 27 Prozent in die Bereiche Lebensmittel, Getränke und Tabakwaren und 24 Prozent stehen im Zusammenhang mit Infrastruktur und Landwirtschaft.
# 
# Gegenstände im Zusammenhang mit Lebensmitteln, Getränken und Tabakwaren werden häufiger an Erhebungsstandorten gefunden, an denen ein grösserer Landanteil von Gebäuden oder festen Infrastrukturen beansprucht wird, ganz im Gegensatz zu Standorten mit einem grösseren Anteil an Wäldern oder landwirtschaftlichen Flächen. Infrastrukturmaterial und fragmentierte Kunststoffe werden allerdings in allen Erhebungsgebieten unabhängig von der Landnutzung rund um die Erhebungsstandorte ähnlich häufig gefunden.

# In[5]:


ssec1 = Paragraph("Medianwert der Erhebungen", style=subsection_title)

p10 = [
    "Die Ergebnisse werden in der Einheit Abfallobjekte (pieces) pro 100 Meter (p/100 m) angegeben. Der Median der Erhebungsergebnisse aller ",
    "Daten lag bei rund 189 p/100 m. Der höchste verzeichnete Wert betrug 6617 p/100 m (Erhebungsgebiet Rhone) und der tiefste Wert 2 p/100 m ",
    "(Erhebungsgebiet Aare). Das Erhebungsgebiet Rhone wies von allen Erhebungen mit 442 p/100 m den höchsten Medianwert auf. Dies kann zum Teil durch ",
    "die im Vergleich zu den anderen Erhebungsgebieten hohe Anzahl städtischer Erhebungsstandorte sowie durch die Ablagerung von fragmentierten Kunststoffen ",
    "und Schaumstoffen am Ausfluss der Rhone im oberen Seebereich erklärt werden."
]

p11 = [
    "Weiter wurde ein Referenzwert berechnet, bei dem die Ergebnisse von Proben von Uferabschnitten mit einer Länge von weniger als 10 m und Gegenständen kleiner als ",
    "2,5 cm ausgeschlossen wurden. Diese in den Marine Beach Litter Baselines der ",
    '<a href="#HG19" color="blue">(HG19)</a> beschriebene Methode wurde verwendet, ',
    "um die Referenz- und Schwellenwerte für alle europäischen Strände für die Jahre 2015 und 2016 zu berechnen. In Anwendung dieser Methode resultierte ein Medianwert ", 
    "von 131 p/100 m. Die Ergebnisse des europäischen Basiswerts liegen ausserhalb des Konfidenzintervalls (KI) von 95 % von 147–213 p/100 m, das anhand der ",
    "IQAASL-Daten ermittelt wurde.",
]

p12 = [
    "Die Erhebungen in der Schweiz waren im Durchschnitt kleinräumiger als in Meeresgebieten sowie an Standorten, die unter den meisten Umständen als städtisch eingestuft ",
    "würden. Bisher werden See und Fliessgewässer flussaufwärts von Küstenregionen auf dem europäischen Kontinent noch nicht flächendeckend überwacht. Allerdings gibt es ",
    "gemeinsame Bestrebungen einer Gruppe von Organisationen in der Schweiz und in Frankreich, um ein gemeinsames Überwachungs- und Datenaustauschprotokoll für das ",
    "Rhonebecken einzuführen. Ausserdem setzt die Universität Wageningen für die Analyse von im Maas-Rhein-Delta erhobenen Daten seit Kurzem ähnliche Protokolle wie bei ",
    'IQAASL ein. <a href="#vEV21" color="blue">(vEV21)</a>'
]

p10_12 = sectionParagraphs([p10, p11, p12], smallspace=smallest_space)

ssec2 = Paragraph("Die am häufigsten gefundenen Gegenstände", style=subsection_title)

p13 = [
    "Als die am häufigsten gefundenen Gegenstände gelten Objekte, die in mindestens der Hälfte aller Erhebungen festgestellt wurden und/oder die zu den zehn ",
    "mengenmässig am häufigsten vorkommenden Gegenständen gehören. Diese häufigsten Gegenstände stellen als Gruppe 68 Prozent aller im Probezeitraum identifizierten ",
    "Objekte dar. Von den häufigsten Gegenständen fallen 27 Prozent in die Bereiche Lebensmittel, Getränke und Tabakwaren und 24 Prozent stehen im Zusammenhang mit ",
    "Infrastruktur und Landwirtschaft.",
]

p14 = [
    "Gegenstände im Zusammenhang mit Lebensmitteln, Getränken und Tabakwaren werden häufiger an Erhebungsstandorten gefunden, an denen ein grösserer Landanteil ",
    "von Gebäuden oder festen Infrastrukturen beansprucht wird, ganz im Gegensatz zu Standorten mit einem grösseren Anteil an Wäldern oder landwirtschaftlichen ",
    "Flächen. Infrastrukturmaterial und fragmentierte Kunststoffe werden allerdings in allen Erhebungsgebieten unabhängig von der Landnutzung rund um die ",
    "Erhebungsstandorte ähnlich häufig gefunden."
]

p13_14 = sectionParagraphs([p13, p14], smallspace=smallest_space)

new_components = [
    small_space,
    ssec1,
    small_space,
    *p10_12,
    ssec2,
    small_space,
    *p13_14
    
   
]
# add those sections
pdfcomponents = addToDoc(new_components, pdfcomponents)


# In[6]:


# the most common objects results
most_common_display = fdx.most_common

# language appropriate columns
cols_to_use = featuredata.most_common_objects_table_de
cols_to_use.update({unit_label:unit_label})

# data for display
most_common_display.rename(columns=cols_to_use, inplace=True)
most_common_display = most_common_display[cols_to_use.values()].copy()
most_common_display = most_common_display.set_index("Objekte", drop=True)

# .pdf output
data = most_common_display.copy()
data["Anteil"] = data["Anteil"].map(lambda x: f"{int(x)}%")
data['Objekte (St.)'] = data['Objekte (St.)'].map(lambda x:featuredata.thousandsSeparator(x, language))
data['Häufigkeitsrate'] = data['Häufigkeitsrate'].map(lambda x: f"{x}%")
data[unit_label] = data[unit_label].map(lambda x: featuredata.replaceDecimal(round(x,1)))

# save a copy for the frnech and italian versions
esum_most_common = data.copy()

# make caption
# get percent of total to make the caption string
mc_caption_string = [
    "Gesamtergebnisse der Erhebung für alle Seen und Fliessgewässer: die am häufigsten gefundenen Gegenstände von März 2020 bis Mai 2021. ",
    "Die Häufigkeitsrate (wird in diesem Bericht als “Ausfallrate” bezeichnet) entspricht dem Verhältnis der Anzahl Ereignisse, bei denen ",
    "ein Gegenstand mindestens einmal gefunden wurde, zur Anzahl der total durchgeführten Erhebungen. Die Menge gibt an, wie häufig ein Objekt ",
    "gefunden wurde, sowie der Medianwert der Abfallobjekte pro 100 Meter (p/100 m). So wurden beispielsweise in 87 Prozent der Erhebungen insgesamt ",
    "8 485 Zigarettenfilter gefunden, was 15 Prozent aller gesammelten Gegenstände entspricht und einen Medianwert von 20 Zigarettenfiltern ",
    "pro 100 m Uferlinie ergibt."
]
   

colWidths = [5.1*cm, 2.2*cm, 2*cm, 2.8*cm, 2*cm]

d_chart = aSingleStyledTable(data, colWidths=colWidths)
d_capt = makeAParagraph(mc_caption_string, caption_style)
mc_table = tableAndCaption(d_chart, d_capt, colWidths)

most_common_display.index.name = None
most_common_display.columns.name = None

# set pandas display
aformatter = {
    "Anteil":lambda x: f"{int(x)}%",
    f"{unit_label}": lambda x: featuredata.replaceDecimal(x, "de"),
    "Häufigkeitsrate": lambda x: f"{int(x)}%",   
    "Objekte (St.)": lambda x: featuredata.thousandsSeparator(int(x), "de")
}

mcdic = most_common_display.style.format(aformatter).set_table_styles(table_css_styles)




IPython.display.display(HTML(cardFigure(html_table=mcdic.to_html(), table_caption= "".join(mc_caption_string))))


# Industriepellets und Schaumstoffe < 5 mm kamen beide in signifikanten Mengen vor, wurden jedoch in weniger als 50 Prozent der Erhebungen festgestellt (Median = 0). Dies deutet darauf hin, dass sie an spezifischen Standorten in hoher Dichte vorkommen. Zwar handelt es sich bei beiden Gegenständen um Mikroplastik, doch unterscheiden sich ihre Verwendung, ihre Herkunft und ihre Häufigkeit je nach Region des Erhebungsgebiets. Industriepellets sind Rohstoffe, die in Spritzgussverfahren verwendet werden, während Schaumstoffkügelchen entstehen, wenn Styropor zerkleinert wird. Weitere Angaben zu Standort, Mengen und Häufigkeit einzelner Gegenstände finden sich im  [Seen und Fleisgewässer](allsurveys).

# In[7]:


p15 = [
    "Industriepellets und Schaumstoffe < 5 mm kamen beide in signifikanten Mengen vor, wurden jedoch in weniger als 50 Prozent der Erhebungen ",
    "festgestellt (Median = 0). Dies deutet darauf hin, dass sie an spezifischen Standorten in hoher Dichte vorkommen. Zwar handelt es sich bei ",
    "beiden Gegenständen um Mikroplastik, doch unterscheiden sich ihre Verwendung, ihre Herkunft und ihre Häufigkeit je nach Region des Erhebungsgebiets. ",
    "Industriepellets sind Rohstoffe, die in Spritzgussverfahren verwendet werden, während Schaumstoffkügelchen entstehen, wenn Styropor zerkleinert wird. ",
    "Weitere Angaben zu Standort, Mengen und Häufigkeit einzelner Gegenstände finden sich im ",
    '<a href="https://hammerdirt-analyst.github.io/IQAASL-End-0f-Sampling-2021/lakes_rivers.html" color="blue"> Seen und Fleisgewässer </a>.'
]

p15 = makeAParagraph(p15)



new_components = [
    mc_table,
    smallest_space,
    p15   
]
# add those sections
pdfcomponents = addToDoc(new_components, pdfcomponents)


# In[8]:


mc_heat_map_caption = [
    "Alle Seen und Fliessgewässer nach Erhebungsgebiet: Der Medianwert der am häufigsten gefundenen Gegenstände; die ",
    "Häufigkeiten variieren je nach Region des Erhebungsgebiets. So wiesen fragmentierte Kunststoffe in den Erhebungsgebieten ",
    "Aare (18,5 p/100 m) und Rhone (48 p/100 m) die höchsten Medianwerte auf."
]
mc_heat_map_caption = ''.join(mc_heat_map_caption)

# calling componentsMostCommon gets the results for the most common codes
# at the component level
components = fdx.componentMostCommonPcsM()

# map to proper names for features
feature_names = featuredata.river_basin_de

# pivot that and quash the hierarchal column index that is created when the table is pivoted
mc_comp = components[["item", unit_label, this_level]].pivot(columns=this_level, index="item")
mc_comp.columns = mc_comp.columns.get_level_values(1)

# insert the proper columns names for display
proper_column_names = {x : feature_names[x] for x in mc_comp.columns}
mc_comp.rename(columns = proper_column_names, inplace=True)

# the aggregated total of the feature is taken from the most common objects table
mc_feature = fdx.most_common[unit_label]
mc_feature = featuredata.changeSeriesIndexLabels(mc_feature, {x:fdx.dMap.loc[x] for x in mc_feature.index})

# the aggregated totals of all the period data
mc_period = period_data.parentMostCommon(parent=False)
mc_period = featuredata.changeSeriesIndexLabels(mc_period, {x:fdx.dMap.loc[x] for x in mc_period.index})

# add the feature, bassin_label and period results to the components table
mc_comp["Alle Erhebungsgebiete"]= mc_feature

caption_prefix =  f'Median {unit_label} der häufigsten Objekte am '
col_widths=[5.1*cm, *[1.2*cm]*(len(mc_comp.columns)-1)]
mc_heatmap_title = Paragraph(f"Häufigste Objekte im Median {unit_label} nach Erhebungsgebiet", featuredata.bold_block)
tables = featuredata.splitTableWidth(mc_comp, gradient=True, caption_prefix=caption_prefix, caption=mc_heat_map_caption,
                    this_feature=this_feature["name"], vertical_header=True, colWidths=col_widths)

# identify the tables variable as either a list or a Flowable:
if isinstance(tables, list):
    grouped_pdf_components = [*tables]
else:
    grouped_pdf_components = [tables]
    

new_components = [
    # featuredata.small_space,
    # mc_heatmap_title,
    # featuredata.small_space,
    *grouped_pdf_components
]

pdfcomponents = featuredata.addToDoc(new_components, pdfcomponents)

# notebook display style
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

# display markdown html
IPython.display.display(HTML(cardFigure(html_table=mcd.to_html(), table_caption= "".join(mc_heat_map_caption))))


# ## Trends 2017–2018
# 
# Ein Vergleich der IQAASL-Ergebnisse mit ähnlichen Daten für Seen und Fliessgewässer, die 2017/2018 (SLR) erhoben wurden, zeigen keine statistischen Unterschiede. Allerdings gab es Abweichungen bei der Häufigkeit der Gegenstände. So wurden in der Erhebungsperiode 2020–2021 im Allgemeinen weniger Zigaretten und Flaschendeckel gefunden. An vielen Standorten wurden jedoch keine Veränderungen beobachtet und die Menge an fragmentierten Kunst- und Schaumstoffen dürfte zugenommen haben ( Details siehe [ Vergleich der Datenerhebungen seit 2018](slr-iqaasl)).
# 
# ```{card}
# :class-card: sd-text-black
# :img-top: resources/output/slr_iqaasl_surveys.jpeg
# +++
# Gesamtwerte der Erhebungen nach Datum.
# ``` 
# 
# ## Die Alpen und der Jura
# 
# Von den 20 Erhebungen im Erhebungsgebiet Alpen wiesen 17 eine Länge und eine Breite von über 10 m auf. Der Medianwert der Erhebungen betrug 110 p/100 m und lag damit unter dem Medianwert der anderen Erhebungsgebiete (189 p/100 m). Gegenstände aus dem Konsumbereich wie Lebensmittel und Getränke oder Tabakwaren machten einen geringeren Anteil an der Gesamtzahl aus und wiesen eine tiefere p/100 m-Rate auf im Vergleich zu den Ergebnissen von Standorten an Uferlinien. Dieser Unterschied könnte teilweise auf den geringen Verstädterungsgrad des Erhebungsgebiets Alpen im Vergleich zu allen anderen Erhebungsgebieten zurückzuführen sein sowie darauf, dass Material sich tendenziell flussabwärts bewegt. Für die Ergebungsmethodik und die Ergebnisse der Erhebung in den Alpen siehe [ Die Alpen und der Jura ](lesalpes)).

# In[9]:


sec2 = Paragraph("Trends 2017-2018", style=section_title)

p16 = [
    "Ein Vergleich der IQAASL-Ergebnisse mit ähnlichen Daten für Seen und Fliessgewässer, die 2017/2018 (SLR) erhoben wurden, ",
    "zeigen keine statistischen Unterschiede. Allerdings gab es Abweichungen bei der Häufigkeit der Gegenstände. So wurden in ",
    "der Erhebungsperiode 2020–2021 im Allgemeinen weniger Zigaretten und Flaschendeckel gefunden. An vielen Standorten wurden ",
    "jedoch keine Veränderungen beobachtet und die Menge an fragmentierten Kunst- und Schaumstoffen dürfte zugenommen haben ",
    '( Details siehe <a href="https://hammerdirt-analyst.github.io/IQAASL-End-0f-Sampling-2021/slr-iqaasl.html" color="blue"> Vergleich der Datenerhebungen seit 2018</a>)',

]
p16 = makeAParagraph(p16)

o_w, o_h = convertPixelToCm("resources/output/slr_iqaasl_surveys.jpeg")
f2cap = [
   "Vergleich der Erhebungsergebnisse von SLR (2018) und IQAASL (2021). <b>Oben links:</b> Gesamtergebnisse der Erhebung nach Datum. <b>Oben rechts:</b> Median ",
    "der Gesamtergebnisse der monatlichen Erhebungen. <b>Unten links: </b> Anzahl Proben im Verhältnis zum Gesamtergebnis der Erhebung. <b>Unten rechts:</b> ",
    "empirische kumulative Verteilung der Gesamtergebnisse der Erhebung.",
]

f2cap = makeAParagraph(f2cap, style=caption_style)

sec3 = Paragraph("Die Alpen und der Jura", style=section_title)

p17 = [
    "Von den 20 Erhebungen im Erhebungsgebiet Alpen wiesen 17 eine Länge und eine Breite von über 10 m auf. Der Medianwert der Erhebungen betrug ",
    "110 p/100 m und lag damit unter dem Medianwert der anderen Erhebungsgebiete (189 p/100 m). Gegenstände aus dem Konsumbereich wie Lebensmittel ",
    "und Getränke oder Tabakwaren machten einen geringeren Anteil an der Gesamtzahl aus und wiesen eine tiefere p/100 m-Rate auf im Vergleich zu ",
    "den Ergebnissen von Standorten an Uferlinien. Dieser Unterschied könnte teilweise auf den geringen Verstädterungsgrad des Erhebungsgebiets Alpen im ",
    "Vergleich zu allen anderen Erhebungsgebieten zurückzuführen sein sowie darauf, dass Material sich tendenziell flussabwärts bewegt. Für die ",
    "Ergebungsmethodik und die Ergebnisse der Erhebung in den Alpen siehe [ Die Alpen und der Jura ](lesalpes)).",
    '( Details siehe <a href="https://hammerdirt-analyst.github.io/IQAASL-End-0f-Sampling-2021/alpes_valaisannes.html" color="blue"> Die Alpen und der Jura</a>)'
]
p17 = makeAParagraph(p17)

figure_kwargs = {
    "image_file":"resources/output/slr_iqaasl_surveys.jpeg",
    "caption": f2cap, 
    "original_width":o_w,
    "original_height":o_h,
    "desired_width": 14,
    "caption_height":1.5,
    "hAlign": "CENTER",
}

f2 = figureAndCaptionTable(**figure_kwargs)

new_components = [
   small_space,
    sec2,
    small_space,
    p16,
    small_space,
    f2,
    small_space,
    sec3,
    small_space,
    p17,
]
# add those sections
pdfcomponents = addToDoc(new_components, pdfcomponents)


# ## Kommunikation der Ergebnisse
# 
# Für die Kommunikation von Verschmutzungsmengen ist es naheliegend, die Ergebnisse in eine einfache Einheit mit der durchschnittlichen Anzahl pro 100 m umzuwandeln, da der Durchschnitt meist höher ist und nur selten null beträgt. Allerdings kann der Durchschnitt bei Extremwerten doppelt so hoch ausfallen wie der Median, was Verwirrung in Bezug auf den Unterschied zwischen den beobachteten und den gemeldeten Ergebnissen stiften kann. Deshalb ist es informativer und reproduzierbarer, die Bandbreite wahrscheinlicher Werte oder die Wahrscheinlichkeit, einen Gegenstand zu finden, anzugeben, wenn ähnliche Protokolle befolgt werden. So etwa bei der Interpretation der Mengen an Industriepellets, die am Genfersee gefunden wurden:
# 
# > 1’387 Produktionspellets aus Kunststoff wurden festgestellt, was 5 Prozent aller am Genfersee identifizierten Gegenstände entspricht. Die Anzahl Pellets pro 100 m schwankt je nach Region zwischen 0 und 1’033. Beim See besteht im Allgemeinen eine Wahrscheinlichkeit von 40 Prozent, in einer Erhebung irgendwo mindestens auf ein Pellet zu stossen. An einigen Standorten, wie Genf (Wahrscheinlichkeit von 60 %) oder Préverenges (Wahrscheinlichkeit von 80 %), werden Produktionspellets regelmässig an den Ufern gefunden. Werte zwischen 3 p/100 m und 56 p/100 m sind üblich.
# 
# ## Schlussfolgerungen
# 
# Auf nationaler Ebene waren die Erhebungsergebnisse des IQAASL-Projekts im Vergleich zu den Erhebungen, die 2017 im Rahmen der SLR-Studie durchgeführt wurden, stabil. Allerdings war ein allgemeiner Rückgang der Menge an Gegenständen im Zusammenhang mit Lebensmitteln, Getränken und Tabakwaren feststellbar. Die Anzahl der identifizierten Infrastrukturobjekte sowie fragmentierten Kunststoffe und Schaumstoffe ging hingegen nicht zurück, an einigen Standorten könnten gar starke Zunahmen verzeichnet worden sein. Die pandemiebedingten Einschränkungen, die grosse Menschenansammlungen im Freien begrenzten, könnten sich positiv ausgewirkt und zu einem Rückgang von Objekten aus den Bereichen Lebensmittel, Getränke und Tabakwaren geführt haben. Die grössten Zunahmen bei infrastrukturbezogenen Gegenständen waren im Wallis, in der Waadt und in Brienz zu beobachten, also an Standorten in der Nähe von Flusseinträgen von Rhone und Aare.
# 
# Die Landnutzung rund um einen Erhebungsstandort hat einen messbaren Effekt auf das Vorkommen bestimmter Gegenstände: Je höher die Anzahl Gebäude und fester Infrastrukturen ist, desto mehr Tabakwaren und Lebensmittelprodukte werden gefunden. Diese Korrelation gilt nicht für Gegenstände wie fragmentierte Kunststoffe und Industriefolien – sie werden unabhängig von der Landnutzung zu fast gleichen Teilen festgestellt, wobei sie bei Eintragsstellen von Flüssen und Kanälen häufiger anzutreffen sind.
# 
# Derzeit werden drei der vier IQAASL-Erhebungsgebiete von Forschungs- und Regierungsstellen flussabwärts der Schweiz aktiv überwacht. Diese verwenden ähnliche Methoden wie die in diesem Bericht vorgestellten. Zudem streben regionale Organisationen in der Schweiz mit Partnerorganisationen in der EU eine Standardisierung von Berichterstattung und Protokollen an.
# 
# IQAASL ist ein Bürgerwissenschaftsprojekt, das ausschliesslich Open-Source-Tools nutzt und Daten mit einer GNU Public License teilt. So ist eine Zusammenarbeit mit Stakeholdern möglich. Am Ende des Mandats per 31. Dezember 2021 übernimmt Hammerdirt die Verantwortung für die Pflege des Code- und Daten-Repositorys, das öffentlich auf Github gehostet wird.
# 
# Die Organisationen, die sich an IQAASL beteiligt haben, suchen aktiv nach Möglichkeiten, den Datenerhebungsprozess und/oder die Ergebnisse in ihr eigenes Geschäftsmodell zu integrieren. Allerdings gibt es in vielen regionalen Organisationen zu wenige Datenwissenschaftlerinnen und Datenwissenschaftler, was den Integrationsprozess verlängern und die Innovationsrate auf der Ebene, auf der sie am nötigsten wäre, drosseln könnte

# In[10]:


sec4 = Paragraph("Kommunikation der Ergebnisse", style=section_title)

p18 = [
    "Für die Kommunikation von Verschmutzungsmengen ist es naheliegend, die Ergebnisse in eine einfache Einheit mit der durchschnittlichen Anzahl pro ",
    "100 m umzuwandeln, da der Durchschnitt meist höher ist und nur selten null beträgt. Allerdings kann der Durchschnitt bei Extremwerten doppelt so ",
    "hoch ausfallen wie der Median, was Verwirrung in Bezug auf den Unterschied zwischen den beobachteten und den gemeldeten Ergebnissen stiften kann. ",
    "Deshalb ist es informativer und reproduzierbarer, die Bandbreite wahrscheinlicher Werte oder die Wahrscheinlichkeit, einen Gegenstand zu finden, ",
    "anzugeben, wenn ähnliche Protokolle befolgt werden. So etwa bei der Interpretation der Mengen an Industriepellets, die am Genfersee gefunden wurden:"
]

p19 = [
    "1’387 Produktionspellets aus Kunststoff wurden festgestellt, was 5 Prozent aller am Genfersee identifizierten Gegenstände entspricht. Die Anzahl ",
    "Pellets pro 100 m schwankt je nach Region zwischen 0 und 1’033. Beim See besteht im Allgemeinen eine Wahrscheinlichkeit von 40 Prozent, in einer ",
    f'Erhebung irgendwo mindestens auf ein Pellet zu stossen. An einigen Standorten, wie Genf (Wahrscheinlichkeit von 60 %) oder Préverenges (Wahrscheinlichkeit von {80} {"%"}), ', 
    f'werden Produktionspellets regelmässig an den Ufern gefunden. Werte zwischen 3 {unit_label} und 56 {unit_label} m sind üblich.'
]

p18 = makeAParagraph(p18)
p19 = makeAParagraph(p19, style=block_quote_style)

sec5 = Paragraph("Schlussfolgerungen", style=section_title)
p20 = [
    "Auf nationaler Ebene waren die Erhebungsergebnisse des IQAASL-Projekts im Vergleich zu den Erhebungen, die 2017 im Rahmen der ",
    "SLR-Studie durchgeführt wurden, stabil. Allerdings war ein allgemeiner Rückgang der Menge an Gegenständen im Zusammenhang mit ",
    "Lebensmitteln, Getränken und Tabakwaren feststellbar. Die Anzahl der identifizierten Infrastrukturobjekte sowie fragmentierten ",
    "Kunststoffe und Schaumstoffe ging hingegen nicht zurück, an einigen Standorten könnten gar starke Zunahmen verzeichnet worden ",
    "sein. Die pandemiebedingten Einschränkungen, die grosse Menschenansammlungen im Freien begrenzten, könnten sich positiv ausgewirkt ",
    "und zu einem Rückgang von Objekten aus den Bereichen Lebensmittel, Getränke und Tabakwaren geführt haben. Die grössten Zunahmen ",
    "bei infrastrukturbezogenen Gegenständen waren im Wallis, in der Waadt und in Brienz zu beobachten, also an Standorten in der Nähe ",
    "von Flusseinträgen von Rhone und Aare."
]


p21 = [
    "Die Landnutzung rund um einen Erhebungsstandort hat einen messbaren Effekt auf das Vorkommen bestimmter Gegenstände: Je höher ",
    "die Anzahl Gebäude und fester Infrastrukturen ist, desto mehr Tabakwaren und Lebensmittelprodukte werden gefunden. Diese Korrelation ",
    "gilt nicht für Gegenstände wie fragmentierte Kunststoffe und Industriefolien – sie werden unabhängig von der Landnutzung zu fast ",
    "gleichen Teilen festgestellt, wobei sie bei Eintragsstellen von Flüssen und Kanälen häufiger anzutreffen sind."
]

p22 = [
    "Derzeit werden drei der vier IQAASL-Erhebungsgebiete von Forschungs- und Regierungsstellen flussabwärts der Schweiz aktiv überwacht. ",
    "Diese verwenden ähnliche Methoden wie die in diesem Bericht vorgestellten. Zudem streben regionale Organisationen in der Schweiz mit ",
    "Partnerorganisationen in der EU eine Standardisierung von Berichterstattung und Protokollen an."
]

p23 = [
    "IQAASL ist ein Bürgerwissenschaftsprojekt, das ausschliesslich Open-Source-Tools nutzt und Daten mit einer GNU Public License teilt. ",
    "So ist eine Zusammenarbeit mit Stakeholdern möglich. Am Ende des Mandats per 31. Dezember 2021 übernimmt Hammerdirt die Verantwortung ",
    "für die Pflege des Code- und Daten-Repositorys, das öffentlich auf Github gehostet wird."
]

p24 = [
    "Die Organisationen, die sich an IQAASL beteiligt haben, suchen aktiv nach Möglichkeiten, den Datenerhebungsprozess und/oder die Ergebnisse ",
    "in ihr eigenes Geschäftsmodell zu integrieren. Allerdings gibt es in vielen regionalen Organisationen zu wenige Datenwissenschaftlerinnen ",
    "und Datenwissenschaftler, was den Integrationsprozess verlängern und die Innovationsrate auf der Ebene, auf der sie am nötigsten wäre, "
    "drosseln könnte. "
]

p20_24 = sectionParagraphs([p20, p21, p22, p23, p24], smallspace=smallest_space)

new_components = [
    small_space,
    sec4,
    small_space,
    p18,
    smallest_space,
    p19,
    small_space,
    sec5,
    small_space,
    *p20_24,
]
# add those sections
pdfcomponents = addToDoc(new_components, pdfcomponents)


# ## Empfehlungen
# ### Überwachung und Berichterstattung
# 
# Effizienzgewinne bei Datenaustausch und Berichterstattung könnten durch die Festlegung eines Standardberichtsformats umgehend erzielt werden. Dies würde es für regionale Verwaltungen einfacher machen, andere Stakeholder über die Prioritäten zu informieren, was wiederum Überwachungsstrategien erleichtern und die Definition von Reduktionszielen unterstützen würde. Hierzu könnten folgende Massnahmen umgesetzt werden:
# 
# >Ein Netz von Organisationen aufbauen, die für die Erhebung und die Berichterstattung über die Ergebnisse zuständig sind.
# >Ein Standardberichtsformat schaffen, um die Kommunikation zwischen Verwaltungen auf Ebene Gemeinde, Kanton und Region/Bezirk zu erleichtern und die Koordination regionaler und lokaler Reduktionsstrategien zu verbessern.
# >Die nächste Probenahmeperiode oder das nächste Probenahmeintervall festlegen.
# 
# Akademische Kreise formell in Planung, Probenahme und Analyse einbeziehen. Dieses Projekt wurde durch die Zusammenarbeit von Professorinnen und Professoren von ETH, UNIGE, EPFL, PSI und FHNW geprägt. Universitäre Partner wären ideal, um die Analysemethoden weiterzuentwickeln. Das Citizen Science Center (ETH) und das Citizen Cyberlab (UNIGE) verfügen über die Erfahrung und die Infrastruktur, um bürgerwissenschaftliche Überwachungsprojekte mit Forschungstätigkeiten zu verknüpfen. Auf diese Weise kann ein äusserst anpassungsfähiger und effizienter Überwachungsplan erarbeitet werden.
# 

# In[11]:


sec6 = Paragraph("Empfehlungen", style=section_title)
ssec3 = Paragraph("Überwachung und Berichterstattung", style=subsection_title)

p25 = [
    "Effizienzgewinne bei Datenaustausch und Berichterstattung könnten durch die Festlegung eines Standardberichtsformats umgehend ",
    "erzielt werden. Dies würde es für regionale Verwaltungen einfacher machen, andere Stakeholder über die Prioritäten zu informieren, ",
    "was wiederum Überwachungsstrategien erleichtern und die Definition von Reduktionszielen unterstützen würde. Hierzu könnten folgende ",
    "Massnahmen umgesetzt werden:"
]

p25 = makeAParagraph(p25)
l5 = [
    "Ein Netz von Organisationen aufbauen, die für die Erhebung und die Berichterstattung über die Ergebnisse zuständig sind.",
    "Ein Standardberichtsformat schaffen, um die Kommunikation zwischen Verwaltungen auf Ebene Gemeinde, Kanton und Region/Bezirk zu erleichtern und die Koordination regionaler und lokaler Reduktionsstrategien zu verbessern.",
    "Die nächste Probenahmeperiode oder das nächste Probenahmeintervall festlegen."
]
l5 = makeAList(l5)

p26 = [
    "Akademische Kreise formell in Planung, Probenahme und Analyse einbeziehen. Dieses Projekt wurde durch die Zusammenarbeit ",
    "von Professorinnen und Professoren von ETH, UNIGE, EPFL, PSI und FHNW geprägt. Universitäre Partner wären ideal, um die ",
    "Analysemethoden weiterzuentwickeln. Das Citizen Science Center (ETH) und das Citizen Cyberlab (UNIGE) verfügen über die ",
    "Erfahrung und die Infrastruktur, um bürgerwissenschaftliche Überwachungsprojekte mit Forschungstätigkeiten zu verknüpfen.  ",
    "Auf diese Weise kann ein äusserst anpassungsfähiger und effizienter Überwachungsplan erarbeitet werden."
]
p26 = makeAParagraph(p26)

new_components = [
    small_space,
    sec6,
    smallest_space,
    ssec3,
    small_space,
    p25,
    smallest_space,
    l5,
    smallest_space,
    p26
]
pdfcomponents = addToDoc(new_components, pdfcomponents)


# ## Beseitigung und Reduktion
# 
# Bei Strategien zur Beseitigung oder Reduktion von Abfällen im Wasser sollte zunächst deren Quelle berücksichtigt werden.
# 
# __Gegenstände im Zusammenhang mit Landnutzungsmerkmalen__
# 
# Die Ergebnisse weisen auf einen positiven Zusammenhang zwischen der Anzahl Gebäude und der Menge an Gegenständen aus den Bereichen Lebensmittel, Getränke und Tabakwaren hin. Dies legt nahe, dass Strategien zur Verringerung dieser Gegenstände in Gebieten ansetzen sollten, die eine hohe Konzentration an Infrastrukturen in Ufernähe aufweisen. Die Ergebnisse aus dem Erhebungsgebiet Rhone lassen vermuten, dass sich lokale Sensibilisierungskampagnen positiv auswirken könnten ( siehe  [Seen und Fleisgewässer](allsurveys). ). Auch wenn alle Gegenstände im Zusammenhang mit Lebensmitteln, Getränken und Tabakwaren, auf die Sensibilisierungskampagnen für Abfall in der Regel abzielen, beseitigt würden, würde dies die Gesamtmengen zwar signifikant reduzieren, doch würden immer noch 64 Prozent des Materials liegen bleiben.
# 
# Weitere gängige Reduktionsstrategien sind u. a. die folgenden:
# 
# * Angemessene Bereitstellung von wetter- und tierbeständigen Abfallbehältern
# * Enger getakteter Zeitplan für Abfallentsorgung und Reinigung
# * Reduktion von Einwegprodukten aus Kunststoff
# 
# Viele Länder haben bereits begonnen, Einschränkungen für bestimmte Gegenstände einzuführen. So dürfen beispielsweise Einwegteller und -besteck aus Plastik, Strohhalme, Ballonstäbe und Wattestäbchen aus Kunststoff seit dem 3. Juli 2021 in den EU-Mitgliedstaaten nicht mehr verkauft werden. In Frankreich werden in Regenwasserkanalisationen erfolgreich Rückhaltenetze eingesetzt, damit Abfälle nicht mehr in Seen und Fliessgewässer gelangen, was jedoch Investitionen in Infrastruktur, Ausrüstung und Arbeitskräfte bedingt.

# In[12]:


sec7 = Paragraph("Beseitigung und Reduktion", style=section_title)

p27 = ["Bei Strategien zur Beseitigung oder Reduktion von Abfällen im Wasser sollte zunächst deren Quelle berücksichtigt werden."]

p28 = [
    "Gegenstände im Zusammenhang mit Landnutzungsmerkmalen"
]

p29 = [
    "Die Ergebnisse weisen auf einen positiven Zusammenhang zwischen der Anzahl Gebäude und der Menge an Gegenständen aus den Bereichen ",
    "Lebensmittel, Getränke und Tabakwaren hin. Dies legt nahe, dass Strategien zur Verringerung dieser Gegenstände in Gebieten ansetzen ",
    "sollten, die eine hohe Konzentration an Infrastrukturen in Ufernähe aufweisen. Die Ergebnisse aus dem Erhebungsgebiet Rhone lassen ",
    "vermuten, dass sich lokale Sensibilisierungskampagnen positiv auswirken könnten ",
    '<a href="https://hammerdirt-analyst.github.io/IQAASL-End-0f-Sampling-2021/lakes_rivers.html" color="blue"> Seen und Fleisgewässer </a>. Auch ',
    "wenn alle Gegenstände im Zusammenhang mit Lebensmitteln, Getränken und Tabakwaren, auf die Sensibilisierungskampagnen für Abfall in der ",
    "Regel abzielen, beseitigt würden, würde dies die Gesamtmengen zwar signifikant reduzieren, doch würden immer noch 64 Prozent des ",
    "Materials liegen bleiben."
]

p30 = ["Weitere gängige Reduktionsstrategien sind u. a. die folgenden:"]
l6 = [
    "Angemessene Bereitstellung von wetter- und tierbeständigen Abfallbehältern",
    "Enger getakteter Zeitplan für Abfallentsorgung und Reinigung",
    "Reduktion von Einwegprodukten aus Kunststoff",
]

l6 = makeAList(l6)

p31 = [
    "Viele Länder haben bereits begonnen, Einschränkungen für bestimmte Gegenstände einzuführen. So dürfen beispielsweise Einwegteller und -besteck aus Plastik, ",
    "Strohhalme, Ballonstäbe und Wattestäbchen aus Kunststoff seit dem 3. Juli 2021 in den EU-Mitgliedstaaten nicht mehr verkauft werden. In Frankreich werden in ",
    "Regenwasserkanalisationen erfolgreich Rückhaltenetze eingesetzt, damit Abfälle nicht mehr in Seen und Fliessgewässer gelangen, was jedoch Investitionen in ",
    "Infrastruktur, Ausrüstung und Arbeitskräfte bedingt."
]

p27 = makeAParagraph(p27)
p28 = makeAParagraph(p28, style=bold_block)
p29 = makeAParagraph(p29)
p30 = makeAParagraph(p30)
p31 = makeAParagraph(p31)
new_components = [
    small_space,
    sec7,
    small_space,
    p27,
    smallest_space,
    p28,
    smallest_space,
    p29,
    smallest_space,
    p30,
    smallest_space,
    l6,
    smallest_space,
    p31
]
# add those sections
pdfcomponents = addToDoc(new_components, pdfcomponents)


# ## Nicht mit der Landnutzung verbundene Gegenstände
# 
# Zur Verringerung der Anzahl Gegenstände, die keine Korrelation mit der Landnutzung aufweisen, ist zumindest auf Ebene des Sees oder des Fliessgewässers sowie bei allen Standorten, die oberhalb der geplanten Erhebungsorte liegen, ein koordiniertes Vorgehen notwendig. Zu den häufigsten Gegenständen zählen die folgenden:
# 
# * Fragmentierte Kunststoffe
# * Fragmentierte Schaumstoffe
# * Baukunststoffe
# * Industriepellets
# * Wattestäbchen
# * Industriefolien
# 
# Diese Gegenstände machen 40 Prozent des gesamten identifizierten Materials aus. Viele Gegenstände werden in der Industrie oder für die Körperpflege verwendet und haben normalerweise nichts mit Tätigkeiten am Ufer zu tun. Eine Ausweitung der Sensibilisierungskampagnen, die auf eine Vermeidung von Materialverlusten an der Quelle aus bestimmten Sektoren abzielen, könnte dafür sorgen, dass weniger Gegenstände wie Industriepellets, die für Spritzgussverfahren verwendet werden, gefunden werden. Einige Gegenstände wie Wattestäbchen aus Kunststoff und andere Gegenstände aus Plastik, die über Toilettenspülungen entsorgt werden, gelangen über Abwasserreinigungsanlagen in Seen und Fliessgewässer
# 
# Reduktionsstrategien könnten Folgendes umfassen:
# 
# * Aufrüstung von Abwasserreinigungsanlagen zur Verringerung von Materialverlusten
# * Sensibilisierungskampagnen für spezifische Gegenstände oder Produkte
# * Sensibilisierungskampagnen für spezifische Branchen
# 
# Beseitigungs- oder Reduktionsstrategien erfordern regionale Massnahmen, um auch die Gemeinden oberhalb der Erhebungsstandorte miteinzubeziehen. Wahrscheinlich würde eine weniger starke Abhängigkeit von Einwegkunststoffen, Schaumstoffen, Baukunststoffen und Industriefolien dazu führen, dass kleinere Mengen dieser Materialien in die Umwelt gelangen. Da diese Materialien günstige Wegwerfwaren sind, wurden sie in allen Sektoren immer häufiger eingesetzt, wodurch eine immer grössere Abhängigkeit entstand. Das geringe Gewicht und ihre Abbaueigenschaften erleichtern die Fragmentierung dieser Materialien sowie ein Entweichen in die Umwelt, insbesondere, wenn sie länger im Freien verbleiben. Kunststoffschadstoffe sind ein weltweites Problem und immer mehr Länder ergreifen Massnahmen, um weniger von Einwegkunststoffen und -schaumstoffen wie Styropor abhängig zu sein.

# In[13]:


sec7 = Paragraph("Nicht mit der Landnutzung verbundene Gegenstände", style=section_title)
p32 = [
    "Zur Verringerung der Anzahl Gegenstände, die keine Korrelation mit der Landnutzung aufweisen, ist zumindest auf Ebene des Sees oder des Fliessgewässers sowie bei ",
    "allen Standorten, die oberhalb der geplanten Erhebungsorte liegen, ein koordiniertes Vorgehen notwendig. Zu den häufigsten Gegenständen zählen die folgenden:"
]

p32 = makeAParagraph(p32)

l8 = [
    "Fragmentierte Kunststoffe",
    "Fragmentierte Schaumstoffe",
    "Baukunststoffe",
    "Industriepellets",
    "Wattestäbchen",
    "Industriefolien"
]
l8 = makeAList(l8)

p33 = [
    "Diese Gegenstände machen 40 Prozent des gesamten identifizierten Materials aus. Viele Gegenstände werden in der Industrie oder für die Körperpflege verwendet ",
    "und haben normalerweise nichts mit Tätigkeiten am Ufer zu tun. Eine Ausweitung der Sensibilisierungskampagnen, die auf eine Vermeidung von Materialverlusten an ",
    "der Quelle aus bestimmten Sektoren abzielen, könnte dafür sorgen, dass weniger Gegenstände wie Industriepellets, die für Spritzgussverfahren verwendet werden, ",
    "gefunden werden. Einige Gegenstände wie Wattestäbchen aus Kunststoff und andere Gegenstände aus Plastik, die über Toilettenspülungen entsorgt werden, gelangen ",
    "über Abwasserreinigungsanlagen in Seen und Fliessgewässer."
]

p34 = ["Reduktionsstrategien könnten Folgendes umfassen:"]
p33_34 = sectionParagraphs([p33, p34], smallspace=smallest_space)

l9 = [
    "Aufrüstung von Abwasserreinigungsanlagen zur Verringerung von Materialverlusten",
    "Sensibilisierungskampagnen für spezifische Gegenstände oder Produkte",
    "Sensibilisierungskampagnen für spezifische Branchen",
]
l9 = makeAList(l9)

p35 = [
    "Beseitigungs- oder Reduktionsstrategien erfordern regionale Massnahmen, um auch die Gemeinden oberhalb der Erhebungsstandorte miteinzubeziehen. Wahrscheinlich "
    "würde eine weniger starke Abhängigkeit von Einwegkunststoffen, Schaumstoffen, Baukunststoffen und Industriefolien dazu führen, dass kleinere Mengen dieser Materialien ",
    "in die Umwelt gelangen. Da diese Materialien günstige Wegwerfwaren sind, wurden sie in allen Sektoren immer häufiger eingesetzt, wodurch eine immer grössere Abhängigkeit ",
    "entstand. Das geringe Gewicht und ihre Abbaueigenschaften erleichtern die Fragmentierung dieser Materialien sowie ein Entweichen in die Umwelt, insbesondere, wenn sie ",
    "länger im Freien verbleiben. Kunststoffschadstoffe sind ein weltweites Problem und immer mehr Länder ergreifen Massnahmen, um weniger von Einwegkunststoffen und ",
    "-schaumstoffen wie Styropor abhängig zu sein."
]

p35 = makeAParagraph(p35)

new_components = [
    small_space,
    sec7,
    small_space,
    p32,
    smallest_space,
    l8,
    smallest_space,
    *p33_34,
    l9,
    smallest_space,
    p35,
   
]
# add those sections
pdfcomponents = addToDoc(new_components, pdfcomponents)




# ## Sommario esecutivo
# 
# | Deutsch | Français |
# 
# IQAASL (Identificazione, quantificazione e analisi dei rifiuti antropogenici in Svizzera) è un progetto commissionato dall’Ufficio federale dell’ambiente (UFAM) per raccogliere dati sugli inquinanti visibili lungo le rive di laghi e fiumi svizzeri. Tutti i materiali scaricati nell’ambiente sono stati raccolti e identificati con l’ausilio di tecniche d’indagine sui rifiuti. Il progetto è stato ampliato al fine di includere 20 ubicazioni nelle Alpi e nel Giura, per un totale di 406 campioni prelevati da 163 ubicazioni in 95 comuni.
# 
# Il presente rapporto costituisce una sintesi e un’analisi sia delle indagini condotte sui rifiuti, sia dei metodi utilizzati in Svizzera da marzo 2020 fino a fine agosto 2021. Questo arco temporale si sovrappone al periodo di rilevamento dell’indagine Swiss Litter Report {cite}`slr`, condotta da aprile 2017 a marzo 2018. Lo Swiss Litter Report è stato il primo progetto a livello nazionale a utilizzare il protocollo standard descritto nella Guida al monitoraggio del littering delle spiagge {cite}`mlwguidance`, o qualsiasi altro metodo comparabile. Poiché il periodo di indagine del presente studio si sovrappone a quello dello SLR è possibile fare una comparazione tra i risultati.
# 
# ```{card}
# :class-card: sd-text-black
# :img-top: resources/maps/esummary_map.jpeg
# +++
# Figure : Karte der Erhebungsstandorte März 2020–August 2021. Die rot dargestellten Standorte betreffen Erhebungen an Fliessgewässern oder Seen, die violetten Punkte sind die Standorte in den Alpen und im Jura.
# ```
# ## Laghi e fiumi
# 
# Laghi e fiumi sono stati campionati da marzo 2020 a maggio 2021, per un totale di 54 744 oggetti prelevati e classificati nel corso di 386 indagini. Le ubicazioni sono state divise in aree di indagine per l’analisi regionale e definite in funzione dei bacini dei fiumi Aare, Rodano, Ticino e Linth/Limmat. Le indagini sono state condotte presso 143 diverse ubicazioni distribuite su 77 comuni. È stata presa in esame una distanza lineare totale di 20 km comprendente una superficie di 9 ettari e una popolazione totale di 1,7 milioni di abitanti.
# 
# La maggior parte delle indagini si è svolta lungo le rive dei laghi (331 campioni), in quanto questi specchi d’acqua offrono tutto l’anno un accesso più costante e sicuro rispetto ai fiumi. Inoltre i laghi sono grandi aree con scorrimento ridotto che hanno come immissari fiumi, ruscelli e sistemi di drenaggio. Sulla scorta di queste caratteristiche, si configurano come ubicazioni ideali per valutare la varietà degli oggetti nei corpi idrici e sulle loro sponde. In totale, 316 campioni sono stati raccolti in sette laghi di grandi dimensioni distribuiti lungo tre bacini fluviali principali. Venti località sono state selezionate per un campionamento con cadenza mensile sull’arco di dodici mesi, con l’eccezione del Lago Maggiore che è stato campionato ogni tre mesi. Sono state condotte indagini anche sul lago di Lugano, sul lago dei Quattro Cantoni, sul lago di Brienz e sul lago di Zugo. Sono state inoltre effettuate 55 indagini su 16 fiumi.
# 
# In totale 316 campioni provenivano da sette laghi principali in 3 maggiori bacini fluviali. Venti località sono state selezionate per essere campionate mensilmente per un periodo di dodici mesi ad eccezione del Lago Maggiore, che è stato campionato ogni tre mesi. Sono state condotte indagini anche sul Lago di Lugano, Lago dei Quattro Cantoni, Lago di Brienz e Lago di Zugo. Inoltre, ci sono state 55 indagini su 16 fiumi.
# 
# __Ubicazioni lacustri con campionamento mensile:__
# 
# * Area d’indagine dell’Aare
#   * Lago di Thun: Spiez, Unterseen
#   * Lago di Biel/Bienne: Biel/Bienne, Vinelz
#   * Lago di Neuchâtel: Neuchâtel, Cheyres-Châbles, Yverdon-les-Bains
# * Area d’indagine della Linth/Limmat
#   * Lago di Zurigo: Zurigo, Küsnacht (ZH), Rapperswil-Jona, Richterswil
#   * Walensee: Walenstadt, Weesen
# * Area d’indagine del Rodano
#   * Lago Lemano: Vevey, Saint-Gingolph, Ginevra, Préverenges, La Tour-de-Peilz
# * Area d’indagine del Ticino
#   * Lago Maggiore: Ascona, Gambarogno (frequenza trimestrale)
# 
# 

# In[14]:


p41 = makeAParagraph(["Area d’indagine dell’Aare"], style=bold_block)
l2i = [
    "Lago di Thun: Spiez, Unterseen",
    "Lago di Biel/Bienne: Biel/Bienne, Vinelz",
    "Lago di Neuchâtel: Neuchâtel, Cheyres-Châbles, Yverdon-les-Bains"
]
l2i = makeAList(l2i)
p42 = makeAParagraph(["Area d’indagine della Linth/Limmat"], style=bold_block)
l3i = [
    "Lago di Zurigo: Zurigo, Küsnacht (ZH), Rapperswil-Jona, Richterswil",
    "Walensee: Walenstadt, Weesen"
]
l3i=makeAList(l3i)
p43 = makeAParagraph(["Area d’indagine del Rodano"], style=bold_block)

l4i = [
    "Lago Lemano: Vevey, Saint-Gingolph, Ginevra, Préverenges, La Tour-de-Peilz"
]
l4i = makeAList(l4i)
p44 = makeAParagraph(["Area d’indagine del Ticino"], style=bold_block)
l5i = ["Lago Maggiore: Ascona, Gambarogno (frequenza trimestrale)"]
l5i = makeAList(l5i)

seci = Paragraph("Sommario esecutivo", style=section_title)

p36 = [
    "IQAASL (Identificazione, quantificazione e analisi dei rifiuti antropogenici in Svizzera) è un progetto commissionato dall’Ufficio ",
    "federale dell’ambiente (UFAM) per raccogliere dati sugli inquinanti visibili lungo le rive di laghi e fiumi svizzeri. Tutti i materiali ",
    "scaricati nell’ambiente sono stati raccolti e identificati con l’ausilio di tecniche d’indagine sui rifiuti. Il progetto è stato ampliato ",
    "al fine di includere 20 ubicazioni nelle Alpi e nel Giura, per un totale di 406 campioni prelevati da 163 ubicazioni in 95 comuni."
]

p37 = [
    "Il presente rapporto costituisce una sintesi e un’analisi sia delle indagini condotte sui rifiuti, sia dei metodi utilizzati in ",
    "Svizzera da marzo 2020 fino a fine agosto 2021. Questo arco temporale si sovrappone al periodo di rilevamento dell’indagine Swiss ",
    'Litter Report <a href="#Bla18" color="blue">(SLR)</a>, condotta da aprile 2017 a marzo 2018. Lo Swiss Litter Report è stato il primo progetto a livello ',
    'nazionale a utilizzare il protocollo standard descritto nella Guida al monitoraggio del littering delle spiagge <a href="#Han13" color="blue">(Han13)</a>, ',
    "o qualsiasi altro metodo comparabile. Poiché il periodo di indagine del presente studio si sovrappone a quello dello SLR è possibile fare "
    "una comparazione tra i risultati."
]
seci2 = Paragraph("Laghi e fiumi", style=section_title)

p36_37 = sectionParagraphs([p36, p37], smallspace=smallest_space)

p38 = [
    "Laghi e fiumi sono stati campionati da marzo 2020 a maggio 2021, per un totale di 54 744 oggetti prelevati e classificati nel corso di 386 indagini. ",
    "Le ubicazioni sono state divise in aree di indagine per l’analisi regionale e definite in funzione dei bacini dei fiumi Aare, Rodano, Ticino e ",
    "Linth/Limmat. Le indagini sono state condotte presso 143 diverse ubicazioni distribuite su 77 comuni. È stata presa in esame una distanza lineare ",
    "totale di 20 km comprendente una superficie di 9 ettari e una popolazione totale di 1,7 milioni di abitanti."
]

p39 = [
    "La maggior parte delle indagini si è svolta lungo le rive dei laghi (331 campioni), in quanto questi specchi d’acqua offrono tutto l’anno un accesso più costante ",
    "e sicuro rispetto ai fiumi. Inoltre i laghi sono grandi aree con scorrimento ridotto che hanno come immissari fiumi, ruscelli e sistemi di drenaggio. Sulla scorta ",
    "di queste caratteristiche, si configurano come ubicazioni ideali per valutare la varietà degli oggetti nei corpi idrici e sulle loro sponde. In totale, 316 campioni ",
    "sono stati raccolti in sette laghi di grandi dimensioni distribuiti lungo tre bacini fluviali principali. Venti località sono state selezionate per un campionamento ",
    "con cadenza mensile sull’arco di dodici mesi, con l’eccezione del Lago Maggiore che è stato campionato ogni tre mesi. Sono state condotte indagini anche sul lago di ",
    "Lugano, sul lago dei Quattro Cantoni, sul lago di Brienz e sul lago di Zugo. Sono state inoltre effettuate 55 indagini su 16 fiumi."
]
p40 = [
    "In totale 316 campioni provenivano da sette laghi principali in 3 maggiori bacini fluviali. Venti località sono state selezionate per essere campionate ",
    "mensilmente per un periodo di dodici mesi ad eccezione del Lago Maggiore, che è stato campionato ogni tre mesi. Sono state condotte indagini anche sul ",
    "Lago di Lugano, Lago dei Quattro Cantoni, Lago di Brienz e Lago di Zugo. Inoltre, ci sono state 55 indagini su 16 fiumi."
]

p38_40 = sectionParagraphs([p38, p39, p40], smallspace=smallest_space)



o_w, o_h = convertPixelToCm("resources/maps/esummary_map.jpeg")

f1icap = [
    "Mappa delle ubicazioni oggetto d’indagine da marzo 2020 ad agosto 2021. Le ubicazioni contrassegnate in rosso indicano le indagini su fiumi ",
    "o laghi e i punti in viola designano le ubicazioni sulle Alpi e nel Giura."
]

f1icap = makeAParagraph(f1icap, style=caption_style)

figure_kwargs = {
    "image_file":"resources/maps/esummary_map.jpeg",
    "caption": f1icap, 
    "original_width":o_w,
    "original_height":o_h,
    "desired_width": 14,
    "caption_height":1.2,
    "hAlign": "CENTER",
}

f1i = figureAndCaptionTable(**figure_kwargs)







new_components = [
    large_space,
    seci,
    small_space,
    *p36_37,
    f1i,
    small_space,
    seci2,
    small_space,
    *p38_40,
    smallest_space,
    p41,
    smallest_space,
    l2i,
    smallest_space,
    p42,
    smallest_space,
    l3i,
    smallest_space,
    p43,
    smallest_space,
    l4i,
    smallest_space,
    p44,
    smallest_space,
    l5i    
]
# add those sections
pdfcomponents = addToDoc(new_components, pdfcomponents)


# ### Totale mediano dell’indagine
# 
# I risultati sono espressi in unità di pezzi di rifiuti per 100 metri lineari (p/100 m). Il risultato mediano dell’indagine per tutti i dati è stato di circa 189 p/100 m. Il valore massimo registrato è stato di 6617 p/100 m (area d’indagine del Rodano), mentre il minimo è stato di 2 p/100 m (area d’indagine dell’Aare). L’area d’indagine del Rodano ha evidenziato il totale d’indagine mediano più alto, pari a 442 p/100 m. Questa incidenza può essere spiegata in parte sia dall’elevato numero di campioni d’indagine in contesti urbani rispetto alle altre aree d’indagine, sia dal deposito di plastiche frammentate e plastiche espanse nella zona di immissione del Rodano nella regione superiore del Lago Lemano.
# 
# Un valore di riferimento è stato calcolato escludendo i risultati dei campioni provenienti da sezioni di rive inferiori a 10 m e da oggetti di diametro inferiore a 2,5 cm. Questo metodo, descritto nella pubblicazione EU Marine Beach Litter Baselines {cite}`eubaselines` è stato utilizzato per calcolare i valori di riferimento e di soglia per tutte le spiagge europee nel 2015 e nel 2016, con un valore mediano di 131 p/100 m. I risultati del valore di baseline europeo si collocano al di fuori dell’intervallo di confidenza (CI) del 95 per cento, pari a 147-213 p/100 m, definito utilizzando i dati IQAASL.
# 
# Le indagini in Svizzera hanno evidenziato in media una portata più ridotta rispetto agli ambienti marini e sono state condotte in ubicazioni che nella maggior parte delle circostanze sarebbero considerate urbane. Finora, nel continente europeo il monitoraggio generalizzato di laghi e fiumi a monte delle regioni costiere non è stato una pratica generalizzata. È tuttavia in atto un’iniziativa coordinata, condotta da un gruppo di associazioni in Svizzera e in Francia, per definire un protocollo comune di monitoraggio e scambio di dati per il bacino del Rodano. L’Università e istituto di ricerca di Wageningen, Paesi Bassi, ha altresì iniziato ad analizzare i dati raccolti nel delta della Mosa e del Reno utilizzando protocolli analoghi a quelli IQAASL {cite}`meuserhine`.
# 

# In[15]:


sseci1 = Paragraph("Totale mediano dell’indagine", style=subsection_title)

p45 = [
    "I risultati sono espressi in unità di pezzi di rifiuti per 100 metri lineari (p/100 m). Il risultato mediano dell’indagine per tutti i dati è stato ",
    "di circa 189 p/100 m. Il valore massimo registrato è stato di 6617 p/100 m (area d’indagine del Rodano), mentre il minimo è stato di 2 p/100 m ",
    "(area d’indagine dell’Aare). L’area d’indagine del Rodano ha evidenziato il totale d’indagine mediano più alto, pari a 442 p/100 m. Questa incidenza ",
    "può essere spiegata in parte sia dall’elevato numero di campioni d’indagine in contesti urbani rispetto alle altre aree d’indagine, sia dal deposito ",
    "di plastiche frammentate e plastiche espanse nella zona di immissione del Rodano nella regione superiore del Lago Lemano."
]

p46 = [
    "Un valore di riferimento è stato calcolato escludendo i risultati dei campioni provenienti da sezioni di rive inferiori a 10 m e da oggetti di diametro inferiore ",
    'a 2,5 cm. Questo metodo, descritto nella pubblicazione EU Marine Beach Litter Baselines <a href="#HG19" color="blue">(HG19)</a> è stato utilizzato per calcolare i valori di riferimento e ',
    "di soglia per tutte le spiagge europee nel 2015 e nel 2016, con un valore mediano di 131 p/100 m. I risultati del valore di baseline europeo si collocano al di fuori ",
    "dell’intervallo di confidenza (CI) del 95 per cento, pari a 147-213 p/100 m, definito utilizzando i dati IQAASL."
]

p47 = [ 
    "Le indagini in Svizzera hanno evidenziato in media una portata più ridotta rispetto agli ambienti marini e sono state condotte in ubicazioni che nella maggior parte delle ",
    "circostanze sarebbero considerate urbane. Finora, nel continente europeo il monitoraggio generalizzato di laghi e fiumi a monte delle regioni costiere non è stato una pratica ",
    "generalizzata. È tuttavia in atto un’iniziativa coordinata, condotta da un gruppo di associazioni in Svizzera e in Francia, per definire un protocollo comune di monitoraggio e ",
    "scambio di dati per il bacino del Rodano. L’Università e istituto di ricerca di Wageningen, Paesi Bassi, ha altresì iniziato ad analizzare i dati raccolti nel delta della Mosa e ",
    'del Reno utilizzando protocolli analoghi a quelli IQAASL.  <a href="#vEV21" color="blue">(vEV21)</a>'
]

p45_47 = sectionParagraphs([p45, p46, p47], smallspace=smallest_space)
new_components = [
    small_space,
    sseci1,
    small_space,
    *p45_47,
    
]
# add those sections
pdfcomponents = addToDoc(new_components, pdfcomponents)


# ### Gli oggetti più comuni
# 
# Gli oggetti più comuni sono definiti come quegli elementi censiti in almeno il 50 per cento di tutte le indagini e/o che si collocano tra i dieci più frequenti per quantità. Come gruppo, gli oggetti più comuni rappresentano il 68 per cento di tutti gli elementi censiti nel periodo di campionamento. Nel novero degli elementi più comuni, il 27 per cento è correlato al consumo di prodotti alimentari, bevande e tabacco, mentre il 24 per cento proviene da infrastrutture e agricoltura.
# 
# Gli oggetti correlati al consumo di prodotti alimentari, bevande e tabacco vengono censiti con percentuali più elevate nelle zone d’indagine con una quota maggiore di edifici o infrastrutture fisse. Una tendenza inversa si riscontra nelle ubicazioni con una percentuale maggiore di terreni ricoperti da boschi o dedicati ad attività agricole. Materiali per infrastrutture e plastiche frammentate sono invece reperiti con una frequenza analoga in tutte le aree d’indagine, indipendentemente dalla destinazione d’uso dei terreni circostanti.

# ```{card}
# :class-card: sd-text-black
# :img-top: resources/output/slr_iqaasl_surveys.jpeg
# +++
# Figure : Gli oggetti correlati al consumo di prodotti alimentari, bevande e tabacco vengono censiti con percentuali più elevate nelle zone d’indagine con una quota maggiore di edifici o 
# ``` 

# In[16]:


f2icap = [
    "Totale delle indagini per tutti i laghi e i fiumi: gli oggetti più comuni censiti da marzo 2020 a maggio 2021. Il tasso ",
    "di occorrenza (indicato come “tasso di insuccesso” in questo rapporto) è il rapporto tra il numero di volte in cui un ",
    "oggetto è stato censito con almeno un’occorrenza rispetto al numero totale di indagini. La quantità è il numero totale ",
    "di elementi raccolti per un oggetto censito e la mediana dei pezzi di rifiuti per 100 metri lineari (p/100 m). Per esempio, ",
    "un totale di 8 485 mozziconi di sigarette è stato censito nell’87 per cento delle indagini, pari al 15 per cento degli elementi ",
    "totali raccolti e con un valore mediano di 20 mozziconi per 100 metri lineari di linea rivierasca."
]

f2i_cap = ''.join(f2icap)
fg = mcdic.to_html()






# In[17]:


sseci2 = Paragraph("Gli oggetti più comuni", style=subsection_title)

p48 = [
    "Gli oggetti più comuni sono definiti come quegli elementi censiti in almeno il 50 per cento di tutte le indagini e/o che si collocano tra i ",
    "dieci più frequenti per quantità. Come gruppo, gli oggetti più comuni rappresentano il 68 per cento di tutti gli elementi censiti nel periodo ",
    "di campionamento. Nel novero degli elementi più comuni, il 27 per cento è correlato al consumo di prodotti alimentari, bevande e tabacco, mentre ",
    "il 24 per cento proviene da infrastrutture e agricoltura."
]

p49 = [
    "Gli oggetti correlati al consumo di prodotti alimentari, bevande e tabacco vengono censiti con percentuali più elevate nelle zone d’indagine con ",
    "una quota maggiore di edifici o infrastrutture fisse. Una tendenza inversa si riscontra nelle ubicazioni con una percentuale maggiore di terreni ",
    "ricoperti da boschi o dedicati ad attività agricole. Materiali per infrastrutture e plastiche frammentate sono invece reperiti con una frequenza ",
    "analoga in tutte le aree d’indagine, indipendentemente dalla destinazione d’uso dei terreni circostanti.",
]

p48_49 = sectionParagraphs([p48, p49], smallspace=smallest_space)

new_components = [
    sseci1,
    small_space,
    *p45_47,
    sseci2,
    small_space,
    *p48_49
    
]
# add those sections
pdfcomponents = addToDoc(new_components, pdfcomponents)


# In[18]:


new_components = [
    PageBreak(),
    *references
]
# add those sections
pdfcomponents = addToDoc(new_components, pdfcomponents)

doc = SimpleDocTemplate(pdf_link, pagesize=A4, leftMargin=2.5*cm, rightMargin=2.5*cm, topMargin=2.5*cm, bottomMargin=1.5*cm)
pageinfo = f'IQAASL/Zusammengefasste/Kurzfassung'
source_prefix = "https://hammerdirt-analyst.github.io/IQAASL-End-0f-Sampling-2021/"
source = "esummary.html"

link_to_source = f'{source_prefix}{source}'

def myLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setLineWidth(.001*cm)
    canvas.setFillAlpha(.8)
    canvas.line(2.5*cm, 27.6*cm,  18.5*cm, 27.6*cm) 
    canvas.setFont('Times-Roman',9)
    canvas.drawString(2.5*cm, 1*cm, link_to_source)
    canvas.drawString(18.5*cm, 1*cm,  "S.%d " % (doc.page,))
    canvas.drawString(2.5*cm, 27.7*cm, pageinfo)
    canvas.restoreState()
    
doc.build(pdfcomponents,  onFirstPage=myLaterPages, onLaterPages=myLaterPages)


# In[ ]:




