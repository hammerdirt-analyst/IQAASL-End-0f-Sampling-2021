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

# sys, file and nav packages:
import datetime as dt

# math packages:
import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.distributions.empirical_distribution import ECDF
from statsmodels.stats.stattools import medcouple
from scipy.optimize import newton
from scipy.special import digamma
import math

# charting:
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import ticker
from matplotlib import colors
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.gridspec import GridSpec
import seaborn as sns

# home brew utitilties
import resources.chart_kwargs as ck
import resources.sr_ut as sut

# images and display
from PIL import Image as PILImage
from IPython.display import Markdown as md
from IPython.display import display
import matplotlib.image as mpimg

# set some parameters:
today = dt.datetime.now().date().strftime("%Y-%m-%d")
start_date = '2020-03-01'
end_date ='2021-05-31'

# name of the output folder:
name_of_project = 'threshold_values'

# the scale for pieces per meter and the column and chart label for the units
reporting_unit = 100
unit_label = 'p/100m'

# get your data:
survey_data = pd.read_csv('resources/checked_sdata_eos_2020_21.csv')
dfBeaches = pd.read_csv("resources/beaches_with_land_use_rates.csv")
dfCodes = pd.read_csv("resources/codes_with_group_names_2015.csv")
dfDims = pd.read_csv("resources/corrected_dims.csv")

# set the index of the beach data to location slug
dfBeaches.set_index('location', inplace=True)

# index the code data
dfCodes.set_index("code", inplace=True)

# these descriptions need to be shortened for display
dfCodes = sut.shorten_the_value(["G74", "description", "Insulation: includes spray foams"], dfCodes)
dfCodes = sut.shorten_the_value(["G940", "description", "Foamed EVA for crafts and sports"], dfCodes)
dfCodes = sut.shorten_the_value(["G96", "description", "Sanitary-pads/tampons, applicators"], dfCodes)
dfCodes = sut.shorten_the_value(["G178", "description", "Metal bottle caps and lids"], dfCodes)
dfCodes = sut.shorten_the_value(["G82", "description", "Expanded foams 2.5cm - 50cm"], dfCodes)
dfCodes = sut.shorten_the_value(["G81", "description", "Expanded foams .5cm - 2.5cm"], dfCodes)
dfCodes = sut.shorten_the_value(["G117", "description", "Expanded foams < 5mm"], dfCodes)
dfCodes = sut.shorten_the_value(["G75", "description", "Plastic/foamed polystyrene 0 - 2.5cm"], dfCodes)
dfCodes = sut.shorten_the_value(["G76", "description", "Plastic/foamed polystyrene 2.5cm - 50cm"], dfCodes)
dfCodes = sut.shorten_the_value(["G24", "description", "Plastic lid rings"], dfCodes)
dfCodes = sut.shorten_the_value(["G33", "description", "Lids for togo drinks plastic"], dfCodes)
dfCodes = sut.shorten_the_value(["G3", "description", "Plastic bags, carier bags"], dfCodes)
dfCodes = sut.shorten_the_value(["G204", "description", "Bricks, pipes not plastic"], dfCodes)

# make a map to the code descriptions
code_description_map = dfCodes.description

# make a map to the code descriptions
code_material_map = dfCodes.material


# (threshholdde)=
# # Abfallobjekte am Strand
# 
# <a href="baselines.html"> English </a>
# 
# Basiswerte (BVs), die manchmal auch als Benchmarks bezeichnet werden, sind die Mengen oder Werte, die zur statistischen Definition einer Situation verwendet werden. Die BVs beziehen sich auf eine Reihe von Daten, die sowohl zeitlich als auch geografisch begrenzt sind und auch als Referenzpunkt oder Basisperiode bezeichnet werden. BVs sind die Größen, an denen der Fortschritt gemessen wird. In dieser Hinsicht sind die BVs eng mit den Daten und den zu ihrer Erhebung verwendeten Methoden verbunden. 
# 
# ## Zählen von Abfallobjekten am Strand: ein Überblick
# 
# Der erste internationale Leitfaden zur Erfassung von Abfallobjekten am Strand wurde 2008 vom Umweltprogramm der Vereinten Nationen (UNEP) und der Zwischenstaatlichen Ozeanographischen Kommission (IOC) veröffentlicht {cite}`unepseas`.  Auf der Grundlage der gesammelten Arbeit vieler Wissenschaftler wurde diese Methode 2010 von der OSPAR-Kommission übernommen{cite}`ospard10`, und 2013 veröffentlichte die EU einen Leitfaden für die Überwachung mariner Abfallobjekte in den europäischen Meeren (der Leitfaden) {cite}`mlwguidance`. Die Schweiz ist Mitglied von OSPAR und hat über 1,000 Proben nach den im Leitfaden beschriebenen Methoden genommen. 
# 
# Auf den Leitfaden folgte 2016 der Leitfaden Riverine Abfallobjekte Monitoring - Options and Recommendations{cite}`riverinemonitor`, der die zunehmende Erkenntnis widerspiegelt, dass Flüsse wichtige Quellen für Haushaltsabfälle in Küstenregionen sind. Zu diesem Zeitpunkt war das erste Projekt zur Überwachung von Abfallobjekten am Genfer See bereits abgeschlossen und die Vorbereitungen für ein einjähriges nationales Projekt in der Schweiz, das von STOPPP initiiert und von WWF-Freiwilligen unterstützt wurde, liefen an, siehe [_Mehr und weniger Müll seit 2017_](slr-iqaaslde).
# 
# 2019 veröffentlichte die Gemeinsame Forschungsstelle (JRC) eine Analyse eines paneuropäischen Datensatzes zu Abfallobjekten am Strand aus den Jahren 2012-2016, ein technisches Dokument, in dem die Methoden und verschiedenen Szenarien zur Berechnung von Basiswerten aus Abfallobjekten am Strand detailliert beschrieben werden. Von besonderem Interesse für das JRC war die Robustheit der Methoden gegenüber Extremwerten und die Transparenz der Berechnungsmethode.{cite}`eubaselines`
# 
# Im September 2020 schließlich legte die EU Basis- und Zielwerte auf der Grundlage der 2015-2016 erhobenen Daten fest. Die Zielwerte beziehen sich auf den guten Umweltzustand der Meeresgewässer, der in der Meeresstrategie-Rahmenrichtlinie (MSRL) beschrieben wird, und die Basiswerte wurden anhand der in der Veröffentlichung von 2019 beschriebenen Methoden berechnet. {cite}`threshholdeu`

# In[2]:


sut.display_image_ipython("resources/images/baselines/takingnotes2.jpg")


# *__Oben:__ 18.052020 Zählen von Abfallobjekten am Zürichsee, Richterswil; 3.49 Objekte pro Meter.*

# ### Schweiz 2020
# 
# Das IQAASL-Projekt begann im März 2020, Standorte in den definierten Erhebungsgebieten wurden 2017 beprobt oder neu eingerichtet. Ähnlich wie die Datenerhebungen Ergebnisse in der Meeresumwelt sind die Daten über Strand-Abfallobjekte in der Schweiz sehr unterschiedlich. Die Werte reichen von Null bis zu Tausenden von Objekten und Fragmenten innerhalb von 100 m vom Fluss- oder Seeufer. 

# ### Das Sammeln von Daten 
# 
# Der Reiseführer ist die Referenz für dieses Projekt. Die Geographie der Schweiz besteht jedoch nicht aus langen, homogenen Küstenabschnitten. Daher müssen bestimmte Empfehlungen in den Kontext der lokalen Topographie gestellt werden. 
# 
# 1. Die empfohlene Länge bleibt bei 100 m, je nach Region ist dies jedoch nicht immer möglich. 
# 
# #### Festlegung des Erhebungsgebiets
# 
# Ein Vermessungsgebiet wird durch den GPS-Punkt und die aufgezeichneten Vermessungsmaße definiert. Die Mindestbreite ist der Abstand zwischen der Wasserkante und der Strandlinie. In einigen Fällen können die Strandlinie und der hintere Teil des Strandes identisch sein. Weitere Informationen darüber, wie die Vermessungsflächen gemessen werden, finden Sie unter [Das Landnutzungsprofil](luseprofilede).

# *__Unten:__ Verschiedene Arten von Datenerhebungen:*

# In[3]:


# read images
img_a = mpimg.imread("resources/images/baselines/tightquarterswholensee.jpg")
img_b = mpimg.imread("resources/images/baselines/deltabad.jpg")
img_c = mpimg.imread("resources/images/baselines/lcherz.jpg")
img_d = mpimg.imread("resources/images/baselines/snow.jpg")

# display images
fig, ax = plt.subplots(2,2, figsize=(12,8))

axone=ax[0,0]
sut.hide_spines_ticks_grids(axone)
axone.imshow(img_a);
axone.set_title("Kalnach, Wohlensee: ländliches Erholungsgebiet", **ck.title_k14)

axtwo=ax[0,1]
sut.hide_spines_ticks_grids(axtwo)
axtwo.imshow(img_b);
axtwo.set_title("Spiez, Thunersee: Vorstadt-Erholungsgebiet", **ck.title_k14)

axthree=ax[1,0]
sut.hide_spines_ticks_grids(axthree)
axthree.imshow(img_c);
axthree.set_title("Lüscherz, Bielersee: ländlicher See", **ck.title_k14)

axfour=ax[1,1]
sut.hide_spines_ticks_grids(axfour)
axfour.set_title("Richterswil, Zurichsee: Stadtwanderweg", **ck.title_k14)
axfour.imshow(img_d);

plt.tight_layout()
plt.show()


# Die Länge und Breite des Erhebungsgebiets wird bei jeder Datenerhebung gemessen. So kann die Anzahl der Gegenstände in einer Standardeinheit unabhängig von den Erhebungsorten angegeben werden. In diesem Bericht wird die von der EU empfohlene Standard-Berichtseinheit verwendet: Abfallobjekte pro 100 Meter.  
# 
# #### Zählen von Objekten 
# 
# Alle sichtbaren Objekte innerhalb eines Untersuchungsgebiets werden gesammelt, klassifiziert und gezählt. Das Gesamtgewicht von Material und Plastik wird ebenfalls erfasst. Die Objekte werden anhand von [ Code-Definitionen ](codegroupsde) klassifiziert, die auf einer Masterliste von Codes im Handbuch basieren. Spezielle Objekte, die von lokalem Interesse sind, wurden unter G9xx und G7xx hinzugefügt. 

# *__Unten:__ Zählen und Klassifizieren einer Probe. Die Objekte werden nach dem Sammeln sortiert und gezählt. Die ursprüngliche Zählung wird in einem Notizbuch festgehalten, und die Daten werden in die Anwendung [ plages-propres ](https://www.plagespropres.ch/) eingegeben wenn der Erheber es wünscht.*

# In[4]:


sut.display_image_ipython("resources/images/baselines/takingnotes.jpg")


# ## Berechnung der Basislinien 
# 
# Die in den Abschnitten 3 und 4 von A European Threshold Value and Assessment Method for Macro Abfallobjekte on Coastlines und den Abschnitten 6, 7 und 8 von Analysis of a pan-European 2012-2016 beach litter data set beschriebenen Methoden werden auf die Ergebnisse der Strand-Abfallaufkommen Untersuchung von April 2020 bis Mai 2021 angewendet. 
# 
# Die verschiedenen Optionen für die Berechnung von Basislinien, die Bestimmung von Konfidenzintervallen und die Identifizierung von Extremwerten werden erläutert und mit Beispielen versehen. 
# 
# __Annahmen:__
# 
# * Je mehr Abfallobjekte auf dem Boden liegen, desto größer ist die Wahrscheinlichkeit, dass eine Person sie findet 
# * **Die Datenerhebungen Ergebnisse stellen die Mindestmenge an Abfallobjekten an diesem Ort dar**
# * Für jede Datenerhebung: Das Auffinden eines Artikels hat keinen Einfluss auf die Wahrscheinlichkeit, einen anderen zu finden. 

# ### Die Daten 
# 
# Nur Datenerhebungen mit einer Länge von mehr als zehn Metern und weniger als 100 Metern werden in die Berechnung der Basislinie einbezogen. Die folgenden Objekte wurden ausgeschlossen: 
# 
# 1. Objekte kleiner als 2,5 cm 
# 2. Paraffin, Wachs, Öl und andere Chemikalien 

# In[5]:


# define the final survey data set here:
a_data = survey_data.copy()

a_data = a_data[a_data.river_bassin != 'les-alpes']

# make a loc_date column from the survey data
# before converting to timestamp
a_data['loc_date']=tuple(zip(a_data.location, a_data.date))

# convert string dates from .csv to timestamp
a_data['date']=pd.to_datetime(a_data['date'], format='%Y-%m-%d')

# slice by start - end date
a_data = a_data[(a_data.date >= start_date)&(a_data.date <= end_date)]

# combine lugano and maggiore
# if the river bassin name does not equal tresa leave it, else change it to ticino
a_data['river_bassin'] = a_data.river_bassin.where(a_data.river_bassin != 'tresa', 'ticino' )

# assign the reporting value
a_data[unit_label] = (a_data.pcs_m * reporting_unit).round(2)

# save the data before aggregating to test
before_agg = a_data.copy()

# !! Remove the objects less than 2.5cm and chemicals !!
codes_todrop = ['G81', 'G78', 'G212', 'G213', 'G214']
a_data = a_data[~a_data.code.isin(codes_todrop)]

# use the code groups to get rid of all objects less than 5mm
a_data = a_data[a_data.groupname !=  'micro plastics (< 5mm)']

# match records to survey data
fd_dims= dfDims[(dfDims.location.isin(a_data.location.unique()))&(dfDims.date >= start_date)&(dfDims.date <= end_date)].copy()

# make a loc_date column and get the unique values
fd_dims['loc_date'] = list(zip(fd_dims.location, fd_dims.date))

# map the survey area name to the dims data record
a_map = fd_dims[['loc_date', 'area']].set_index('loc_date')
l_map = fd_dims[['loc_date', 'length']].set_index('loc_date')

# map length and area from dims to survey data
for a_survey in fd_dims.loc_date.unique():
    a_data.loc[a_data.loc_date == a_survey, 'length'] = l_map.loc[[a_survey], 'length'][0]
    a_data.loc[a_data.loc_date == a_survey, 'area'] = a_map.loc[[a_survey], 'area'][0]

# exclude surveys less 10 meters or less
gten_lhun = a_data.loc[(a_data.length > 10)].copy()

# this is a common aggregation
agg_pcs_quantity = {unit_label:'sum', 'quantity':'sum'}

# survey totals by location
dt_all = gten_lhun.groupby(['loc_date','location','river_bassin', 'water_name_slug','date'], as_index=False).agg(agg_pcs_quantity)


# *__Unten:__ Datenerhebungen Ergebnisse und zusammenfassende Statistiken: Proben größer als 10m und ohne Objekte kleiner als 2,5cm und Chemikalien, n=372*

# In[6]:


# palettes and labels
bassin_pallette = {'rhone':'dimgray', 'aare':'salmon', 'linth':'tan', 'ticino':'steelblue', 'reuss':'purple'}
comp_labels = {"linth":"Linth/Limmat", "rhone":"Rhône", 'aare':"Aare", "ticino":"Ticino/Cerisio", "reuss":"Reuss"}
comp_palette = {"Linth/Limmat":"dimgray", "Rhône":"tan", "Aare":"salmon", "Ticino/Cerisio":"steelblue", "Reuss":"purple"}

# months locator, can be confusing
# https://matplotlib.org/stable/api/dates_api.html
months = mdates.MonthLocator(interval=1)
months_fmt = mdates.DateFormatter('%b')
days = mdates.DayLocator(interval=7)

# sns.set_style('whitegrid')

fig = plt.figure(figsize=(8,5))

gs = GridSpec(1,5)

ax = fig.add_subplot(gs[:,0:3])
axtwo = fig.add_subplot(gs[:, 3:])

# scale the chart as needed to accomodate for extreme values
scale_back = 98

# the results gets applied to the y_limit function in the chart
the_90th = np.percentile(dt_all[unit_label], scale_back)

# the survey totals
sns.scatterplot(data=dt_all, x='date', y=unit_label, hue='river_bassin', palette=bassin_pallette, alpha=1, ax=ax)

# set params on ax:
ax.set_ylim(0,the_90th )
ax.set_ylabel(unit_label, **ck.xlab_k14)

ax.set_xlabel("")
ax.xaxis.set_minor_locator(days)
ax.xaxis.set_major_formatter(months_fmt)

# axtwo
a_color = "dodgerblue"

# summarize the survey totals and format for printing
table_data = dt_all[unit_label].describe()
table_data.drop('count', inplace=True)
table_data = table_data.astype('int')
table_data = table_data.map(lambda x: "{:,}".format(x))

# make a 2d array
t_data = list(zip(table_data.index, table_data.values))

sut.hide_spines_ticks_grids(axtwo)

the_first_table_data = axtwo.table(t_data,  colLabels=["Stat", unit_label], colWidths=[.5,.5], bbox=[0, 0, 1, 1])

a_summary_table_one = sut.make_a_summary_table(the_first_table_data,t_data,["Stat", unit_label], a_color, s_et_bottom_row=True)

a_summary_table_one.get_celld()[(0,0)].get_text().set_text(" ")
axtwo.tick_params(which='both', axis='both', labelsize=14)
ax.tick_params(which='both', axis='both', labelsize=14)
ax.grid(b=True, which='major', axis='y', linestyle='-', linewidth=1, c='black', alpha=.1, zorder=0)

plt.tight_layout()
plt.show()
plt.close()


# *__Unten:__ Verteilung der Datenerhebungen und Perzentilwerte: alle Erhebungen. Beachten Sie, dass der Mittelwert (341p/100m) größer ist als der Median (180p/100m).*

# In[7]:


# percentile rankings  1, 5, 10, 15, 20
these_vals = []
for element in [.01,.05,.10,.15,.20, .5, .9 ]:
    a_val = np.quantile(dt_all[unit_label].to_numpy(), element)
    these_vals.append((F"{element*100}%",F"{int(a_val)}"))
    


fig = plt.figure(figsize=(10,5))

gs = GridSpec(1,5)

ax = fig.add_subplot(gs[:,0:3])
axtwo = fig.add_subplot(gs[:, 3:])
ax.grid(b=True, which='major', axis='y', linestyle='-', linewidth=1, c='black', alpha=.1, zorder=0)

sns.histplot(data=dt_all, x=unit_label, stat='count', ax=ax, alpha=0.6)
ax.axvline(x=dt_all[unit_label].median(), c='magenta', label='median')
ax.axvline(x=dt_all[unit_label].mean(), c='red', label='mean')
ax.legend()

sut.hide_spines_ticks_grids(axtwo)

the_first_table_data = axtwo.table(these_vals,  colLabels=('ranking', unit_label), colWidths=[.5,.5], bbox=[0, 0, 1, 1])

a_summary_table_one = sut.make_a_summary_table(the_first_table_data,these_vals,('ranking', unit_label), a_color, s_et_bottom_row=True)

a_summary_table_one.get_celld()[(0,0)].get_text().set_text("ranking")
axtwo.tick_params(which='both', axis='both', labelsize=14)
ax.tick_params(which='both', axis='both', labelsize=14)
plt.show()


# ### Die Bewertungsmetrik 
# 
# Die Berechnung von Basiswerten erfordert die Aggregation von Datenerhebungen Ergebnissen auf verschiedenen zeitlichen und geografischen Ebenen. Das ist die beste Methode: 
# 
# * Robust in Bezug auf Ausreißer 
# * Einfach zu berechnen 
# * Weithin verstanden 
# 
# Die beiden gebräuchlichsten Teststatistiken, die zum Vergleich von Daten verwendet werden, sind der Mittelwert und der Median. Der Mittelwert ist der beste Prädiktor für die zentrale Tendenz, wenn die Daten $\approxeq$ normal verteilt sind. Die Ergebnisse von Strand-Abfallaufkommen Untersuchungen weisen jedoch eine hohe Varianz im Verhältnis zum Mittelwert auf. Es können Methoden auf die Daten angewendet werden, um die Auswirkungen der hohen Varianz bei der Berechnung des Mittelwerts zu verringern: 
# 
# 1. _getrimmter Mittelwert:_ entfernt einen kleinen, festgelegten Prozentsatz der größten und kleinsten Werte, bevor der Mittelwert berechnet wird 
# 2. _tri-Mittelwert:_ der gewichtete Durchschnitt des Medians und des oberen und unteren Quartils $(Q1 + 2Q2 + Q3)/4$
# 3. _mittleres Scharnier:_ $(Q1 + Q3)/2$
# 
# Die bisherigen Methoden sind zwar wirksam, um die Auswirkungen von Ausreißern zu reduzieren, aber sie sind nicht so einfach zu berechnen wie der Mittelwert oder der Median, so dass die Signifikanz der Ergebnisse möglicherweise nicht richtig verstanden wird. 
# 
# Der Median (50. Perzentil) ist ein ebenso guter Prädiktor für die zentrale Tendenz, wird aber im Vergleich zum Mittelwert viel weniger von Extremwerten beeinflusst. Je mehr sich ein Datensatz einer Normalverteilung nähert, desto näher kommen sich Median und Mittelwert. Der Median und die dazugehörigen Perzentil-Funktionen sind in den meisten Tabellenkalkulationsprogrammen verfügbar. 
# 
# For the reasons cited previously, **wird der Medianwert einer Mindestanzahl von Proben, die während eines Probenahmezeitraums in einem Erhebungsgebiet gesammelt wurden, als statistisch geeignet für die Bewertung von Strand-Abfallobjekten angesehen.**. Für die Meeresumwelt beträgt die Mindestanzahl der Proben 40 pro Unterregion und der **Probenahmezeitraum 6 Jahre**. {cite}`eubaselines` 

# ### Konfidenzintervalle (KIs) 
# 
# Konfidenzintervalle (KI) helfen dabei, die Unsicherheit der Ergebnisse von Strand-Abfallobjekten im Hinblick auf allgemeine Schlussfolgerungen über die Häufigkeit von Strand-Abfallobjekten in einer Region zu vermitteln. Der KI gibt den unteren und oberen Bereich der Schätzung der Teststatistik angesichts der Stichprobendaten an. 
# 
# Der beste Weg, die Unsicherheit zu verringern, ist eine angemessene Anzahl von Proben für die Region oder das Gebiet von Interesse. Strand-Abfallerhebungen weisen jedoch eine hohe Varianz auf und jede Schätzung eines Gesamtwerts sollte diese Varianz oder Unsicherheit widerspiegeln. KIs geben einen wahrscheinlichen Wertebereich angesichts der Unsicherheit/Varianz der Daten an. {cite}`eubaselines`
# 
# Bei dieser Methode werden die Daten NICHT von den Basisberechnungen und Konfidenzintervallen ausgeschlossen: 
# 
# > Man einigte sich darauf, die extremen Ergebnisse im Datensatz zu belassen, gleichzeitig aber die Notwendigkeit zu betonen, extreme Daten von Fall zu Fall zu überprüfen und den Median für die Berechnung von Durchschnittswerten zu verwenden. Auf diese Weise können alle Daten verwendet werden, ohne dass die Ergebnisse durch einzelne außergewöhnlich hohe Abfallobjekte verzerrt werden.  {cite}`threshholdeu`
# 
# #### Bootstrap-Methoden: 
# Bootstrapping ist eine Methode zur Wiederholung von Stichproben, bei der Zufallsstichproben mit Ersetzung verwendet werden, um den Stichprobenprozess zu wiederholen oder zu simulieren. Bootstrapping ermöglicht die Schätzung der Stichprobenverteilung von Stichprobenstatistiken unter Verwendung von Zufallsstichprobenverfahren. {cite}`bootstrapdef` {cite}`bsci` {cite}`usingbootstrap`
# 
# Bootstrap-Methoden werden verwendet, um die KI der Teststatistiken zu berechnen, indem der Stichprobenprozess wiederholt wird und der Median bei jeder Wiederholung ausgewertet wird. Der Wertebereich, der durch die mittleren 95% der Bootstrap-Ergebnisse beschrieben wird, ist der CI für die beobachtete Teststatistik. 
# 
# Es stehen mehrere Berechnungsmethoden zur Auswahl, z. B. Perzentil, BCa und Student's t. Für dieses Beispiel wurden zwei Methoden getestet: 
# 
# 1. Perzentil-Bootstrap
# 2. Bias-korrigiertes beschleunigtes Bootstrap-Konfidenzintervall (BCa) 
# 
# Die Perzentil-Methode berücksichtigt nicht die Form der zugrunde liegenden Verteilung, was zu Konfidenzintervallen führen kann, die nicht mit den Daten übereinstimmen. Die BCa-Methode korrigiert dies. Die Implementierung dieser Methoden ist mit den bereits zitierten Paketen einfach zu bewerkstelligen. {cite}`bcatheory` {cite}`bcaimpdrysdale` {cite}`bcaconfidence`
# 
# ### Vergleich der Bootstrap-KIs 

# *__Unten:__ Konfidenzintervalle berechnet mit der Percentile Bootstrap Methode*

# In[8]:


# this code was modified from this source:
# http://bebi103.caltech.edu.s3-website-us-east-1.amazonaws.com/2019a/content/recitations/bootstrapping.html
# if you want to get the confidence interval around another point estimate use np.percentile
# and add the percentile value as a parameter

def draw_bs_sample(data):
    """Draw a bootstrap sample from a 1D data set."""
    return np.random.choice(data, size=len(data))

def compute_jackknife_reps(data, statfunction=None, stat_param=False):
    '''Returns jackknife resampled replicates for the given data and statistical function'''
    # Set up empty array to store jackknife replicates
    jack_reps = np.empty(len(data))

    # For each observation in the dataset, compute the statistical function on the sample
    # with that observation removed
    for i in range(len(data)):
        jack_sample = np.delete(data, i)
        if not stat_param:
            jack_reps[i] = statfunction(jack_sample)
        else:
            jack_reps[i] = statfunction(jack_sample, stat_param)          
        
    return jack_reps


def compute_a(jack_reps):
    '''Returns the acceleration constant a'''

    mean = np.mean(jack_reps)
    try:
        a = sum([(x**-(i+1)- (mean**-(i+1)))**3 for i,x in enumerate(jack_reps)])
        b = sum([(x**-(i+1)-mean-(i+1))**2 for i,x in enumerate(jack_reps)])
        c = 6*(b**(3/2))
        data = a/c
    except:
        print(mean)
    return data


def bootstrap_replicates(data, n_reps=1000, statfunction=None, stat_param=False):
    '''Computes n_reps number of bootstrap replicates for given data and statistical function'''
    boot_reps = np.empty(n_reps)
    for i in range(n_reps):
        if not stat_param:
            boot_reps[i] = statfunction(draw_bs_sample(data))
        else:
            boot_reps[i] = statfunction(draw_bs_sample(data), stat_param)     
        
    return boot_reps


def compute_z0(data, boot_reps, statfunction=None, stat_param=False):
    '''Computes z0 for given data and statistical function'''
    if not stat_param:
        s = statfunction(data)
    else:
        s = statfunction(data, stat_param)
    return stats.norm.ppf(np.sum(boot_reps < s) / len(boot_reps))


def compute_bca_ci(data, alpha_level, n_reps=1000, statfunction=None, stat_param=False):
    '''Returns BCa confidence interval for given data at given alpha level'''
    # Compute bootstrap and jackknife replicates
    boot_reps = bootstrap_replicates(data, n_reps, statfunction=statfunction, stat_param=stat_param)
    jack_reps = compute_jackknife_reps(data, statfunction=statfunction, stat_param=stat_param)

    # Compute a and z0
    a = compute_a(jack_reps)
    z0 = compute_z0(data, boot_reps, statfunction=statfunction, stat_param=stat_param)

    # Compute confidence interval indices
    alphas = np.array([alpha_level/2., 1-alpha_level/2.])
    zs = z0 + stats.norm.ppf(alphas).reshape(alphas.shape+(1,)*z0.ndim)
    avals = stats.norm.cdf(z0 + zs/(1-a*zs))
    ints = np.round((len(boot_reps)-1)*avals)
    ints = np.nan_to_num(ints).astype('int')

    # Compute confidence interval
    boot_reps = np.sort(boot_reps)
    ci_low = boot_reps[ints[0]]
    ci_high = boot_reps[ints[1]]
    return (ci_low, ci_high)

quantiles = [.1, .2, .5, .9]
q_vals = {x:dt_all[unit_label].quantile(x) for x in quantiles}

the_bcas = {}
for a_rank in quantiles:
    an_int = int(a_rank*100)
    a_result = compute_bca_ci(dt_all[unit_label].to_numpy(), .05, n_reps=5000, statfunction=np.percentile, stat_param=an_int)
    observed = np.percentile(dt_all[unit_label].to_numpy(), an_int)
    the_bcas.update({F"{int(a_rank*100)}":{'2.5% ci':a_result[0], "Beobachtung": observed, '97.5% ci': a_result[1]}})


bca_cis = pd.DataFrame(the_bcas)
bcas = bca_cis.reset_index()
bcas[['10', '20', '50', '90']] = bcas[['10', '20', '50', '90']].astype('int')
bcas['b-method'] = 'BCa'


# In[9]:


# bootstrap percentile confidence intervals
# resample the survey totals for n times to help
# define the range of the sampling statistic
# the number of reps
n=5000

# keep the observed values
observed_median = dt_all[unit_label].median()
observed_tenth = dt_all[unit_label].quantile(.15)

# quantiles = [.1, .2, .5, .9]
# q_vals = {x:dt_all[unit_label].quantile(x) for x in quantiles}

the_cis = {}

for a_rank in quantiles:
    # for the median
    sim_ptile = []

    # for the tenth percentile
    sim_ten = []
    for element in np.arange(n):
        less = dt_all[unit_label].sample(n=len(dt_all), replace=True)    
        a_ptile = less.quantile(a_rank)
        sim_ptile.append(a_ptile)
    # get the upper and lower range of the test statistic disrtribution:
    a_min = np.percentile(sim_ptile, 2.5)
    a_max = np.percentile(sim_ptile, 97.5)
    
    # add the observed value and update the dict
    the_cis.update({F"{int(a_rank*100)}":{'2.5% ci':a_min, "Beobachtung": q_vals[a_rank], '97.5% ci': a_max}})

# make df
p_cis = pd.DataFrame(the_cis)
p_cis = p_cis.astype("int")
p_cis['b-method'] = '%'
p_cis.reset_index(inplace=True)


# *__Unten links:__ Konfidenzintervalle, die durch eine 5.000-fache Wiederholungsstichprobe der Umfrageergebnisse für jede Bedingung berechnet wurden. __Unten rechts:__ Die gleichen Intervalle unter Verwendung der verzerrungskorrigierten Methode.*

# In[10]:


fig, axs = plt.subplots(1,2, figsize=(11,3))

axone = axs[0]
axtwo = axs[1]

data = p_cis.values
sut.hide_spines_ticks_grids(axone)
sut.hide_spines_ticks_grids(axtwo)
colLabels = ["$" + F"{x}" +"^{th}$" for x in p_cis.columns[:-1]]
colLabels.append('method')

table_one = sut.make_a_table(axone, data, colLabels=colLabels, colWidths=[.25,*[.15]*5], bbox=[0, 0, 1, 1])
table_two = sut.make_a_table(axtwo, bcas.values, colLabels=colLabels, colWidths=[.25,*[.15]*5], bbox=[0, 0, 1, 1])

table_one.get_celld()[(0,0)].get_text().set_text(" ")
table_two.get_celld()[(0,0)].get_text().set_text(" ")

plt.tight_layout()
plt.show()
plt.close()


# *__Unten:__ Beispielwert für das Konfidenzintervall: Das Ergebnis der Datenerhebungen in Biel am 31.01.2021 war größer als der Medianwert für alle Datenerhebungen. Es wurden 123 Objekte (pcs) über 40 Meter (m) Uferlinie gesammelt. Zunächst wird der Wert der Datenerhebungen in Abfallobjekte pro Meter (pcs/m) umgerechnet und dann mit der erforderlichen Anzahl von Metern (100) multipliziert.* 
# 
# $(pcs/m)*100 = (123_{pcs} / 40_m)*100m \approxeq 313p/100m$

# In[11]:


sut.display_image_ipython('resources/images/baselines/mullermatte_bielersee31_01_2021.png', thumb=(1200, 700))


# ### Baseline Werte 
# 
# Für diesen Datensatz sind die Unterschiede zwischen den mit der BCa-Methode oder der Perzentilmethode berechneten KI minimal. Die BCa-Methode wird verwendet, um die Basiswerte und KI's anzugeben. 
# 
# #### Basismedianwert aller Datenerhebungen Ergebnisse 
# 
# Wenn man nur Datenerhebungen mit einer Länge von mehr als 10 Metern berücksichtigt und Objekte mit einer Größe von weniger als 2,5 cm ausschließt, __lag der Medianwert aller Daten bei 181 p/100 m mit einem CI von 147 p/100 m - 213 p/100 m__. Der gemeldete Medianwert für die EU lag bei 133p/100m und damit im Bereich des CI der IQAASL-Erhebungsergebnisse. Während der Medianwert in der Schweiz höher sein könnte, liegt der Mittelwert der EU-Studie bei 504p/100m gegenüber 341p/100m in der Schweiz.{cite}`eubaselines`
# 
# Das deutet darauf hin, dass die höheren Extremwerte eher in der Meeresumwelt zu finden sind, aber der erwartete Medianwert beider Datensätze ist ähnlich. 
# 
# #### Baseline-Median und KI pro Erhebungsgebiet 
# 
# Es gab vier Erhebungsgebiete im IQAASL, von denen 3 mehr als 40 Proben während des Erhebungszeitraums hatten. 

# *__Unten:__ Der Median und das 95%-Konfidenzintervall der Erhebungsgebiete Linth, Aare und Rhône. Das Erhebungsgebiet Tessin ist mangels ausreichender Anzahl von Datenerhebungen nicht enthalten.*

# In[12]:


bassins = ["linth", "aare", "rhone"]
the_sas = {}
for a_bassin in bassins:
    an_int = int(a_rank*100)
    a_result = compute_bca_ci(dt_all[dt_all.river_bassin == a_bassin][unit_label].to_numpy(), .05, n_reps=5000, statfunction=np.percentile, stat_param=50)
    observed = np.percentile(dt_all[dt_all.river_bassin == a_bassin][unit_label].to_numpy(), 50)
    the_sas.update({a_bassin:{'2.5% ci':a_result[0], "Beobachtung": observed, '97.5% ci': a_result[1]}})

sas = pd.DataFrame(the_sas)
sas['b-method'] = 'bca'
sas = sas.reset_index()

fig, axs = plt.subplots()

data = sas.values
sut.hide_spines_ticks_grids(axs)

the_first_table_data = axs.table(data, colLabels=sas.columns, colWidths=[.25,*[.15]*5], bbox=[0, 0, 1, 1])

a_summary_table_one = sut.make_a_summary_table(the_first_table_data,data,sas.columns, a_color, s_et_bottom_row=True)

a_summary_table_one.get_celld()[(0,0)].get_text().set_text(" ")

plt.show()
plt.close()


# ## Extremwerte 
# 
# Wie bereits erwähnt, werden Extremwerte (EVs) oder Ausreißer bei der Berechnung von Basislinien oder CIs nicht aus den Daten ausgeschlossen. Die Identifizierung von EVs und wo und wann sie auftreten, ist jedoch ein wesentlicher Bestandteil des Überwachungsprozesses. 
# 
# Das Auftreten von Extremwerten kann den Durchschnitt der Daten und die Interpretation der Datenerhebungen Ergebnisse beeinflussen. Laut dem GFS-Bericht: 
# 
# >  Die Methodik zur Identifizierung von Extremwerten kann entweder auf einem Expertenurteil beruhen oder auf statistischen und modellierenden Ansätzen, wie der Anwendung von Tukey's Box Plots zur Erkennung potenzieller Ausreißer. Für schiefe Verteilungen ist der angepasste Boxplot besser geeignet. {cite}`eubaselines`
# 
# ### Extremwerte definieren
# 
# Die Referenzen geben keine Hinweise auf den numerischen Wert eines EV. Im Gegensatz zu dem Zielwert von 20p/100m oder dem 15. Perzentil bleibt die Definition eines EV der Person überlassen, die die Daten interpretiert. Die Obergrenze von Tukeys Boxplots (unangepasst) ist ungefähr das 90. Perzentil der Daten. Diese Methode ist mit der Bewertungsmetrik kompatibel, und Boxplots lassen sich visuell relativ leicht auflösen.
# 
# #### Angepasste Boxplots 
# 
# Tukey's Boxplot wird verwendet, um die Verteilung eines univariaten Datensatzes zu visualisieren. Die Proben, die innerhalb des ersten Quartils (25%) und des dritten Quartils (75%) liegen, werden als innerhalb des inneren Quartilsbereichs (IQR) betrachtet. Punkte, die außerhalb des inneren Quartils liegen, werden als Ausreißer betrachtet, wenn ihr Wert größer oder kleiner als einer der beiden Grenzwerte ist: 
# 
# * Untere Grenze =   $Q_1 - (1.5*IQR)$
# * Obergrenze =   $Q_3 + (1.5*IQR)$
# 
# Bei der Anpassung des Boxplots wird die Konstante 1,5 durch einen anderen Parameter ersetzt. Dieser Parameter wird mit einer Methode namens Medcouple (MC) berechnet und das Ergebnis dieser Methode auf die Konstante 1,5 angewendet. {cite}`tukeysbox` {cite}`medcouple` 
# 
# Die neue Berechnung sieht wie folgt aus: 
# 
# * Untere Grenze = $Q_1 - (1.5e^{-4MC}*IQR)$
# 
# * Obergrenze = $Q_3 + (1.5e^{3MC}*IQR)$
# 
# Die Grenzen werden erweitert oder reduziert, um der Form der Daten besser zu entsprechen. Infolgedessen repräsentieren die oberen und unteren Grenzen einen größeren Wertebereich in Bezug auf das Perzentil-Ranking als bei der unangepassten Version.  
# 
# *__Unten__: Die Grenze, ab der eine Datenerhebung als extrem gilt, erstreckt sich auf das 98. Perzentil, wenn die Boxplots angepasst werden, im Gegensatz zum 90. Perzentil, wenn die Konstante bei 1,5 belassen wird.*

# In[13]:


# implementation of medcouple
a_whis = medcouple(dt_all[unit_label].to_numpy())

# get the ecdf 
ecdf = ECDF(dt_all[unit_label].to_numpy())

# quantiles and IQR of the data
q1 = dt_all[unit_label].quantile(0.25)
q3 =dt_all[unit_label].quantile(0.75)
iqr = q3 - q1

# the upper and lower limit of extreme values unadjusted:
limit_lower = q1 - 1.5*iqr
limit_upper = q3 + 1.5*iqr

# the upper and lower limit of extreme values adjusted:
a_fence = q1 - (1.5*(math.exp((-4*a_whis))))*iqr
a_2fence = q3 + (1.5*(math.exp((3*a_whis))))*iqr

fig, ax = plt.subplots(figsize=(4,6))
box_props = {
    'boxprops':{'facecolor':'none', 'edgecolor':'magenta'},
    'medianprops':{'color':'magenta'},
    'whiskerprops':{'color':'magenta'},
    'capprops':{'color':'magenta'}
}

sns.stripplot(data=dt_all, y=unit_label, ax=ax, zorder=1, color='black', jitter=.35, alpha=0.3, s=8)
sns.boxplot(data=dt_all, y=unit_label, ax=ax, zorder=3, orient='v', showfliers=False, **box_props)
ax.axhline(y=a_2fence, xmin=.25, xmax=.75, c='magenta', zorder=3,)
ax.set_ylabel(unit_label, **ck.xlab_k14)

ax.tick_params(which='both', axis='both', labelsize=14)
ax.tick_params(which='both', axis='x', bottom=False)

ax.set_ylim(0, a_2fence+200)

ax.annotate("Bereinigt",
                  xy=(0, a_2fence), xycoords='data',
                  xytext=(.2,a_2fence-200), textcoords='data',
                  size=14, va="center", ha="center",
                  bbox=dict(boxstyle="round4", fc="w", alpha=0.5),
                  arrowprops=dict(arrowstyle="-|>",
                                  connectionstyle="arc3,rad=-0.2",
                                  fc="black"),)

ax.annotate("nicht bereinigt",
                  xy=(0, limit_upper), xycoords='data',
                  xytext=(-.2,limit_upper+400), textcoords='data',
                  size=14, va="center", ha="center",
                  bbox=dict(boxstyle="round4", fc="w",alpha=0.5),
                  arrowprops=dict(arrowstyle="-|>",
                                  connectionstyle="arc3,rad=-0.2",
                                  fc="black"),)
ax.grid(b=True, which='major', axis='y', linestyle='-', linewidth=1, c='black', alpha=.1, zorder=0)

plt.show()


# In[14]:


caption = F"""
*Der Unterschied zwischen bereinigten und normalen Boxplots. Bereinigt = {int(a_2fence)} {unit_label},  nicht bereinigt = {int(limit_upper)} {unit_label}.*
"""
md(caption)


# Bei Verwendung der bereinigten Boxplots steigt die Extremwertschwelle (EVT) auf über 1600p/100m. Die unbereinigten Boxplots liegen jedoch innerhalb der KI des erwarteten Perzentils der Umfragedaten. 

# *__Unten:__ Beispiel für bereinigte Extremwerte: St. Gingolph, 08-12-2020. Es wurden 514 Objekte (pcs) über 31 Meter (m) Uferlinie gesammelt. Zunächst wird der Wert der Datenerhebungen in Abfallobjekte pro Meter (pcs/m) umgerechnet und dann mit der erforderlichen Anzahl von Metern (100) multipliziert:* 
# 
# $(pcs/m)*100 = (514_{pcs} / 31_m)*100m \approxeq 1652p/100m$

# In[15]:


sut.display_image_ipython('resources/images/baselines/onethous60053pcs100m.jpg')


# #### Modellierung 
# 
# Extremwerte können identifiziert werden, indem man davon ausgeht, dass die Daten zu einer zugrunde liegenden bekannten statistischen Verteilung gehören. Im Allgemeinen wird davon ausgegangen, dass Zähldaten eine Poisson-Verteilung oder eine sehr ähnliche Form aufweisen. Bei der Poisson-Verteilung wird angenommen, dass der Mittelwert gleich der Varianz ist. Die Daten des IQAASL und die Abfallobjekte am Strand haben im Allgemeinen eine hohe Varianz, die in der Regel größer als der Mittelwert ist. 
# 
# Für die negative Binomialverteilung (NB) gilt diese Anforderung nicht. Die NB ist eine Poisson-Verteilung mit dem Parameter λ, wobei λ selbst nicht fest ist, sondern eine Zufallsvariable, die einer Gamma-Verteilung folgt. {cite}`cameron` {cite}`wolfram` {cite}`nbinom` 
# 
# > Der Modellierungsansatz zur Identifizierung von Extremwerten erfolgt dann durch Anpassung der NB-Verteilung an die Daten mittels maximaler Wahrscheinlichkeit (MLE) und Kennzeichnung aller Werte im rechten Schwanz als potenziell extreme Werte, wenn die Wahrscheinlichkeit, dass sie zur angepassten NB-Verteilung gehören, kleiner als z.B. 0,001 ist.  {cite}`threshholdeu`
# 
# Der MLE ist eine der beiden empfohlenen Methoden zur Modellierung oder Anpassung von Datenwerten an eine angenommene Verteilung: 
# 
# * Methode der Momente (MOM) 
# * MLE: Maximum-Likelihood-Schätzung 
# 
# ##### Methode der Momente (MOM)
# 
# Die Methode der Momente geht davon aus, dass die aus der Stichprobe abgeleiteten Parameter den Populationsparametern nahe kommen oder ähnlich sind. Im Falle von Strand-Abfallerhebungen bedeutet dies, dass der Median, der Mittelwert und die Varianz der Stichprobe als gute Annäherung an die tatsächlichen Werte angesehen werden können, wenn alle Strände an allen Seen und Flüssen untersucht werden. 
# 
# Konkret werden die Parameter eines wahrscheinlichen Verteilungsmodells geschätzt, indem sie aus den Beispieldaten berechnet werden. Diese Methode ist einfach anzuwenden, da die meisten Parameterberechnungen für die gängigsten Verteilungen gut bekannt sind.  {cite}`srikanta` {cite}`2020SciPy` {cite}`examplemmoments`
# 
# ##### Maximum-Likelihood-Schätzung (MLE)
# 
# MLE ist eine Methode zur Schätzung der Parameter eines statistischen Modells bei gegebenen Daten. In dieser Hinsicht unterscheidet sie sich nicht von der MOM. Der Unterschied besteht darin, dass bei der MOM die Modellparameter aus den Daten berechnet werden, während bei der MLE die Parameter so gewählt werden, dass die Daten angesichts des statistischen Modells am wahrscheinlichsten sind. 
# 
# Diese Methode ist rechenintensiver als die MOM, hat aber einige Vorteile: 
# 
# * Wenn das Modell korrekt angenommen wird, ist der MLE der effizienteste Schätzer. 
# * Es führt zu unverzerrten Schätzungen in größeren Stichproben. 

# *__Anpassen der Daten an die zugrunde liegende NB-Verteilung.__ Die beobachteten Datenerhebungen Ergebnisse werden mit den geschätzten Datenerhebungen unter Verwendung der Methode der Momente und der Maximum-Likelihood-Schätzung verglichen. __Links:__ Histogramm der Ergebnisse im Vergleich zu den beobachteten Daten. __Rechts:__ Verteilung der Ergebnisse im Vergleich zu den beobachteten Daten mit 90. Perzentil.* 

# In[16]:


# implementaion of MLE
# https://github.com/pnxenopoulos/negative_binomial/blob/master/negative_binomial/core.py

def r_derv(r_var, vec):
    ''' Function that represents the derivative of the negbinomial likelihood
    '''

    total_sum = 0
    obs_mean = np.mean(vec)  # Save the mean of the data
    n_pop = float(len(vec))  # Save the length of the vector, n_pop

    for obs in vec:
        total_sum += digamma(obs + r_var)

    total_sum -= n_pop*digamma(r_var)
    total_sum += n_pop*math.log(r_var / (r_var + obs_mean))

    return total_sum

def p_equa(r_var, vec):
    ''' Function that represents the equation for p in the negbin likelihood
     '''
    data_sum = sum(vec)
    n_pop = float(len(vec))
    p_var = 1 - (data_sum / (n_pop * r_var + data_sum))
    return p_var

def neg_bin_fit(vec, init=0.0001):
    ''' Function to fit negative binomial to data
    vec: the data vector used to fit the negative binomial distribution
   
    '''
    est_r = newton(r_derv, init, args=(vec,))
    est_p = p_equa(est_r, vec)
    return est_r, est_p

# the data to model
vals = dt_all[unit_label].to_numpy()

# the variance
var = np.var(vals)

# the average
mean = np.mean(vals)

# dispersion
p = (mean/var)
n = (mean**2/(var-mean))

# implementation of method of moments
r = stats.nbinom.rvs(n,p, size=len(vals))

# format data for charting
df = pd.DataFrame({unit_label:vals, 'group':"Beobachtung"})
df = df.append(pd.DataFrame({unit_label:r, 'group':'MOM'}))

scp = df[df.group == 'MOM'][unit_label].to_numpy()
obs = df[df.group == "Beobachtung"][unit_label].to_numpy()

scpsx = [{unit_label:x, 'model':'MOM'} for x in scp]
obsx = [{unit_label:x, 'model':"Beobachtung"} for x in obs]

# ! implementation of MLE
estimated_r, estimated_p = neg_bin_fit(obs, init = 0.0001)

# ! use the MLE estimators to generate data
som_data = stats.nbinom.rvs(estimated_r, estimated_p, size=len(dt_all))
som_datax = pd.DataFrame([{unit_label:x, 'model':'MLE'}  for x in som_data])

# combined the different results in to one df
data = pd.concat([pd.DataFrame(scpsx), pd.DataFrame(obsx), pd.DataFrame(som_datax)])

# the 90th
ev = data.groupby('model', as_index=False)[unit_label].quantile(.9)
xval={'MOM':0, 'Beobachtung':1, 'MLE':2}
ev['x'] = ev.model.map(lambda x: xval[x])
box_palette = {'MOM':'salmon', 'MLE':'magenta', 'Beobachtung':'dodgerblue'}

fig, axs = plt.subplots(1,2, figsize=(10,6))

ax=axs[0]
axone=axs[1]

bw=80

sns.histplot(data=data, x=unit_label, ax=ax, hue='model', zorder=2, palette=box_palette, binwidth=bw, element='bars', multiple='stack', alpha=0.4)

box_props = {
    'boxprops':{'facecolor':'none', 'edgecolor':'black'},
    'medianprops':{'color':'black'},
    'whiskerprops':{'color':'black'},
    'capprops':{'color':'black'}
}


sns.boxplot(data=data, x='model', y=unit_label, ax=axone, zorder=5, palette=box_palette, showfliers=False, dodge=False, **box_props)
sns.stripplot(data=data, x='model', y=unit_label, hue='model', zorder=0,palette=box_palette, ax=axone, s=8, alpha=0.2, dodge=False, jitter=0.4)
axone.scatter(x=ev.x.values, y=ev[unit_label].values, label="90%", color='black', s=60)
axone.set_ylim(0,np.percentile(r, 95))
ax.get_legend().remove()
ax.set_ylabel("# der Erhebungen", **ck.xlab_k14)
axone.set_ylabel(unit_label, **ck.xlab_k14)

handles, labels = axone.get_legend_handles_labels()
axone.get_legend().remove()
h3=handles[:3]
hlast= handles[-1:]
axone.set_xlabel("")
axone.tick_params(which='both', axis='both', labelsize=14)
ax.tick_params(which='both', axis='both', labelsize=14)
l3 = labels[:3]
llast = labels[-1:]

ax.grid(b=True, which='major', axis='y', linestyle='-', linewidth=1, c='black', alpha=.2, zorder=0)
axone.grid(b=True, which='major', axis='y', linestyle='-', linewidth=1, c='black', alpha=.2, zorder=0)

fig.legend([*h3, *hlast], [*l3, *llast], bbox_to_anchor=(.48, .96), loc='upper right', fontsize=14)
plt.tight_layout()
plt.show()


# In[17]:


evx = ev.set_index('model')

pnt =  F"""*90% p/100m: &nbsp;MLE={evx.loc['MLE'][unit_label].astype('int')},  &nbsp;Observed={evx.loc["Beobachtung"][unit_label].astype('int')},  &nbsp;MOM={evx.loc['MOM'][unit_label].astype('int')}*"""
md(pnt)


# ## Umsetzung
# 
# Die vorgeschlagenen Bewertungsmaßstäbe und -methoden für die Ergebnisse der Strand-Abfallaufkommen Untersuchungen sind ähnlich und kompatibel mit den zuvor in der Schweiz angewandten Methoden. Diese erste Analyse hat gezeigt, dass: 
# 
# * Die von der EU vorgeschlagenen Methoden zur Überwachung von Abfallobjekten sind in der Schweiz anwendbar
# * Konfidenzintervalle und Basislinien können für verschiedene Erhebungsgebiete berechnet werden
# * Aggregierte Ergebnisse können zwischen Regionen verglichen werden 
# 
# Sobald die BV für ein Erhebungsgebiet berechnet ist, können alle Proben, die innerhalb dieses Erhebungsgebiets durchgeführt werden, direkt mit ihr verglichen werden. Es ist der Fall, dass die Erhebungsgebiete in der Schweiz in den Jahren 2020 - 2021 unterschiedliche Median-Baselines haben. Diese Situation ist analog zur EU, was die Unterschiede zwischen den verschiedenen Regionen und Verwaltungsgebieten des Kontinents betrifft. 
# 
# Durch die Anwendung der vorgeschlagenen Methoden auf die aktuellen Ergebnisse von IQAASL können die bedenklichen Objekte für jedes Untersuchungsgebiet identifiziert werden. 

# *__Unten:__ Vergleichen Sie die Ausgangswerte der häufigsten Objekte. Alle Datenerhebungen 2020 - 2021. Das Erhebungsgebiet Ticino/Cerisio hat weniger als 100 Datenerhebungen.*

# In[18]:


sut.display_image_ipython("resources/images/baselines/lakes_rivers_de_22_0.png", thumb=(800, 1200))


# Der erwartete Medianwert pro Datenerhebung und der Medianwert der häufigsten Objekte pro Erhebung ist im Erhebungsgebiet Rhône höher. Wenn der Medianwert verwendet wird, zeigt die BV auch, dass 2/12 der häufigsten Objekte in weniger als 50% der Datenerhebungen landesweit gefunden wurden, nämlich diejenigen mit einem Medianwert von Null. 
# 
# Die Methode kann vertikal skaliert werden, um eine detailliertere Ansicht eines Erhebungsgebiets zu erhalten. Die Berechnungsmethode bleibt dieselbe, daher sind Vergleiche vom See bis zur nationalen Ebene möglich. 

# *__Unten:__ Vergleichen Sie die Ausgangswerte der häufigsten Objekte. Aare-Erhebungsgebiet Seen und Flüsse 2020 - 2021. Orte mit mehr als 30 Datenerhebungen: Bielersee, Neuenburgersee und Thunersee.*

# In[19]:


sut.display_image_ipython("resources/images/baselines/aare_sa_de_23_0.png", thumb=(800, 800))


# Die empfohlene Mindestanzahl von Datenerhebungen (40) pro Probenahmezeitraum soll sicherstellen, dass die BV-Berechnungen auf einer ausreichenden Anzahl von Stichproben basieren. Dies ist wegen der hohen Variabilität der Strand-Abfallobjekte-Untersuchungen wichtig. 
# 
# Der Probenahmezeitraum für IQAASL war April bis Mai 2020 - 2021. In Bezug auf die Mindestanzahl der Proben gibt es drei Basiswerte für das Aare-Erhebungsgebiet: 
# 
# 1. Bielersee 
# 2. Neuenburgersee 
# 3. Das Aare-Erhebungsgebiet  
# 
# Für Bewertungszwecke bedeutet dies, dass eine Stichprobe als Stichprobenbewertung dienen kann und die Ergebnisse direkt mit einer der regionalen Basislinien verglichen werden können, was ein sofortiges Feedback ermöglicht. Diese Art der Bewertung vereinfacht den Prozess und versetzt die lokalen Akteure in die Lage, unabhängige Bewertungen vorzunehmen, Schlussfolgerungen zu ziehen und auf der Grundlage der Ergebnisse der festgelegten BV für das Erhebungsgebiet Minderungsstrategien festzulegen. 
# 
# In den vorherigen Beispielen sind keine Schwellenwerte oder Extremwerte angegeben. Werte, die größer als Null sind, sind der erwartete Medianwert des Objekts für jede gemessene Einheit. Ein Nullwert bedeutet, dass das Objekt in weniger als 50% der Datenerhebungen gefunden wurde. Der Perzentil-Rang für ein bestimmtes Objekt lässt sich ableiten, indem Sie die Wertetabelle in horizontaler Richtung lesen. 
# 
# Wie aussagekräftig diese Ergebnisse für die Bewertung von Minderungsstrategien sind, hängt von der Anzahl und Qualität der Proben ab. Interessengruppen auf kommunaler oder lokaler Ebene benötigen detaillierte Daten über bestimmte Objekte. Nationale und internationale Stakeholder hingegen tendieren dazu, breitere, aggregierte Gruppen zu verwenden. 
# 
# Die Qualität der Daten steht in direktem Zusammenhang mit der Ausbildung und Unterstützung der Personen, die die Datenerhebung durchführen. Der Identifizierungsprozess erfordert ein gewisses Maß an Fachwissen, da viele Objekte und Materialien dem Durchschnittsbürger nicht bekannt sind. Ein Kernteam von erfahrenen Personen, die bei der Entwicklung und Schulung helfen, stellt sicher, dass die Datenerhebungen im Laufe der Zeit konsistent durchgeführt werden. 
# 
# Das Überwachungsprogramm in der Schweiz hat es geschafft, mit den Entwicklungen auf dem Kontinent Schritt zu halten, es gibt jedoch viele Bereiche, die verbessert werden können: 
# 
# 1. Festlegung einer standardisierten Berichtsmethode für kommunale, kantonale und föderale Akteure 
# 2. Definieren Sie Überwachungs- oder Bewertungsziele 
# 3. Formalisierung des Datenspeichers und der Methode zur Implementierung auf verschiedenen Verwaltungsebenen  
# 4. Aufbau eines Netzwerks von Verbänden, die sich die Verantwortung und die Ressourcen für die Vermessung des Gebiets teilen 
# 5. Entwickeln und implementieren Sie ein formelles Schulungsprogramm für Personen, welche die Datenerhebung ausführt 
# 6. Bestimmen Sie in Zusammenarbeit mit akademischen Partnern die idealen Stichproben-Szenarien und den Forschungsbedarf.
# 7. Entwickeln Sie eine Finanzierungsmethode, um die empfohlene Mindestanzahl von Datenerhebungen (40) pro Stichprobenzeitraum und pro Erhebungsgebiet durchzuführen, um sicherzustellen, dass genaue Bewertungen vorgenommen werden können und die Forschungsanforderungen erfüllt werden. 
# 
# Veränderungen in den Ergebnissen von Strand-Abfalluntersuchungen sind Signale, und die Verwendung von Basiswerten hilft, das Ausmaß dieser Signale zu erkennen. Ohne Kontext oder zusätzliche Informationen können diese Signale jedoch zufällig erscheinen. 
# 
# Zu einem fachkundigen Urteil gehört die Fähigkeit, Datenerhebungen Ergebnisse in den Kontext lokaler Ereignisse und der Topographie einzuordnen. Dieses Urteilsvermögen in Bezug auf die Daten und die Umgebung ist entscheidend für die Identifizierung potenzieller Quellen und Prioritäten. 

# In[ ]:




