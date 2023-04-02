#!/usr/bin/env python
# coding: utf-8

# In[1]:


# -*- coding: utf8 -*-
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
from resources.featuredata import makeAList

# images and display
import matplotlib.image as mpimg
from myst_nb import glue
from PIL import Image as PILImage

# loc = locale.getlocale()
# lang =  "de_CH.utf8"
# locale.setlocale(locale.LC_ALL, lang)

# set some parameters:
start_date = '2020-03-01'
end_date ='2021-05-31'

# name of the output folder:
name_of_project = 'reuse_remake'
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


# the scale for pieces per meter and the column and chart label for the units
reporting_unit = 100
unit_label = 'p/100 m'

# # get your data:
# survey_data = pd.read_csv('resources/checked_sdata_eos_2020_21.csv')
# dfBeaches = pd.read_csv("resources/beaches_with_land_use_rates.csv")
# dfCodes = pd.read_csv("resources/codes_with_group_names_2015.csv")
# dfDims = pd.read_csv("resources/corrected_dims.csv")


# # Recyceln und neugestalten
# 
# {Download}`Download </resources/pdfs/recycle_remake.pdf>`
# 
# Precious Plastic Léman ([PPL](https://preciousplasticleman.ch/)) st ein Verein, der sich aktiv für die 
# Wiederverwendung und  Reduzierung von Kunststoffabfällen in der Genferseeregion einsetzt. Die Mitglieder stellen neue Produkte her, indem sie die Kunststoffabfälle aus ihrer Werkstatt in Lausanne umwandeln. 
# 
# Als Designer und Verarbeiter verbringen die Mitglieder von PPL mehr Zeit in der Werkstatt als draussen mit dem Sammeln von Abfallobjekten aus Plastik. PPL erhält in erster Linie gebrauchte Kunststoffe aus Spenden, die am Arbeitsplatz abgegeben werden. In Bezug auf die Abfallobjekte an Gewässern hatten die Mitglieder von PPL zwei Fragen, die sie beantworten wollten:
# 
# 1. Wie viel des gesammelten Plastikmülls könnte für den Betrieb von PPL verwendet werden?
# 2. Was genau wäre erforderlich, um die am Ufer gesammelten Kunststoffe zu recyceln?
# 
# Die Mitglieder von PPL waren für drei Erhebungsorte am Genfersee verantwortlich und sammelten von April 2020 bis Mai 2021 Proben. Die Umwandlung von gebrauchten Kunststoffen in neue Produkte ist ein mehrstufiger Prozess. Sobald die Objekte gesammelt sind, müssen sie sortiert, gereinigt, zu Granulat verarbeitet und dann spritzgegossen werden. Es ist zu beachten, dass die Gesamtmengen und Prozentsätze der identifizierten Objekte, die im Folgenden erörtert werden, aufgezeichnete Daten aus dem Seen-und-Fliessgewässer-Teil des IQAALS-Projekts sind.
# 
# ## Sortieren
# 
# Verschiedene Arten von Kunststoffen haben unterschiedliche Eigenschaften. PPL achtet darauf, dass bei der Verarbeitung und Herstellung von Produkten keine Kunststoffarten vermischt werden. Bei Objekten, bei denen die Art des Kunststoffs nicht eindeutig angegeben ist, verwendet PPL die FTIR-Technologie zur Unterscheidung der Kunststoffarten.

# ```{figure} resources/images/reuse_recycle/machine.jpeg
# ---
# name: remake_machine
# ---
# ` ` 
# ```
# {numref}`Abbildung %s: <remake_machine>` Identifizierung von Kunststoffen aus Ufer-Abfallaufkommen-Untersuchungen

# Bei einer Untersuchung des Ufer-Abfallaufkommens stösst man auf eine Vielzahl von Kunststoffen. Nicht alles davon kann in Produkte mit Mehrwert umgewandelt werden. Durch die Identifizierung und Gruppierung der Kunststoffe nach ihrer Art kann PPL Objekte herstellen, die am besten zu den Eigenschaften des verwendeten Kunststoffs passen.

# In[2]:


pdfcomponents = []

chapter_title = Paragraph("Recyceln und neugestalten", style=title_style)

p1 = [
    'Precious Plastic Léman (<a href="https://preciousplasticleman.ch/" color="blue"> PPL</a>) ist ein Verein, der sich aktiv für die Wiederverwendung und ',
    "Reduzierung von Kunststoffabfällen in der Genferseeregion einsetzt. Die Mitglieder stellen neue Produkte her, indem sie die Kunststoffabfälle aus ",
    "ihrer Werkstatt in Lausanne umwandeln."
]

p2 = [
    "Als Designer und Verarbeiter verbringen die Mitglieder von PPL mehr Zeit in der Werkstatt als draussen mit dem Sammeln von Abfallobjekten aus Plastik. ",
    "PPL erhält in erster Linie gebrauchte Kunststoffe aus Spenden, die am Arbeitsplatz abgegeben werden. In Bezug auf die Abfallobjekte an Gewässern hatten ",
    "die Mitglieder von PPL zwei Fragen, die sie beantworten wollten:"
]

l1 = [
    "Wie viel des gesammelten Plastikmülls könnte für den Betrieb von PPL verwendet werden?",
    "Was genau wäre erforderlich, um die am Ufer gesammelten Kunststoffe zu recyceln?",
]

p3 = [
    "Die Mitglieder von PPL waren für drei Erhebungsorte am Genfersee verantwortlich und sammelten von April 2020 bis Mai 2021 Proben. ",
    "Die Umwandlung von gebrauchten Kunststoffen in neue Produkte ist ein mehrstufiger Prozess. Sobald die Objekte gesammelt sind, müssen ",
    "sie sortiert, gereinigt, zu Granulat verarbeitet und dann spritzgegossen werden. Es ist zu beachten, dass die Gesamtmengen und ",
    "Prozentsätze der identifizierten Objekte, die im Folgenden erörtert werden, aufgezeichnete Daten aus dem Seen-und-Fliessgewässer-Teil ",
    "des IQAALS-Projekts sind."
]

sect1_t = Paragraph("Sortieren", style=section_title)

p4 = [
    "Verschiedene Arten von Kunststoffen haben unterschiedliche Eigenschaften. PPL achtet darauf, dass bei der Verarbeitung und ",
    "Herstellung von Produkten keine Kunststoffarten vermischt werden. Bei Objekten, bei denen die Art des Kunststoffs nicht ",
    "eindeutig angegeben ist, verwendet PPL die FTIR-Technologie zur Unterscheidung der Kunststoffarten."
]

p5 = [
    "Bei einer Untersuchung des Ufer-Abfallaufkommens stösst man auf eine Vielzahl von Kunststoffen. Nicht alles davon ",
    "kann in Produkte mit Mehrwert umgewandelt werden. Durch die Identifizierung und Gruppierung der Kunststoffe nach ",
    "ihrer Art kann PPL Objekte herstellen, die am besten zu den Eigenschaften des verwendeten Kunststoffs passen."
]

p1_2 = sectionParagraphs([p1, p2], smallspace=smallest_space)
p4 = makeAParagraph(p4)
p5 = makeAParagraph(p5)
l1 = makeAList(l1)
p3 = makeAParagraph(p3)

o_w, o_h = convertPixelToCm("resources/images/reuse_recycle/machine.jpeg")
f1caption = makeAParagraph(["Identifizierung von Kunststoffen aus Ufer-Abfallaufkommen-Untersuchungen"], style=caption_style)
figure_kwargs = {
    "image_file":"resources/images/reuse_recycle/machine.jpeg",
    "caption": f1caption, 
    "original_width":o_w,
    "original_height":o_h,
    "desired_width": 8,
    "caption_height":.75,
    "hAlign": "CENTER",
}

f1 = figureAndCaptionTable(**figure_kwargs)

colWidths=[8.1*cm, 8.1*cm]

table_data = [
    [[sect1_t, small_space, p4, small_space, p5], f1]
]
f1_text = Table(table_data, style=featuredata.side_by_side_style_figure_right, colWidths=colWidths)



new_components = [
    chapter_title,
    large_space,
    *p1_2,
    l1,
    smallest_space,
    p3,
    small_space,
    f1_text
   
]

pdfcomponents = addToDoc(new_components, pdfcomponents)


# ### Polyethylenterephthalat (PET)
# 
# Das meiste PET, das während des Probenahmezeitraums gefunden wurde, lag in Form von Getränkeflaschen und Lebensmittelbehältern vor. Der grösste Teil der weltweiten Produktion von PET wird jedoch zur Herstellung von Fasern verwendet. PET ist für das derzeitige Herstellungsverfahren bei PPL nicht gut geeignet und wird daher nicht verwendet.
# 
# Nur 88 PET-Getränkeflaschen wurden in den Jahren 2020–2021 landesweit entlang der Datenerhebungen des Wassersystems erfasst.
# 
# ### Polyethylen hoher Dichte (HDPE2)
# 
# HDPE2 hat ein hohes Verhältnis von Festigkeit zu Dichte und funktioniert gut im PPL-System. HDPE2 hat die Form vieler Objekte, die bei Datenerhebungen identifiziert wurden:
# 
# * Flaschendeckel
# * bestimmte Getränkebehälter
# * Behälter für Reinigungsmittel und Chemikalien
# * Spielzeug
# 
# Zusammengenommen hätten mindestens 4 % aller Objekte als HDPE klassifiziert werden können. Aus diesen Objekten stellt PPL Schlüsselanhänger, Blumentöpfe und Karabiner her.

# In[3]:


subsect1 = Paragraph("Polyethylenterephthalat (PET)", style=subsection_title)

p6 = [
    "Das meiste PET, das während des Probenahmezeitraums gefunden wurde, lag in Form von Getränkeflaschen und Lebensmittelbehältern ",
    "vor. Der grösste Teil der weltweiten Produktion von PET wird jedoch zur Herstellung von Fasern verwendet. PET ist für das ",
    "derzeitige Herstellungsverfahren bei PPL nicht gut geeignet und wird daher nicht verwendet."
]

p7 = [
    "Nur 88 PET-Getränkeflaschen wurden in den Jahren 2020–2021 landesweit entlang der Datenerhebungen des Wassersystems erfasst."
]

subsect2 = Paragraph("Polyethylen hoher Dichte (HDPE2)", style=subsection_title)

p8 = [
    "HDPE2 hat ein hohes Verhältnis von Festigkeit zu Dichte und funktioniert gut im PPL-System. HDPE2 hat die Form vieler Objekte, die bei Datenerhebungen identifiziert wurden:"
]

l2 = [
    "Flaschendeckel",
    "bestimmte Getränkebehälter",
    "Behälter für Reinigungsmittel und Chemikalien",
    "Spielzeug"
]

p9 = [
    "Zusammengenommen hätten mindestens 4 % aller Objekte als HDPE klassifiziert werden können. Aus diesen Objekten stellt PPL Schlüsselanhänger, Blumentöpfe und Karabiner her."
]

p6_7 = sectionParagraphs([p6, p7], smallspace=smallest_space)
p8 = makeAParagraph(p8)
l2 = makeAList(l2)
p9 = makeAParagraph(p9)


new_components = [
    subsect1,
    small_space,
    *p6_7,
    subsect2,
    small_space,
    p8,
    smallest_space,
    l2,
    smallest_space,
    p9  
   
]

pdfcomponents = addToDoc(new_components, pdfcomponents)


# ### Polyvinylchlorid (PVC3)
# 
# PVC3 ist ein gängiges Material für Kunststoffe im Bauwesen. Baukunststoffe gehören zu den am häufigsten verwendeten Objekten am Genfersee und im ganzen Land. Leider ist dieses Produkt bei unsachgemässer Handhabung giftig. PPL recycelt dieses Material nicht.
# 
# Bauabfälle aus Kunststoff wurden in 52 % aller Proben identifiziert und machten mindestens 2 % aller identifizierten Objekte aus.
# 
# ### Polyethylen niedriger Dichte (LDPE4)
# 
# LDPE4 wird in der Regel nicht recycelt, da es entweder nicht gekennzeichnet oder sehr schwer zu reinigen ist. LDPE4 wird oft unter Industriefolien oder Dünnschicht-Plastiksäcken eingeordnet.
# 
# Industriefilme wurden in 69 % aller Proben gefunden und waren mindestens 4 % aller identifizierten Objekte.
# 
# ### Polypropylen (PP5)
# PP5 nimmt verschiedene Formen an, wenn es an Gewässern gefunden wird. PP5 kann in Chipstüten, Eimern, Medizinflaschen, Strohhalmen und Kunststoffseilen verwendet werden.
# 
# PPL hat viele Verwendungsmöglichkeiten für PP5 gefunden, darunter Töpfe, Wanduhren, Frisbees und Schlüsselanhänger.
# 
# PP55 steht für eine grosse Gruppe von Abfallobjekten an Gewässern. Kombiniert mit fragmentierten Kunststoffen steht PPL für ca. 30–40 % aller gefundenen Objekte und wurde in 98 % der Datenerhebungen identifiziert.
# 
# ### Polystyrol (PS6)
# 
# PS6 wurde bei fast allen Proben entweder in extrudiertem oder geschäumtem Kunststoff gefunden. PS6 kann von PPL zu starren Platten recycelt werden, die eine feine Politur erhalten. Dazu werden zwei Arten von Polystyrol verwendet: expandiert und extrudiert.
# 
# Expandiertes und extrudiertes Polystyrol wurde in 68 % bzw. 53 % aller Proben identifiziert. Zusammengenommen sind sie für mindestens 13 % aller identifizierten Objekte verantwortlich.
# 
# ### Acrylnitril-Butadien-Styrol (ABS)
# 
# ABS ist leicht und kann spritzgegossen oder extrudiert werden. PPL verwendet ABS und hochschlagfestes Polystyrol (HIPS) zur Herstellung von starren, recycelten Platten.
# 
# ABS wird bei der Inventarisierung mit den Konstruktionskunststoffen mitgerechnet.

# In[4]:


subsect3 = Paragraph("Polyvinlychlorid (PVC3)", style=subsection_title)

p10 = [
    "PVC3 ist ein gängiges Material für Kunststoffe im Bauwesen. Baukunststoffe gehören zu den am häufigsten verwendeten Objekten am Genfersee und im ganzen ",
    "Land. Leider ist dieses Produkt bei unsachgemässer Handhabung giftig. PPL recycelt dieses Material nicht."
]

p11 = [
    "Bauabfälle aus Kunststoff wurden in 52 % aller Proben identifiziert und machten mindestens 2 % aller identifizierten Objekte aus."
]

p10_11 = sectionParagraphs([p10, p11], smallspace=smallest_space)

subsect4 = Paragraph("Polyethylen niedriger Dichte (LDPE4)", style=subsection_title)

p12 = [
    "LDPE4 wird in der Regel nicht recycelt, da es entweder nicht gekennzeichnet oder sehr schwer zu reinigen ist. LDPE4 wird oft unter Industriefolien oder Dünnschicht-Plastiksäcken eingeordnet."
]

p13 = [
    "Industriefilme wurden in 69 % aller Proben gefunden und waren mindestens 4 % aller identifizierten Objekte."
]

p12_13 = sectionParagraphs([p12, p13], smallspace=smallest_space)

subsect5 = Paragraph("Polypropylen (PP5)", style=subsection_title)

p14 = [
    "PP5 nimmt verschiedene Formen an, wenn es an Gewässern gefunden wird. PP5 kann in Chipstüten, Eimern, Medizinflaschen, Strohhalmen und Kunststoffseilen verwendet werden."
]

p15 = [
    "PPL hat viele Verwendungsmöglichkeiten für PP5 gefunden, darunter Töpfe, Wanduhren, Frisbees und Schlüsselanhänger."
]

p16 = [
    "PP55 steht für eine grosse Gruppe von Abfallobjekten an Gewässern. Kombiniert mit fragmentierten Kunststoffen steht ",
    "PPL für ca. 30–40 % aller gefundenen Objekte und wurde in 98 % der Datenerhebungen identifiziert."
]

p14_16 = sectionParagraphs([p14, p15, p16], smallspace=smallest_space)

subsect6 = Paragraph("Polystyrol (PS6)", style=subsection_title)

p17 =[
    "PS6 wurde bei fast allen Proben entweder in extrudiertem oder geschäumtem Kunststoff gefunden. PS6 kann von PPL zu starren Platten ",
    "recycelt werden, die eine feine Politur erhalten. Dazu werden zwei Arten von Polystyrol verwendet: expandiert und extrudiert."
]

p18 = [
    "Expandiertes und extrudiertes Polystyrol wurde in 68 % bzw. 53 % aller Proben identifiziert. Zusammengenommen sind sie für mindestens 13 % aller identifizierten Objekte verantwortlich."
]

p17_18 = sectionParagraphs([p17, p18], smallspace=smallest_space)

subsect7 = Paragraph("Acrylnitril-Butadien-Styrol (ABS)", style=subsection_title)

p19 = [
    "ABS ist leicht und kann spritzgegossen oder extrudiert werden. PPL verwendet ABS und hochschlagfestes Polystyrol (HIPS) zur Herstellung von starren, recycelten Platten."
]

p20 = [
    "ABS wird bei der Inventarisierung mit den Konstruktionskunststoffen mitgerechnet."
]

p19_20 = sectionParagraphs([p19, p20], smallspace=smallest_space)



new_components = [
    small_space,
    subsect3,
    small_space,
    *p10_11,
    small_space,
    subsect4,
    small_space,
    *p12_13,
    small_space,
    subsect5,
    small_space,
    *p14_16,
    small_space,
    subsect6,
    small_space,
    *p17_18,
    small_space,
    subsect7,
    small_space,
    *p19_20  
   
]

pdfcomponents = addToDoc(new_components, pdfcomponents)


# ## Reinigung

# ```{figure} resources/images/reuse_recycle/sampleplastics.jpeg
# ---
# name: sampled_plastics
# ---
# ` ` 
# ```
# {numref}`Abbildung %s: <sampled_plastics>` Bei der Probenahme gesammelte Objekte

# Sobald die Objekte identifiziert und sortiert sind, müssen sie gereinigt werden, bevor eine Umwandlung erfolgen kann. PPL verwendete eine Kombination aus Backpulver und Essig mit Wasser, um Schlamm und Schmutz von den an Gewässern gesammelten Objekten zu entfernen.

# ```{figure} resources/images/reuse_recycle/cleaning.jpeg
# ---
# name: cleaning_plastics
# ---
# ` ` 
# ```
# {numref}`Abbildung %s: <cleaning_plastics>` Probenmaterial schrubben und einweichen

# ```{figure} resources/images/reuse_recycle/cleaning1.jpeg
# ---
# name: cleaning_plastics1
# ---
# ` ` 
# ```
# {numref}`Abbildung %s: <cleaning_plastics1>` Nach einer Einweichzeit von 12 Stunden werden die Objekte von Hand gebürstet und zum Trocknen ausgelegt.

# In[5]:


sect2 = Paragraph("Reinigung", style=section_title)

p22 = [
    "Sobald die Objekte identifiziert und sortiert sind, müssen sie gereinigt werden, bevor eine Umwandlung erfolgen kann. ",
    "PPL verwendete eine Kombination aus Backpulver und Essig mit Wasser, um Schlamm und Schmutz von den an ",
    "Gewässern gesammelten Objekten zu entfernen."
]

p22 = makeAParagraph(p22)

o_w, o_h = convertPixelToCm("resources/images/reuse_recycle/sampleplastics.jpeg")
f2caption = makeAParagraph("Bei der Probenahme gesammelte Objekte", style=caption_style)
figure_kwargs = {
    "image_file":"resources/images/reuse_recycle/sampleplastics.jpeg",
    "caption": f2caption, 
    "original_width":o_w,
    "original_height":o_h,
    "desired_width": 8,
    "caption_height":.5,
    "hAlign": "CENTER",
}

f2 = figureAndCaptionTable(**figure_kwargs)



o_w, o_h = convertPixelToCm("resources/images/reuse_recycle/cleaning.jpeg")
f3caption = makeAParagraph("Probenmaterial schrubben und einweichen", style=caption_style)
figure_kwargs = {
    "image_file":"resources/images/reuse_recycle/cleaning.jpeg",
    "caption": f3caption, 
    "original_width":o_w,
    "original_height":o_h,
    "desired_width": 8,
    "caption_height":.5,
    "hAlign": "CENTER",
}

f3 = figureAndCaptionTable(**figure_kwargs)

o_w, o_h = convertPixelToCm("resources/images/reuse_recycle/cleaning1.jpeg")
f4caption = makeAParagraph("Nach einer Einweichzeit von 12 Stunden werden die Objekte von Hand gebürstet und zum Trocknen ausgelegt.", style=caption_style)
figure_kwargs = {
    "image_file":"resources/images/reuse_recycle/cleaning1.jpeg",
    "caption": f4caption, 
    "original_width":o_w,
    "original_height":o_h,
    "desired_width": 8,
    "caption_height":.75,
    "hAlign": "CENTER",
}

f4 = figureAndCaptionTable(**figure_kwargs)

colWidths=[8.1*cm, 8.1*cm]

table_data = [
    [ [f2, f3],[sect2, small_space, p22, small_space, f4]]
]
f2_text = Table(table_data, style=featuredata.side_by_side_style_figure_right, colWidths=colWidths)

new_components = [
    PageBreak(),
    f2_text   
]

pdfcomponents = addToDoc(new_components, pdfcomponents)


# ## Transformieren
# Die gereinigten, sortierten und getrockneten Kunststoffe werden zu Granulat zerkleinert, das im Spritzgussverfahren verarbeitet wird.

# ```{figure} resources/images/reuse_recycle/granulate.jpeg
# ---
# name: granulate
# ---
# ` ` 
# ```
# {numref}`Abbildung %s: <cleaning_plastics1>` Zu Granulat verarbeitete Kunststoffe für die Produktion.

# In[6]:


sect3 = Paragraph("Transformieren", style=section_title)

p23 = [
    "Die gereinigten, sortierten und getrockneten Kunststoffe werden zu Granulat zerkleinert, das im Spritzgussverfahren verarbeitet wird."
]

p23 = makeAParagraph(p23)

o_w, o_h = convertPixelToCm("resources/images/reuse_recycle/granulate.jpeg")
f5caption = makeAParagraph("Zu Granulat verarbeitete Kunststoffe für die Produktion.", style=caption_style)
figure_kwargs = {
    "image_file":"resources/images/reuse_recycle/granulate.jpeg",
    "caption": None, 
    "original_width":o_w,
    "original_height":o_h,
    "desired_width": 8,
    "caption_height":0,
    "hAlign": "CENTER",
}

f5 = figureAndCaptionTable(**figure_kwargs)

colWidths=[8.1*cm, 8.1*cm]

table_data = [
    [[sect3, small_space, p23, small_space, f5caption], f5]
]
f5_text = Table(table_data, style=featuredata.side_by_side_style_figure_right, colWidths=colWidths)

new_components = [
    large_space,
    f5_text   
]

pdfcomponents = addToDoc(new_components, pdfcomponents)


# ## Herstellung
# 
# PP5 und HDPE2 sind die am häufigsten vorkommenden Objekte aus den Abfallobjekten und funktionieren gut mit dem PPL-System. Aus den Kunststoffen am Genfersee wurden zwei Arten von Produkten hergestellt.

# ```{figure} resources/images/reuse_recycle/carabiniers.jpeg
# ---
# name: carabiners
# ---
# ` ` 
# ```
# {numref}`Abbildung %s: <carabiners>` Karabiner.

# ```{figure} resources/images/reuse_recycle/flowerpot.jpeg
# ---
# name: flowerpot
# ---
# ` ` 
# ```
# {numref}`Abbildung %s: <flowerpot>` Blumentöpfe 

# In[7]:


sect4 = Paragraph("Hersellung", style=section_title)

p24 = [
    "PP5 und HDPE2 sind die am häufigsten vorkommenden Objekte aus den Abfallobjekten und funktionieren gut mit dem PPL-System. ",
    "Aus den Kunststoffen am Genfersee wurden zwei Arten von Produkten hergestellt."
]

p24 = makeAParagraph(p24)

o_w, o_h = convertPixelToCm("resources/images/reuse_recycle/carabiniers.jpeg")
f6caption = makeAParagraph("Karabiner", style=caption_style)
figure_kwargs = {
    "image_file":"resources/images/reuse_recycle/carabiniers.jpeg",
    "caption": f6caption, 
    "original_width":o_w,
    "original_height":o_h,
    "desired_width": 8,
    "caption_height":.5,
    "hAlign": "CENTER",
}

f6 = figureAndCaptionTable(**figure_kwargs)

o_w, o_h = convertPixelToCm("resources/images/reuse_recycle/flowerpot.jpeg")
f7caption = makeAParagraph("Blumentöpfe", style=caption_style)
figure_kwargs = {
    "image_file":"resources/images/reuse_recycle/flowerpot.jpeg",
    "caption": f7caption, 
    "original_width":o_w,
    "original_height":o_h,
    "desired_width": 8,
    "caption_height":.5,
    "hAlign": "CENTER",
}

f7 = figureAndCaptionTable(**figure_kwargs)

colWidths=[8.1*cm, 8.1*cm]

table_data = [
    [f6,f7]
]
f7_text = Table(table_data, style=featuredata.side_by_side_style_figure_right, colWidths=colWidths)


new_components = [
    PageBreak(),
    sect4,
    small_space,
    p24,
    small_space,
    f7_text   
]

pdfcomponents = addToDoc(new_components, pdfcomponents)


# ## Diskussion
# 
# In der Mehrzahl der gesammelten Proben wurden wiederverwendbare Kunststoffe gefunden. Polypropylen, HDPE, PS6 und LDPE waren die wichtigsten identifizierten Polymere. Fragmentierte Kunststoffe, Schaumstoffe und Flaschenverschlüsse können alle vor Ort mit den bei Precious Plastic angewandten Methoden recycelt werden.
# 
# Die weggeworfenen Objekte erforderten einen wesentlich höheren Reinigungsaufwand als das Material, an das PPL gewöhnt ist. Die Reinigung von gebrauchten Kunststoffprodukten ist ein grosser Kostenfaktor in der Recyclingindustrie, und PPL ist da keine Ausnahme. Grosse Recyclinganlagen verfügen über Wasseraufbereitungsanlagen, um die Reinigungsmittel und Verunreinigungen zu entfernen, die beim Reinigungsprozess entstehen. PPL verwendet Backpulver und Essig, wodurch die Gesamtmenge an Wasser reduziert und die Verwendung von Reinigungsmitteln, die sich negativ auf die Umwelt auswirken können, vermieden wird. Diese Methode eignet sich für sehr kleine Produktionsmengen, ist aber arbeitsaufwändig.
# 
# Solange die Reinigungs- und Sortierprozesse ordnungsgemäss durchgeführt wurden, gab es keine Qualitätseinbussen bei den hergestellten Produkten. Die gesammelten Abfallobjekten reichen nicht aus, um irgendeine Art von Produktionskapazität aufrechtzuerhalten. Es gibt jedoch eine Fülle von recycelbaren Kunststoffen, die in die Umwelt gelangen.
# 
# Das Vorhandensein von leicht wiederverwertbaren Produkten im Wasser bedeutet, dass Gelegenheiten verpasst werden, diese Ressourcen wertzuschätzen. Zusammen mit der Vielzahl von Objekten, die aus PP5 hergestellt sind, macht die geschätzte Anzahl der an Gewässern gesammelten wiederverwertbaren Objekte 40–50 % der Gesamtmenge der gesammelten Objekte aus.
# 
# Diese Ergebnisse sind nicht spezifisch für eine bestimmte Region und charakterisieren bis zu einem gewissen Grad die Situation in allen Erhebungsgebieten des IQAASL-Projekts.

# ```{figure} resources/images/reuse_recycle/20201122walenstadtPPL.jpeg
# ---
# name: martin
# ---
# ` ` 
# ```
# {numref}`Abbildung %s: <martin>` Strand-Abfallaufkommen Untersuchung, 22.11.202, Walenstadt, Walensee

# In[8]:


lastsec = Paragraph("Diskussion", style=section_title)

p25 = [
    "In der Mehrzahl der gesammelten Proben wurden wiederverwendbare Kunststoffe gefunden. Polypropylen, HDPE, PS6 und LDPE ",
    "waren die wichtigsten identifizierten Polymere. Fragmentierte Kunststoffe, Schaumstoffe und Flaschenverschlüsse können ",
    "alle vor Ort mit den bei Precious Plastic angewandten Methoden recycelt werden."
]

p26 = [
    "Die weggeworfenen Objekte erforderten einen wesentlich höheren Reinigungsaufwand als das Material, an das PPL gewöhnt ist. ",
    "Die Reinigung von gebrauchten Kunststoffprodukten ist ein grosser Kostenfaktor in der Recyclingindustrie, und PPL ist da ",
    "keine Ausnahme. Grosse Recyclinganlagen verfügen über Wasseraufbereitungsanlagen, um die Reinigungsmittel und Verunreinigungen ",
    "zu entfernen, die beim Reinigungsprozess entstehen. PPL verwendet Backpulver und Essig, wodurch die Gesamtmenge an Wasser ",
    "reduziert und die Verwendung von Reinigungsmitteln, die sich negativ auf die Umwelt auswirken können, vermieden wird. Diese ",
    "Methode eignet sich für sehr kleine Produktionsmengen, ist aber arbeitsaufwändig."
]

p27 = [
    "Solange die Reinigungs- und Sortierprozesse ordnungsgemäss durchgeführt wurden, gab es keine Qualitätseinbussen bei den ",
    "hergestellten Produkten. Die gesammelten Abfallobjekten reichen nicht aus, um irgendeine Art von Produktionskapazität ",
    "aufrechtzuerhalten. Es gibt jedoch eine Fülle von recycelbaren Kunststoffen, die in die Umwelt gelangen."
]

p28 = [
    "Das Vorhandensein von leicht wiederverwertbaren Produkten im Wasser bedeutet, dass Gelegenheiten verpasst werden, diese ",
    "Ressourcen wertzuschätzen. Zusammen mit der Vielzahl von Objekten, die aus PP5 hergestellt sind, macht die geschätzte Anzahl ",
    "der an Gewässern gesammelten wiederverwertbaren Objekte 40–50 % der Gesamtmenge der gesammelten Objekte aus."
]

p29 = [
    "Diese Ergebnisse sind nicht spezifisch für eine bestimmte Region und charakterisieren bis zu einem gewissen Grad die Situation in allen Erhebungsgebieten des IQAASL-Projekts."
]

p25_29 = sectionParagraphs([p25, p26, p27, p28, p29], smallspace=smallest_space)

new_components = [
    small_space,
    lastsec,
    small_space,
    *p25_29,
       
]

pdfcomponents = addToDoc(new_components, pdfcomponents)


# In[9]:


doc = SimpleDocTemplate("resources/pdfs/recycle_remake.pdf", pagesize=A4, leftMargin=2.5*cm, rightMargin=2.5*cm, topMargin=2.5*cm, bottomMargin=1.5*cm)
pageinfo= f"IQAASL/Anwendungen/Recyceln und neugestalten"

source_prefix = "https://hammerdirt-analyst.github.io/IQAASL-End-0f-Sampling-2021/"
source = "shared_responsibility.html"

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




