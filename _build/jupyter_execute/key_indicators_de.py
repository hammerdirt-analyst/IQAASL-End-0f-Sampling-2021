#!/usr/bin/env python
# coding: utf-8

# In[1]:


# sys, file and nav packages:
import datetime as dt
import locale

# math packages:
import pandas as pd
import numpy as np
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

loc = locale.getlocale()
lang =  'de_DE.utf8'
locale.setlocale(locale.LC_ALL, lang)


# set some parameters:
today = dt.datetime.now().date().strftime("%Y-%m-%d")
start_date = "2020-03-01"
end_date ="2021-05-31"
a_fail_rate = 50

# the city, lake and river bassin we are aggregating to
# the keys are column names in the survey data
levels = {"city":"Biel/Bienne","water_name_slug":'bielersee', "river_bassin":'aare'}
level_names = [levels['city'], "Bielersee","Aare-Erhebungsgebiet"]

# colors for gradients
cmap2 = ck.cmap2
colors_palette = ck.colors_palette


# (keyindicatorsde)=
# # Statistische Schlüsselindikatoren
# 
# Die Schlüsselindikatoren sind einfach zu berechnen und werden direkt aus den Erhebungsergebnissen entnommen. Sie sind für die Identifizierung von Akkumulationszonen im Wassereinzugsgebiet unerlässlich. Wenn sie im Rahmen eines Abfallüberwachungsprogramms verwendet und mit spezifischen Kenntnissen über die Umgebung kombiniert werden, helfen die Schlüsselindikatoren, potenzielle Abfallquellen zu identifizieren. {cite}`mlwguidance`
# 
# Auswertungen von Strand-Abfallaufkommen Untersuchungen beschreiben den Ort, die Häufigkeit und die Zusammensetzung der gefundenen Gegenstände {cite}`eubaselines`. Die Schlüsselindikatoren beantworten die folgenden Fragen:
# 
# *  Welche Gegenstände werden gefunden? 
# *  Wie viel wird gefunden? (Gesamtgewichte und Anzahl der Artikel) 
# *  Wie oft werden diese Gegenstände gefunden? 
# *  Wo sind diese Gegenstände in den größten Konzentrationen zu finden? 
#    
# Ähnlich wie bei der Zählung von Vögeln oder Wildblumen muss eine Person die Erhebung durchführen, um die Zielobjekte finden und dann identifizieren. Dieser Prozess ist gut dokumentiert und wurde unter vielen Bedingungen getestet. {cite}`ryan2015` {cite}`Rech`.
# 
# __Indikatoren für die am häufigsten gestellten Fragen__
# 
# Die Schlüsselindikatoren geben Antworten auf die am häufigsten gestellten Fragen zum Zustand der Abfälle in der natürlichen Umwelt. Die Schlüsselindikatoren sind:
# 
# 1. Anzahl der Proben 
# 2. Bestehens- und Misserfolgsquote (Fail-Rate) 
# 3. Anzahl der Objekte pro Meter (pcs/m oder pcs/m²) 
# 4. Zusammensetzung (% der Gesamtmenge) 
# 
# __Annahmen zu den Schlüsselindikatoren:__
# 
# Die Zuverlässigkeit dieser Indikatoren beruht auf den folgenden Annahmen:
# 
# 1. Je mehr Abfallobjekte auf dem Boden liegen, desto größer ist die Wahrscheinlichkeit, dass eine Person sie findet. 
# 2. Die Datenerhebung Ergebnisse stellen die Mindestmenge an Abfallobjekten an diesem Standort dar 
# 3. Die Besichtiger befolgen das Protokoll und zeichnen die Ergebnisse genau auf 
# 4. Für jede Datenerhebung: Das Auffinden eines Artikels hat keinen Einfluss auf die Wahrscheinlichkeit, einen anderen zu finden {cite}`iid`
# 
# Verwendung der Schlüsselindikatoren 
# 
# Die Schlüsselindikatoren der häufigsten Objekte werden mit jeder Datenzusammenfassung auf jeder Aggregationsebene angegeben. Wenn die vorherigen Annahmen beibehalten werden, sollte die Anzahl der Proben in der Region von Interesse immer als Maß für die Unsicherheit betrachtet werden. Je mehr Proben innerhalb definierter geografischer und zeitlicher Grenzen liegen, desto größer ist das Vertrauen in die numerischen Ergebnisse, die aus Ergebnissen innerhalb dieser Grenzen gewonnen werden. 
# 
# ## Definition: die häufigsten Objekte
# 
# _Die am häufigsten vorkommenden Objekte sind die Objekte, die eine Ausfallrate von mindestens 50% haben und/oder in einem bestimmten geografischen Gebiet unter den Top-Ten nach Menge oder Stückzahl/m sind._

# In[2]:


# get your data:
survey_data = pd.read_csv("resources/checked_sdata_eos_2020_21.csv")
dfBeaches = pd.read_csv("resources/beaches_with_land_use_rates.csv")
dfCodes = pd.read_csv("resources/codes_with_group_names_2015.csv")

# set the index of the beach data to location slug
dfBeaches.set_index('slug', inplace=True)

city_map = dfBeaches['city']

# make changes to code def for display
dfCodes.set_index("code", inplace=True)

# language specific
# importing german code descriptions
de_codes = pd.read_csv("resources/codes_german_Version_1.csv")
de_codes.set_index("code", inplace=True)

for x in dfCodes.index:
    dfCodes.loc[x, "description"] = de_codes.loc[x, "german"]

# there is a convenience function to shorten the values of the code description for charting:
# dfCodes = sut.shorten_the_value(["G74", "description", "Insulation: includes spray foams"], dfCodes)

# make a map to the code descriptions
code_description_map = dfCodes.description

# make a map to the code descriptions
code_material_map = dfCodes.material


# ## Die wichtigsten Indikatoren

# In[3]:


dfSurveys = sut.fo_rmat_and_slice_date(survey_data.copy(), a_format="%Y-%m-%d", start_date=start_date, end_date=end_date)
dfSurveys['city'] = dfSurveys.location.map(lambda x: city_map.loc[x])
trb = dfSurveys[dfSurveys.river_bassin == levels['river_bassin']].copy()

# describe the data set:
num_obs = len(trb)
num_samps = len(trb.loc_date.unique())
num_obj = trb.quantity.sum()
num_locs = len(trb.location.unique())

# the city that we are looking at:
biel = trb[trb.city == levels['city']]

# samples at biel
biel_locd = biel.loc_date.unique()

# locations at biel
biel_loc = biel.location.unique()

# example data summary and keys
biel_t = biel.quantity.sum()


# In[4]:


sut.display_image_ipython("resources/maps/survey_areas/aare_scaled.jpeg", thumb=(1200, 700))


# Zwischen dem 2020-03-01 und dem 2020-05-31 wurden bei 140 Erhebungen im Aare-Erhebungsgebiet 13'847 Objekte gesammelt. 

# In[5]:


# the labels for the summary table:
unit_label= 'pcs_m'
fail_rate = 50

# select data
data = trb.groupby(['loc_date','location',  'date'], as_index=False).agg({'pcs_m':'sum', 'quantity':'sum'})

# get the basic statistics from pd.describe
d_aare = data['pcs_m'].describe().round(2)

# add project totals
d_aare['total objects'] = data.quantity.sum()
d_aare['# locations'] = data.location.nunique()

# format table one
aare_table = sut.change_series_index_labels(d_aare, sut.create_summary_table_index(unit_label, lang="DE"))
table_one = sut.fmt_combined_summary(aare_table, nf=[])

# select data
db = biel.groupby(['loc_date','location',  'date'], as_index=False).agg({'pcs_m':'sum', 'quantity':'sum'})

# get the basic statistics from pd.describe
d_biel = db['pcs_m'].describe().round(2)

# add project totals
d_biel['total objects'] = db.quantity.sum()
d_biel['# locations'] = db.location.nunique()

# format table two
biel_table = sut.change_series_index_labels(d_biel, sut.create_summary_table_index(unit_label, lang="DE"))
table_two = sut.fmt_combined_summary(biel_table, nf=[])

# format for time series
months = mdates.MonthLocator(interval=1)
months_fmt = mdates.DateFormatter('%b')
days = mdates.DayLocator(interval=7)

# get the data
dt_all = trb.groupby(['loc_date', 'date'], as_index=False).pcs_m.sum()
bt_all = biel.groupby(['loc_date', 'date'], as_index=False).pcs_m.sum()
monthly_plot = dt_all.set_index('date', drop=True).pcs_m.resample('M').median()

# chart that
fig = plt.figure(figsize=(10, 12))

spec = GridSpec(ncols=8, nrows=18, figure=fig)
axone = fig.add_subplot(spec[0:8,:])
axtwo = fig.add_subplot(spec[9:,0:4])
axthree = fig.add_subplot(spec[9:,4:8])

sns.scatterplot(data=dt_all, x='date', y='pcs_m', color='black', alpha=0.4, label="Aare-Erhebungsgebiet", ax=axone)
sns.scatterplot(data=bt_all, x='date', y='pcs_m', color='red', alpha=0.8, label="Biel/Bienne", ax=axone)
sns.lineplot(data=monthly_plot, x=monthly_plot.index, y=monthly_plot, color='magenta', label=F"Monatsmedian:{level_names[2]}", ax=axone)

the_90th = np.percentile(dt_all.pcs_m, 99)

not_included = F"Werte größer als das 99. Perzentil ({round(the_90th, 2)}) werden nicht angezeigt."

axone.set_ylabel("pcs/m", **ck.xlab_k14)
axone.set_ylim(0,the_90th )
axone.set_title(F"{level_names[2]}, {start_date[:7]} bis {end_date[:7]}, n={num_samps}\n{not_included}",  **ck.title_k)
axone.xaxis.set_minor_locator(days)
axone.xaxis.set_major_formatter(months_fmt)
axone.set_xlabel("")

axtwo.set_xlabel(" ")
sut.hide_spines_ticks_grids(axtwo)
a_col = ["Aare-Erhebungsgebiet", "total"]
table1 = sut.make_a_table(axtwo, table_one,  colLabels=a_col, colWidths=[.5,.25,.25],  bbox=[0,0,1,1], **{"loc":"lower center"})

axthree.set_xlabel(" ")
sut.hide_spines_ticks_grids(axthree)
a_col = ["Biel/Bienne", "total"]
table2 = sut.make_a_table(axthree, table_two,  colLabels=a_col, colWidths=[.5,.25,.25],  bbox=[0,0,1,1], **{"loc":"lower center"})

plt.show()


# ### Die Anzahl der Proben
# 
# Die Anzahl der Proben bezieht sich auf die Anzahl der Proben innerhalb eines geografischen und zeitlichen Bereichs. Wie bereits erwähnt, kann den Ergebnissen der Analyse umso mehr Vertrauen geschenkt werden, je mehr Proben innerhalb eines bestimmten Gebiets und Zeitraums vorhanden sind. 
# 
# ### Die Fail-Rate
# 
# Die Fail-Rate ist die Anzahl der Fälle, in denen ein Objekt mindestens einmal gefunden wurde, geteilt durch die Anzahl der Datenerhebungen.  
# 
# **Was bedeutet das?** Die Fail-Rate beschreibt den Prozentsatz der Fälle, in denen eine Kategorie im Verhältnis zur Anzahl der durchgeführten Datenerhebungen identifiziert wurde. 
# 
# > Verwenden Sie die Fail-Rate, um festzustellen, wie häufig ein Objekt innerhalb eines geografischen Bereichs gefunden wurde. Objekte können anhand der Fail-Rate unterschieden werden. Verwenden Sie die Fail-Rate und pcs/m, um Objekte zu identifizieren, die nur selten, aber in großen Mengen gefunden werden. 
# 
# __Unterschiedliche Fail-Raten auf verschiedenen Ebenen__
# 
# Die Fail-Rate wird auf jeder Aggregationsebene berechnet. Daher ändert sich die Fail-Rate für ein bestimmtes Objekt je nach den geografischen Grenzen, die die Aggregationsebene definieren. Betrachten Sie alle Objekte, die bei mindestens 1/2 Erhebungen im Aare-Erhebungsgebiet gefunden wurden. 
# 
# _Aare-Umfragebereich alle Artikel, die eine Fehlerquote von mehr als 49,999 haben._

# In[6]:


# identify the most common and the most abundant objects in the river bassin
trb_mc = trb.groupby(['loc_date','code'], as_index=False).agg({'fail':'sum', 'quantity':'sum', unit_label:'sum'})
trb_mcom = trb_mc.groupby('code', as_index=False).agg({'fail':'sum', 'quantity':'sum', unit_label:'median'})

# get the fail rate and separate the data into most common and most abundant
trb_mcom['f_r'] = trb_mcom.fail/trb.loc_date.nunique()

# most common
trb_grt50 = trb_mcom[trb_mcom.f_r >= fail_rate]

# top ten
trb_pcs = trb_mcom.sort_values(by='quantity', ascending=False)

# codes from each
c_grt50 = trb_grt50.code.unique()
c_qty = trb_pcs.code.unique()[:10]

# joint list
thecommon = list(set(c_grt50) | set(c_qty))

biel_fail = biel[biel.code.isin(thecommon)].groupby('code', as_index=False).fail.sum()
biel_fail['rate'] = biel_fail.fail/biel.loc_date.nunique()
bf = biel_fail.sort_values(by='rate', ascending=False)
m_common = bf.copy()

# map the desctiption to the code
m_common['item'] = m_common.code.map(lambda x: code_description_map.loc[x])
m_common['label'] = 'Biel/Bienne'

# pivot that
mcp = m_common[['item', 'rate', 'label']].pivot(columns='label', index='item')

# quash the hierarchal column index
mcp.columns = mcp.columns.get_level_values(1)

group = ["loc_date", "code"]

def make_total_colums(df,name="Alle Erhebungsgebiete", new_col_name="pt", desc="item", agg_col="quantity"):
    a_s_a = df.groupby('code', as_index=False)[agg_col].sum()
    a_s_a[new_col_name] = a_s_a.quantity/dfSurveys.quantity.sum()
    a_s_a[desc] = a_s_a.code.map(lambda x: code_description_map.loc[x])
    a_s_a.set_index(desc, inplace=True)
    a_s_a[name] = a_s_a[new_col_name]
    
    return a_s_a[name]

def make_median_colums(df,name="Alle Erhebungsgebiete", new_col_name="p", desc="item", agg_col="pcs_m"):
    b_s_a = df.groupby('code', as_index=False)[agg_col].median()
    b_s_a[desc] = b_s_a.code.map(lambda x: code_description_map.loc[x])
    b_s_a.set_index(desc, inplace=True)
    b_s_a[name] = b_s_a[agg_col]
    
    return b_s_a[name]

def make_fail_rate_columns(df, fails, name="Alle Erhebungsgebiete", new_col_name="rate", desc="item", agg_col="pcs_m"):
    data = fails.copy()
    bsee_samps = df.loc_date.nunique()
    data[new_col_name] = data.fail/bsee_samps
    b_s_a = data.sort_values(by=new_col_name, ascending=False)
    b_s_a[desc] = b_s_a.code.map(lambda x: code_description_map.loc[x])
    b_s_a.set_index(desc, inplace=True)
    b_s_a[name] = b_s_a[new_col_name]
    
    return b_s_a[name]

# the aggregated totals for the lake
b_s_ax = trb[(trb.code.isin(thecommon ))&(trb.water_name_slug == 'bielersee')].groupby('code', as_index=False).fail.sum()
b_s_a_col = make_fail_rate_columns(trb[(trb.code.isin(thecommon ))&(trb.water_name_slug == 'bielersee')], b_s_ax, name= "Bielersee")

# the aggregated totals for the survey area
t_s_ax = trb[(trb.code.isin(thecommon ))].groupby('code', as_index=False).fail.sum()
t_s_a_col = make_fail_rate_columns(trb[(trb.code.isin(thecommon ))], t_s_ax, name= "Aare-Erhebungsgebiet")

# repeat for all the survey areas
a_s_ax = dfSurveys[(dfSurveys.code.isin(thecommon ))].groupby('code', as_index=False).fail.sum()
a_s_a_col = make_fail_rate_columns(dfSurveys[(dfSurveys.code.isin(thecommon ))], a_s_ax)

# combine into one matrix
ad_t_ten = pd.concat([mcp, b_s_a_col, t_s_a_col, a_s_a_col], axis=1).sort_values(by='Biel/Bienne', ascending=False)

# chart that
fig, ax  = plt.subplots(figsize=(len(ad_t_ten.columns)*.9,len(ad_t_ten)*.9))
axone = ax

sns.heatmap(ad_t_ten, ax=axone, cmap=cmap2, annot=True, annot_kws={"fontsize":12}, fmt=".0%", square=True, cbar=False, linewidth=.1, linecolor='white')

axone.set_ylabel("")
axone.tick_params(labelsize=10, which='both', axis='y')
axone.tick_params(labelsize=14, which='both', axis='x')

plt.setp(axone.get_xticklabels(), rotation=90)

plt.show()
plt.close()


# Mit Ausnahme von Industriefolien und Kunststofffragmenten war die Fehlschlagquote in Biel/Bienne höher als in allen anderen Untersuchungsgebieten. Das bedeutet, dass die Wahrscheinlichkeit, diese Objekte zu finden, in Biel pro Untersuchung größer war als an den meisten anderen Orten. 
# 
# Die Pass-Fail-Rate ist die wahrscheinlichste Schätzung (MLE) der Wahrscheinlichkeit, mindestens ein Objekt zu finden {cite}`mle`. Wenn das Objekt in allen vorherigen Stichproben identifiziert wurde und sich die Abschwächung der Präventionsmaßnahmen nicht geändert hat, kann man davon ausgehen, dass auch in den folgenden Stichproben mindestens ein Objekt zu finden sein wird. 
# 
# __Hinweis:__ Die Fail-Rate gibt keinen Hinweis auf die Menge 

# ### Stücke pro Meter
# 
# Stücke pro Meter (pcs/m) ist die Anzahl der bei jeder Untersuchung gefundenen Objekte geteilt durch die Länge der untersuchten Uferlinie. 
# 
# **Was bedeutet das?** pcs/m beschreibt die Menge eines Objekts, das pro Meter vermessenen Strandufer Abschnitts gefunden wurde. Es handelt sich um eine Methode zur Normalisierung der Daten aus allen Vermessungen, damit sie verglichen werden können. 
# 
# > Verwenden Sie Stücke pro Meter, um die Objekte zu finden, die in den größten Mengen gefunden wurden. Verwenden Sie Stücke pro Meter, um Zonen der Anhäufung zu identifizieren.
# 
# _Warum nicht die Fläche verwenden? Der empfohlene EU-Standard besteht darin, die Ergebnisse als Anzahl der Objekte pro Länge der untersuchten Küstenlinie anzugeben, normalerweise 100 Meter {cite}`eubaselines`. Die Fläche wurde für 99% aller Erhebungen in IQAASL berechnet. Die Ergebnisse für diese Analyse werden in pcs/m angegeben._
# 
# _Aare-Untersuchungsgebiet: der Median der pcs/m der häufigsten Objekte_

# In[7]:


# aggregated survey totals for the most common codes for all the water features
# a common aggregation
agg_pcs_quantity = {unit_label:'sum', 'quantity':'sum'}

m_common_st = biel[biel.code.isin(thecommon)].copy()

m_common_ft = m_common_st.groupby(['code'], as_index=False)[unit_label].median()

m_common_ft = m_common_ft.sort_values(by=unit_label, ascending=False)

# proper name of water feature for display
m_common_ft['f_name'] = 'Biel/Bienne'

# map the desctiption to the code
m_common_ft['item'] = m_common_ft.code.map(lambda x: code_description_map.loc[x])

# pivot that
m_c_p = m_common_ft[['item', unit_label, 'f_name']].pivot(columns='f_name', index='item')

# quash the hierarchal column index
m_c_p.columns = m_c_p.columns.get_level_values(1)

# the aggregated totals for the lake
b_s_ax = trb[(trb.code.isin(thecommon))&(trb.water_name_slug == 'bielersee')].groupby(group, as_index=False).agg(agg_pcs_quantity)
b_s_a_col = make_median_colums(b_s_ax, name="Bielersee")

# the aggregated totals for the survey area
t_s_ax = trb[(trb.code.isin(thecommon))].groupby(group, as_index=False).agg(agg_pcs_quantity)
t_s_a_col = make_median_colums(t_s_ax, name="Aare-Erhebungsgebiet")

# repeat for all the survey areas
a_s_ax = dfSurveys[dfSurveys.code.isin(thecommon)].groupby(group, as_index=False).agg(agg_pcs_quantity)
a_s_a_col = make_median_colums(a_s_ax)

# combine into one matrix
ad_t_ten = pd.concat([m_c_p, b_s_a_col, t_s_a_col, a_s_a_col], axis=1).sort_values(by='Biel/Bienne', ascending=False)

# chart that
fig, ax  = plt.subplots(figsize=(len(ad_t_ten.columns)*.9,len(ad_t_ten)*.9))

axone = ax

sns.heatmap(ad_t_ten, ax=axone, cmap=cmap2, annot=True, annot_kws={"fontsize":12}, fmt=".2f", square=True, cbar=False, linewidth=.1, linecolor='white')

axone.set_ylabel("")
axone.tick_params(labelsize=10, which='both', axis='y')
axone.tick_params(labelsize=14, which='both', axis='x')

plt.setp(axone.get_xticklabels(), rotation=90)

plt.show()
plt.close()


# Der gemeldete Wert ist der Median der Datenerhebung Ergebnissen für diese Aggregationsebene und dieses Objekt. Ein Medianwert von Null bedeutet, dass das Objekt in weniger als 1/2 Datenerhebungen für diese Aggregationsebene identifiziert wurde. Betrachten Sie zum Beispiel die Ergebnisse für Isoliermaterial: umfasst Sprühschäume. Der Medianwert für das Aare-Erhebungsgebiet ist Null. Wenn jedoch nur die Ergebnisse von Bielersee oder Biel/Bienne betrachtet werden, ist der Medianwert größer als Null. Das deutet darauf hin, dass am Bielersee und speziell in Biel/Bienne mehr Dämmstoffe gefunden wurden als im übrigen Aaregebiet. 

# ####  Prozentsatz der Gesamt
# 
# Der prozentuale Anteil an der Gesamtzahl ist die Menge eines gefundenen Objekts geteilt durch die Gesamtzahl aller gefundenen Objekte für einen bestimmten Ort/Region und Datumsbereich. 
# 
# **Was bedeutet das?** TDer prozentuale Anteil an der Gesamtmenge beschreibt die Zusammensetzung des gefundenen Abfallobjekten.
# 
# > Verwenden Sie den prozentualen Anteil an der Gesamtmenge, um die wichtigsten Abfallobjekten zu definieren. Verwenden Sie den prozentualen Anteil an der Gesamtmenge, um Prioritäten auf regionaler Ebene zu ermitteln.
# 
# Ähnlich wie bei den Stücken pro Meter ist ein Objekt mit einer niedrigen Pass-Fail-Rate und einem hohen Prozentsatz an der Gesamtzahl ein Signal dafür, dass Objekte möglicherweise in unregelmäßigen Abständen in großen Mengen deponiert werden: Verklappung oder Unfälle. 

# In[8]:


ac = biel[biel.code.isin(thecommon)].groupby('code', as_index=False).quantity.sum()
accounted_total = ac.quantity.sum()
ac.sort_values(by='quantity', ascending=False, inplace=True)

bsee = ac.copy()
bsee['pt'] = ac.quantity/biel.quantity.sum()
these_codes = bsee.sort_values(by='pt', ascending=False).code.unique()
bsee.sort_values(by='pt', ascending=False, inplace=True)
bsee['item'] = bsee.code.map(lambda x: code_description_map.loc[x])
bsee.set_index('item', inplace=True)
bsee['Biel/Bienne'] = bsee['pt']

# the aggregated totals for the lake
b_s_ax = trb[(trb.code.isin(these_codes))&(trb.water_name_slug == 'bielersee')].groupby(group, as_index=False).agg(agg_pcs_quantity)
b_s_a_col = make_total_colums(b_s_ax,name='Bielersee')

# the aggregated totals for the river bassin
t_s_ax = trb[(trb.code.isin(these_codes))].groupby(group, as_index=False).agg(agg_pcs_quantity)
ts_a_col = make_total_colums(t_s_ax,name="Aare-Erhebungsgebiet")

# repeat for all the survey areas
a_s_ax = dfSurveys[dfSurveys.code.isin(these_codes)].groupby(group, as_index=False).agg(agg_pcs_quantity)
a_s_a_col = make_total_colums(a_s_ax)

# combine the totals
ad_t_ten = pd.concat([bsee['Biel/Bienne'], b_s_a_col, ts_a_col, a_s_a_col], axis=1).sort_values(by='Biel/Bienne', ascending=False)


# *Die häufigsten Objekte im Untersuchungsgebiet der Aare sind  rund 66% (2'022) der Gesamtzahl der erfassten Objekte (3.067) an den drei Standorten in Biel/Bienne*

# In[9]:


# chart that
fig, ax  = plt.subplots(figsize=(len(ad_t_ten.columns)*.9,len(ad_t_ten)*.9))
axone = ax

sns.heatmap(ad_t_ten, ax=axone, cmap=cmap2, annot=True, annot_kws={"fontsize":12}, fmt=".0%", square=True, cbar=False, linewidth=.1, linecolor='white')

axone.set_ylabel("")
axone.tick_params(labelsize=14, which='both', axis='both')

plt.setp(axone.get_xticklabels(), rotation=90)
axone.tick_params(labelsize=10, which='both', axis='y')
axone.tick_params(labelsize=14, which='both', axis='x')

plt.show()
plt.close()


# ### Diskussion
# 
# Zwischen April 2020 und Mai 2021 wurden 16 Strand-Abfallaufkommen Datenerhebungen an drei verschiedenen Orten in Biel/Bienne durchgeführt, bei denen 3.067 Objekte identifiziert werden konnten. Die häufigsten Objekte aus dem Aare-Erhebungsgebiet machen 66% aller in Biel identifizierten Objekte aus. Objekte, die in direktem Zusammenhang mit dem Konsum stehen (Lebensmittel, Getränke, Tabak), werden in einer Häufigkeit gefunden, die über dem Median des Erhebungsgebiets liegt, den diese Objekte stellen rund 34% der gesammelten Abfallobjekte in Biel/Bienne dar, im Vergleich zu 25% für alle Untersuchungsgebiete. 
# 
# Gegenstände, die nicht direkt mit Konsumverhalten in Verbindung stehen, wie zerbrochene Kunststoffe, Industriefolien, expandiertes Polystyrol oder Industriepellets, werden in größeren Mengen gefunden als im übrigen Aare-Erhebungsgebiet. Expandiertes Polystyrol wird als äußere Isolierhülle für Gebäude (Neubauten und Renovierungen) und zum Schutz von Bauteilen beim Transport verwendet. Biel hat eine starke industrielle Basis und eine aktive Bau- und Produktionsbasis. Zusammengenommen machen diese Objekte 30% der insgesamt gesammelten Objekte aus. 
# 
# #### Anwendung 
# 
# Die Schlüsselindikatoren sind einfache Verhältnisse, die direkt aus den Datenerhebung Ergebnissen entnommen werden. Änderungen in der Größenordnung dieser Verhältnisse signalisieren Änderungen in der relativen Menge bestimmter Objekte. Wenn die Schlüsselindikatoren im Rahmen eines Überwachungsprogramms verwendet werden, ermöglichen sie die Identifizierung wahrscheinlicher Anreicherungszonen. 
# 
# ###  Praktische Übung
# 
# Industrielle Kunststoffgranulate (GPI) sind das wichtigste Material zur Herstellung von Kunststoffgegenständen, die in der Schweiz in großem Umfang verwendet werden. Sie sind scheiben- oder pelletförmig und haben einen Durchmesser von 5mm. 
# 
# Beantworten Sie anhand der folgenden Datenerhebung Ergebnissen, der Karte mit den Datenerhebungs Standorten und unter Beibehaltung der zu Beginn dieses Artikels vorgestellten Annahmen die folgenden Fragen: 
# 
# 1. Wo besteht die größte Wahrscheinlich, mindestens ein Vorkommen des Abfallobjekts zu finden? 
# 2. Wie groß ist die wahrscheinliche Mindestmenge an Pellets, die Sie bei einer Untersuchung von 50 Metern finden würden? 
# 3. Warum haben Sie sich für diesen Ort oder diese Orte entschieden? Wie sicher sind Sie sich bei Ihrer Wahl? 

# In[10]:


aggs = {'loc_date':'nunique', 'fail':'sum', 'pcs_m':'mean', "quantity":"sum"}
new_col_names = {"loc_date":"Proben", "fail":"# fail", "pcs_m":"median pcs/m", "quantity":"# gefunden"}

biel_g95 = dfSurveys[(dfSurveys.water_name_slug == levels['water_name_slug'])&(dfSurveys.code == 'G112')].groupby(['location']).agg(aggs)
biel_g95.rename(columns=new_col_names, inplace=True)

biel_g95


# <br></br>

# In[11]:


sut.display_image_ipython("resources/maps/key_indicators.jpeg", thumb=(1200, 700))

