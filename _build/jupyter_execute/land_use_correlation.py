#!/usr/bin/env python
# coding: utf-8

# In[1]:


# sys, file and nav packages:
import datetime as dt

# math packages:
import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.distributions.empirical_distribution import ECDF

# charting:
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.dates as mdates
from matplotlib import ticker
import seaborn as sns

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

# home brew utitilties
import resources.chart_kwargs as ck
import resources.sr_ut as sut

# images and display
from PIL import Image as PILImage
from IPython.display import Markdown as md
from myst_nb import glue
import locale
loc = locale.getlocale()
lang =  "de_CH.utf8"
locale.setlocale(locale.LC_ALL, lang)

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

pdf_link = 'resources/pdfs/land_use_correlation_de.pdf'

# set some parameters:
today = dt.datetime.now().date().strftime("%Y-%m-%d")
start_date = "2020-03-01"
end_date ="2021-05-31"
unit_label = "pcs_m"

# banded color for table
a_color = "saddlebrown"

# get the data:
survey_data = pd.read_csv("resources/checked_sdata_eos_2020_21.csv")
dfBeaches = pd.read_csv("resources/beaches_with_land_use_rates.csv")
dfCodes = pd.read_csv("resources/codes_with_group_names_2015.csv")

# set the index of the beach data to location slug
dfBeaches.set_index("slug", inplace=True)

# set the code index and edit descriptions for display:
dfCodes.set_index("code", inplace=True)

# make a map to the code descriptions
code_description_map = dfCodes.description

# make a map to the code materials
code_material_map = dfCodes.material
codes_class = featuredata.Codes(code_data=dfCodes, language='de')
codes_class.adjustForLanguage()

# language specific
# importing german code descriptions and material type transaltions
de_codes = pd.read_csv("resources/codes_german_Version_1.csv")
de_codes.set_index("code", inplace=True)

# for x in dfCodes.index:
#     dfCodes.loc[x, "description"] = de_codes.loc[x, "german"]
    
# dfCodes["material"] = dfCodes.material.map(lambda x: sut.mat_ge[x])


dfCodes = codes_class.dfCodes


# (luseprofile)=
# # Landnutzungsprofil
# 
# {Download}`Download </resources/pdfs/land_use_correlation_de.pdf>`
# 
# *Das Landnutzungsprofil* ist eine numerische Darstellung der Art und des Umfangs der wirtschaftlichen Aktivität um den Erhebungsort. Das Profil wird anhand von Daten berechnet, die in Kartenebenen gespeichert sind, die im [_Geoportal des Bundes_](https://www.geo.admin.ch/) und beim [_Bundesamt für Statistik_](https://www.bfs.admin.ch/bfs/en/home.html) verfügbar sind.
# 
# Abfallobjekte sind weggeworfene Objekte, die in der natürlichen Umgebung gefunden werden. Das Objekt selbst und der Kontext, in dem es gefunden wird, sind Indikatoren für die wirtschaftliche und geografische Herkunft. Wie das Land in der Nähe des Erhebungsortes genutzt wird, ist ein wichtiger Kontext, der bei der Bewertung der Erhebungsergebnisse berücksichtigt werden muss. {cite}`aydin` {cite}`grelaud`
# 
# Im September 2020 hat die Europäische Union Basislinien und Zielwerte für Abfallobjekte am Strand veröffentlicht. Nach Abwägung vieler Faktoren, darunter die Transparenz der Berechnungsmethode und die Leistung in Bezug auf Ausreisser, hat die EU entschieden, dass der Medianwert der Datenerhebungen zum Vergleich der Basiswerte zwischen den Regionen verwendet wird. Dies hat das Interesse der Gemeinden geweckt, punktuelle Abfallobjekte besser zu identifizieren und zu quantifizieren, da sie versuchen, den effizientesten Weg zur Einhaltung der Zielwerte zu finden. Die Identifizierung relevanter Landnutzungsmuster und -merkmale ist ein wesentliches Element in diesem Prozess. {cite}`threshholdeu` {cite}`eubaselines` {cite}`vanemmerick`
# 
# Hier schlagen wir eine Methode vor, um die Ergebnisse von Untersuchungen des Ufer-Abfallaufkommens im Hinblick auf das Landnutzungsprofil im Umkreis von 1500 m um den Erhebungsort auszuwerten. Die Erhebungsergebnisse der häufigsten Objekte werden mit Hilfe von Spearmans Rho oder Spearmans ranked correlation, einem nicht-parametrischen Test auf Assoziation mit den gemessenen Landnutzungsmerkmalen getestet. {cite}`defspearmans` 
# 
# ## Berechnung des Landnutzungsprofils
# 
# Das Landnutzungsprofil setzt sich aus den messbaren Eigenschaften zusammen, die geografisch verortet sind und aus den aktuellen Versionen der *Arealstatisik der Schweiz* und *swissTLMRegio* extrahiert werden können. {cite}`superficie` {cite}`tlmregio`. 
# 
# Die folgenden Werte wurden in einem Radius von 1500 m um jeden Erhebungsort berechnet:
# 
# * Fläche, die von Gebäuden eingenommen wird in \%
# * Fläche, die dem Wald vorbehalten ist in \%
# * Fläche, die für Aktivitäten im Freien genutzt wird in \%
# * Fläche, die von der Landwirtschaft genutzt wird in \%
# * Strassen in Gesamtzahl der Strassenkilometer
# * Anzahl Flussmündungen
# 
# **Berechnung des Landnutzungsprofils**
# 
# Das Bundesamt für Statistik stellt die Arealstatistik zur Verfügung, ein Raster von Punkten 100m x 100m, das die Schweiz abdeckt. Jedem Punkt ist eine von 27 verschiedenen Landnutzungskategorien zugeordnet, die durch die Standardklassifikation von 2004 definiert sind. Dieses Raster dient als Grundlage für die Berechnung des Landnutzungsprofils in der Umgebung des Erhebungsorts. Für diese Studie wurden die Landnutzungskategorien in sieben Gruppen aus den siebenundzwanzig verfügbaren Kategorien zusammengefasst.
# 
# Die aggregierten Werte und die entsprechenden Landnutzungskategorien
# 
# * Gebäude: (1, 2, 3, 4, 5, 9)
# * Transport:(6, 7, 8)
# * Erholung: (10)
# * Landwirtschaft: (11, 12, 13, 14, 15, 16, 18)
# * Wald: (17, 19, 20, 21, 22)
# * Wasser: (23, 24)
# * unproduktiv: (25, 26, 27)
# 
# Für jeden Erhebungsort wurde die kumulative Summe und die kumulative Summe jeder Gruppe innerhalb des 1500-m-Puffers berechnet. Die dem Wasser zugewiesene Menge wurde von der kumulativen Summe abgezogen. Das Ergebnis wurde verwendet, um den Prozentsatz der Landnutzung für jede Kategorie zu berechnen.
# 
# Die Kategorie Aktivitäten im Freien umfasst verschiedene Anwendungen für die öffentliche Nutzung. Die Nutzung reicht von Sportplätzen bis hin zu Friedhöfen und umfasst alle Bereiche, die für soziale Aktivitäten zur Verfügung stehen.
# 
# **Berechnung der Strassenlänge**
# 
# Die Strassenlänge wurde berechnet, indem die Kartenebene swissTLM3D_TLM_STRASSE mit dem 1500-m-Puffer jedes Erhebungsortes geschnitten wurde. Alle Strassen und Wege wurden zu einer Linie zusammengefasst (QGIS: dissolve) und die Länge der Linie ist der angegebene Wert der Strassenkilometer.
# 
# **Zählen der Einträge aus Fliessgewässern**
# 
# Für Erhebungsorte an Seen wurde die Anzahl der Flussmündungen im Umkreis von 1500 m von jedem Erhebungsort berechnet. Die Kartenebene swissTLM3D_TLM_FLIESSGEWAESSER (Fliessgewässer) wurde mit swissTLM3D_TLM_STEHENDES_GEWAESSER (Seen) geschnitten (QGI: «Linienschnittpunkte»), und die Anzahl der Schnittpunkte pro 1500 m Puffer wurde gezählt (QGI: «Punkte im Polygon zählen»). Die Kartenebene der Seen wurde um 100 Meter erweitert, um alle Abflussstellen oder Bäche zu erfassen, die in der Nähe des Sees enden. {cite}`qgis_software` {cite}`tlmregio`

# In[2]:


pdfcomponents = []

chapter_title = Paragraph("Landnutzungsprofil", style=title_style)

p_1 = [
    "<i>Das Landnutzungsprofil</i> ist eine numerische Darstellung der Art und des Umfangs der wirtschaftlichen ",
    "Aktivität um den Erhebungsort. Das Profil wird anhand von Daten berechnet, die in Kartenebenen gespeichert ",
    "sind, die im ",
    '<a href="https://www.geo.admin.ch/" color="blue">Geoportal des Bundes</a> und beim ',
    '<a href="https://www.bfs.admin.ch/bfs/en/home.html" color="blue">Bundesamt für Statistik</a> verfügbar sind.'
]

p_2 = [
    "Abfallobjekte sind weggeworfene Objekte, die in der natürlichen Umgebung gefunden werden. Das Objekt selbst ",
    "und der Kontext, in dem es gefunden wird, sind Indikatoren für die wirtschaftliche und geografische Herkunft. ",
    "Wie das Land in der Nähe des Erhebungsortes genutzt wird, ist ein wichtiger Kontext, der bei der Bewertung der ",
    'Erhebungsergebnisse berücksichtigt werden muss. <a href="#ea16" color="blue">(ea16)</a><a href="#GM20" color="blue">(GM20)</a>'
]

p_3 = [
    "Im September 2020 hat die Europäische Union Basislinien und Zielwerte für Abfallobjekte am Strand veröffentlicht. ",
    "Nach Abwägung vieler Faktoren, darunter die Transparenz der Berechnungsmethode und die Leistung in Bezug auf ",
    "Ausreisser, hat die EU entschieden, dass der Medianwert der Datenerhebungen zum Vergleich der Basiswerte zwischen ",
    "den Regionen verwendet wird. Dies hat das Interesse der Gemeinden geweckt, punktuelle Abfallobjekte besser zu ",
    "identifizieren und zu quantifizieren, da sie versuchen, den effizientesten Weg zur Einhaltung der Zielwerte zu finden. ",
    "Die Identifizierung relevanter Landnutzungsmuster und -merkmale ist ein wesentliches Element in diesem Prozess.",
    '<a href="#VLW20" color="blue">(VLW20)</a><a href="#HG19" color="blue">(HG19)</a><a href="#vEV21" color="blue">(vEV21)</a>',
]

p_4 = [
    "Hier schlagen wir eine Methode vor, um die Ergebnisse von Untersuchungen des Ufer-Abfallaufkommens im Hinblick auf ",
    "das Landnutzungsprofil im Umkreis von 1500 m um den Erhebungsort auszuwerten. Die Erhebungsergebnisse der häufigsten ",
    "Objekte werden mit Hilfe von Spearmans Rho oder Spearmans ranked correlation, einem nicht-parametrischen Test auf ",
    'Assoziation mit den gemessenen Landnutzungsmerkmalen getestet.<a href="#Wikd" color="blue">(Wikd)</a>'
]

p_1_4 = sectionParagraphs([p_1, p_2, p_3, p_4], smallspace=smallest_space)

section_one_title = Paragraph("Berechnung des Landnutzungsprofils", style = section_title)

p_5 = [
    "Das Landnutzungsprofil setzt sich aus den messbaren Eigenschaften zusammen, die geografisch verortet sind und aus ",
    "den aktuellen Versionen der <i>Arealstatisik der Schweiz</i> und <i>swissTLMRegio</i> extrahiert werden können.",
    '<a href="#Con21a" color="blue">(Con21a)</a><a href="#Con21b" color="blue">(Con21b)</a>'
]

p_6 = [
    "Die folgenden Werte wurden in einem Radius von 1500 m um jeden Erhebungsort berechnet:"
]

p_5_6 = sectionParagraphs([p_5, p_6], smallspace=smallest_space)

first_list = [
    "Fläche, die von Gebäuden eingenommen wird in \%",
    "Fläche, die dem Wald vorbehalten ist in \%",
    "Fläche, die für Aktivitäten im Freien genutzt wird in \%",
    "Fläche, die von der Landwirtschaft genutzt wird in \%",
    "Strassen in Gesamtzahl der Strassenkilometer",
    "Anzahl Flussmündungen"
]
first_list = makeAList(first_list)

p_7 = [
    "Das Bundesamt für Statistik stellt die Arealstatistik zur Verfügung, ein Raster von Punkten 100m x 100m, das ",
    "die Schweiz abdeckt. Jedem Punkt ist eine von 27 verschiedenen Landnutzungskategorien zugeordnet, die durch ",
    "die Standardklassifikation von 2004 definiert sind. Dieses Raster dient als Grundlage für die Berechnung des ",
    "Landnutzungsprofils in der Umgebung des Erhebungsorts. Für diese Studie wurden die Landnutzungskategorien in ",
    "sieben Gruppen aus den siebenundzwanzig verfügbaren Kategorien zusammengefasst."
]

p_8 = [
    "Die aggregierten Werte und die entsprechenden Landnutzungskategorie:"
]

p_7_8 = sectionParagraphs([p_7, p_8], smallspace=smallest_space)

second_list = [
    "Gebäude: (1, 2, 3, 4, 5, 9)",
    "Transport:(6, 7, 8)",
    "Erholung: (10)",
    "Landwirtschaft: (11, 12, 13, 14, 15, 16, 18)",
    "Wald: (17, 19, 20, 21, 22)",
    "Wasser: (23, 24)",
    "unproduktiv: (25, 26, 27)"
]

second_list = makeAList(second_list)

p_9 = [
    "Für jeden Erhebungsort wurde die kumulative Summe und die kumulative Summe jeder Gruppe innerhalb des 1500-m-Puffers ",
    "berechnet. Die dem Wasser zugewiesene Menge wurde von der kumulativen Summe abgezogen. Das Ergebnis wurde verwendet, ",
    "um den Prozentsatz der Landnutzung für jede Kategorie zu berechnen."
]

p_10 = [
    "Die Kategorie Aktivitäten im Freien umfasst verschiedene Anwendungen für die öffentliche Nutzung. Die Nutzung reicht ",
    "von Sportplätzen bis hin zu Friedhöfen und umfasst alle Bereiche, die für soziale Aktivitäten zur Verfügung stehen."
]

p_9_10 = sectionParagraphs([p_9, p_10], smallspace=smallest_space)

bold_one = Paragraph("Berechnung der Strassenlänge", style=bold_block)

p_11 = [
    "Die Strassenlänge wurde berechnet, indem die Kartenebene swissTLM3D_TLM_STRASSE mit dem 1500-m-Puffer jedes Erhebungsortes ",
    "geschnitten wurde. Alle Strassen und Wege wurden zu einer Linie zusammengefasst (QGIS: dissolve) und die Länge der Linie ist ",
    "der angegebene Wert der Strassenkilometer."
]

p_11 = makeAParagraph(p_11)

bold_two = Paragraph("Zählen der Einträge aus Fliessgewässern", style=bold_block)

p_12 = [
    "Für Erhebungsorte an Seen wurde die Anzahl der Flussmündungen im Umkreis von 1500 m von jedem Erhebungsort berechnet. ",
    "Die Kartenebene swissTLM3D_TLM_FLIESSGEWAESSER (Fliessgewässer) wurde mit swissTLM3D_TLM_STEHENDES_GEWAESSER (Seen) ",
    "geschnitten (QGI: «Linienschnittpunkte»), und die Anzahl der Schnittpunkte pro 1500 m Puffer wurde gezählt (QGI: «Punkte im Polygon zählen»). ",
    "Die Kartenebene der Seen wurde um 100 Meter erweitert, um alle Abflussstellen oder Bäche zu erfassen, die in der Nähe des Sees enden.",
    '<a href="#QGISDTeam09" color="blue">(QGISDTeam09)</a><a href="#Con21b" color="blue">(Con21b)</a>'
]

p_12 = makeAParagraph(p_12)


new_components = [
    chapter_title,
    large_space,
    *p_1_4,
    section_one_title,
    small_space,
    *p_5_6,
    first_list,
    smallest_space,
    *p_7_8,
    second_list,
    smallest_space,
    *p_9_10,
    bold_one,
    smallest_space,
    p_11,
    smallest_space,
    bold_two,
    smallest_space,
    p_12
]

pdfcomponents = addToDoc(new_components, pdfcomponents)


# references
gm20_team = "Ziveri P. Grelaud M."
gm20pub = [
    "The generation of marine litter in mediterranean island beaches as an effect of tourism and its mitigation. Science Reports, 2020. ",
    "doi:10.1038/s41598-020-77225-5",
]
gm20pub = ''.join(gm20pub)
gm20 = makeAParagraph(featuredata.makeBibEntry(name="GM20", team=gm20_team, pub=gm20pub))

ea16_team = "C. Aydin et all."
ea16pub = [
    "The influence of land use on coastal litter: an approach to identify abundance and sources in the coastal area of cilician basin, turkey. ",
    "Turkish Journal of Fisheries and Aquatic Sciences, 2016"
]
ea16pub = ''.join(ea16pub)
ea16 = makeAParagraph(featuredata.makeBibEntry(name="ea16", team=ea16_team, pub=ea16pub))

vlw20_team = "Fleet D. Van Loon W., Hanke G."
vlw20pub = [
    "A european threshold value and assessment method for macro litter on coastlines. Publications Office of the European Union, 2020."
]
vlw20pub = ''.join(vlw20pub)
vlw20 = makeAParagraph(featuredata.makeBibEntry(name="VLW20", team=vlw20_team, pub=vlw20pub))

hg19team = "Van Loon W. Hanke G., Walvoort D."
hg19pub = [
    "Eu marine beach litter baselines. Publications Office of the European Union, 2019. doi:10.2760/16903."
]
hg19pub = ''.join(hg19pub)
hg19 = makeAParagraph(featuredata.makeBibEntry(name="HG19", team=hg19team, pub=hg19pub))

vev21team = "T.H.M. van Emmerik and P. Vriend."
vev21pub = [
    "Roadmap litter monitoring in dutch rivers. Wageningen University, Report., 2021."
]
vev21pub = ''.join(vev21pub)
vev21= makeAParagraph(featuredata.makeBibEntry(name="vEV21", team=vev21team, pub=vev21pub))

wikdpub = [
    "Wikepedia. Spearman's rank correlation coefficient. URL: https://en.wikipedia.org/wiki/Spearman%27s_rank_correlation_coefficient."
]
wikdpub = ''.join(wikdpub)
wikd = makeAParagraph(featuredata.makeBibEntry(name="Wikd", team="Wikepedia", pub=wikdpub))

con21apub = [
    "Confederation. Statistique de la superficie selon nomenclature 2004 - utilisation du sol, description: métainformations sur les géodonnées. 2021. ",
    "URL: https://www.bfs.admin.ch/bfs/en/home/services/geostat/swiss-federal-statistics-geodata/land-use-cover-suitability/swiss-land-use-statistics/standard-nomenclature.html."
]
con21apub = ''.join(con21apub)
con21a = makeAParagraph(featuredata.makeBibEntry(name="Con21a", team="Confederation", pub=con21apub))

con21bpub = [
    "Confederation. Swisstlmregio: le modèle numérique de la suisse à petite échelle. 2021. URL: ",
    " https://www.swisstopo.admin.ch/fr/geodata/landscape/tlmregio.html."
]
con21bpub = ''.join(con21bpub)

con21b =  makeAParagraph(featuredata.makeBibEntry(name="Con21b", team="Confederation", pub=con21bpub))

qgteam ="QGIS Development Team"

qgpub = [
    "QGIS Geographic Information System. Open Source Geospatial Foundation, 2009. URL: ",
    "http://qgis.osgeo.org",
]
qgpub = ''.join(qgpub)
qgis = makeAParagraph(featuredata.makeBibEntry(name="QGISDTeam09", team=qgteam, pub=qgpub))

references = [
    gm20, 
    smallest_space,
    ea16,
    smallest_space,
    hg19,
    smallest_space, 
    vev21, 
    smallest_space,
    vlw20,
    smallest_space,
    wikd,
    smallest_space,
    con21a,
    smallest_space,
    con21b,
    smallest_space,
    qgis,
    smallest_space
]


# ```{figure} resources/images/land_use_profile/land_use_dispaly_20.jpeg
# :name: land_use_example
# ` `
# ```
# {numref}`Abildung %s: <land_use_example>` Für die Berechnung des Landnutzungsprofils verwendete Kartenebenen. __Oben links:__ alle messbaren Werte innerhalb von 1500 m. __Oben rechts:__ Strassen und Flussmündungen innerhalb von 1500 m. __Unten rechts:__ Landnutzungspunkte, die zur Berechnung des prozenutalen Anteils der Gesamtfläche und der Gesamtfläche verwendet werden.

# Berechnetes Landnutzungsprofil von Hauterive-petite-plage, NE 31-07-2020.
# 
# * Fläche, die von Gebäuden eingenommen wird: 32,7 %
# * Fläche, die für Aktivitäten im Freien genutzt wird: 9,9 %
# * Fläche, die von der Landwirtschaft genutzt wird: 18,9 %
# * Fläche, die dem Wald vorbehalten ist: 24,3 %
# * Strassen in Gesamtzahl der Strassenkilometer: 85
# * Anzahl Flussmündungen: 2

# In[3]:


caption_one = [
    'Für die Berechnung des Landnutzungsprofils verwendete Kartenebenen. <b>Oben links:</b> ',
    'alle messbaren Werte innerhalb von 1500 m. <b>Oben rechts:</b> Strassen und Flussmündungen ',
    'innerhalb von 1500 m. <b>Unten rechts:</b> Landnutzungspunkte, die zur Berechnung des ',
    "prozenutalen Anteils der Gesamtfläche und der Gesamtfläche verwendet werden.",
]
caption_one = ''.join(caption_one)

caption_one = makeAParagraph(caption_one, style=caption_style)

def convertPixelToCm(file_name: str = None):
    im = PILImage.open(file_name)
    width, height = im.size
    dpi = im.info.get("dpi", (72, 72))
    width_cm = width / dpi[0] * 2.54
    height_cm = height / dpi[1] * 2.54
    
    return width_cm, height_cm

o_w, o_h = convertPixelToCm("resources/images/land_use_profile/land_use_dispaly_20.jpeg")

figure_kwargs = {
    "image_file":"resources/images/land_use_profile/land_use_dispaly_20.jpeg",
    "caption": caption_one, 
    "original_width":o_w,
    "original_height":o_h,
    "desired_width": 16,
    "caption_height":1.5,
    "hAlign": "LEFT",
}

first_figure = figureAndCaptionTable(**figure_kwargs)

p_13 = ["<i>Berechnetes Landnutzungsprofil von Hauterive-petite-plage, NE 31-07-2020:</i>"]
p_13 = makeAParagraph(p_13, style=featuredata.p_style)

third_list = [
    "Fläche, die von Gebäuden eingenommen wird: 32,7 \%",
    "Fläche, die für Aktivitäten im Freien genutzt wird: 9,9 \%",
    "Fläche, die von der Landwirtschaft genutzt wird: 18,9 \%",
    "Fläche, die dem Wald vorbehalten ist: 24,3 \%",
    "Strassen in Gesamtzahl der Strassenkilometer: 85",
    "Anzahl Flussmündungen: 2"
]

third_list = makeAList(third_list)

o_w, o_h = convertPixelToCm("resources/images/land_use_profile/land_use_dispaly_20.jpeg")

figure_kwargs = {
    "image_file":"resources/images/land_use_profile/land_use_dispaly_20.jpeg",
    "caption": None, 
    "original_width":o_w,
    "original_height":o_h,
    "desired_width": 9.5,
    "caption_height":3,
    "hAlign": "LEFT",
}

first_figure = figureAndCaptionTable(**figure_kwargs)

figure_text = [
    [first_figure, [third_list]],
   
]

side_by_side = Table(figure_text, style=featuredata.side_by_side_style_figure_left, colWidths=[9.1*cm, 6.9*cm])

new_components = [
    
    KeepTogether([
        smallest_space,
        p_13,
        smallest_space,
        side_by_side,
        smallest_space,
        caption_one
    ])    
]

pdfcomponents = addToDoc(new_components, pdfcomponents)


# ```{figure} resources/images/land_use_profile/tightquarterswholensee.jpg
# :name: tight_quarters
# ` `
# ```
# {numref}`Abildung %s: <tight_quarters>` _Datenerhebungen in einer ländlichen Umgebung. Kallnach, BE 26.02.2021_

# ```{figure} resources/images/land_use_profile/urban2_800_600.jpg
# :name: urban_samples
# ` `
# ```
# {numref}`Abildung %s: <urban_samples>` _Datenerhebungen in einer städtischen Umgebung. Vevey, 28.02.2021_

# In[4]:


o_w, o_h = convertPixelToCm("resources/images/land_use_profile/tightquarterswholensee.jpg")
caption_two = ["Datenerhebungen in einer ländlichen Umgebung. Kallnach, BE 26.02.2021"]
caption_two = makeAParagraph(caption_two)


figure_kwargs = {
    "image_file":"resources/images/land_use_profile/tightquarterswholensee.jpg",
    "caption": caption_two, 
    "original_width":o_w,
    "original_height":o_h,
    "desired_width": 7.9,
    "caption_height":1,
    "hAlign": "LEFT",
}

figure_2 = figureAndCaptionTable(**figure_kwargs)

o_w, o_h = convertPixelToCm("resources/images/land_use_profile/urban2_800_600.jpg")
caption_3 = ["Datenerhebungen in einer städtischen Umgebung. Vevey, 28.02.2021"]
caption_3 = makeAParagraph(caption_3)

figure_kwargs = {
    "image_file":"resources/images/land_use_profile/urban2_800_600.jpg",
    "caption": caption_two, 
    "original_width":o_w,
    "original_height":o_h,
    "desired_width": 7.9,
    "caption_height":1,
    "hAlign": "LEFT",
}

figure_3 = figureAndCaptionTable(**figure_kwargs)


# <!-- <table>
# <tr>
# <th>Json 1</th>
# <th>Markdown</th>
# </tr>
# <tr>
# <td>
# <pre>
# {
#   "id": 1,
#   "username": "joe",
#   "email": "joe@example.com",
#   "order_id": "3544fc0"
# }
# </pre>
# </td>
# <td>
# 
# ```json
# {
#   "id": 5,
#   "username": "mary",
#   "email": "mary@example.com",
#   "order_id": "f7177da"
# }
# ```
# 
# </td>
# </tr>
# </table> -->

# ### Landnutzungsprofil des Projekts
# 
# Das Landnutzungsprofil zeigt die prozentualen Anteile jeder Landnutzungskategorie innerhalb eines Radius von 1500 m um den Erhebungsort zugeordnet wird. Das Verhältnis der gefundenen Abfallobjekte unterscheidet sich je nach Landnutzungsprofil. Das Verhältnis gibt daher einen Hinweis auf die ökologischen und wirtschaftlichen Bedingungen um den Erhebungsort.

# *Verteilung der Anzahl der Datenerhebungen für die verschiedenen Landnutzungsmerkmale, n = 350 Stichproben* 

# In[5]:


# explanatory variables that are being considered
luse_exp = ['% to buildings', '% to recreation', '% to agg', '% to woods', 'streets km', 'intersects']
luse_ge = sut.luse_ge
# columns needed
use_these_cols = ['loc_date' ,
                  'date',
                  '% to buildings',
                  '% to trans',
                  '% to recreation',
                  '% to agg',
                  '% to woods',
                  'population',
                  'water_name_slug',
                  'streets km',
                  'intersects',
                  'groupname',
                  'code'
                 ]

# the land use data was unvailable for these municipalities
no_land_use = ['Walenstadt', 'Weesen', 'Glarus Nord', 'Quarten']

# slice the data by start and end date, remove the locations with no land use data
use_these_args = ((survey_data["date"] >= start_date)&(survey_data["date"] <= end_date)&(~survey_data.city.isin(no_land_use)))
survey_data = survey_data[use_these_args].copy()

# format the data and column names
survey_data['date'] = pd.to_datetime(survey_data.date)

# the survey total for each survey indifferent of object
dfdt = survey_data.groupby(use_these_cols[:-2], as_index=False).agg({unit_label:'sum', 'quantity':'sum'})

sns.set_style("whitegrid")
fig, axs = plt.subplots(2, 3, figsize=(9,9), sharey="row")

for i, n in enumerate(luse_exp):
    r = i%2
    c = i%3
    ax=axs[r,c]  
    
    # the ECDF of the land use variable
    the_data = ECDF(dfdt[n].values)
    sns.lineplot(x=the_data.x, y= the_data.y, ax=ax, color='dodgerblue', label="% der Oberfläche")
    
    # get the median % of land use for each variable under consideration from the data
    the_median = dfdt[n].median()
    
    # plot the median and drop horzontal and vertical lines
    ax.scatter([the_median], 0.5, color='red',s=50, linewidth=2, zorder=100, label="Median")
    ax.vlines(x=the_median, ymin=0, ymax=0.5, color='red', linewidth=2)
    ax.hlines(xmax=the_median, xmin=0, y=0.5, color='red', linewidth=2)
    
    #remove the legend from ax   
    ax.get_legend().remove()
    if i <= 3:
        if i == 0:            
            ax.set_ylabel("Prozent der Standorte", **ck.xlab_k)
        ax.xaxis.set_major_formatter(ticker.PercentFormatter(1.0, 0, "%"))        
    else:
        pass
    handles, labels = ax.get_legend_handles_labels()
    
    
    # add the median value from all locations to the ax title
    ax.set_title(F"median: {(round(the_median, 2))}",fontsize=12, loc='left')
    ax.set_xlabel(featuredata.luse_de[n], **ck.xlab_k)

plt.tight_layout()
# plt.subplots_adjust(top=.88, hspace=.3)
plt.subplots_adjust(top=.91, hspace=.5)
plt.suptitle("Landnutzung im Umkries von 1 500 m um den Erhebungsort", ha="center", y=1, fontsize=16)
fig.legend(handles, labels, bbox_to_anchor=(.5,.5), loc="upper center", ncol=6) 
figure_name = f"landnutzung_im_Umkreis"

landnutzung_file_name = f'{save_fig_prefix}{figure_name}.jpeg'
save_figure_kwargs.update({"fname":landnutzung_file_name})
plt.savefig(**save_figure_kwargs)

glue("landnutzung_im_Umkreis", fig, display=False)
plt.close()


# ```{glue:figure} landnutzung_im_Umkreis
# :name: "landnutzung_im_Umkreis"
# ` `
# ```
# {numref}`Abildung %s: <landnutzung_im_Umkreis>` Verteilung der Anzahl der Datenerhebungen für die verschiedenen Landnutzungsmerkmale, n = 350 Stichproben

# **Die Landnutzung** in der Umgebung der Datenerhebungen war stärker auf Gebäude als auf Landwirtschaft und Wald ausgerichtet. So entfielen bei der Hälfte aller Datenerhebungen mindestens 37 % der Landnutzung auf Gebäude gegenüber 19 % für die Landwirtschaft und 13 % für Wälder. Bei der Hälfte aller Stichproben betrug der Anteil der Landnutzung für Aktivitäten im Freien mindestens 6 %.
# 
# **Die Länge des Strassennetzes** innerhalb der Pufferzone unterscheidet sich zwischen Orten, die ansonsten ähnliche Landnutzungsmerkmale aufweisen. Die Länge des Strassennetzes pro Pufferzone reicht von 13 km bis 212 km. 50 % der Datenerhebungen hatten ein Strassennetz von weniger als 67 km.
# 
# **Die Anzahl der Datenerhebungen** reicht von 0 bis 23. Von den 354 Datenerhebungen hatten 50 % 3 oder weniger Flussmündungen innerhalb von 1500 m um den Erhebungsort. Die Grösse des mündenden Flusses oder Kanals wurde nicht berücksichtigt. Datenerhebungen an Fliessgewässern haben 0 Flussmündungen.
# 
# **Die Bevölkerung** (nicht gezeigt) stammt aus der Statistik der Bevölkerung und der Haushalte 2018 und stellt die Bevölkerung der Gemeinde dar, die den Erhebungsort umgibt. Die kleinste Einwohnerzahl betrug 442 und die grösste 415 367. Von den gesamten Datenerhebungen stammen 50 % aus Gemeinden mit einer Einwohnerzahl von mindestens 12 812.

# In[6]:


subsection_one = Paragraph("Landnutzungsprofil des Projekts", subsection_title)

p_14 = [
    "Das Landnutzungsprofil zeigt die prozentualen Anteile jeder Landnutzungskategorie innerhalb ",
    "eines Radius von 1500 m um den Erhebungsort zugeordnet wird. Das Verhältnis der gefundenen ",
    "Abfallobjekte unterscheidet sich je nach Landnutzungsprofil. Das Verhältnis gibt daher einen ",
    "Hinweis auf die ökologischen und wirtschaftlichen Bedingungen um den Erhebungsort."
]

p_15 = [
    "<b>Die Landnutzung</b> in der Umgebung der Datenerhebungen war stärker auf Gebäude als auf Landwirtschaft ",
    "und Wald ausgerichtet. So entfielen bei der Hälfte aller Datenerhebungen mindestens 37 % der Landnutzung ",
    "auf Gebäude gegenüber 19 % für die Landwirtschaft und 13 % für Wälder. Bei der Hälfte aller Stichproben ",
    "betrug der Anteil der Landnutzung für Aktivitäten im Freien mindestens 6 %.",
]

p_16 = [
    "<b>Die Länge des Strassennetzes</b> innerhalb der Pufferzone unterscheidet sich zwischen Orten, die ansonsten ähnliche ",
    "Landnutzungsmerkmale aufweisen. Die Länge des Strassennetzes pro Pufferzone reicht von 13 km bis 212 km. 50 % der ",
    "Datenerhebungen hatten ein Strassennetz von weniger als 67 km."
]

p_16_1 = [
    "<b>Die Anzahl der Datenerhebungen</b> reicht von 0 bis 23. Von den 354 Datenerhebungen hatten 50 % 3 oder weniger ",
    "Flussmündungen innerhalb von 1500 m um den Erhebungsort. Die Grösse des mündenden Flusses oder Kanals wurde nicht ",
    "berücksichtigt. Datenerhebungen an Fliessgewässern haben 0 Flussmündungen."
]
p_16_1 = makeAParagraph(p_16_1)

p_16_2 =[
    "<b>Die Bevölkerung</b> (nicht gezeigt) stammt aus der Statistik der Bevölkerung und der Haushalte 2018 und stellt ",
    "die Bevölkerung der Gemeinde dar, die den Erhebungsort umgibt. Die kleinste Einwohnerzahl betrug 442 und die grösste ",
    "415 367. Von den gesamten Datenerhebungen stammen 50 % aus Gemeinden mit einer Einwohnerzahl von mindestens 12 812."
]

p_16_2 = makeAParagraph(p_16_2)

p_14_16 = sectionParagraphs([p_14,], smallspace=smallest_space)

p_14 = makeAParagraph(p_14)
p_15 = makeAParagraph(p_15)
p_16 = makeAParagraph(p_16)

o_w, o_h = convertPixelToCm(landnutzung_file_name)
caption_4 = ["Verteilung der Anzahl der Datenerhebungen für die verschiedenen Landnutzungsmerkmale, n = 350 Stichproben"]
caption_4 = makeAParagraph(caption_4)

figure_kwargs = {
    "image_file":landnutzung_file_name,
    "caption": caption_4, 
    "original_width":o_w,
    "original_height":o_h,
    "desired_width": 7.9,
    "caption_height":1.5,
    "hAlign": "LEFT",
}

figure_4 = figureAndCaptionTable(**figure_kwargs)



# ### Auswahl der Datenerhebungsorte
# 
# Die Erhebungsorte wurden anhand der folgenden Kriterien ausgewählt:
# 
# * Daten aus früheren Datenerhebungen (SLR, MCBP)
# * Ganzjährig sicherer Zugang
# * Innerhalb von 30 Minuten zu Fuss von den nächsten öffentlichen Verkehrsmitteln entfernt
# 
# **Die Erhebungsorte repräsentieren die mit öffentlichen Verkehrsmitteln erreichbaren Landnutzungsbedingungen von etwa 1,7 Millionen Menschen.**.

# In[7]:


subsection_two = Paragraph("Auswahl der Datenerhebungsorte", subsection_title)

p_17 = [
    "Die Erhebungsorte wurden anhand der folgenden Kriterien ausgewählt:"
]

fourth_list = [
    "Daten aus früheren Datenerhebungen (SLR, MCBP)",
    "Ganzjährig sicherer Zugang",
    "Innerhalb von 30 Minuten zu Fuss von den nächsten öffentlichen Verkehrsmitteln entfernt"
]

p_18 = [
    "Die Erhebungsorte repräsentieren die mit öffentlichen Verkehrsmitteln erreichbaren ",
    "Landnutzungsbedingungen von etwa 1,7 Millionen Menschen."
]

p_17 = makeAParagraph(p_17)
p_18 = makeAParagraph(p_18)
fourth_list = makeAList(fourth_list)


texts = [
    subsection_one,
    smallest_space,
    p_14,
    smallest_space,
    p_15,
    smallest_space,
    p_16,
    smallest_space,
    p_16_1,
    smallest_space,
    p_16_2,
    smallest_space,
    subsection_two,
    smallest_space,
    p_17,
    smallest_space,
    fourth_list,
    smallest_space,
    p_18,
]


figure_text = [
    [[figure_2, large_space, figure_3, large_space, figure_4 ], texts],
   
]

side_by_side = Table(figure_text, style=featuredata.side_by_side_style_figure_left, colWidths=[8*cm, 8*cm])

new_components = [
    side_by_side,
    PageBreak()
]
pdfcomponents = addToDoc(new_components, pdfcomponents)


# ## Zuordnung von Landnutzung zu Erhebungsergebnissen
# 
# Es gibt 350 Datenerhebungen an 129 Erhebungsorten entlang von Fliessgewässern und Seen. Der Mittelwert war mehr als doppelt so hoch wie der Median, was die extremen Werte widerspiegelt, die für Ufer-Abfallobjekte-Untersuchungen typisch sind. {cite}`eubaselines` 

# In[8]:


section_two = Paragraph("Zuordnung von Landnutzung zu Erhebungsergebnissen", style=section_title)

p_19 = [
    "Es gibt 350 Datenerhebungen an 129 Erhebungsorten entlang von Fliessgewässern und Seen. ",
    "Der Mittelwert war mehr als doppelt so hoch wie der Median, was die extremen Werte ",
    "widerspiegelt, die für Ufer-Abfallobjekte-Untersuchungen typisch sind.",
    '<a href="#HG19" color="blue">(HG19)</a>'
]


# In[9]:


# set the date intervals for the chart
months = mdates.MonthLocator(interval=1)
months_fmt = mdates.DateFormatter('%b')
days = mdates.DayLocator(interval=7)

# set the grid for the chart
sns.set_style("whitegrid")

# chart the daily totals and the ECDF of all surveys under consideration
fig, ax = plt.subplots(1,2, figsize=(10,6), sharey=False)

axone=ax[0]
axtwo = ax[1]

axone.set_ylabel("p/m", **ck.xlab_k14)
axone.xaxis.set_minor_locator(days)
axone.xaxis.set_major_formatter(months_fmt)
axone.set_xlabel(" ")

axtwo.set_ylabel("Prozent der Standorte", **ck.xlab_k14)
axtwo.set_xlabel("p/m", **ck.xlab_k)

# time series plot of the survey results
sns.scatterplot(data=dfdt, x='date', y=unit_label, color="dodgerblue", s=34, ec='white', ax=axone)

# ecdf of the survey results
this_ecdf = ECDF(dfdt.pcs_m.values)

# plot the cumulative disrtibution
sns.lineplot(x=this_ecdf.x,y=this_ecdf.y, ax=axtwo, label='Kumulativverteilung')

# get the median and mean from the data
the_median = dfdt.pcs_m.median()
the_mean = dfdt.pcs_m.mean()

# get the percentile ranking of the mean
p_mean = this_ecdf(the_mean)

# plot the median and drop horzontal and vertical lines
axtwo.scatter([the_median], 0.5, color='red',s=50, linewidth=2, zorder=100, label="Median")
axtwo.vlines(x=the_median, ymin=0, ymax=0.5, color='red', linewidth=1)
axtwo.hlines(xmax=the_median, xmin=0, y=0.5, color='red', linewidth=1)

# plot the mean and drop horzontal and vertical lines
axtwo.scatter([the_mean], p_mean, color='magenta',s=50, linewidth=2, zorder=100, label="Mittelwert")
axtwo.vlines(x=the_mean, ymin=0, ymax=p_mean, color='magenta', linewidth=1)
axtwo.hlines(xmax=the_mean, xmin=0, y=p_mean, color='magenta', linewidth=1)

handle, labels = axtwo.get_legend_handles_labels()

plt.legend(handle,labels)

plt.tight_layout()
figure_name = f"results_distribution"

results_distribution_file_name = f'{save_fig_prefix}{figure_name}.jpeg'
save_figure_kwargs.update({"fname":results_distribution_file_name})
plt.savefig(**save_figure_kwargs)

results_distribution_cpt = [
    "<b>Links:</b> Erhebungsergebnisse. <b>Rechts:</b> kumulative Verteilung aller Seen und Fliessgewässer ohne Walensee ",
    "(das Walenseegebiet wurde mangels ausreichender Landnutzungsdaten ausgeschlossen). Anzahl der Proben: 350. ",
    "Anzahl der Erhebungsorte: 129. Median: 2,14 p/m. Mittelwert: 4,15 p/m.",
]


results_distribution_caption = ''.join(results_distribution_cpt)

glue("results_distributionresults_distribution_caption", results_distribution_caption, display=False)

glue("results_distribution_example", fig, display=False)

plt.close()


# ```{glue:figure} results_distribution_example
# :name: "results_distribution_example"
# ` `
# ```
# {numref}`Abildung %s: <results_distribution_example>` __Links:__ Erhebungsergebnisse. __Rechts:__ kumulative Verteilung aller Seen und Fliessgewässer ohne Walensee (das Walenseegebiet wurde mangels ausreichender Landnutzungsdaten ausgeschlossen). Anzahl der Proben: 350. Anzahl der Erhebungsorte: 129. Median: 2,14 p/m. Mittelwert: 4,15 p/m.

# In[10]:


fig_5_cap = makeAParagraph(results_distribution_cpt, style=caption_style)
o_w, o_h = convertPixelToCm(results_distribution_file_name)
figure_kwargs.update({
    "image_file":results_distribution_file_name,
    "original_width":o_w,
    "original_height":o_h,
    "desired_width": 15,
    "caption": fig_5_cap,
})

figure_5 = figureAndCaptionTable(**figure_kwargs)


# ### Spearmans $\rho$ – ein Beispiel
# 
# Die Rangkorrelation nach Spearman testet auf eine statistisch signifikante monotone Beziehung oder Assoziation zwischen zwei Variablen. Die Hypothese lautet, dass es keinen Zusammenhang zwischen dem Landnutzungsprofil und den Erhebungsergebnissen gibt. {cite}`defspearmans` 
# 
# Die Testergebnisse beziehen sich auf die Richtung (Rho) einer Assoziation und darauf, ob diese Assoziation wahrscheinlich auf einen Zufall zurückzuführen ist (p-Wert) oder nicht.) Damit ein Test als signifikant gilt, muss der p-Wert kleiner als 0,05 sein. {cite}`impspearmans`
# 
# * Nullhypothese: Es gibt keine monotone Beziehung zwischen den beiden Variablen.
# * Alternativhypothese: Es besteht eine monotone Beziehung und das Vorzeichen (+/-) gibt die Richtung an.
# 
# Sie gibt keine Auskunft über das Ausmass der Beziehung. Als Beispiel sei die Beziehung zwischen den Erhebungsergebnissen von Zigarettenstummeln und der bebauten oder landwirtschaftlich genutzten Fläche angeführt. {cite}`spearmansexplained`

# In[11]:


p_19 = makeAParagraph(p_19)

subsection_3 = Paragraph("Spearmans Rho – ein Beispiel", style=subsection_title)

p_20 = [
    "Die Rangkorrelation nach Spearman testet auf eine statistisch signifikante monotone ",
    "Beziehung oder Assoziation zwischen zwei Variablen. Die Hypothese lautet, dass es keinen ",
    "Zusammenhang zwischen dem Landnutzungsprofil und den Erhebungsergebnissen gibt.",
    '<a href="#Wikd" color="blue">(Wikd)</a>'
]

p_21 = [
    "Die Testergebnisse beziehen sich auf die Richtung ($\rho$) einer Assoziation und darauf, ",
    "ob diese Assoziation wahrscheinlich auf einen Zufall zurückzuführen ist (p-Wert) oder nicht. ",
    "Damit ein Test als signifikant gilt, muss der p-Wert kleiner als 0,05 sein.",
    '<a href="#scc" color="blue">(scc)</a>'
]

p_20_21 = sectionParagraphs([p_20, p_21], smallspace=smallest_space)

fifth_list = [
    "Nullhypothese: Es gibt keine monotone Beziehung zwischen den beiden Variablen.",
    "Alternativhypothese: Es besteht eine monotone Beziehung und das Vorzeichen (+/-) gibt die Richtung an."
]

fifth_list = makeAList(fifth_list)

p_22 = [
    "Sie gibt keine Auskunft über das Ausmass der Beziehung. Als Beispiel sei die Beziehung "
    "zwischen den Erhebungsergebnissen von Zigarettenstummeln und der bebauten oder ",
    "landwirtschaftlich genutzten Fläche angeführt.",
    '<a href="#Inn" color="blue">(Inn)</a>'
]

p_22 = makeAParagraph(p_22)

def addBibEntry(name, team, pub):
    joined = ''.join(pub)
    return makeAParagraph(featuredata.makeBibEntry(name=name, team=team, pub=pub))

team = "Scipy, Numfocus"
pub = [
    "Python scientific computing. Scipy stats spearmanr: implementation. URL: ",
    "https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.spearmanr.html."
]
name = "scc"

scc = addBibEntry(name, team, pub)

references = [*references, smallest_space, scc]

name = "Inn"
team = "Mathematics Education Innovation"
pub = [
    "Mathematics Education Innovation. Spearmans rank correlation. URL: ",
    "https://mei.org.uk/files/pdf/Spearmanrcc.pdf."
]

meinn = addBibEntry(name, team, pub)

references = [*references, smallest_space, meinn]


# In[12]:


# data for the example
data = survey_data[survey_data.code == "G27"].groupby(["loc_date","% to buildings", "% to agg"], as_index=False)[unit_label].sum()

# run the test under the two conditions
sprmns_b = stats.spearmanr(data["% to buildings"], data[unit_label])
sprmns_a = stats.spearmanr(data["% to agg"], data[unit_label])

# plot the survey results with respect to the land use profile
fig, axs = plt.subplots(1,2, figsize=(8,5.5), sharey=True)

sns.scatterplot(data=data, x="% to buildings", y=unit_label, ax=axs[0], color="magenta")
sns.scatterplot(data=data, x="% to agg", y=unit_label, ax=axs[1], color="dodgerblue")

axs[0].set_xlabel("% Gebäude", **ck.xlab_k14)
axs[1].set_xlabel("% Landwirtschaft", **ck.xlab_k14)

axs[0].set_ylabel("p/m", **ck.xlab_k14)

plt.tight_layout()
figure_name = f"spearmans_example"

spearmans_example_file_name = f'{save_fig_prefix}{figure_name}.jpeg'
save_figure_kwargs.update({"fname":spearmans_example_file_name})
plt.savefig(**save_figure_kwargs)

spearmans_example_cpt = [
    "<b>Links:</b> Erhebungsergebnisse. <b>Rechts:</b> kumulative Verteilung aller Seen und Fliessgewässer ohne Walensee ",
    "(das Walenseegebiet wurde mangels ausreichender Landnutzungsdaten ausgeschlossen). Anzahl der Proben: 350. ",
    "Anzahl der Erhebungsorte: 129. Median: 2,14 p/m. Mittelwert: 4,15 p/m.",
]

spearmans_example_caption = ''.join(spearmans_example_cpt)

glue("spearmans_example_caption", spearmans_example_caption, display=False)

glue("spearmans_example", fig, display=False)
plt.close()


# ```{glue:figure} spearmans_example
# :name: "spearmans_example"
# ` `
# ```
# {numref}`Abildung %s: <spearmans_example>` __Links:__ Datenerhebungen der Zigarettenstummel in Bezug auf den prozentualen Anteil der Grundstücke an den Gebäuden. Rho = 0,39, p-value < 0,001. __Rechts:__ Datenerhebungen der Zigarettenstummel in Bezug auf den Prozentsatz der landwirtschaftlichen Nutzfläche. Rho = -0,31, p-value < 0,001.

# In[13]:


fig_6_caption = [
    "<b>Links:</b> Datenerhebungen der Zigarettenstummel in Bezug auf den prozentualen Anteil der Grundstücke an den ",
    "Gebäuden. Rho = 0,39, p-value < 0,001. <b>Rechts:</b> Datenerhebungen der Zigarettenstummel in Bezug auf den ",
    "Prozentsatz der landwirtschaftlichen Nutzfläche. Rho = -0,31, p-value < 0,001."
]

fig_6_caption = makeAParagraph(fig_6_caption, style=caption_style)

o_w, o_h = convertPixelToCm(spearmans_example_file_name)
figure_kwargs.update({
    "image_file":spearmans_example_file_name,
    "original_width":o_w,
    "original_height":o_h,
    "desired_width": 12,
    "caption": fig_6_caption,
    "hAlign":"CENTER"
})

figure_6 = figureAndCaptionTable(**figure_kwargs)

new_components = [
    section_two,
    small_space,
    p_19,
    smallest_space,
    figure_5,    
    small_space,
    PageBreak(),
    subsection_3,
    small_space,
    *p_20_21,
    fifth_list,
    smallest_space,
    p_22,
    small_space,
    figure_6,
    small_space,
    
 
]
pdfcomponents = addToDoc(new_components, pdfcomponents)


# Betrachtet man die Erhebungsergebnisse für Zigarettenstummel in Bezug auf den prozentualen Anteil von bebauten oder landwirtschaftlich genutzten Flächen, ist der Wert von Rho entgegengesetzt.
# 
# ### Zuordnung der Erhebungssummen zur Landnutzung
# 
# Ergebnisse des Spearman-Rangkorrelationstests: Summen der Datenerhebungen in Bezug auf das Landnutzungsprofil
# 
# * Rot/Rosa steht für eine positive Assoziation
# * Gelb steht für eine negative Assoziation
# * Weiss bedeutet, dass keine statistische Grundlage für die Annahme eines Zusammenhangs vorliegt, p > 0,05

# In[14]:


p_23 = [
    "Betrachtet man die Erhebungsergebnisse für Zigarettenstummel in Bezug auf den ",
    "prozentualen Anteil von bebauten oder landwirtschaftlich genutzten Flächen, ",
    "ist der Wert von Rho entgegengesetzt."
]
p_23 = makeAParagraph(p_23)

subsection_4 = Paragraph("Zuordnung der Erhebungssummen zur Landnutzung", style=subsection_title)

p_24 = [
    "Ergebnisse des Spearman-Rangkorrelationstests: Summen der Datenerhebungen in Bezug auf das Landnutzungsprofil"
]

p_24 = makeAParagraph(p_24)

sixth_list = [
    "Rot/Rosa steht für eine positive Assoziation",
    "Gelb steht für eine negative Assoziation",
    "Weiss bedeutet, dass keine statistische Grundlage für die Annahme eines Zusammenhangs vorliegt, p > 0,05"
]

sixth_list = makeAList(sixth_list)

new_components = [
    p_23,
    smallest_space,
    
  
]
 
pdfcomponents = addToDoc(new_components, pdfcomponents)


# In[15]:


# correlation  of survey total to land use attributes:
fig, axs = plt.subplots(2, 3, figsize=(8,7), sharey="row")

for i, n in enumerate(luse_exp):
    r = i%2
    c = i%3
    ax=axs[r,c] 
    ax, corr, a_p = sut.make_plot_with_spearmans(dfdt, ax, n, unit_label=unit_label)
    if c == 0:
        ax.set_ylabel('pcs/m', **ck.xlab_k)
    ax.set_xlabel(featuredata.luse_de[n], **ck.xlab_k)
    if a_p <= .001:
        title_str = "p < .001"
    else:
        title_str = F"p={round(a_p, 3)}"
    
    ax.set_title(rF"$\rho={round(corr,4)}$, {title_str}")
    
    # find p    
    if a_p < 0.05:
        if corr > 0:
            ax.patch.set_facecolor('salmon')
            ax.patch.set_alpha(0.5)
        else:
            ax.patch.set_facecolor('palegoldenrod')
            ax.patch.set_alpha(0.5)

plt.tight_layout()

figure_name = f"sprmns_ex_survey_total"

sprmns_ex_survey_total_file_name = f'{save_fig_prefix}{figure_name}.jpeg'
save_figure_kwargs.update({"fname":sprmns_ex_survey_total_file_name})
plt.savefig(**save_figure_kwargs)

spearmans_example_cpt = [
    "Im Allgemeinen kann ein positiver Zusammenhang zwischen den Erhebungsergebnissen und dem prozentualen Anteil ",
    "der Flächen für Gebäude oder Aktivitäten im Freien und ein negativer Zusammenhang mit ",
    "Wäldern und Landwirtschaf angenommen werden."
]

sprmns_ex_survey_total_caption = ''.join(spearmans_example_cpt)

glue("sprmns_ex_survey_total_caption", sprmns_ex_survey_total_caption, display=False)

glue("sprmns_ex_survey_total", fig, display=False)
plt.close()


# In[16]:


fig_7_caption = [
    "Im Allgemeinen kann ein positiver Zusammenhang zwischen den Erhebungsergebnissen und dem prozentualen Anteil ",
    "der Flächen für Gebäude oder Aktivitäten im Freien und ein negativer Zusammenhang mit ",
    "Wäldern und Landwirtschaf angenommen werden."
]

fig_7_caption = makeAParagraph(fig_7_caption, style=caption_style)

o_w, o_h = convertPixelToCm(sprmns_ex_survey_total_file_name)
figure_kwargs.update({
    "image_file":sprmns_ex_survey_total_file_name,
    "original_width":o_w,
    "original_height":o_h,
    "desired_width": 12,
    "caption": fig_7_caption,
})

figure_7 = figureAndCaptionTable(**figure_kwargs)

new_components = [
    subsection_4,
    small_space,
    p_24,
    smallest_space,
    sixth_list,
    figure_7
]
 
pdfcomponents = addToDoc(new_components, pdfcomponents)


# ```{glue:figure} sprmns_ex_survey_total
# :name: sprmns_ex_survey_total
# ` `
# ```
# {numref}`Abildung %s: <sprmns_ex_survey_total>` {glue:text}`sprmns_ex_survey_total_caption`

# ### Zuordnung der häufigsten Objekte zur Landnutzung
# 
# Die häufigsten Objekte sind alle Objekte, die entweder die zehn häufigsten nach Anzahl sind oder alle Objekte, die in mindestens 50 % aller Datenerhebungen identifiziert wurden, was ungefähr 68 % aller identifizierten und gezählten Objekte entspricht. Einige Objekte wurden in 50 % der Fälle identifiziert, kamen aber nicht so häufig vor, dass sie in die «Top-Ten-Liste» aufgenommen werden konnten.

# In[17]:


subsection_five = Paragraph("Zuordnung der häufigsten Objekte zur Landnutzung", style=subsection_title)

p_25 = [
    "Die häufigsten Objekte sind alle Objekte, die entweder die zehn häufigsten nach Anzahl sind oder alle Objekte, ",
    "die in mindestens 50 % aller Datenerhebungen identifiziert wurden, was ungefähr 68 % aller identifizierten und gezählten ",
    "Objekte entspricht. Einige Objekte wurden in 50 % der Fälle identifiziert, kamen aber nicht so häufig vor, dass sie in die ",
    "«Top-Ten-Liste» aufgenommen werden konnten."
]
p_25 = makeAParagraph(p_25)


# In[18]:


# common aggregations of survey data
agg_pcs_quantity = {unit_label:"sum", "quantity":"sum"}
agg_pcs_median = {unit_label:"median", "quantity":"sum"}

# cumulative statistics for each code
c_t_params = dict(agg=agg_pcs_median, description_map=code_description_map, material_map=code_material_map)
code_totals = sut.the_aggregated_object_values(survey_data, **c_t_params)
code_totals['item'] = code_totals.index.map(lambda x: codes_class.dMap.loc[x])

# all codes with a fail rate > fail rate = most common objects
better_than_50 = code_totals[code_totals["fail rate"] >= 50]

# the ten objects with the greatest quantity
t_ten = code_totals.sort_values(by="quantity", ascending=False)[:10]

# combine the most abundant with the most common
abundant_codes = list(set(t_ten.index) | set(better_than_50.index))

# get the survey data for the most common codes for the final table data
cols_to_use = ['item','quantity', 'fail rate', '% of total']
m_common = code_totals.loc[abundant_codes, cols_to_use].sort_values(by="quantity", ascending=False)
m_common["% of total"] = ((m_common.quantity/survey_data.quantity.sum())*100).astype('int')


# format values for table
new_columns = featuredata.most_common_objects_table_de
mcc = m_common[list(new_columns.keys())]


colLabels = list(new_columns.values())
mcc.rename(columns=new_columns, inplace=True)


language = "de"
# .pdf output
data = mcc.copy()
data["Anteil"] = data["Anteil"].map(lambda x: f"{int(x)}%")
data['Objekte (St.)'] = data['Objekte (St.)'].map(lambda x:featuredata.thousandsSeparator(x, language))
data['Häufigkeitsrate'] = data['Häufigkeitsrate'].map(lambda x: f"{x}%")
data.set_index("Objekte", drop=True, inplace=True)

mc_caption_string = [
  "Die am häufigsten gefundenen Objekte sind die zehn mengenmässig am meisten vorkommenden Objekte ",
   "und/oder Objekte, die in mindestens 50\% aller Datenerhebungen identifiziert wurden (Häufigkeitsrate)."
]

mc_caption_string = "".join(mc_caption_string)

pdf_mc_table  = featuredata.aStyledTable(data, caption=mc_caption_string, colWidths=[7*cm, 2.2*cm, 2*cm, 2.8*cm])


# this defines the css rules for the note-book table displays
header_row = {'selector': 'th:nth-child(1)', 'props': f'background-color: #FFF;'}
even_rows = {"selector": 'tr:nth-child(even)', 'props': f'background-color: rgba(139, 69, 19, 0.08);'}
odd_rows = {'selector': 'tr:nth-child(odd)', 'props': 'background: #FFF;'}
table_font = {'selector': 'tr', 'props': 'font-size: 12px;'}
table_css_styles = [even_rows, odd_rows, table_font, header_row]

# set pandas display
aformatter = {
   "Anteil":lambda x: f"{int(x)}%",
   "Häufigkeitsrate": lambda x: f"{int(x)}%",   
   "Objekte (St.)": lambda x: featuredata.thousandsSeparator(int(x), "de")
}

mcc.set_index("Objekte", inplace=True, drop=True)
mcc.index.name = None
mcc.columns.name = None


mcd = mcc.style.format(aformatter).set_table_styles(table_css_styles)
glue('mcommon_caption', mc_caption_string, display=False)
glue('mcommon_tables', mcd, display=False)


# ```{glue:figure} mcommon_tables
# :name: mcommon_tables
# ` `
# ```
# {numref}`Abildung %s: <mcommon_tables>` Die am häufigsten gefundenen Objekte sind die zehn mengenmässig am meisten vorkommenden Objekte, und/oder Objekte, die in mindestens 50 \% aller Datenerhebungen identifiziert wurden (Häufigkeitsrate).

# In[19]:


new_components = [
    small_space,
    subsection_five,
    small_space,
    p_25,
    smallest_space,    
    pdf_mc_table,    
]
 
pdfcomponents = addToDoc(new_components, pdfcomponents)


# #### Ergebnisse Spearmans $\rho$
# 
# Aus der ersten Abbildung lässt sich ein positiver Zusammenhang zwischen der Anzahl der identifizierten Objekte und dem prozentualen Anteil der Flächen, die Gebäuden und Orten für Aktivitäten im Freien zugeordnet sind, ableiten. Das Umgekehrte gilt für den prozentualen Anteil von Landwirtschaft und Wald. Es gibt keine statistische Grundlage für die Annahme eines Zusammenhangs zwischen der Länge von Strassen oder der Anzahl von Flussmündungen und dem Gesamtergebnis der Erhebung.
# 
# Das Ergebnis von Spearmans Rho für die am häufigsten vorkommenden Objekte steht im Zusammenhang mit den Ergebnissen in der vorangegangenen Abbildung und veranschaulicht, wie sich verschiedene Objekte unter verschiedenen Bedingungen anhäufen.
# 
# * Rot/Rosa steht für eine positive Assoziation
# * Gelb steht eine negative Assoziation
# * Weiss bedeutet, dass keine statistische Grundlage für die Annahme eines Zusammenhangs vorliegt, p > 0,05
# 

# In[20]:


subsection_six = Paragraph("Ergebnisse Spearmans Rho", style=subsection_title)

p_26 = [
    "Aus der ersten Abbildung lässt sich ein positiver Zusammenhang zwischen der Anzahl ",
    "der identifizierten Objekte und dem prozentualen Anteil der Flächen, die Gebäuden und ",
    "Orten für Aktivitäten im Freien zugeordnet sind, ableiten. Das Umgekehrte gilt für den ",
    "prozentualen Anteil von Landwirtschaft und Wald. Es gibt keine statistische Grundlage für ",
    "die Annahme eines Zusammenhangs zwischen der Länge von Strassen oder der Anzahl von ",
    "Flussmündungen und dem Gesamtergebnis der Erhebung."
]

p_27 = [
    "Das Ergebnis von Spearmans Rho für die am häufigsten vorkommenden Objekte steht im ",
    "Zusammenhang mit den Ergebnissen in der vorangegangenen Abbildung und veranschaulicht, ",
    "wie sich verschiedene Objekte unter verschiedenen Bedingungen anhäufen."
]

p_26_27 = sectionParagraphs([p_26, p_27], smallspace=smallest_space)

seventh_list = [
    "Rot/Rosa steht für eine positive Assoziation",
    "Gelb steht eine negative Assoziation",
    "Weiss bedeutet, dass keine statistische Grundlage für die Annahme eines Zusammenhangs vorliegt, p > 0,05"
]

seventh_list = makeAList(seventh_list)



new_components = [
    PageBreak(),
    subsection_six,
    small_space,
    *p_26_27
     
   
]
 
pdfcomponents = addToDoc(new_components, pdfcomponents)


# In[21]:


fig, axs = plt.subplots(len(abundant_codes),len(luse_exp), figsize=(len(luse_exp)+6,len(abundant_codes)), sharey='row')

for i,code in enumerate(m_common.index):
    data = survey_data[survey_data.code == code]
    for j, n in enumerate(luse_exp):
        this_data = data.groupby(['loc_date', n], as_index=False)[unit_label].sum()
        ax=axs[i, j]
        ax.grid(False)
        ax.tick_params(axis='both', which='both',bottom=False,top=False,labelbottom=False, labelleft=False, left=False)
       
        if i == 0:
            ax.set_title(F"{luse_ge[n]}", fontsize=10)
        else:
            pass
        
        if j == 0:
            ax.set_ylabel(F"{codes_class.dMap.loc[code]}", rotation=0, ha='right', **ck.xlab_k14)
            ax.yaxis.label.set(fontsize=10)
            ax.set_xlabel(" ")
        else:
            ax.set_xlabel(" ")
            ax.set_ylabel(" ")
               
        _, corr, a_p = sut.make_plot_with_spearmans(this_data, ax, n, unit_label=unit_label)
        
        if a_p < 0.05:
            if corr > 0:
                ax.patch.set_facecolor('salmon')
                ax.patch.set_alpha(0.5)
            else:
                ax.patch.set_facecolor('palegoldenrod')
                ax.patch.set_alpha(0.5)

plt.tick_params(labelsize=10, which='both', axis='both')

plt.tight_layout()

plt.subplots_adjust(wspace=0.02, hspace=0.02)

figure_name = f"sprmns_mcommon"

sprmns_mcommon_file_name = f'{save_fig_prefix}{figure_name}.jpeg'
save_figure_kwargs.update({"fname":sprmns_mcommon_file_name})
plt.savefig(**save_figure_kwargs)

sprmns_mcommon_cpt = [
    " "
]

sprmns_mcommon_caption = ''.join(sprmns_mcommon_cpt)

glue("sprmns_mcommon_captionl_caption", sprmns_mcommon_caption, display=False)

glue("sprmns_mcommon", fig, display=False)

plt.close()


# ```{glue:figure} sprmns_mcommon
# :name: sprmns_mcommon
# ` `
# ```
# {numref}`Abildung %s: <sprmns_mcommon>` {glue:text}`sprmns_ex_survey_total_caption`

# ### Spearmans $\rho$ interpretieren 
# 
# Eine positive Assoziation bedeutet, dass die Erhebungsergebnisse tendenziell zunehmen, wenn der prozentuale Wert des Landnutzungsmerkmals steigt. Dies kann auf eine Kovarianz der Merkmale zurückzuführen sein. In jedem Fall ist eine positive Assoziation ein Signal dafür, dass sich die Objekte unter diesen Bedingungen eher häufen.
# 
# Eine negative Assoziation bedeutet, dass das Landnutzungsmerkmal die Akkumulation des Objekts nicht erleichtert. Dieses Ergebnis ist für landwirtschaftliche Flächen und Wälder auf nationaler Ebene üblich. Eine negative Assoziation ist ein Signal dafür, dass die Objekte unter diesen Bedingungen nicht zur Akkumulation neigen.
# 
# Keine oder wenige Assoziationen bedeutet, dass die Landnutzungsmerkmale keinen Einfluss auf die Akkumulation des Objekts hatten. Die Erhebungsergebnisse der häufigsten Objekte ohne oder mit wenigen Assoziationen lassen sich in zwei Kategorien einteilen: 
# 
# * Allgegenwärtig: hohe Häufigkeitsrate, hohe Stückzahl pro Meter. Unabhängig von der Landnutzung im gesamten Untersuchungsgebiet in gleichbleibenden Raten gefunden.
# * Vorübergehend: niedrige Häufigkeitsrate, hohe Menge, hohe Stückzahl pro Meter, wenige Verbände. Gelegentlich in grossen Mengen an bestimmten Orten gefunden 

# In[22]:


fig_8_caption = sprmns_mcommon_cpt

fig_8_caption = makeAParagraph(fig_8_caption, style=caption_style)

o_w, o_h = convertPixelToCm(sprmns_mcommon_file_name)
figure_kwargs.update({
    "image_file":sprmns_mcommon_file_name,
    "original_width":o_w,
    "original_height":o_h,
    "desired_width": 16,
    "caption": fig_8_caption,
})

figure_8 = figureAndCaptionTable(**figure_kwargs)

subsection_seven = Paragraph("Spearmans Rho interpretieren", style=subsection_title)

p_28 = [
    "Eine positive Assoziation bedeutet, dass die Erhebungsergebnisse tendenziell ",
    "zunehmen, wenn der prozentuale Wert des Landnutzungsmerkmals steigt. Dies kann ",
    "auf eine Kovarianz der Merkmale zurückzuführen sein. In jedem Fall ist eine ",
    "positive Assoziation ein Signal dafür, dass sich die Objekte unter",
    "diesen Bedingungen eher häufen."
]

p_29 = [
    "Eine negative Assoziation bedeutet, dass das Landnutzungsmerkmal die Akkumulation ",
    "des Objekts nicht erleichtert. Dieses Ergebnis ist für landwirtschaftliche Flächen ",
    "und Wälder auf nationaler Ebene üblich. Eine negative Assoziation ist ein Signal ",
    "dafür, dass die Objekte unter diesen Bedingungen nicht zur Akkumulation neigen."
]

p_30 = [
    "Keine oder wenige Assoziationen bedeutet, dass die Landnutzungsmerkmale keinen Einfluss ",
    "auf die Akkumulation des Objekts hatten. Die Erhebungsergebnisse der häufigsten Objekte ",
    "ohne oder mit wenigen Assoziationen lassen sich in zwei Kategorien einteilen:"
]

p_28_30 = sectionParagraphs([p_28, p_29, p_30], smallspace=smallest_space)

eigth_list = [
    "Allgegenwärtig: hohe Häufigkeitsrate, hohe Stückzahl pro Meter. Unabhängig von der Landnutzung im gesamten Untersuchungsgebiet in gleichbleibenden Raten gefunden.",
    "Vorübergehend: niedrige Häufigkeitsrate, hohe Menge, hohe Stückzahl pro Meter, wenige Verbände. Gelegentlich in grossen Mengen an bestimmten Orten gefunden"
]

eigth_list = makeAList(eigth_list)

new_components = [
    small_space,
    figure_8,
    PageBreak(),
    subsection_seven,
    small_space,
    *p_28_30,
    eigth_list,   
  
] 
pdfcomponents = addToDoc(new_components, pdfcomponents)


# ## Diskussion
# 
# Insgesamt war es wahrscheinlich, dass Datenerhebungen an Orten mit mehr Gebäuden und Möglichkeiten für Aktivitäten im Freien die Anhäufung von Objekten an Gewässern begünstigten. Betrachtet man die häufigsten Objekte, so wurden nur vier der zwölf Objekte in Anwesenheit von mehr Gebäuden häufiger identifiziert. Dabei handelt es sich in der Regel um Objekte, die mit dem Verzehr von Lebensmitteln und/oder Tabakwaren in der Nähe des Ortes zusammenhängen. Das deutet darauf hin, dass in stark frequentierten Gebieten in Wassernähe noch einiges an Vorbeugung und Verminderung möglich ist.
# 
# Sechs der zwölf Objekte haben jedoch keine positive Assoziation zur Fläche, die von Gebäuden eingenommen wird, wurden aber in mindestens 50 % aller Datenerhebungen gefunden. Diese Objekte werden im Allgemeinen mit der beruflichen Nutzung oder im Fall der Wattestäbchen mit der persönlichen Hygiene
# 
# * Kunststoff-Bauabfälle
# * fragmentierte Kunststoffe
# * Industriefolien
# * expandiertes Polystyrol
# * Wattestäbchen/Stäbchen
# * Isolierung, einschliesslich Sprühschäume
# 
# Ausserdem haben diese Objekte im Vergleich zu Produkten, die mit Tabakwaren oder Nahrungsmitteln in Verbindung stehen, im Allgemeinen weniger positive Assoziationen. Dies deutet darauf hin, dass das entsprechende Landnutzungsmerkmal derzeit nicht berücksichtigt wird und/oder diese Objekte unabhängig von den Landnutzungsmerkmalen in ähnlichen Mengen identifiziert werden. Es kann davon ausgegangen werden, dass diese Objekte in der Umwelt allgegenwärtig sind.
# 
# Schliesslich wurden zwei der zwölf häufigsten Objekte in weniger als 50 % der Datenerhebungen gefunden und weisen nur wenige positive Assoziationen auf:
# 
# * Industriepellets
# * expandierte Schaumstoffe < 5 mm
# 
# Diese Objekte werden in grossen Mengen sporadisch an bestimmten Orten gefunden. Sie wurden in allen Untersuchungsgebieten und in allen Seen identifiziert. Industriepellets haben einen sehr spezifischen Verwendungszweck und Kundenstamm, so dass es möglich ist, auf der Grundlage der Dichte und des Erhebungsorts der identifizierten Pellets und des Standorts des nächstgelegenen Verbrauchers oder Herstellers von Pellets, siehe [Geteilte Verantwortung](transport)¶, die Quelle zu bestimmen und die Auswirkungen zu verringern.
# 
# ### Anwendung
# 
# Die Anzahl der Stichproben, die verwendet werden, um eine Assoziation mit Spearman zu bestimmen, muss vorsichtig gewählt sein.
# 
# Ebenso das Gewicht, das den Ergebnissen beigemessen wird. Die Ergebnisse für Zigarettenfilter sind ein gutes Beispiel. Die Diagramme zeigen eindeutig sowohl negative als auch positive Assoziationen in Abhängigkeit von der Landnutzung, aber Rho ist kleiner als 0,5. Es handelt sich also keineswegs um eine lineare Beziehung und das Ausmass bleibt unbestimmt.
# 
# Die Betroffenen sollten diese Ergebnisse und deren Anwendbarkeit auf ihre spezifische Situation prüfen. Eine Schlussfolgerung, die gezogen werden kann, ist, dass es eine Methode gibt, um auf der Grundlage der empirischen Daten aus den Datenerhebungen mit angemessener Sicherheit Zonen der Akkumulation zu identifizieren. Diese Ergebnisse ermöglichen es den Akteuren, ihre Prioritäten auf die Herausforderungen zu setzen, die für ihre Region oder Situation spezifisch sind.
# 
# Der Korrelationskoeffizient nach Spearman lässt sich leicht anwenden, sobald der endgültige Datensatz bestimmt wurde. Der Wert des Koeffizienten ändert sich jedoch je nach Erhebungsgebiet oder See, an dem der Test angewendet wird. Das bedeutet, dass das Verständnis und die Interpretation dieser Ergebnisse nicht nur ein nationales, sondern auch ein regionales und kommunales Anliegen ist. 
# 
# __Warum 1500 Meter?__ Für diese Studie haben wir uns mit Objekten befasst, die hohe Werte für Rho bei kleineren Radien aufwiesen, die dem Massstab der bereitgestellten Daten angemessen waren. Es wurden auch andere Entfernungen in Betracht gezogen (2 km, 2,5 km, 5 km und 10 km). Generell gilt, dass mit zunehmendem Radius die den Gebäuden zugewiesene Fläche abnimmt und damit auch der Wert von Rho. Dieses Thema wurde in einem Artikel, der derzeit für das Peer-Review-Verfahren vorbereitet wird, ausführlicher behandelt.
# 
# Die Überprüfung einer Assoziation erfolgt durch die Berücksichtigung aller anderen Schlüsselindikatoren und das Urteil von Experten. Das kommunale Reinigungs- und Unterhaltspersonal ist mit den Bedingungen vor Ort vertraut und ist eine der besten Informationsquellen. Die Wiederholung von Stichproben an einem bestimmten Ort für einen bestimmten Zeitraum und der Vergleich der Ergebnisse mit den Ausgangswerten für das Erhebungsgebiet ist ebenfalls eine zuverlässige Methode, um die Leistung in Bezug auf das Erhebungsgebiet zu bestimmen.
# 
# Der Rangkorrelationskoeffizient ist eine effiziente und zuverlässige Methode, mit der sich Landnutzungsklassifizierungen identifizieren lassen, die mit erhöhten oder verringerten Mengen an bestimmten Abfallobjekten verbunden sind. Das Ausmass der Beziehung in Bezug auf die Anzahl der Objekte auf dem Boden bleibt jedoch undefiniert.
# 
# Um mehr darüber zu erfahren, wie sich die Erhebungsergebnisse je nach Landnutzung ändern und/oder gleichbleiben, siehe [Geteilte Verantwortung](transport).
# 
# Um zu verstehen, wie die Abfallobjekte für diesen Bericht berechnet wurden, siehe [Basiswerte für Abfallobjekte an Gewässern](threshhold).

# In[23]:


section_three = Paragraph("Diskussion", style=section_title)

p_31 = [
    "Insgesamt war es wahrscheinlich, dass Datenerhebungen an Orten mit mehr Gebäuden und Möglichkeiten ",
    "für Aktivitäten im Freien die Anhäufung von Objekten an Gewässern begünstigten. Betrachtet man ",
    "die häufigsten Objekte, so wurden nur vier der zwölf Objekte in Anwesenheit von mehr Gebäuden häufiger ",
    "identifiziert. Dabei handelt es sich in der Regel um Objekte, die mit dem Verzehr von Lebensmitteln ",
    "und/oder Tabakwaren in der Nähe des Ortes zusammenhängen. Das deutet darauf hin, dass in stark frequentierten ",
    "Gebieten in Wassernähe noch einiges an Vorbeugung und Verminderung möglich ist."
]

p_32 = [
    "Sechs der zwölf Objekte haben jedoch keine positive Assoziation zur Fläche, die von Gebäuden ",
    "eingenommen wird, wurden aber in mindestens 50 % aller Datenerhebungen gefunden. Diese Objekte ",
    "werden im Allgemeinen mit der beruflichen Nutzung oder im Fall ",
    "der Wattestäbchen mit der persönlichen Hygiene"
]

p_31_32 = sectionParagraphs([p_31, p_32], smallspace=smallest_space)
ninth_list = [
    "Kunststoff-Bauabfälle",
    "fragmentierte Kunststoffe",
    "Industriefolien",
    "expandiertes Polystyrol",
    "Wattestäbchen/Stäbchen",
    "Isolierung, einschliesslich Sprühschäume"
]

ninth_list = makeAList(ninth_list)

p_33 = [
    "Ausserdem haben diese Objekte im Vergleich zu Produkten, die mit Tabakwaren oder Nahrungsmitteln ",
    "in Verbindung stehen, im Allgemeinen weniger positive Assoziationen. Dies deutet darauf hin, dass ",
    "das entsprechende Landnutzungsmerkmal derzeit nicht berücksichtigt wird und/oder diese Objekte ",
    "unabhängig von den Landnutzungsmerkmalen in ähnlichen Mengen identifiziert werden. Es kann davon ",
    "ausgegangen werden, dass diese Objekte in der Umwelt allgegenwärtig sind."
]

p_34 = [
    "Schliesslich wurden zwei der zwölf häufigsten Objekte in weniger als 50 % der ",
    "Datenerhebungen gefunden und weisen nur wenige positive Assoziationen auf:"
]


p_33_34 = sectionParagraphs([p_33, p_34], smallspace=smallest_space)
last_list = [
    "Industriepellets",
    "expandierte Schaumstoffe < 5 mm"
]

last_list = makeAList(last_list)

p_35 = [
    "Diese Objekte werden in grossen Mengen sporadisch an bestimmten Orten gefunden. Sie wurden in allen Untersuchungsgebieten und ",
    "in allen Seen identifiziert. Industriepellets haben einen sehr spezifischen Verwendungszweck und Kundenstamm, so dass es möglich ",
    "ist, auf der Grundlage der Dichte und des Erhebungsorts der identifizierten Pellets und des Standorts des nächstgelegenen ",
    "Verbrauchers oder Herstellers von Pellets, siehe [Geteilte Verantwortung](transport)¶, die Quelle zu bestimmen und die ",
    "Auswirkungen zu verringern."
]

p_35 = makeAParagraph(p_35)

subsection_nine = Paragraph("Anwendung", style=subsection_title)

p_37 = [
    "Die Anzahl der Stichproben, die verwendet werden, um eine Assoziation mit Spearman zu bestimmen, muss vorsichtig gewählt sein."
]

p_38 = [
    "Ebenso das Gewicht, das den Ergebnissen beigemessen wird. Die Ergebnisse für Zigarettenfilter sind ein gutes Beispiel. ",
    "Die Diagramme zeigen eindeutig sowohl negative als auch positive Assoziationen in Abhängigkeit von der Landnutzung, aber ",
    "Rho ist kleiner als 0,5. Es handelt sich also keineswegs um eine lineare Beziehung und das Ausmass bleibt unbestimmt."
]

p_39 = [
    "Die Betroffenen sollten diese Ergebnisse und deren Anwendbarkeit auf ihre spezifische Situation prüfen. Eine ",
    "Schlussfolgerung, die gezogen werden kann, ist, dass es eine Methode gibt, um auf der Grundlage der empirischen ",
    "Daten aus den Datenerhebungen mit angemessener Sicherheit Zonen der Akkumulation zu identifizieren. Diese ",
    "Ergebnisse ermöglichen es den Akteuren, ihre Prioritäten auf die Herausforderungen zu setzen, die für ihre Region ",
    "oder Situation spezifisch sind."
]

p_40 = [
    "Der Korrelationskoeffizient nach Spearman lässt sich leicht anwenden, sobald der endgültige Datensatz bestimmt wurde. ",
    "Der Wert des Koeffizienten ändert sich jedoch je nach Erhebungsgebiet oder See, an dem der Test angewendet wird. ",
    "Das bedeutet, dass das Verständnis und die Interpretation dieser Ergebnisse nicht nur ein nationales, sondern auch ",
    "ein regionales und kommunales Anliegen ist."
]

p_41 = [
    "<b>Warum 1500 Meter?</b> Für diese Studie haben wir uns mit Objekten befasst, die hohe Werte für Rho bei kleineren Radien ",
    "aufwiesen, die dem Massstab der bereitgestellten Daten angemessen waren. Es wurden auch andere Entfernungen in ",
    "Betracht gezogen (2 km, 2,5 km, 5 km und 10 km). Generell gilt, dass mit zunehmendem Radius die den Gebäuden zugewiesene ",
    "Fläche abnimmt und damit auch der Wert von Rho. Dieses Thema wurde in einem Artikel, der derzeit für das ",
    "Peer-Review-Verfahren vorbereitet wird, ausführlicher behandelt."
]

p_42 = [
    "Die Überprüfung einer Assoziation erfolgt durch die Berücksichtigung aller anderen Schlüsselindikatoren und das Urteil ",
    "von Experten. Das kommunale Reinigungs- und Unterhaltspersonal ist mit den Bedingungen vor Ort vertraut und ist eine der ",
    "besten Informationsquellen. Die Wiederholung von Stichproben an einem bestimmten Ort für einen bestimmten Zeitraum und der ",
    "Vergleich der Ergebnisse mit den Ausgangswerten für das Erhebungsgebiet ist ebenfalls eine zuverlässige Methode, ", 
    "um die Leistung in Bezug auf das Erhebungsgebiet zu bestimmen."
]

p_43 = [
    "Der Rangkorrelationskoeffizient ist eine effiziente und zuverlässige Methode, mit der sich Landnutzungsklassifizierungen ",
    "identifizieren lassen, die mit erhöhten oder verringerten Mengen an bestimmten Abfallobjekten verbunden sind. Das Ausmass ",
    "der Beziehung in Bezug auf die Anzahl der Objekte auf dem Boden bleibt jedoch undefiniert."
]

p_44 = [
    "Um mehr darüber zu erfahren, wie sich die Erhebungsergebnisse je nach Landnutzung ändern und/oder ",
    'gleichbleiben, siehe <a href= "https://hammerdirt-analyst.github.io/IQAASL-End-0f-Sampling-2021/shared_responsibility.html" color="blue"> Geteilte Verantwortung </a>.'
]

p_45 = [
    "Um zu verstehen, wie die Abfallobjekte für diesen Bericht berechnet wurden, ",
    'siehe <a href="https://hammerdirt-analyst.github.io/IQAASL-End-0f-Sampling-2021/baselines.html" color="blue">Basiswerte für Abfallobjekte an Gewässern</a>.'
]

p_37_45 = sectionParagraphs([p_37, p_38, p_39, p_40, p_41, p_42, p_43, p_44, p_45], smallspace=smallest_space)


    
new_components = [
    *p_31_32,
    ninth_list,
    smallest_space,
    *p_33_34,
    last_list,
    smallest_space,
    p_35,
    smallest_space,
    subsection_nine,
    small_space,
    *p_37_45,   
    PageBreak(),
    Paragraph("Bibliographie", style=title_style),
    small_space,
    *references 
]
 
pdfcomponents = addToDoc(new_components, pdfcomponents)


# In[24]:


doc = SimpleDocTemplate(pdf_link, pagesize=A4, leftMargin=2.5*cm, rightMargin=1.5*cm, topMargin=3*cm, bottomMargin=1.5*cm)
pageinfo= f"IQAASL: Landnutzungsprofil"


def myLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Italic',9)
    canvas.drawString(1*cm, 1*cm, "S.%d %s" % (doc.page, pageinfo))
    canvas.restoreState()
    
doc.build(pdfcomponents,  onFirstPage=myLaterPages, onLaterPages=myLaterPages)

