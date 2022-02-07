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

from PIL import Image as PILImage
from IPython.display import Markdown as md
from IPython.display import display
import matplotlib.image as mpimg

# home brew utitilties
import resources.sr_ut as sut
import resources.chart_kwargs as ck

# when setting the code group names the defintions
# are pushed to .JSON format
def push_this_to_json(filename="", data=[]):
    with open(filename, "w") as a_file:
        json.dump(data, a_file)


# (codegroupsde)=
# # Code-Gruppen
# 
# <a href="code_groups.html"> English </a>
# 
# Das IQAASL-Projekt verwendete die Objektcodes und Beschreibungen aus der Masterliste des Marine Strategy Framework (MSFD) {cite}`mlwguidance`. Die Identifizierung von Gegenständen folgt den Protokollen der MSFD Technical Subgroup on Marine Litter. Die Hauptliste wurde auf der Grundlage der in einer Reihe von Programmen verwendeten Kategorien von Gegenständen entwickelt und ist eine der detailliertesten, die etablierte EU-Protokolle repräsentiert. Es gibt 217 Identifikationscodes, um alle bei einer Erhebung gesammelten Gegenstände zu klassifizieren. Die Objektcodes beginnen mit G1 und enden mit G217. 
# 
# ## Buchhaltung für regionale Objekte
# 
# Es gibt in der Schweiz regelmäßig identifizierte Artikel, die nicht in der Stammliste erscheinen. Um dies zu berücksichtigen, wurden der Masterliste 43 Codes unter dem übergeordneten Code G124 hinzugefügt. Diese Codes beginnen mit G900 und enden mit G999. 
# 
# Einige MSFD-Codes wie G124 Sonstige Artikel aus Kunststoff/Polystyrol, identifizierbar ermöglichen die Quantifizierung von nicht aufgelisteten identifizierbaren Kunststoffartikeln. Ein zusätzlicher Artikel wie G913 Schnuller kann unabhängig quantifiziert und mit dem MSFD-Code G124 verknüpft werden. Diese Arbeit wird auf dem Server erledigt und die Daten können in beiden Formen analysiert werden. 
# 
# Identifizierbare Kunststoffgegenstände wurden entweder einem zusätzlichen Code wie G913 zugeordnet, oder wenn kein anderer Code den Gegenstand beschrieb, wurde G124 verwendet. Einige Codes wurden aufgenommen, um pandemiebezogene Artikel zu erfassen, wie z.B.: 
# 
# * G901: Maske medizinisch, synthetisch, übergeordneter Code = G124: andere Artikel aus  Kunststoff/Polystyrol identifizierbar 
# 
# * G902: Maske medizinisch, Stoff, übergeordneter Code = G145: andere Textilien 
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
dfCodes["material"] = dfCodes.material.map(lambda x: sut.mat_ge[x])

# translate the code groups and columns to local
dfCodes["groupname"] = dfCodes["groupname"].map(lambda x: sut.group_names_de[x])

# rename the columns
new_names = {"description":"Objekte", "groupname":"Gruppenname", "material":"Material", "Parent code":"pc"}
dfCodes.rename(columns=new_names, inplace=True)

# the columns to display
cols_to_display = list(new_names.values())

dfCodes.loc[["G124", "G902", "G145","G937"]][cols_to_display]


# ### Modifikation von Artikeln nach Größe und Materialbeschreibungen
# 
# Der IQAASL-Bericht enthält mehrere wichtige Größen- und Materialänderungen in den Kategorien zerbrochener Kunststoff und Schaumstoff. Andere Änderungen umfassen die Erweiterung oder Einschränkung von Artikelbeschreibungen.
# 
# Zum Beispiel: 
# 
# * G96 Damenbinden, Slipeinlagen, die so verändert wurden, dass sie Tampon-Applikatoren aus Kunststoff enthalten. 
# * G211 Klebebandagen, geändert von nicht klassifiziertem Material in Kunststoff. 
# Um Mikrokunststoffe für dieses Projekt bestmöglich zu identifizieren und zu quantifizieren, wurden 3 Codes aus der Masterliste nach Größe modifiziert. Codes geändert, um Objekte mit einer Größe von weniger als 5 mm zu berücksichtigen: 
# 
# * G75 Kunststoff-/Polystyrolstücke 0 - 2,5 cm modifiziert auf 0,5 cm - 2,5 cm 
# * G78 Kunststoffteile 0 - 2,5cm modifiziert auf 0,5cm - 2,5cm 
# * G81 Polystyrolstücke 0 - 2,5 cm modifiziert auf 0,5 cm - 2,5 cm

# In[3]:


sut.display_image_ipython("resources/images/codegroups/20200819_080041.jpg", thumb=(700,1100), rotate=0)


# *__Oben:__ Plastikteile in verschiedenen Größen*

# In[4]:


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


# ### Gfoams: Geschäumte Kunststoffe, GSchaumstoffe
# 
# Expandiertes Polystyrol G81, G82, G83, zusammengefasst als Gfoam, sind leichte, mürbe, oft weiße Schaumstoffe, die für Verpackungen oder zur Isolierung verwendet werden. Geschäumte Kunststoffartikel, die üblicherweise für Lebensmittel zum Mitnehmen G10, Schwammschäume G73 und dichtere Isolierschäume G74 verwendet werden, werden separat kategorisiert und sind nicht in der Gruppe des expandierten Polystyrols enthalten. 
# 
# Der Verpackungsschaumstoff/Isolierschaumstoff/Polyurethan G74 wurde in dieser Studie um extrudierte Polystyrole (XPS) erweitert, die üblicherweise als Isoliermaterial verwendet werden, und umgekehrt für G81, G82 und G83 Polystyrolstücke auf expandiertes Polystyrol (EPS) größer als 0,5 cm eingegrenzt. Mit diesen Änderungen sollten Isolierschaumstoffe von Verpackungsschaumstoffen unterschieden werden, obwohl beide für eine Vielzahl von Anwendungen verwendet werden. Die Materialänderungen an den geschäumten Kunststoffen werden für die Analyse zum übergeordneten Code zusammengefasst und separat erfasst. Ein detailliertes Verzeichnis der Art und Größe des Schaumstoffs wird mit jedem Bericht geliefert. 
# 
# :::{note}
# Polystyrolkügelchen unter 5 mm, Markenname Styrofoam® sind mit Mikrokunststoffen (G117) Styropor < 5 mm gruppiert.
# :::

# In[5]:


wwcodes = dfCodes.loc[["G81", "G82", "G83"]][cols_to_display]
wwcodes


# In[6]:


sut.display_image_ipython("resources/images/codegroups/20210221CheyresFoam.jpg", thumb=(600,1000), rotate=360)


# *__Oben:__ Verschiedene Größen von weißem expandiertem Polystyrol und anderen Schaumstoffen*

# ### Nicht anwendbar oder ausgelassene Punkte
# 
# Von den 217 verfügbaren MSFD-Codes wurden 176 in den Erhebungen 2020-2021 identifiziert. Mehrere Punkte sind nicht auf Schweizer Gewässer anwendbar, da sie sich auf die marine Aquakulturproduktion beziehen: 
# 
# * G207 Oktopus-Töpfe 
# * G163 Krabben- und Hummerkörbe 
# * G215 Lebensmittelabfälle/Getränkeabfälle*
# 
# *__Unten:__ Alle natürlich biologisch abbaubaren Lebensmittelabfälle sowie die Sammlung und Quantifizierung von Fäkalien wurden bei diesem Projekt ausgelassen.*

# In[7]:


sut.display_image_ipython("resources/images/codegroups/petite_plage_yverdon_lesBains15_02_2021.png", thumb=(800,1200), rotate=0)


# ## Objekte gruppiert nach Nutzen 
# 
# Der Nutzen basiert auf der Nutzung des Objekts, bevor es weggeworfen wurde, oder auf der Artikelbeschreibung, wenn die ursprüngliche Nutzung unbestimmt ist. Identifizierte Objekte werden in einen der vordefinierten Kategoriecodes eingeordnet. Diese einzelnen Artikelcodes wurden gruppiert, um die Verwendung oder die Materialart für diesen Bericht bestmöglich zu beschreiben. Die Gruppierung der Codes ist eine breit angelegte Analysemethode, um die in den Wassersystemen gefundenen weggeworfenen Materialien nach Wirtschaftszweigen oder physikalischen Eigenschaften zu bewerten. Die Gegenstände werden in diesem Bericht auch unabhängig voneinander analysiert. Die Gruppierung wurde aus Feldbeobachtungen und Untersuchungen abgeleitet, um mögliche Quellen für verschiedene Schadstoffe zu ermitteln.
# 
# * __Abwasser:__ Gegenstände, die aus Kläranlagen freigesetzt werden, einschließlich Gegenstände, die wahrscheinlich mit der Toilette gespült werden
# * __Mikrokunststoffe:__ (< 5mm): zersplitterte Kunststoffe, geschäumte Kunststoffe und Kunststoffharze für die Vorproduktion  
# * __Infrastruktur:__ Posten im Zusammenhang mit dem Bau und der Instandhaltung von Gebäuden, Straßen und der Wasser-/Stromversorgung 
# * __Essen und Trinken:__ alle Materialien, die mit dem Konsum von Essen und Trinken zu tun haben 
# * __Landwirtschaft:__ hauptsächlich industrielle Folien, z.B. Mulch und Reihenabdeckungen, Gewächshäuser, Bodenbegasung, Ballenverpackungen. Einschließlich Hartkunststoffe für landwirtschaftliche Zäune, Blumentöpfe usw. 
# * __Tabak:__ hauptsächlich Zigarettenfilter, einschließlich aller mit dem Rauchen verbundenen Materialien 
# * __Erholung:__ Objekte, die mit Sport und Freizeit zu tun haben, z. B. Angeln, Jagen, Wandern usw. 
# * __Verpackungen, die nicht für Lebensmittel und Getränke bestimmt sind:__ Verpackungsmaterial, das nicht als Lebensmittel, Getränke oder Tabakwaren gekennzeichnet ist
# * __Kunststoffteile (> 5mm):__ zersplitterte Kunststoffe unbestimmter Herkunft oder Verwendung  
# * __Persönliche Gegenstände:__ Accessoires, Hygieneartikel und Kleidung 
# * __Nicht klassifiziert:__ nicht gruppierte Artikelcodes

# In[8]:


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
plt.show()


# *__Oben:__ Objekte gruppiert nach Nutzen*

# ### Abwasserbehandlung 
# 
# Zu den Codes für die Abwasserbehandlung gehören Biomassehalter, die in Abfallbehandlungsprozessen verwendet werden, sowie wahrscheinliche Toilettenspülungen wie Wattestäbchen.  
# 
# :::{note}
# G98 umfasst Windeln und Feuchttücher. Windeln werden in den Schweizer Wassersystemen nur selten gefunden, die Mengen sollten den Körperpflegetüchern zugeordnet werden. 
# :::

# In[9]:


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
wwcodes 


# ### Micro plastics 
# 
# Die Gruppe der Mikrokunststoffe umfasst alle Kunststoffe und geschäumten Kunststoffe mit einer Größe von weniger als 5 mm aus der (MSFD)-Stammliste  {cite}`mlwguidance` der Positionen G103-G123. In unseren Daten sind nicht alle Codes identifiziert worden. Das Ziel dieses Projekts war die Quantifizierung der beobachtbaren Abfälle, die in der Regel größer als 5 mm sind, aber die untere Grenze der natürlichen sichtbaren Erkennung bei der Vermessung einer Küstenlinie liegt bei etwa 2 - 5 mm. Im Laufe einer Untersuchung werden mit dem größeren Material auch sichtbare Kleinstteile gesammelt, deren Zusammensetzung im Allgemeinen identifizierbar ist. Im Rahmen des IQAASL-Projekts wurden keine Methoden zur gezielten Erfassung von Objekten mit einer Größe von weniger als 5 mm eingesetzt, aber alle sichtbaren Mikrokunststoffe, die während einer Untersuchung gesammelt wurden, wurden quantifiziert, gewogen und kategorisiert.

# In[10]:


# define group
codesmicro=["G112", "G106", "G117", "G103", "G104", "G105", "G107", "G108", "G109", "G110", "G111", "G113", "G114", "G115", "G116", "G118", "G119", "G120", "G121", "G122", "G123"]

# make table
wwcodes = dfCodes.loc[codesmicro][cols_to_display]
wwcodes


# ### Infrastructure 
# 
# Infrastruktur bezieht sich auf alle Formen des Baus, der Renovierung und der Instandhaltung von öffentlichen und privaten Bauwerken, einschließlich Straßen, Brücken und Häfen sowie der Strom- und Wasserversorgung. Entlang aller untersuchten Seen wurden bedeutende Mengen an Baukunststoffen und insbesondere an geschäumten Kunststoffen festgestellt. Siehe Erhebungsergebnisses 2020-2021 [Alle Erhebungen](allsurveysde)
# 
# Gängige Kunststoffe im Bauwesen sind Rohrstücke, Kabelschutzvorrichtungen, flexible und starre Schläuche sowie die dazugehörigen Verbindungsstücke, Armaturen und Abdeckungen. Kunststoffe, die bei der Betonherstellung verwendet werden, wie Dübel, Anker und Abstandshalter, wurden ebenfalls häufig identifiziert. Einige Artikel, die mit Kunststoffen im Bauwesen in Verbindung gebracht werden, haben eindeutige Codes wie G93: Kabelbinder oder G17: Behälter für Injektionspistolen. 
# 
# Andere Elemente in der Gruppe Infrastruktur haben einen allgemeineren Anwendungsfall: 
# 
# * G186 Industrieschrott 
# * G194 Metallkabel 

# ####  Infrastruktur: geschäumter Kunststoff¶ 
# 
# Alle geschäumten Kunststoffe, die mit Isolieranwendungen in Verbindung gebracht werden, werden der Gruppe Infrastruktur zugeordnet. Extrudierte Schaumstoffe sind relativ dichte mehrfarbige Schaumstoffplatten und Sprühschäume, die größer als 0,5 cm sind. Expandiertes Polystyrol wird aufgrund der häufigen Verwendung als Außenisolierung für oberirdische Anwendungen als Infrastruktur eingestuft. Zusätzliche Codes wurden geschaffen, um Größenvariationen von Schaumstoffen zu quantifizieren, G909 - G912. Die Änderungen in der Materialbeschreibung zielen darauf ab, Schaumstoffe zur Bauisolierung von Verpackungsschaumstoffen zu unterscheiden, obwohl beide für eine Vielzahl von Anwendungen verwendet werden. Die Materialänderungen an den geschäumten Kunststoffen werden für die Analyse unter dem übergeordneten Code zusammengefasst und separat erfasst. Ein detailliertes Verzeichnis der Art und Größe der geschäumten Kunststoffe wird mit jedem Bericht geliefert. 

# In[11]:


sut.display_image_ipython("resources/images/codegroups/fragfoam_450_600.jpg", thumb=(600, 1000), rotate=0)


# *__Oben:__ Schaumstoffe in verschiedenen Größen; XPS, EPS und Sprühschäume (SPF) entlang der Schweizer Uferlinien*

# In[12]:


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
wwcodes


# ### Essen und Trinken
# 
# Beinhaltet alle Materialien, die mit Essen und Trinken in Verbindung stehen. Die größten Mengen an Einwegkunststoffen (SUP) werden im Zusammenhang mit dem Verzehr im Freien oder zum Mitnehmen verwendet. Verpackungen für Süßigkeiten und Snacks (G30) und Glasscherben (G200) sind an den Schweizer Küsten am häufigsten anzutreffen. Siehe Erhebungsergebnisses 2020-2021 [Alle Erhebungen](allsurveysde)

# In[13]:


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
wwcodes


# ### Landwirtschaft
# 
# Mehrere Codes wurden hinzugefügt, um Artikel zu kennzeichnen, die mit der Landwirtschaft in Verbindung stehen, wie z.B. G937: Pheromonköder aus Kunststoff, die üblicherweise in Weinbergen verwendet werden, und G943: Kunststoffzäune für die saisonale Viehweide. Der spezifische Foliencode G936: Gewächshausfolien und Silofolien wurde für eine besondere Art von Produkten hinzugefügt, bei denen die landwirtschaftliche Verwendung erkennbar ist. 
# 
# Industriefolien (G67) ist eine weit gefasste Kategorie, die Kunststoffplatten und -folien umfasst, bei denen es sich um flache Kunststoffteile handelt, die zur Verwendung in bestimmten Anwendungen auf eine bestimmte Dicke gebracht werden. Die Produkte unterscheiden sich in Bezug auf Materialien, Eigenschaften und Abmessungen [ogsapfpss]. Es ist schwierig, die Verwendung von Kunststofffolien in der Landwirtschaft einzugrenzen, da die gleichen Kunststoffe auch in der Verpackungs- und Baubranche in großem Umfang verwendet werden. Vor allem an den Schweizer Küsten sind die Kunststofffolien extrem verwittert und zersplittert, so dass eine eindeutige Verwendung und Herkunft schwer zu bestimmen ist. 
# 
# Industriefolien werden der Landwirtschaft zugeschrieben, da sie über einen längeren Zeitraum physikalischen Einflüssen ausgesetzt sind und in unmittelbarer Nähe von Flüssen, Bächen und Kanälen verwendet werden. Industriefolien werden auch der Landwirtschaft zugerechnet, da Kunststoffmaterialien zunehmend in landwirtschaftlichen Anwendungen eingesetzt werden, die gemeinhin als Plastikkulturen bezeichnet werden. Die Plastikkultur umfasst Bewässerungsschläuche, Kunststofftöpfe für Baumschulen und eine umfangreiche Verwendung von Folien für den Gartenbau, den Getreideanbau und die Milchwirtschaft {cite}`plasticulture`.
# 
# Folien und Filme aus Plastikkulturen G67: 
# 
# * Mulchfolie 
# * Zeilenabdeckungen 
# * Polytunnels 
# * Kunststoff-Gewächshäuser 
# * Filme zur Bodenbegasung 
# * Silageballen-Verpackung

# In[14]:


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
wwcodes 


# ### Tabak-Codes
# 
# Alle tabakbezogenen Artikel. 

# In[15]:


tobac = [
    "G25",
    "G26",
    "G27",
    "G152"
    ]

wwcodes = dfCodes.loc[tobac][cols_to_display]
wwcodes


# ### Codes für die Freizeitgestaltung
# 
# Die Freizeitgruppe umfasst Objekte, die mit Sport und Freizeit zu tun haben, d.h. Angeln, Jagen, Wandern, Bootfahren und Strandaktivitäten, Lebensmittel, Getränke und Tabak sind ausgeschlossen. Schrotpatronen aus Plastik (G70) wurden in überraschend großen Mengen gefunden, wenn man bedenkt, dass die Jagd in der Nähe der großen Seen nicht erlaubt ist. Dies könnte ein wichtiger Indikator für die zurückgelegten Entfernungen in den Gewässern sein.

# In[16]:


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
wwcodes


# ### Verpackungen, die sich nicht auf Lebensmittel, Getränke, Tabak oder unbekannte Herkunft beziehen.
# 
# Sämtliches Verpackungs- oder Umhüllungsmaterial, das nicht als Lebensmittel-, Getränke- oder Tabakverpackung gekennzeichnet ist. Die Gruppe der Verpackungen, die nicht zu Lebensmitteln/Getränken gehören, enthält (G941) einen Code, der hinzugefügt wurde, um dünne Verpackungsfolien von dickeren Industriefolien zu unterscheiden. Die Folien sind in der Regel stark beschädigt und zersplittert, so dass der ursprüngliche Verwendungszweck und die Herkunft schwer zu bestimmen sind. 
# 
# *Verpackungen, die weder mit Tabak noch mit Lebensmitteln und Getränken in Verbindung stehen oder deren Herkunft unbekannt ist:*

# In[17]:


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
wwcodes


# ### Fragmentierte Kunststoffe: Gfrags¶ 
# 
# Die Gruppe der Kunststofffragmente (Gfrags für die Analyse) sind alle Kunststoff- und Schaumstoff-/Kunststoffverbundstücke, die größer als 0,5 cm sind. Bei den Kunststofffragmenten, die an den Schweizer Küsten gefunden wurden, handelt es sich überwiegend um kleine, harte, stark fragmentierte Stücke eines pigmentierten Gegenstands. Der ursprüngliche Verwendungszweck und die Herkunft sind im Prinzip unbestimmt. Die einzelnen Plastikteile wurden nach Material und Größe quantifiziert: 

# In[18]:


plasticpcs = [
    "G78",
    "G79",
    "G80",
    "G75", 
    "G76", 
    "G77" 
    ]

wwcodes = dfCodes.loc[plasticpcs][cols_to_display]
wwcodes


# In[19]:


sut.display_image_ipython("resources/images/codegroups/Yverdon_lesBainsLacNeuchâtel15_02_2021.jpg", thumb=(800, 1200), rotate=0)


# *__Oben:__ Verschiedene Größen von Plastikteilen*

# ### Persönliche Gegenstände¶ 
# 
# Persönliches Material für Hygiene, Kleidung und Zubehör, das verloren oder weggeworfen wurde. Dazu gehören auch pandemiebezogene Artikel wie Gesichtsmasken.

# In[20]:


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
wwcodes


# ### Nicht klassifizierte Posten¶ 
# 
# Bei den nicht gruppierten Codes handelt es sich überwiegend um Elemente, deren Ursprung unklar ist, die selten identifiziert werden oder die sich nicht auf die Überwachung der Schweizer Wassersysteme an der Küste beziehen. Viele der Elemente haben einen Gesamtwert von 0 für alle in diesem Bericht enthaltenen Erhebungsdaten. 
# 
# Bemerkenswerte Ausnahmen sind G208 Glas- oder Keramikfragmente >2,5cm. Bei G208 handelt es sich überwiegend um Keramikstücke unbekannter Verwendung oder Herkunft, die häufig und in relativ hohen Konzentrationen gefunden werden. Das Vorkommen von Keramikfragmenten kann mit den Quellen des Materials für die Strandauffüllungspraktiken sowie mit natürlichen Transport- und Ablagerungsprozessen zusammenhängen. Identifizierbare Glasflaschen und -stücke werden als (G200) klassifiziert und mit Lebensmitteln und Getränken gruppiert. 

# In[21]:


wwcodes = dfCodes[dfCodes.Gruppenname== "nicht klassifiziert"][cols_to_display]
wwcodes 


# ## Liste der Zusatzcodes
# 
# Codes für Schweizer Wassersysteme hinzugefügt 

# In[22]:


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
wwcodes


# ## Lokale Codes für die Schweizer Alpen hinzugefügt

# In[23]:


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

wwcodes

