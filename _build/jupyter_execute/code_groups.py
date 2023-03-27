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
import os
import datetime as dt
import csv, json

# math packages:
import pandas as pd
import numpy as np
import datetime as dt

# charting:
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import ticker

# build report
import reportlab
from reportlab.platypus.flowables import Flowable
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle
from reportlab.lib.colors import HexColor
from reportlab.lib import colors

# the module that has all the methods for handling the data
import resources.featuredata as featuredata
from resources.featuredata import makeAList, small_space, large_space, aSingleStyledTable, smallest_space
from resources.featuredata import caption_style, subsection_title, title_style, block_quote_style
from resources.featuredata import figureAndCaptionTable, tableAndCaption, aStyledTableWithTitleRow
from resources.featuredata import sectionParagraphs, section_title, addToDoc, makeAParagraph, bold_block


from PIL import Image as PILImage
from IPython.display import Markdown as md
from IPython.display import display
import matplotlib.image as mpimg

# home brew utitilties
import resources.sr_ut as sut
import resources.chart_kwargs as ck

from myst_nb import glue

# when setting the code group names the defintions
# are pushed to .JSON format
def push_this_to_json(filename="", data=[]):
    with open(filename, "w") as a_file:
        json.dump(data, a_file)
        
save_fig_prefix = "resources/output/"

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

def convertPixelToCm(file_name: str = None):
    im = PILImage.open(file_name)
    width, height = im.size
    dpi = im.info.get("dpi", (72, 72))
    width_cm = width / dpi[0] * 2.54
    height_cm = height / dpi[1] * 2.54
    
    return width_cm, height_cm

pdf_link = 'resources/pdfs/codegroups.pdf'
        
# this defines the css rules for the note-book table displays
header_row = {'selector': 'th:nth-child(1)', 'props': f'background-color: #FFF;'}
even_rows = {"selector": 'tr:nth-child(even)', 'props': f'background-color: rgba(139, 69, 19, 0.08);'}
odd_rows = {'selector': 'tr:nth-child(odd)', 'props': 'background: #FFF;'}
table_font = {'selector': 'tr', 'props': 'font-size: 12px;'}
table_css_styles = [even_rows, odd_rows, table_font, header_row]

style = TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('INNERGRID', (1, 1), (-1, -1), 0.25, HexColor("#8b451330", hasAlpha=True)),
            ('ROWBACKGROUNDS', (1, 1), (-1, -1), [HexColor("#8b451320", hasAlpha=True), colors.white]),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('VALIGN', (1, 0), (-1, -1), "MIDDLE"),
            ('HALIGN', (0,0), (-1, -1), "LEFT"),
        ])


# (codegroups)=
# # Codegruppen
# 
# {Download}`Download </resources/pdfs/codegroups.pdf>`
# 
# Das IQAASL-Projekt verwendete die Objektcodes und Beschreibungen aus der Masterliste des Marine Strategy Framework (MSFD) {cite}`mlwguidance`. Die Identifizierung von Objekten folgt den Protokollen der MSFD Technical Subgroup on Marine Litter. Die Hauptliste wurde auf der Grundlage der in einer Reihe von Programmen verwendeten Kategorien von Objekten entwickelt und ist eine der detailliertesten, die etablierte EU-Protokolle repräsentiert. Es gibt 217 Identifikationscodes, um alle bei einer Erhebung gesammelten Objekte zu klassifizieren. Die Objektcodes beginnen mit G1 und enden mit G217.
# 
# ## Buchhaltung für regionale Objekte
# 
# Es gibt in der Schweiz regelmässig identifizierte Artikel, die nicht in der Stammliste erscheinen. Um diese zu berücksichtigen, wurden der Masterliste 43 Codes unter dem übergeordneten Code G124 hinzugefügt. Diese Codes beginnen mit G900 und enden mit G999.
# 
# Einige MSFD-Codes wie G124 Sonstige Artikel aus Kunststoff/Polystyrol ermöglichen die Quantifizierung von nicht aufgelisteten identifizierbaren Kunststoffartikeln. Ein zusätzlicher Artikel wie G913 Schnuller kann unabhängig quantifiziert und mit dem MSFD-Code G124 verknüpft werden. Diese Arbeit wird auf dem Server erledigt und die Daten können in beiden Formen analysiert werden. 
# 
# Identifizierbare Kunststoffobjekte wurden entweder einem zusätzlichen Code wie G913 zugeordnet, oder, wenn kein anderer Code das Objekt beschrieb, wurde G124 verwendet. Einige Codes wurden aufgenommen, um pandemiebezogene Artikel zu erfassen, wie z. B.:
# 
# * G901: Maske medizinisch, synthetisch. Übergeordneter Code = G124: andere Artikel aus Kunststoff/Polystyrol identifizierbar.
# * G902: Maske medizinisch, Stoff. Übergeordneter Code = G145: andere Textilien.
# 
# Codes und übergeordnete Codes: Berücksichtigung von regionalen Unterschieden. G902 ist mit G145 durch den Wert in der Spalte parent_code verknüpft. G937 ist über den übergeordneten Code mit G124 verknüpft.

# In[2]:


# aggregated survey data
dfAgg = pd.read_csv("resources/checked_before_agg_sdata_eos_2020_21.csv")
dfAgg["date"] = pd.to_datetime(dfAgg["date"])

# get the data:
dfCodes = pd.read_csv("resources/codes_with_group_names_2015.csv")
dfCodes["pc"] = dfCodes.parent_code.where(dfCodes.parent_code != "Parent code", "none")

# language specific
# importing german code descriptions
de_codes = pd.read_csv("resources/codes_german_Version_1.csv")

# match the indexes:
de_codes.set_index("code", inplace=True)
dfCodes.set_index("code", inplace=True)

# the surveyor designated the object as aluminum instead of metal
dfCodes.loc["G708", "material"] = "Metal"

# rename the german descriptions
for x in de_codes.index:
    dfCodes.loc[x, "description"] = de_codes.loc[x, "german"]


# translate the material
dfCodes = dfCodes[dfCodes.material.isin(['Metal', 'Chemicals', 'Cloth', 'Glass', 'Paper', 'Plastic',
       'Rubber', 'Undefined', 'Unidentified', 'Wood'])]
dfCodes["material"] = dfCodes.material.map(lambda x: sut.mat_ge[x])

# translate the code groups and columns to local
dfCodes["groupname"] = dfCodes["groupname"].map(lambda x: featuredata.group_names_de[x])

# rename the columns
new_names = {"description":"Objekte", "groupname":"Gruppenname", "material":"Material", "Parent code":"pc"}
dfCodes.rename(columns=new_names, inplace=True)

# the columns to display
cols_to_display = list(new_names.values())

mcc = dfCodes.loc[["G124", "G902", "G145","G937"]][cols_to_display]
mcc.index.name = None
mcc.columns.name = None

data = mcc.copy()

regional_objects  = featuredata.aSingleStyledTable(data, style=style, colWidths=[1.5*cm, 7.3*cm, 3.5*cm, 2*cm, 2*cm])

mcc = mcc.style.set_table_styles(table_css_styles)
mcc


# In[3]:


pdfcomponents = []
chapter_title = Paragraph("Codegruppen", style=title_style)

p_one = [
    "Das IQAASL-Projekt verwendete die Objektcodes und Beschreibungen aus der Masterliste des Marine Strategy Framework ",
    '(MSFD) <a href="#Han13" color="blue"> (Han13) </a>. Die Identifizierung von Objekten folgt den Protokollen der MSFD Technical Subgroup on ',
    "Marine Litter. Die Hauptliste wurde auf der Grundlage der in einer Reihe von Programmen verwendeten Kategorien von ",
    "Objekten entwickelt und ist eine der detailliertesten, die etablierte EU-Protokolle repräsentiert. Es gibt 217 ",
    "Identifikationscodes, um alle bei einer Erhebung gesammelten Objekte zu klassifizieren. Die Objektcodes beginnen ",
    "mit G1 und enden mit G217."
]

p_one = makeAParagraph(p_one)

section_one = Paragraph("Buchhaltung für regionale Objekte", style=subsection_title)

p_two = [
    "Es gibt in der Schweiz regelmässig identifizierte Artikel, die nicht in der Stammliste erscheinen. Um ",
    "diese zu berücksichtigen, wurden der Masterliste 43 Codes unter dem übergeordneten Code G124 hinzugefügt. ",
    "Diese Codes beginnen mit G900 und enden mit G999."
]

p_3 = [
    "Einige MSFD-Codes wie G124 Sonstige Artikel aus Kunststoff/Polystyrol ermöglichen die Quantifizierung von ",
    "nicht aufgelisteten identifizierbaren Kunststoffartikeln. Ein zusätzlicher Artikel wie G913 Schnuller kann ",
    "unabhängig quantifiziert und mit dem MSFD-Code G124 verknüpft werden. Diese Arbeit wird auf dem Server erledigt ",
    "und die Daten können in beiden Formen analysiert werden."
]

p_4 = [
    "Identifizierbare Kunststoffobjekte wurden entweder einem zusätzlichen Code wie G913 zugeordnet, oder, wenn kein ",
    "anderer Code das Objekt beschrieb, wurde G124 verwendet. Einige Codes wurden aufgenommen, um pandemiebezogene ",
    "Artikel zu erfassen, wie z. B.:"
]

p_2_4 = sectionParagraphs([p_two, p_3, p_4], smallspace=smallest_space)

first_list = [
    "G901: Maske medizinisch, synthetisch. Übergeordneter Code = G124: andere Artikel aus Kunststoff/Polystyrol identifizierbar.",
    "G902: Maske medizinisch, Stoff. Übergeordneter Code = G145: andere Textilien."
]

first_list = makeAList(first_list)

p_5 = [
    "Codes und übergeordnete Codes: Berücksichtigung von regionalen Unterschieden. G902 ist mit G145 durch ",
    "den Wert in der Spalte parent_code verknüpft. G937 ist über den übergeordneten Code mit G124 verknüpft."
]

p_5 = makeAParagraph(p_5)

Han13 = [
    '<a name="Han13"/>Han13: <i>George Hanke</i>. Guidance on monitoring of marine litter in european seas. Joint Research Centre of the European Commission, 2013.'
]

han13 = makeAParagraph(Han13)

references = [han13]


# ### Modifikation von Artikeln nach Grösse und Materialbeschreibungen
# 
# Der IQAASL-Bericht enthält mehrere wichtige Grössen- und Materialänderungen in den Kategorien zerbrochener Kunststoff und Schaumstoff. Andere Änderungen umfassen die Erweiterung oder Einschränkung von Artikelbeschreibungen.
# 
# Zum Beispiel: 
# 
# * G96 Damenbinden, Slipeinlagen enthält neu auch Tampon-Applikatoren aus Kunststoff.
# * G211 Klebebandagen, bisher als nicht klassifiziertes Material aus Kunststoff erfasst.
# 
# Um Mikrokunststoffe für dieses Projekt bestmöglich zu identifizieren und zu quantifizieren, wurden 3 Codes aus der Masterliste nach Grösse modifiziert.
# 
# Folgende Codes wurden geändert, um Objekte mit einer Grösse von weniger als 5 mm zu berücksichtigen:
# 
# * G75 Kunststoff-/Polystyrolstücke 0 – 2,5 cm modifiziert auf 0,5 cm – 2,5 cm
# * G78 Kunststoffteile 0 – 2,5 cm modifiziert auf 0,5 cm – 2,5 cm
# * G81 Polystyrolstücke 0 – 2,5 cm modifiziert auf 0,5 cm – 2,5 cm

# ```{figure} resources/images/codegroups/20200819_080041.jpg
# :name: image_one_codes
# ` `
# ```
# {numref}`Abildung %s: <image_one_codes>` Plastikteile in verschiedenen Grössen

# In[4]:


subsection_one = Paragraph("Modifikation von Artikeln nach Grösse und Materialbeschreibungen", style=subsection_title)

p_6 = [
    "Der IQAASL-Bericht enthält mehrere wichtige Grössen- und Materialänderungen in den Kategorien zerbrochener Kunststoff und ",
    "Schaumstoff. Andere Änderungen umfassen die Erweiterung oder Einschränkung von Artikelbeschreibungen."
]

p_7 = ["Zum Beispiel:"]

p_6_7 = sectionParagraphs([p_6, p_7], smallspace=smallest_space)

second_list = [
    "G96 Damenbinden, Slipeinlagen enthält neu auch Tampon-Applikatoren aus Kunststoff.",
    "G211 Klebebandagen, bisher als nicht klassifiziertes Material aus Kunststoff erfasst."
]

second_list = makeAList(second_list)

p_8 = [
    "Um Mikrokunststoffe für dieses Projekt bestmöglich zu identifizieren und zu quantifizieren, wurden 3 Codes aus der Masterliste nach Grösse modifiziert."
]

p_9 = [
    "Folgende Codes wurden geändert, um Objekte mit einer Grösse von weniger als 5 mm zu berücksichtigen:"
]

p_8_9 = sectionParagraphs([p_8, p_9], smallspace=smallest_space)

third_list = [
    "G75 Kunststoff-/Polystyrolstücke 0 – 2,5 cm modifiziert auf 0,5 cm – 2,5 cm",
    "G78 Kunststoffteile 0 – 2,5 cm modifiziert auf 0,5 cm – 2,5 cm",
    "G81 Polystyrolstücke 0 – 2,5 cm modifiziert auf 0,5 cm – 2,5 cm"
]

third_list = makeAList(third_list)
o_w, o_h = convertPixelToCm("resources/images/codegroups/20200819_080041.jpg")
caption_1 = [" Plastikteile in verschiedenen Grössen"]
caption_1 = makeAParagraph(caption_1)

figure_kwargs = {
    "image_file":"resources/images/codegroups/20200819_080041.jpg",
    "caption": caption_1, 
    "original_width":o_w,
    "original_height":o_h,
    "desired_width": 15,
    "caption_height":.75,
    "hAlign": "CENTER",
}

figure_1 = figureAndCaptionTable(**figure_kwargs)

new_components = [
    chapter_title,
    small_space,
    p_one,
    small_space,
    section_one,
    small_space,
    *p_2_4,
    first_list,
    smallest_space,
    p_5,
    small_space,
    regional_objects,
    small_space,
    subsection_one,
    small_space,
    *p_6_7,
    second_list,
    smallest_space,
    *p_8_9,
    third_list,    
    small_space,   
    figure_1
]

pdfcomponents = addToDoc(new_components, pdfcomponents)


# In[5]:


# directory listing of the group definitions
code_group2 = {
    "waste water": "wastewater.json" ,
    "micro plastics (< 5mm)":"codeListMicros.json",
    "infrastructure":"construction2.json",
    "food and drink":"foodstuff.json",
    "agriculture":"ag2.json",
    "tobacco":"tobac.json",
    "plastic pieces":"plasticpcs.json",
    "recreation":"recreation.json",    
    "packaging non food":"packaging.json",
    "personal items":"pi.json", 
    "unclassified": "nogroup.json"
}
# saving to .json
# push_this_to_json(filename=F"{project_directory}/code_group2.json", data=code_group2)


# ###  Gfoams: Geschäumte Kunststoffe, Gschaumstoffe
# 
# Expandiertes Polystyrol G81, G82, G83, zusammengefasst als Gfoam, sind leichte, mürbe, oft weisse Schaumstoffe, die für Verpackungen oder zur Isolierung verwendet werden. Geschäumte Kunststoffartikel, die üblicherweise für Lebensmittel zum Mitnehmen (G10), Schwammschäume (G73) und dichtere Isolierschäume (G74) verwendet werden, werden separat kategorisiert und sind nicht in der Gruppe des expandierten Polystyrols enthalten. 
# 
# Der Verpackungsschaumstoff/Isolierschaumstoff/Polyurethan G74 wurde in dieser Studie um extrudierte Polystyrole (XPS) erweitert, die üblicherweise als Isoliermaterial verwendet werden, und umgekehrt für G81, G82 und G83 Polystyrolstücke auf expandiertes Polystyrol (EPS) grösser als 0,5 cm eingegrenzt. Mit diesen Änderungen sollten Isolierschaumstoffe von Verpackungsschaumstoffen unterschieden werden, obwohl beide für eine Vielzahl von Anwendungen verwendet werden. Die Materialänderungen an den geschäumten Kunststoffen werden für die Analyse zum übergeordneten Code zusammengefasst und separat erfasst. Ein detailliertes Verzeichnis der Art und Grösse des Schaumstoffs wird mit jedem Bericht geliefert. 
# 
# :::{note}
# Polystyrolkügelchen unter 5 mm, Markenname Styrofoam® sind mit Mikrokunststoffen (G117) Styropor < 5 mm gruppiert.
# :::

# In[6]:


wwcodes = dfCodes.loc[["G81", "G82", "G83"]][cols_to_display]
wwcodes.index.name = None

data = wwcodes.copy()

gfoams  = featuredata.aSingleStyledTable(data, style=style, colWidths=[1.5*cm, 7.3*cm, 3.5*cm, 2*cm, 2*cm])
wwcodes.style.set_table_styles(table_css_styles)


# ```{figure} resources/images/codegroups/20210221CheyresFoam.jpg
# :name: image_two_codes
# ` `
# ```
# {numref}`Abildung %s: <image_two_codes>` Verschiedene Grössen von weissem expandiertem Polystyrol und anderen Schaumstoffen

# In[7]:


subsection_two = Paragraph("Gfoams: Geschäumte Kunststoffe, Gschaumstoffe", style=subsection_title)

p10 = [
    "Expandiertes Polystyrol G81, G82, G83, zusammengefasst als Gfoam, sind leichte, mürbe, oft weisse ",
    "Schaumstoffe, die für Verpackungen oder zur Isolierung verwendet werden. Geschäumte Kunststoffartikel, ",
    "die üblicherweise für Lebensmittel zum Mitnehmen (G10), Schwammschäume (G73) und dichtere Isolierschäume ",
    "(G74) verwendet werden, werden separat kategorisiert und sind nicht in der Gruppe des expandierten ",
    "Polystyrols enthalten."
]

p11 = [
    "Der Verpackungsschaumstoff/Isolierschaumstoff/Polyurethan G74 wurde in dieser Studie um extrudierte Polystyrole ",
    "(XPS) erweitert, die üblicherweise als Isoliermaterial verwendet werden, und umgekehrt für G81, G82 und G83 ",
    "Polystyrolstücke auf expandiertes Polystyrol (EPS) grösser als 0,5 cm eingegrenzt. Mit diesen Änderungen sollten ",
    "Isolierschaumstoffe von Verpackungsschaumstoffen unterschieden werden, obwohl beide für eine Vielzahl von ",
    "Anwendungen verwendet werden. Die Materialänderungen an den geschäumten Kunststoffen werden für die Analyse zum ",
    "übergeordneten Code zusammengefasst und separat erfasst. Ein detailliertes Verzeichnis der Art ",
    "und Grösse des Schaumstoffs wird mit jedem Bericht geliefert."
]

p12 = ["Polystyrolkügelchen unter 5 mm, Markenname Styrofoam® sind mit Mikrokunststoffen (G117) Styropor < 5 mm gruppiert."]

p_10_11 = sectionParagraphs([p10, p11], smallspace=smallest_space)

p_12 = makeAParagraph(p12, style=bold_block)

o_w, o_h = convertPixelToCm("resources/images/codegroups/20210221CheyresFoam.jpg")
caption_2 = ["Verschiedene Grössen von weissem expandiertem Polystyrol und anderen Schaumstoffen"]
caption_2 = makeAParagraph(caption_2)

figure_kwargs = {
    "image_file":"resources/images/codegroups/20210221CheyresFoam.jpg",
    "caption": caption_2, 
    "original_width":o_w,
    "original_height":o_h,
    "desired_width": 15,
    "caption_height":.75,
    "hAlign": "CENTER",
}

figure_2 = figureAndCaptionTable(**figure_kwargs)

new_components = [
    PageBreak(),
    subsection_two,
    small_space,
    *p_10_11,
    p_12,
    small_space,
    gfoams,
    small_space,
    figure_2
    
]

pdfcomponents = addToDoc(new_components, pdfcomponents)


# ### Nicht anwendbar oder ausgelassene Punkte
# 
# Von den 217 verfügbaren MSFD-Codes wurden 176 in den Erhebungen 2020–2021 identifiziert. Mehrere Punkte sind nicht auf Schweizer Gewässer anwendbar, da sie sich auf die marine Aquakulturproduktion beziehen:
# 
# * G207 Oktopus-Töpfe
# * G163 Krabben- und Hummerkörbe
# * G215 Lebensmittelabfälle/Getränkeabfälle

# ```{figure} resources/images/codegroups/petite_plage_yverdon_lesBains15_02_2021.png
# :name: image_three_codes
# ` `
# ```
# {numref}`Abildung %s: <image_three_codes>` Alle biologisch abbaubaren Lebensmittelabfälle sowie die Sammlung und Quantifizierung von Fäkalien wurden bei diesem Projekt ausgelassen.

# ## Objekte gruppiert nach Nutzen 
# 
# Der Nutzen basiert auf der Nutzung des Objekts, bevor es weggeworfen wurde, oder auf der Artikelbeschreibung, wenn die ursprüngliche Nutzung unbestimmt ist. Identifizierte Objekte werden in einen der vordefinierten Kategoriecodes eingeordnet. Diese einzelnen Artikelcodes wurden gruppiert, um die Verwendung oder die Materialart für diesen Bericht bestmöglich zu beschreiben. Die Gruppierung der Codes ist eine breit angelegte Analysemethode, um die in den Wassersystemen gefundenen weggeworfenen Materialien nach Wirtschaftszweigen oder physikalischen Eigenschaften zu bewerten. Die Objekte werden in diesem Bericht auch unabhängig voneinander analysiert. Die Gruppierung wurde aus Feldbeobachtungen und Untersuchungen abgeleitet, um mögliche Quellen für verschiedene Schadstoffe zu ermitteln
# 
# * __Abwasser:__ Gegenstände, die aus Kläranlagen freigesetzt werden, einschliesslich Gegenstände, die wahrscheinlich mit der Toilette gespült werden
# * __Mikrokunststoffe:__ (< 5mm): zersplitterte Kunststoffe, geschäumte Kunststoffe und Kunststoffharze für die Vorproduktion  
# * __Infrastruktur:__ Posten im Zusammenhang mit dem Bau und der Instandhaltung von Gebäuden, Strassen und der Wasser-/Stromversorgung 
# * __Essen und Trinken:__ alle Materialien, die mit dem Konsum von Essen und Trinken zu tun haben 
# * __Landwirtschaft:__ hauptsächlich industrielle Folien, z.B. Mulch und Reihenabdeckungen, Gewächshäuser, Bodenbegasung, Ballenverpackungen. Einschliesslich Hartkunststoffe für landwirtschaftliche Zäune, Blumentöpfe usw. 
# * __Tabakwaren:__ hauptsächlich Zigarettenfilter, einschliesslich aller mit dem Rauchen verbundenen Materialien 
# * __Erholung:__ Objekte, die mit Sport und Freizeit zu tun haben, z. B. Angeln, Jagen, Wandern usw. 
# * __Verpackungen, die nicht für Lebensmittel und Getränke bestimmt sind:__ Verpackungsmaterial, das nicht als Lebensmittel, Getränke oder Tabakwaren gekennzeichnet ist
# * __Kunststoffteile (> 5mm):__ zersplitterte Kunststoffe unbestimmter Herkunft oder Verwendung  
# * __Persönliche Gegenstände:__ Accessoires, Hygieneartikel und Kleidung 
# * __Nicht klassifiziert:__ nicht gruppierte Artikelcodes

# In[8]:


o_w, o_h = convertPixelToCm("resources/images/codegroups/petite_plage_yverdon_lesBains15_02_2021.png")
caption_3 = ["Alle biologisch abbaubaren Lebensmittelabfälle sowie die Sammlung und Quantifizierung von Fäkalien wurden bei diesem Projekt ausgelassen."]
caption_3 = makeAParagraph(caption_3)

figure_kwargs = {
    "image_file":"resources/images/codegroups/petite_plage_yverdon_lesBains15_02_2021.png",
    "caption": caption_3, 
    "original_width":o_w,
    "original_height":o_h,
    "desired_width": 15,
    "caption_height":1,
    "hAlign": "CENTER",
}

figure_3 = figureAndCaptionTable(**figure_kwargs)

subsection_three = Paragraph("Nicht anwendbar oder ausgelassene Punkte", style=subsection_title)

p13 = [
    "Von den 217 verfügbaren MSFD-Codes wurden 176 in den Erhebungen 2020–2021 identifiziert. Mehrere ",
    "Punkte sind nicht auf Schweizer Gewässer anwendbar, da sie sich auf die marine Aquakulturproduktion beziehen:"
]
p13 = makeAParagraph(p13)

fourth_list = [
    "G207 Oktopus-Töpfe",
    "G163 Krabben- und Hummerkörbe",
    "G215 Lebensmittelabfälle/Getränkeabfälle"
]
fourth_list = makeAList(fourth_list)

section_2_title = Paragraph("Objekte gruppiert nach Nutzen", style=section_title)

p14 = [
    "Der Nutzen basiert auf der Nutzung des Objekts, bevor es weggeworfen wurde, oder auf der Artikelbeschreibung, ",
    "wenn die ursprüngliche Nutzung unbestimmt ist. Identifizierte Objekte werden in einen der vordefinierten ",
    "Kategoriecodes eingeordnet. Diese einzelnen Artikelcodes wurden gruppiert, um die Verwendung oder die Materialart ",
    "für diesen Bericht bestmöglich zu beschreiben. Die Gruppierung der Codes ist eine breit angelegte Analysemethode, ",
    "um die in den Wassersystemen gefundenen weggeworfenen Materialien nach Wirtschaftszweigen oder physikalischen ",
    "Eigenschaften zu bewerten. Die Objekte werden in diesem Bericht auch unabhängig voneinander analysiert. Die ",
    "Gruppierung wurde aus Feldbeobachtungen und Untersuchungen abgeleitet, um mögliche Quellen für verschiedene Schadstoffe zu ermitteln"
]

p14=makeAParagraph(p14)

fifth_list = [
    "<b>Abwasser: </b> Gegenstände, die aus Kläranlagen freigesetzt werden, einschliesslich Gegenstände, die wahrscheinlich mit der Toilette gespült werden",
    "<b>Mikrokunststoffe (< 5mm): </b> zersplitterte Kunststoffe, geschäumte Kunststoffe und Kunststoffharze für die Vorproduktion",
    "<b>Infrastruktur: </b> Posten im Zusammenhang mit dem Bau und der Instandhaltung von Gebäuden, Strassen und der Wasser-/Stromversorgung",
    "<b>Essen und Trinken: </b> alle Materialien, die mit dem Konsum von Essen und Trinken zu tun haben",
    "<b>Landwirtschaft: </b> hauptsächlich industrielle Folien, z.B. Mulch und Reihenabdeckungen, Gewächshäuser, Bodenbegasung, Ballenverpackungen. Einschliesslich Hartkunststoffe für landwirtschaftliche Zäune, Blumentöpfe usw.",
    "<b>Tabakwaren: </b>hauptsächlich Zigarettenfilter, einschliesslich aller mit dem Rauchen verbundenen Materialien",
    "<b>Erholung: </b>Objekte, die mit Sport und Freizeit zu tun haben, z. B. Angeln, Jagen, Wandern usw.",
    "<b>Verpackungen, die nicht für Lebensmittel und Getränke bestimmt sind: </b> Verpackungsmaterial, das nicht als Lebensmittel, Getränke oder Tabakwaren gekennzeichnet ist",
    "<b>Kunststoffteile (> 5mm): </b>zersplitterte Kunststoffe unbestimmter Herkunft oder Verwendung",
    "<b>Persönliche Gegenstände: </b>Accessoires, Hygieneartikel und Kleidung",
    "<b>Nicht klassifiziert: </b>nicht gruppierte Artikelcodes"
]

fifth_list = makeAList(fifth_list)
p15 = [
    "Im Anhang befindet sich die vollständige Liste der identifizierten Objekte, einschliesslich Beschreibungen und Gruppenklassifizierung."
]

p15 = makeAParagraph(p15)

new_components = [
    PageBreak(),
    subsection_three,
    small_space,
    p13,
    smallest_space,
    fourth_list,
    smallest_space,
    figure_3,
    small_space,
    section_2_title,
    small_space,
    p14,
    smallest_space,
    fifth_list,
    smallest_space,
    p15
    
]

pdfcomponents = addToDoc(new_components, pdfcomponents)


# In[9]:


# read images
img_a = mpimg.imread("resources/images/codegroups/industrialsheeting_800_600.jpg")
img_b = mpimg.imread("resources/images/codegroups/20210419yverdon_rec.jpg")
img_c = mpimg.imread("resources/images/codegroups/infrastructure_450_600.jpg")
img_d = mpimg.imread("resources/images/codegroups/20201220_wt_pi_crop.jpg")

# display images
fig, ax = plt.subplots(2,2, figsize=(14,11))

axone=ax[0,0]
sut.hide_spines_ticks_grids(axone)
axone.imshow(img_a);
axone.set_title("Landwirtschaft, Industriefolien", **ck.title_k14)

axtwo=ax[0,1]
sut.hide_spines_ticks_grids(axtwo)
axtwo.imshow(img_b);
axtwo.set_title("Freizeit: Spielzeug, Feuerwerkskörper, Flintenpatronen, Angelartikel", **ck.title_k14)

axthree=ax[1,0]
sut.hide_spines_ticks_grids(axthree)
axthree.imshow(img_c);
axthree.set_title("Infrastruktur: Kunststoffbau", **ck.title_k14)

axfour=ax[1,1]
sut.hide_spines_ticks_grids(axfour)
axfour.set_title("Abwasser und persönliche Gegenstände: Biofilter, Damenbinde", **ck.title_k14)
axfour.imshow(img_d);

plt.tight_layout()


figure_name = f"code_groups_images"
types_survey_locations_file_name = f'{save_fig_prefix}{figure_name}.jpeg'

# figure caption
sample_total_notes = [
    "Erhebungsergebnisse und zusammenfassende Statistiken: ",
    "Proben grösser als 10m und ohne Objekte kleiner als 2,5cm und Chemikalien, n=372"
]

code_groups_images_notes = ''.join(sample_total_notes)

glue("code_groups_images_notes", code_groups_images_notes, display=False)


glue("code_groups_images", fig, display=False)
plt.close()


# ```{glue:figure} code_groups_images
# :name: "code_groups_images"
# 
# 
# ` `
# 
# ```
# 
# {numref}`Abbildung {number}: <code_groups_images>` Objekte gruppiert nach Nutzen

# In[10]:


o_w, o_h = convertPixelToCm("resources/images/codegroups/industrialsheeting_800_600.jpg")

figure_kwargs = {
    "image_file":"resources/images/codegroups/industrialsheeting_800_600.jpg",
    "caption": None, 
    "original_width":o_w,
    "original_height":o_h,
    "desired_width": 7.95,
    "caption_height":1,
    "hAlign": "CENTER",
}

one_of_4 = figureAndCaptionTable(**figure_kwargs)
cap_one = Paragraph("Landwirtschaft, Industriefolien", caption_style)

o_w, o_h = convertPixelToCm("resources/images/codegroups/20210419yverdon_rec.jpg")
figure_kwargs.update({
    "image_file":"resources/images/codegroups/20210419yverdon_rec.jpg",
    "original_width":o_w,
    "original_height":o_h,
    "desired_width": 7.95,
})

two_of_4 = figureAndCaptionTable(**figure_kwargs)
cap_two = Paragraph("Freizeit: Spielzeug, Feuerwerkskörper, Flintenpatronen", caption_style)

o_w, o_h = convertPixelToCm("resources/images/codegroups/infrastructure_450_600.jpg")
figure_kwargs.update({
    "image_file":"resources/images/codegroups/infrastructure_450_600.jpg",
    "original_width":o_w,
    "original_height":o_h,
    "desired_width": 7.95,
})

three_of_4 = figureAndCaptionTable(**figure_kwargs)
cap_three = Paragraph("Infrastruktur: Kunststoffbau", caption_style)

o_w, o_h = convertPixelToCm("resources/images/codegroups/20201220_wt_pi_crop.jpg")
figure_kwargs.update({
    "image_file":"resources/images/codegroups/20201220_wt_pi_crop.jpg",
    "original_width":o_w,
    "original_height":o_h,
    "desired_width": 7.95,
})

four_of_4 = figureAndCaptionTable(**figure_kwargs)
cap_four = Paragraph("Abwasser und persönliche Gegenstände: Biofilter", caption_style)

table_data = [
    [[cap_one, one_of_4], [cap_two, two_of_4]],
    [[cap_three, three_of_4], [cap_four,four_of_4]]
]

col_widths = [8*cm, 8*cm]

fig_one_to_four = Table(table_data, colWidths=col_widths)

new_components = [small_space, fig_one_to_four, small_space]
pdfcomponents = addToDoc(new_components, pdfcomponents)


# ### Abwasserbehandlung
# 
# Zu den Codes für die Abwasserbehandlung gehören Biomassehalter, die in Abfallbehandlungsprozessen verwendet werden, sowie wahrscheinliche Toilettenspülungen wie Wattestäbchen.  
# 
# :::{note}
# G98 umfasst Windeln und Feuchttücher. Windeln werden in den Schweizer Wassersystemen nur selten gefunden, die Mengen sollten den Körperpflegetüchern zugeordnet werden.
# :::

# In[11]:


subsection_four = Paragraph("Abwasserbehandlung", style=subsection_title)

p16 = [
    "Zu den Codes für die Abwasserbehandlung gehören Biomassehalter, die in Abfallbehandlungsprozessen ",
    "verwendet werden, sowie wahrscheinliche Toilettenspülungen wie Wattestäbchen."
]

p16 = makeAParagraph(p16)

p17 = [
    "G98 umfasst Windeln und Feuchttücher. Windeln werden in den Schweizer Wassersystemen nur selten gefunden, die Mengen sollten den Körperpflegetüchern zugeordnet werden."
]

p17 = makeAParagraph(p17, style=bold_block)

# group definition
wastewater = [
    "G91",
    "G95",
    "G96",
    "G98",
    "G97",
    "G100",
    "G133",
    "G932",
    "G144"
]

wwcodes = dfCodes.loc[wastewater][cols_to_display]
wwcodes.index.name = None

data = wwcodes.copy()

abwasser  = featuredata.aSingleStyledTable(data, style=style, colWidths=[1.5*cm, 7.3*cm, 3.5*cm, 2*cm, 2*cm])
wwcodes.style.set_table_styles(table_css_styles)


# In[12]:


new_components = [
    PageBreak(),
    subsection_four,
    small_space,
    p16,
    smallest_space,
    p17,
    small_space,
    abwasser,
    
]
pdfcomponents = addToDoc(new_components, pdfcomponents)   


# ### Mikrokunststoffe 
# 
# Die Gruppe der Mikrokunststoffe umfasst alle Kunststoffe und geschäumten Kunststoffe mit einer Grösse von weniger als 5 mm aus der MSFD-Stammliste {cite}`mlwguidance` der Positionen G103–G123. In unseren Daten sind nicht alle Codes identifiziert worden. Das Ziel dieses Projekts war die Quantifizierung der beobachtbaren Abfälle, die in der Regel grösser als 5 mm sind, aber die untere Grenze der ohne Hilfsmittel sichtbaren Objekte bei der Vermessung einer Uferlinie liegt bei etwa 2–5 mm. Im Laufe einer Untersuchung werden mit dem grösseren Material auch sichtbare Kleinstteile gesammelt, deren Zusammensetzung im Allgemeinen identifizierbar ist. Im Rahmen des IQAASL-Projekts wurden keine Methoden zur gezielten Erfassung von Objekten mit einer Grösse von weniger als 5 mm eingesetzt, aber alle sichtbaren Mikrokunststoffe, die während einer Untersuchung gesammelt wurden, wurden quantifiziert, gewogen und kategorisiert.

# In[13]:


# define group
codesmicro=["G112", "G106", "G117", "G103", "G104", "G105", "G107", "G108", "G109", "G110", "G111", "G113", "G114", "G115", "G116", "G118", "G119", "G120", "G121", "G122", "G123"]

# make table
wwcodes = dfCodes.loc[codesmicro][cols_to_display]
wwcodes.index.name = None
data = wwcodes.copy()

mikrokuntsoffe  = featuredata.aSingleStyledTable(data, style=style, colWidths=[1.5*cm, 7.3*cm, 3.5*cm, 2*cm, 2*cm])
wwcodes.style.set_table_styles(table_css_styles)


# In[14]:


subsection_five = Paragraph("Mikrokunststoffe", style=subsection_title)

p18 = [
    "Die Gruppe der Mikrokunststoffe umfasst alle Kunststoffe und geschäumten Kunststoffe mit einer Grösse ",
    'von weniger als 5 mm aus der MSFD-Stammliste <a href="#Han13" color="blue"> (Han13) </a> der Positionen G103–G123. In unseren Daten ',
    "sind nicht alle Codes identifiziert worden. Das Ziel dieses Projekts war die Quantifizierung der beobachtbaren ",
    "Abfälle, die in der Regel grösser als 5 mm sind, aber die untere Grenze der ohne Hilfsmittel sichtbaren Objekte ",
    "bei der Vermessung einer Uferlinie liegt bei etwa 2–5 mm. Im Laufe einer Untersuchung werden mit dem grösseren ",
    "Material auch sichtbare Kleinstteile gesammelt, deren Zusammensetzung im Allgemeinen identifizierbar ist. Im ",
    "Rahmen des IQAASL-Projekts wurden keine Methoden zur gezielten Erfassung von Objekten mit einer Grösse von weniger ",
    "als 5 mm eingesetzt, aber alle sichtbaren Mikrokunststoffe, die während einer Untersuchung gesammelt wurden, wurden ",
    "quantifiziert, gewogen und kategorisiert."
]

p18 = makeAParagraph(p18)

new_components = [
    PageBreak(),
    subsection_five,
    small_space,
    p18,
    small_space,
    mikrokuntsoffe,
    
    
]
pdfcomponents = addToDoc(new_components, pdfcomponents)
    


# ### Infrastruktur 
# 
# Infrastruktur bezieht sich auf alle Formen des Baus, der Renovierung und der Instandhaltung von öffentlichen und privaten Bauwerken, einschliesslich Strassen, Brücken und Häfen sowie der Strom- und Wasserversorgung. Entlang aller untersuchten Seen wurden bedeutende Mengen an Baukunststoffen und insbesondere an geschäumten Kunststoffen festgestellt [Alle Erhebungen](allsurveys).
# 
# Gängige Kunststoffe im Bauwesen sind Rohrstücke, Kabelschutzvorrichtungen, flexible und starre Schläuche sowie die dazugehörigen Verbindungsstücke, Armaturen und Abdeckungen. Kunststoffe, die bei der Betonherstellung verwendet werden, wie Dübel, Anker und Abstandshalter, wurden ebenfalls häufig identifiziert. Einige Artikel, die mit Kunststoffen im Bauwesen in Verbindung gebracht werden, haben eindeutige Codes wie G93 Kabelbinder oder G17 Behälter für Injektionspistolen. 
# 
# Andere Elemente in der Gruppe Infrastruktur haben einen allgemeineren Anwendungsfall:
# 
# * G186 Industrieschrott
# * G194 Metallkabel

# In[15]:


subsection_six = Paragraph("Infrastruktur", style=subsection_title)

p19 =[
    "Infrastruktur bezieht sich auf alle Formen des Baus, der Renovierung und der Instandhaltung von ",
    "öffentlichen und privaten Bauwerken, einschliesslich Strassen, Brücken und Häfen sowie der Strom- ",
    "und Wasserversorgung. Entlang aller untersuchten Seen wurden bedeutende Mengen an Baukunststoffen ",
    "und insbesondere an geschäumten Kunststoffen festgestellt",
    '<a href="https://hammerdirt-analyst.github.io/IQAASL-End-0f-Sampling-2021/lakes_rivers.html" color="blue"> Alle Erhebunen </a>'
]

p20 = [
    "Gängige Kunststoffe im Bauwesen sind Rohrstücke, Kabelschutzvorrichtungen, flexible und starre Schläuche ",
    "sowie die dazugehörigen Verbindungsstücke, Armaturen und Abdeckungen. Kunststoffe, die bei der Betonherstellung ",
    "verwendet werden, wie Dübel, Anker und Abstandshalter, wurden ebenfalls häufig identifiziert. Einige Artikel, ",
    "die mit Kunststoffen im Bauwesen in Verbindung gebracht werden, haben eindeutige Codes wie G93 Kabelbinder ",
    "oder G17 Behälter für Injektionspistolen."
]

p21 = [
    "Andere Elemente in der Gruppe Infrastruktur haben einen allgemeineren Anwendungsfall:"
]

p19_21 = sectionParagraphs([p19, p20, p21], smallspace=smallest_space)

sixth_list = [
    "G186 Industrieschrott",
    "G194 Metallkabel"
]

sixth_list = makeAList(sixth_list)


# ####  Infrastruktur: geschäumter Kunststoff
# 
# Alle geschäumten Kunststoffe, die mit Isolieranwendungen in Verbindung gebracht werden, werden der Gruppe Infrastruktur zugeordnet. Extrudierte Schaumstoffe sind relativ dichte mehrfarbige Schaumstoffplatten und Sprühschäume, die grösser als 5 mm sind. Expandiertes Polystyrol wird aufgrund der häufigen Verwendung als Aussenisolierung für oberirdische Anwendungen als Infrastruktur eingestuft. Zusätzliche Codes wurden geschaffen, um Grössenvariationen von Schaumstoffen zu quantifizieren, G909–G912. Die Änderungen in der Materialbeschreibung zielen darauf ab, Schaumstoffe zur Bauisolierung von Verpackungsschaumstoffen zu unterscheiden, obwohl beide für eine Vielzahl von Anwendungen verwendet werden. Die Materialänderungen an den geschäumten Kunststoffen werden für die Analyse unter dem übergeordneten Code zusammengefasst und separat erfasst. Ein detailliertes Verzeichnis der Art und Grösse der geschäumten Kunststoffe wird mit jedem Bericht geliefert.

# ```{figure} resources/images/codegroups/fragfoam_450_600.jpg
# :name: image_four_codes
# ` `
# ```
# {numref}`Abildung %s: <image_four_codes>`Schaumstoffe in verschiedenen Grössen; XPS, EPS und Sprühschäume (SPF) entlang der Schweizer Uferlinien

# In[16]:


subsection_seven = Paragraph("Infrastruktur: geschäumter Kunststoff", style=subsection_title)

p22 = [
    "Alle geschäumten Kunststoffe, die mit Isolieranwendungen in Verbindung gebracht werden, werden ", 
    "der Gruppe Infrastruktur zugeordnet. Extrudierte Schaumstoffe sind relativ dichte mehrfarbige ",
    "Schaumstoffplatten und Sprühschäume, die grösser als 5 mm sind. Expandiertes Polystyrol wird ",
    "aufgrund der häufigen Verwendung als Aussenisolierung für oberirdische Anwendungen als Infrastruktur ",
    "eingestuft. Zusätzliche Codes wurden geschaffen, um Grössenvariationen von Schaumstoffen zu ",
    "quantifizieren, G909–G912. Die Änderungen in der Materialbeschreibung zielen darauf ab, Schaumstoffe ",
    "zur Bauisolierung von Verpackungsschaumstoffen zu unterscheiden, obwohl beide für eine Vielzahl von ",
    "Anwendungen verwendet werden. Die Materialänderungen an den geschäumten Kunststoffen werden für die ",
    "Analyse unter dem übergeordneten Code zusammengefasst und separat erfasst. Ein detailliertes Verzeichnis ",
    "der Art und Grösse der geschäumten Kunststoffe wird mit jedem Bericht geliefert."
]
p22 = makeAParagraph(p22)

cap_four = [
    "Schaumstoffe in verschiedenen Grössen; XPS, EPS und Sprühschäume (SPF) entlang der Schweizer Uferlinien"
]

cap_four = makeAParagraph(cap_four, style=caption_style)
o_w, o_h = convertPixelToCm("resources/images/codegroups/fragfoam_450_600.jpg")

figure_kwargs = {
    "image_file":"resources/images/codegroups/fragfoam_450_600.jpg",
    "caption": cap_four, 
    "original_width":o_w,
    "original_height":o_h,
    "desired_width": 15,
    "caption_height":.75,
    "hAlign": "CENTER",
}

image_four = figureAndCaptionTable(**figure_kwargs)


new_components = [
    PageBreak(),
    subsection_six,
    small_space,
    *p19_21,
    sixth_list,
    PageBreak(),
    subsection_seven,
    small_space,
    p22,
    smallest_space,
    image_four
]

pdfcomponents = addToDoc(new_components, pdfcomponents)


# In[17]:


# define group
construction2= [
            "G9",
            "G204",
            "G187",
            "G919",
            "G65",
            "G17",
            "G22",
            "G66",
            "G68",
            "G69",
            "G72",
            "G74",
            "G81",
            "G82",
            "G83",
            "G87",
            "G89",
            "G93",
            "G160",
            "G162",
            "G166",
            "G169",
            "G174",
            "G186",
            "G188",
            "G189",
            "G190",
            "G194",
            "G197",
            "G198",
            "G199",
            "G214",
            "G908",
            "G909",
            "G910",
            "G911",
            "G912",
            "G921",
            "G927",
            "G931"
]

wwcodes = dfCodes.loc[construction2][cols_to_display]
wwcodes.index.name = None

data = wwcodes.copy()

infrastruktur  = featuredata.aSingleStyledTable(data, style=style, colWidths=[1.5*cm, 7.3*cm, 3.5*cm, 2*cm, 2*cm])
wwcodes.style.set_table_styles(table_css_styles)


# In[18]:


new_components = [
    PageBreak(),
    infrastruktur,
    small_space,   
]
pdfcomponents = addToDoc(new_components, pdfcomponents)


# ### Essen und Trinken
# 
# Beinhaltet alle Materialien, die mit Essen und Trinken in Verbindung stehen. Die grössten Mengen an Einwegkunststoffen (SUP) werden im Zusammenhang mit dem Verzehr im Freien oder zum Mitnehmen verwendet. Verpackungen für Süssigkeiten und Snacks (G30) und Glasscherben (G200) sind an den Schweizer Gewässern am häufigsten anzutreffen [Alle Erhebungen](allsurveys)

# In[19]:


foodstuff = [
    "G1",
    "G8",
    "G7",
    "G10",
    "G21",
    "G24",
    "G30",
    "G151",
    "G175",
    "G176",
    "G177",
    "G178",
    "G179",
    "G181",
    "G200",
    "G201",
    "G203",
    "G150",
    "G153",
    "G159",
    "G165",
    "G31",
    "G33",
    "G34",
    "G35",
    "G906",
    "G907",
    "G926",
    "G938"
    ]

wwcodes = dfCodes.loc[foodstuff][cols_to_display]
wwcodes.index.name = None

data = wwcodes.copy()

essentrinken  = featuredata.aSingleStyledTable(data, style=style, colWidths=[1.5*cm, 7.3*cm, 3.5*cm, 2*cm, 2*cm])
wwcodes.style.set_table_styles(table_css_styles)


# In[20]:


subsection_eight = Paragraph("Essen und Trinken", style=subsection_title)

p23 = [
    "Beinhaltet alle Materialien, die mit Essen und Trinken in Verbindung stehen. Die grössten ",
    "Mengen an Einwegkunststoffen (SUP) werden im Zusammenhang mit dem Verzehr im Freien oder zum ",
    "Mitnehmen verwendet. Verpackungen für Süssigkeiten und Snacks (G30) und Glasscherben (G200) sind ",
    "an den Schweizer Gewässern am häufigsten anzutreffen ",
    '<a href="https://hammerdirt-analyst.github.io/IQAASL-End-0f-Sampling-2021/lakes_rivers.html" color="blue"> Alle Erhebunen </a>.'
]

p23 = makeAParagraph(p23)


new_components = [
    PageBreak(),
    subsection_eight,
    small_space,
    p23,
    small_space,
    essentrinken,
]
pdfcomponents = addToDoc(new_components, pdfcomponents)


# ### Landwirtschaft
# 
# Mehrere Codes wurden hinzugefügt, um Artikel zu kennzeichnen, die mit der Landwirtschaft in Verbindung stehen, wie z. B. G937 Pheromonköder aus Kunststoff, die üblicherweise in Weinbergen verwendet werden, und G943 Kunststoffzäune für die saisonale Viehweide. Der spezifische Foliencode G936 Gewächshausfolien und Silofolien wurde für eine besondere Art von Produkten hinzugefügt, bei denen die landwirtschaftliche Verwendung erkennbar ist. 
# 
# Industriefolien (G67) ist eine weit gefasste Kategorie, die Kunststoffplatten und -folien umfasst, bei denen es sich um flache Kunststoffteile handelt, die zur Verwendung in bestimmten Anwendungen auf eine bestimmte Dicke gebracht werden. Die Produkte unterscheiden sich in Bezug auf Materialien, Eigenschaften und Abmessungen [ogsapfpss]. Es ist schwierig, die Verwendung von Kunststofffolien in der Landwirtschaft einzugrenzen, da die gleichen Kunststoffe auch in der Verpackungs- und Baubranche in grossem Umfang verwendet werden. Vor allem an den Schweizer Gewässern sind die Kunststofffolien stark verwittert und zersplittert, so dass eine eindeutige Verwendung und Herkunft schwer zu bestimmen ist. 
# 
# Industriefolien werden der Landwirtschaft zugeschrieben, da sie über einen längeren Zeitraum physikalischen Einflüssen ausgesetzt sind und in unmittelbarer Nähe von Fliessgewässern verwendet werden. Industriefolien werden auch der Landwirtschaft zugerechnet, da Kunststoffmaterialien zunehmend in landwirtschaftlichen Anwendungen eingesetzt werden, die gemeinhin als Plastikkulturen bezeichnet werden. Die Plastikkultur umfasst Bewässerungsschläuche, Kunststofftöpfe für Baumschulen und eine umfangreiche Verwendung von Folien für den Gartenbau, den Getreideanbau und die Milchwirtschaft.{cite}`plasticulture`
# 
# Folien und Filme aus Plastikkulturen G67: 
# 
# * Mulchfolie
# * Zeilenabdeckungen
# * Polytunnels
# * Kunststoff-Gewächshäuser
# * Filme zur Bodenbegasung
# * Silageballen-Verpackung

# In[21]:


ag2 = [
    "G36",
    "G936",
    "G937",
    "G13",
    "G18", 
    "G41",
    "G65",
    "G67",
    "G90",
    "G140",
    "G161",
    "G168",
    "G170",
    "G171",
    "G172",
    "G191",
    "G192",
    "G934",
    "G943"
]

wwcodes = dfCodes.loc[ag2][cols_to_display]
wwcodes.index.name = None
data = wwcodes.copy()

landwirtschaft  = featuredata.aSingleStyledTable(data, style=style, colWidths=[1.5*cm, 7.3*cm, 3.5*cm, 2*cm, 2*cm])
wwcodes.style.set_table_styles(table_css_styles) 


# In[22]:


subsection_nine = Paragraph("Landwirtschaft", style=subsection_title)

p24 = [
    "Mehrere Codes wurden hinzugefügt, um Artikel zu kennzeichnen, die mit der Landwirtschaft in Verbindung stehen, ",
    "wie z. B. G937 Pheromonköder aus Kunststoff, die üblicherweise in Weinbergen verwendet werden, und G943 ",
    "Kunststoffzäune für die saisonale Viehweide. Der spezifische Foliencode G936 Gewächshausfolien und Silofolien ",
    "wurde für eine besondere Art von Produkten hinzugefügt, bei denen die landwirtschaftliche Verwendung erkennbar ist."
]

p25 = [
    "Industriefolien (G67) ist eine weit gefasste Kategorie, die Kunststoffplatten und -folien umfasst, bei denen es sich ",
    "um flache Kunststoffteile handelt, die zur Verwendung in bestimmten Anwendungen auf eine bestimmte Dicke gebracht werden. ",
    'Die Produkte unterscheiden sich in Bezug auf Materialien, Eigenschaften und Abmessungen <a href="#ogsapfpss" color="blue">(ogsapfpss)</a>. Es ist schwierig, ',
    "die Verwendung von Kunststofffolien in der Landwirtschaft einzugrenzen, da die gleichen Kunststoffe auch in der Verpackungs- ",
    "und Baubranche in grossem Umfang verwendet werden. Vor allem an den Schweizer Gewässern sind die Kunststofffolien stark ",
    "verwittert und zersplittert, so dass eine eindeutige Verwendung und Herkunft schwer zu bestimmen ist."
]

p26 = [
    "Industriefolien werden der Landwirtschaft zugeschrieben, da sie über einen längeren Zeitraum physikalischen Einflüssen ",
    "ausgesetzt sind und in unmittelbarer Nähe von Fliessgewässern verwendet werden. Industriefolien werden auch der Landwirtschaft ",
    "zugerechnet, da Kunststoffmaterialien zunehmend in landwirtschaftlichen Anwendungen eingesetzt werden, die gemeinhin als ",
    "Plastikkulturen bezeichnet werden. Die Plastikkultur umfasst Bewässerungsschläuche, Kunststofftöpfe für Baumschulen und ",
    "eine umfangreiche Verwendung von Folien für den Gartenbau, den Getreideanbau und die Milchwirtschaft.",
    '<a href="#Orz17" color="blue">(Orz17)</a>'
]

p27 = ["Folien und Filme aus Plastikkulturen G67:"]


seventh_list = [
    "Mulchfolie",
    "Zeilenabdeckungen",
    "Polytunnels",
    "Kunststoff-Gewächshäuser",
    "Filme zur Bodenbegasung",
    "Silageballen-Verpackung"
]

seventh_list = makeAList(seventh_list)

# ogsapfpss Website of global spec a plastic film and plastic sheeting supplier. Plastic sheet film. URL: https://www.www.globalspec.com.
# Orz17 Michael D. Orzolek. A Guide to the Manufacture, Performance, and Potential of Plastics in Agriculture. Matthew Deans, 2017.

ogsapfpss = ['<a name="Orz17"/>Orz17: <i>Michael D. Orzolek.</i>. A Guide to the Manufacture, Performance, and Potential of Plastics in Agriculture. Matthew Deans, 2017.']

ogsapfpss = makeAParagraph(ogsapfpss)

orz17 = ['<a name="ogsapfpss"/>ogsapfpss: Website of global spec a plastic film and plastic sheeting supplier. Plastic sheet film.URL: https://www.www.globalspec.com.']   

orz17 = makeAParagraph(orz17)
p24_27 = sectionParagraphs([p24, p25, p26, p27], smallspace=smallest_space)


references = [Paragraph("Bibliographie", style=section_title), small_space, *references, KeepTogether(smallest_space), orz17, KeepTogether(smallest_space), ogsapfpss]

new_components = [
    PageBreak(),
    subsection_nine,
    small_space,
    *p24_27,
    seventh_list,
    small_space,    
    landwirtschaft,
    small_space,
    
]
pdfcomponents = addToDoc(new_components, pdfcomponents)


# ### Tabakwaren
# 
# Alle tabakbezogenen Artikel. 

# In[23]:


tobac = [
    "G25",
    "G26",
    "G27",
    "G152"
    ]

wwcodes = dfCodes.loc[tobac][cols_to_display]
wwcodes.index.name = None

data = wwcodes.copy()

tabakwaren  = featuredata.aSingleStyledTable(data, style=style, colWidths=[1.5*cm, 7.3*cm, 3.5*cm, 2*cm, 2*cm])
wwcodes.style.set_table_styles(table_css_styles)


# In[24]:


subsection_ten = Paragraph("Tabakwaren", style=subsection_title)
p28 = makeAParagraph(["Alle tabakbezogenen Artikel."])

new_components = [
    PageBreak(),
    subsection_ten,
    small_space,
    p28,
    small_space,
    tabakwaren,
    small_space,
   
]
pdfcomponents = addToDoc(new_components, pdfcomponents)


# ### Codes für die Freizeitgestaltung 
# 
# Die Freizeitgruppe umfasst Objekte, die mit Sport und Freizeit zu tun haben, d. h. Angeln, Jagen, Wandern, Bootfahren und Strandaktivitäten. Lebensmittel, Getränke und Tabak sind ausgeschlossen. Schrotpatronen aus Plastik (G70) wurden in überraschend grossen Mengen gefunden, wenn man bedenkt, dass die Jagd in der Nähe der grossen Seen nicht erlaubt ist. Dies könnte ein wichtiger Indikator für die zurückgelegten Entfernungen in den Gewässern sein.

# In[25]:


recreation = [
    "G32",
    "G43",
    "G48",
    "G49",
    "G50",
    "G49",
    "G51",
    "G52",
    "G53",
    "G54",
    "G53",
    "G55",
    "G56",
    "G57",
    "G58",
    "G59",
    "G60",
    "G61",
    "G63",
    "G70",
    "G73",
    "G86",
    "G92",
    "G94",
    "G206",
    "G132",
    "G142",
    "G143",
    "G155",
    "G164",
    "G167",
    "G182",
    "G183",
    "G125",
    "G126",
    "G11",
    "G213",
    "G904",
    "G940"
  ]

wwcodes = dfCodes.loc[recreation][cols_to_display]
wwcodes.index.name = None
data = wwcodes.copy()

freizeitgestaltung  = featuredata.aSingleStyledTable(data, style=style, colWidths=[1.5*cm, 7.3*cm, 3.5*cm, 2*cm, 2*cm])
wwcodes.style.set_table_styles(table_css_styles)


# In[26]:


subsection_11 = Paragraph("Codes für die Freizeitgestaltung", style=subsection_title)
p29 = makeAParagraph([
    "Die Freizeitgruppe umfasst Objekte, die mit Sport und Freizeit zu tun haben, d. h. Angeln, ",
    "Jagen, Wandern, Bootfahren und Strandaktivitäten. Lebensmittel, Getränke und Tabak sind ausgeschlossen. ",
    "Schrotpatronen aus Plastik (G70) wurden in überraschend grossen Mengen gefunden, wenn man bedenkt, ",
    "dass die Jagd in der Nähe der grossen Seen nicht erlaubt ist. Dies könnte ein wichtiger Indikator ",
    "für die zurückgelegten Entfernungen in den Gewässern sein."
])

new_components = [
    PageBreak(),
    subsection_11,
    small_space,
    p29,
    small_space,    
    freizeitgestaltung,
    small_space,
   
]
pdfcomponents = addToDoc(new_components, pdfcomponents)


# ### Verpackungen, die sich nicht auf Lebensmittel, Getränke, Tabak oder unbekannte Herkunft beziehen.
# 
# Sämtliches Verpackungs- oder Umhüllungsmaterial, das nicht als Lebensmittel-, Getränke- oder Tabakverpackung gekennzeichnet ist. Die Gruppe der Verpackungen, die nicht zu Lebensmitteln/Getränken gehören, enthält einen Code (G941), der hinzugefügt wurde, um dünne Verpackungsfolien von dickeren Industriefolien zu unterscheiden. Die Folien sind in der Regel stark beschädigt und zersplittert, so dass der ursprüngliche Verwendungszweck und die Herkunft schwer zu bestimmen sind 
# 
# Verpackungen, die weder mit Tabak noch mit Lebensmitteln und Getränken in Verbindung stehen oder deren Herkunft unbekannt ist:

# In[27]:


packaging = [
    "G23",
    "G2",
    "G146",
    "G148",
    "G149", 
    "G3", 
    "G20",
    "G4",
    "G6",
    "G147",
    "G922",
    "G941",
    "G156",
    "G157",
    "G158",
    "G925",
    "G5"
    ]

wwcodes = dfCodes.loc[packaging][cols_to_display]
wwcodes.loc["G925", "description"] = "Dessicants/moisture absorbers"
wwcodes.index.name = None
data = wwcodes.copy()

verpackungen  = featuredata.aSingleStyledTable(data, style=style, colWidths=[1.5*cm, 7.3*cm, 3.5*cm, 2*cm, 2*cm])
wwcodes.style.set_table_styles(table_css_styles)


# In[28]:


subsection_12 = Paragraph("Verpackungen, die sich nicht auf Lebensmittel, Getränke, Tabak oder unbekannte Herkunft beziehen.", style=subsection_title)

p30 =[
    "Sämtliches Verpackungs- oder Umhüllungsmaterial, das nicht als Lebensmittel-, Getränke- oder Tabakverpackung gekennzeichnet ist. ",
    "Die Gruppe der Verpackungen, die nicht zu Lebensmitteln/Getränken gehören, enthält einen Code (G941), der hinzugefügt wurde, um ",
    "dünne Verpackungsfolien von dickeren Industriefolien zu unterscheiden. Die Folien sind in der Regel stark beschädigt und zersplittert, ",
    "so dass der ursprüngliche Verwendungszweck und die Herkunft schwer zu bestimmen sind"
]

p31 = [
    "Verpackungen, die weder mit Tabak noch mit Lebensmitteln und Getränken in Verbindung stehen oder deren Herkunft unbekannt ist:"
]

p30_31 = sectionParagraphs([p30, p31], smallspace=smallest_space)


new_components = [
    PageBreak(),
    subsection_12,
    small_space,
    *p30_31,
    small_space,
    verpackungen,
    small_space,
    
]
pdfcomponents = addToDoc(new_components, pdfcomponents)


# ### Fragmentierte Kunststoffe: Gfrags¶ 
# 
# Die Gruppe der Kunststofffragmente (Gfrags für die Analyse) sind alle Kunststoff- und Schaumstoff-/Kunststoffverbundstücke, die grösser als 0,5 cm sind. Bei den Kunststofffragmenten, die an den Schweizer Küsten gefunden wurden, handelt es sich überwiegend um kleine, harte, stark fragmentierte Stücke eines pigmentierten Gegenstands. Der ursprüngliche Verwendungszweck und die Herkunft sind im Prinzip unbestimmt. Die einzelnen Plastikteile wurden nach Material und Grösse quantifiziert: 

# In[29]:


plasticpcs = [
    "G78",
    "G79",
    "G80",
    "G75", 
    "G76", 
    "G77" 
    ]

wwcodes = dfCodes.loc[plasticpcs][cols_to_display]
wwcodes.index.name = None
data = wwcodes.copy()

fragmentierte  = featuredata.aSingleStyledTable(data, style=style, colWidths=[1.5*cm, 7.3*cm, 3.5*cm, 2*cm, 2*cm])
wwcodes.style.set_table_styles(table_css_styles)


# ```{figure} resources/images/codegroups/Yverdon_lesBainsLacNeuchâtel15_02_2021.jpg
# :name: image_five_codes
# ` `
# ```
# {numref}`Abildung %s: <image_five_codes>` Verschiedene Grössen von Plastikteilen

# In[30]:


subsection_13 = Paragraph("Fragmentierte Kunststoffe: Gfrags", style=subsection_title)

p32 = [
    "Die Gruppe der Kunststofffragmente (Gfrags für die Analyse) sind alle Kunststoff- und Schaumstoff-/Kunststoffverbundstücke, ",
    "die grösser als 0,5 cm sind. Bei den Kunststofffragmenten, die an den Schweizer Küsten gefunden wurden, handelt es sich ",
    "überwiegend um kleine, harte, stark fragmentierte Stücke eines pigmentierten Gegenstands. Der ursprüngliche Verwendungszweck ",
    "und die Herkunft sind im Prinzip unbestimmt. Die einzelnen Plastikteile wurden nach Material und Grösse quantifiziert:"
]
p32 = makeAParagraph(p32)


cap_five = [
    "Verschiedene Grössen von Plastikteilen"
]

cap_five = makeAParagraph(cap_five, style=caption_style)
o_w, o_h = convertPixelToCm("resources/images/codegroups/Yverdon_lesBainsLacNeuchâtel15_02_2021.jpg")

figure_kwargs = {
    "image_file":"resources/images/codegroups/Yverdon_lesBainsLacNeuchâtel15_02_2021.jpg",
    "caption": cap_five, 
    "original_width":o_w,
    "original_height":o_h,
    "desired_width": 15,
    "caption_height":.75,
    "hAlign": "CENTER",
}

image_five = figureAndCaptionTable(**figure_kwargs)

new_components = [
    PageBreak(),
    KeepTogether(small_space),
    subsection_13,
    KeepTogether(small_space),
    p32,
    KeepTogether(small_space),
    fragmentierte,
    KeepTogether(small_space),
    image_five,
   
   
  
]
pdfcomponents = addToDoc(new_components, pdfcomponents)


# ### Persönliche Gegenstände 
# 
# Persönliches Material für Hygiene, Kleidung und Zubehör, das verloren oder weggeworfen wurde. Dazu gehören auch pandemiebezogene Artikel wie Gesichtsmasken.

# In[31]:


pi = [
    "G211",
    "G84",
    "G99",
    "G101",
    "G102",
    "G127",
    "G131",
    "G135",
    "G136",
    "G137",
    "G138",
    "G139",
    "G37",
    "G39",
    "G40",
    "G145",
    "G28",
    "G29",
    "G154",
    "G195",
    "G900",
    "G901",
    "G902",
    "G903",
    "G905",
    "G913",
    "G914",
    "G915",
    "G918",
    "G916",
    "G933",
    "G929",
    "G939",
    "G945",
    "G923",
    "G928",
    "G12",
    "G71",
    "G88",
    "G935",
    "G930"
    ]
wwcodes = dfCodes.loc[pi][cols_to_display]
wwcodes.index.name = None
data = wwcodes.copy()

persönliche  = featuredata.aSingleStyledTable(data, style=style, colWidths=[1.5*cm, 7.3*cm, 3.5*cm, 2*cm, 2*cm])
wwcodes.style.set_table_styles(table_css_styles)


# In[32]:


s_section_14 = Paragraph("Persönliche Gegenstände", style=subsection_title)

p33 = [
    "Persönliches Material für Hygiene, Kleidung und Zubehör, das verloren oder weggeworfen wurde. Dazu gehören auch pandemiebezogene Artikel wie Gesichtsmasken."
]

p33 = makeAParagraph(p33)

new_components = [
    PageBreak(),
    s_section_14,
    small_space,
    p33,
    small_space,
    persönliche,
    small_space,
  
]
pdfcomponents = addToDoc(new_components, pdfcomponents)


# ### Nicht klassifizierte Objekte¶ 
# 
# Bei den nicht gruppierten Codes handelt es sich überwiegend um Elemente, deren Ursprung unklar ist, die selten identifiziert werden oder die sich nicht auf die Überwachung der Schweizer Wassersysteme beziehen. Viele der Elemente haben einen Gesamtwert von 0 für alle in diesem Bericht enthaltenen Erhebungsdaten. 
# 
# Bemerkenswerte Ausnahmen sind G208 Glas- oder Keramikfragmente > 2,5 cm. Bei G208 handelt es sich überwiegend um Keramikstücke unbekannter Verwendung oder Herkunft, die häufig und in relativ hohen Konzentrationen gefunden werden. Das Vorkommen von Keramikfragmenten kann mit den Quellen des Materials für die Strandauffüllung sowie mit natürlichen Transport- und Ablagerungsprozessen zusammenhängen. Glasflaschen und identifizierbare Glasflaschenfragmente werden als (G200) klassifiziert und mit Lebensmitteln und Getränken gruppiert.

# In[33]:


wwcodes = dfCodes[dfCodes.Gruppenname== "nicht klassifiziert"][cols_to_display]
wwcodes.index.name = None

data = wwcodes.copy()

nichtk  = featuredata.aSingleStyledTable(data, style=style, colWidths=[1.5*cm, 7.3*cm, 3.5*cm, 2*cm, 2*cm])
wwcodes.style.set_table_styles(table_css_styles)


# In[34]:


s_sec_15 = Paragraph("Nicht klassifizierte Objekte", style=subsection_title)

p34 = [
    "Bei den nicht gruppierten Codes handelt es sich überwiegend um Elemente, deren Ursprung unklar ist, ",
    "die selten identifiziert werden oder die sich nicht auf die Überwachung der Schweizer Wassersysteme ",
    "beziehen. Viele der Elemente haben einen Gesamtwert von 0 für alle in diesem Bericht enthaltenen Erhebungsdaten."
]

p35 = [
    "Bemerkenswerte Ausnahmen sind G208 Glas- oder Keramikfragmente > 2,5 cm. Bei G208 handelt es sich überwiegend ",
    "um Keramikstücke unbekannter Verwendung oder Herkunft, die häufig und in relativ hohen Konzentrationen gefunden ",
    "werden. Das Vorkommen von Keramikfragmenten kann mit den Quellen des Materials für die Strandauffüllung sowie mit ",
    "natürlichen Transport- und Ablagerungsprozessen zusammenhängen. Glasflaschen und identifizierbare ",
    "Glasflaschenfragmente werden als (G200) klassifiziert und mit Lebensmitteln und Getränken gruppiert."
]

p34_35 = sectionParagraphs([p34, p35], smallspace=smallest_space)



new_components = [
    PageBreak(),
    s_sec_15,
    small_space,
    *p34_35,
    small_space,
    nichtk,
    small_space,
     
]
pdfcomponents = addToDoc(new_components, pdfcomponents)


# ## Liste der Zusatzcodes
# 
# Codes, die für Schweizer Wassersysteme hinzugefügt wurden.

# In[35]:


addcodes = [
    "G900", 
    "G901", 
    "G902", 
    "G903", 
    "G904", 
    "G905",
    "G906", 
    "G907", 
    "G908", 
    "G909", 
    "G910", 
    "G911", 
    "G912", 
    "G913", 
    "G914", 
    "G915", 
    "G916", 
    "G917", 
    "G918", 
    "G919", 
    "G920", 
    "G921", 
    "G922", 
    "G923", 
    "G925", 
    "G926", 
    "G927", 
    "G928", 
    "G929", 
    "G930",
    "G931",
    "G932",
    "G933",
    "G934",
    "G935",
    "G936",
    "G937",
    "G938",
    "G939",
    "G940",
    "G941",
    "G942",
    "G943",
    "G944",
    "G945"
]

wwcodes = dfCodes[dfCodes.index.isin(addcodes)][cols_to_display]
wwcodes.index.name = None
data = wwcodes.copy()

zusatzcodes  = featuredata.aSingleStyledTable(data, style=style, colWidths=[1.5*cm, 7.3*cm, 3.5*cm, 2*cm, 2*cm])
wwcodes.style.set_table_styles(table_css_styles)


# In[36]:


sec_3 = Paragraph("Liste der Zusatzcodes", style=section_title)
p36 = ["Codes, die für Schweizer Wassersysteme hinzugefügt wurden."]

p36 = makeAParagraph(p36)

new_components = [
    PageBreak(),
    sec_3,
    small_space,
    p36,
    small_space,
    zusatzcodes,
    small_space
]
pdfcomponents = addToDoc(new_components, pdfcomponents)


# ## Lokale Codes für die Schweizer Alpen hinzugefügt

# In[37]:


alpcodes = [
    "G708", 
    "G712", 
    "G705", 
    "G703", 
    "G704",
    "G706", 
    "G707", 
    "G709", 
    "G710", 
    "G711", 
    "G713", 
    "G702"
]

wwcodes = dfCodes.loc[alpcodes][cols_to_display]
wwcodes.index.name = None
data = wwcodes.copy()
locale  = featuredata.aSingleStyledTable(data, style=style, colWidths=[1.5*cm, 7.3*cm, 3.5*cm, 2*cm, 2*cm])
wwcodes.style.set_table_styles(table_css_styles)


# In[38]:


sec_4 = Paragraph("Lokale Codes für die Schweizer Alpen hinzugefügt", style=section_title)
new_components = [
    PageBreak(),
    sec_4,
    KeepTogether([small_space]),
    locale,
    KeepTogether([small_space]),
    *references    
]
pdfcomponents = addToDoc(new_components, pdfcomponents)


# In[39]:


doc = SimpleDocTemplate(pdf_link, pagesize=A4, leftMargin=2.5*cm, rightMargin=1.5*cm, topMargin=3*cm, bottomMargin=1.5*cm)
pageinfo= f"IQAASL: Codegruppen"


def myLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Italic',9)
    canvas.drawString(1*cm, 1*cm, "S.%d %s" % (doc.page, pageinfo))
    canvas.restoreState()
    
doc.build(pdfcomponents,  onFirstPage=myLaterPages, onLaterPages=myLaterPages)

