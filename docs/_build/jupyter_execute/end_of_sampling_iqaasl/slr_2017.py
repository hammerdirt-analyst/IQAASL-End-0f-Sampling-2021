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
import statsmodels.api as sm
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
import resources.utility_functions as ut
import resources.abundance_classes as ac
import resources.chart_kwargs as ck

import resources.sr_ut as sut

# images and display
import base64, io, IPython
from PIL import Image as PILImage
from IPython.display import Markdown as md
from IPython.display import display, Math, Latex

# set some parameters:
today = dt.datetime.now().date().strftime("%Y-%m-%d")
start_date = '2015-11-01'
end_date ='2021-05-31'

unit_label = 'p/100m'

unit_value = 100

fail_rate = 50

# colors for gradients
colors = ['beige', 'navajowhite', 'sandybrown', 'salmon', 'sienna']
nodes = [0.0, 0.2, 0.6, 0.8, 1.0]
cmap2 = LinearSegmentedColormap.from_list("mycmap", list(zip(nodes, colors)))

# name of the output folder:
name_of_project = 'time_series_2017_2020'

# add the folder to the directory tree:
project_directory = ut.make_project_folder('output', name_of_project)

# get your data:
survey_data = pd.read_csv('resources/agg_results_with_land_use_2015.csv')
river_bassins = ut.json_file_get("resources/river_basins.json")
dfBeaches = pd.read_csv("resources/beaches_with_land_use_rates.csv")
dfCodes = pd.read_csv("resources/codes_with_group_names_2015.csv")

# set the index of the beach data to location slug
dfBeaches.set_index('slug', inplace=True)

# map locations to feature names
location_wname_key = dfBeaches.water_name_slug

# map water_name_slug to water_name
wname_wname = dfBeaches[['water_name_slug','water_name']].reset_index(drop=True).drop_duplicates()
wname_wname.set_index('water_name_slug', inplace=True)

# map water name slug to type
wname_type = dfBeaches[["water_name_slug", "water"]].reset_index(drop=True).drop_duplicates()
# water_type_map = wname_type.set_index('water_name_slug', drop=True)

# convenience function for doing land use correlations
def make_plot_with_spearmans(data, ax, n):
    sns.scatterplot(data=data, x=n, y=unit_label, ax=ax, color='black', s=30, edgecolor='white', alpha=0.6)
    corr, a_p = stats.spearmanr(data[n], data[unit_label])
    return ax, corr, a_p

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


# # More and less trash since 2017
# 
# __The Swiss Litter Report April 2017 - March 2018__
# 
# The Swiss Litter Report (SLR) was a project intiated by Gabriele Kuhl of STOPPP.ch and supported by the World Wildlife Fund Switzerland (WWF). The protocol was bassed on the GMML, the project was managed by the WWF and the surveys were conducted by volunteers from both organizations. Starting in April 2017 and running to March 2018 the SLR covered much of the national territory with the exception of Ticino.
# 
# Between April 2017 and March 2018 1,052 samples were taken from 112 locations in the Swiss Litter Report. More than 150 trained volunteers from 81 municipalities collected and categorized 98,474 pieces of trash from the shores of 48 lakes and 67 rivers in Switzerland. {cite}`slr`
# 
# ## Scope of projects SLR - IQAASL

# In[2]:


# make sure date is time stamp
survey_data['date'] = pd.to_datetime(survey_data['date'], format='%Y-%m-%d')

# identify any misnamed river bassin or survey area ids
na_bassins = survey_data[survey_data.river_bassin == '0'].copy()

# keep the river bassins that are valid
valid_bassins = survey_data[survey_data.river_bassin != '0'].copy()

# get only the water features that were sampled in 2020
after_2020 = valid_bassins[valid_bassins.date >= '2020-01-01'].water_name_slug.unique()
a_data = survey_data[survey_data.water_name_slug.isin(after_2020)]

# get rid of a duplicate sample and codes that were not counted in 2017
a_data = a_data[(a_data.location != "lac-leman-hammerdirt")&(~a_data.code.isin(['G81', 'G78','G74', 'G112']))]

# convert pcs-m to p/100m
a_data['pcs_m'] = a_data.pcs_m * unit_value
a_data['pcs_m'] = a_data.pcs_m.astype('int')
a_data.rename(columns={'pcs_m':unit_label}, inplace=True)

# the date ranges of two projects
first_date_range = (a_data.date >= "2017-04-01")&(a_data.date <= "2018-03-31")
second_date_range = (a_data.date >= "2020-04-01")&(a_data.date <= "2021-03-31")

# a df for each set
slr_data = a_data[first_date_range].copy()
iqasl_data = a_data[second_date_range].copy()

# only use codes identified in the first project
these_codes = slr_data[slr_data.quantity > 0].code.unique()

# add a survey year column to each data set
iqasl_data['survey year'] = '2020'
slr_data['survey year'] = '2017'

# put the two sets of data back together
combined_data = pd.concat([iqasl_data, slr_data])
combined_data['length'] = (combined_data.quantity/combined_data[unit_label])*unit_value

# unique locations in both years
sdlocs = slr_data.location.unique()
iqs = iqasl_data.location.unique()

# locations common to both
both_years = list(set(sdlocs).intersection(iqs))

# locations specific to each year
just_2017 = [x for x in sdlocs if x not in iqs]
j_2020 = [x for x in iqs if x not in sdlocs]

# lakes that have samples in both years
these_lakes = ["zurichsee", "bielersee", "lac-leman", "neuenburgersee", "walensee", "thunersee"]

# make a points layer for gos
geo_output = dfBeaches.loc[set([*iqs, *sdlocs])].copy()
geo_output['samp_year'] = " "
geo_output.loc[geo_output.index.isin(just_2017), 'samp_year'] = '2017'
geo_output.loc[geo_output.index.isin(both_years), 'samp_year'] = 'Both'
geo_output.loc[geo_output.index.isin(j_2020), 'samp_year'] = '2020'

geo_output[["location", "latitude", "longitude", 'samp_year', 'water_name_slug']][~geo_output.water_name_slug.isin(['lago-maggiore', 'ticino', 'moesa'])].to_csv(F"{project_directory}/slr_iqaals.csv", index=True)


# In[3]:


bassin_map = PILImage.open("resources/maps/slr_iqasl.jpeg")

output = io.BytesIO()
bassin_map.thumbnail((1200, 800))
bassin_map.save(output, format='PNG')
encoded_string = base64.b64encode(output.getvalue()).decode()

html = '<img src="data:image/png;base64,{}"/>'.format(encoded_string)
IPython.display.HTML(html)


# ### Land use profile of survey locations
# 
# The land use profile is the measurable properties that are geolocated and can be extracted from the current versions of *Statistique Suisse de la superficie* {cite}`superficie` and *swissTlmRegio* {cite}`tlmregio`. The following values were calculated within a radius of 1500m of each survey location:
# 
# 1. \% of surface area attributed to buildings
# 2. \% of surface area left to woods
# 3. \% of surface area attributed to outdoor activities
# 4. \% of surface area attributed to aggriculture
# 5. length in meters of all roadways 
# 6. number of river discharge intersections
# 
# As of June 22, 2021 the land use data for Walensee was not up to date. It has been estimated by visually inspecting the relevant map layers and comparing land use rates to other locations that have a similar population.See the section on land use features for a detailed description of the method of calcualtion.

# In[4]:


# use only the codes identified in 2017, the protocol only called for certain MLW codes
df = combined_data[combined_data.code.isin(these_codes)].copy()

# scale the streets value
df['streets km'] = df.streets/1000

# a common aggregation
agg_pcs_quantity = {unit_label:'sum', 'quantity':'sum'}

# referene columns
use_these_cols = ['survey year','loc_date' ,'% to buildings', '% to trans', '% to recreation', '% to agg', '% to woods','population','water_name_slug','streets km', 'intersects', 'groupname','code']

# !!walensee landuse is approximated by comparing the land use profile from similar locations!!
# the classification for that part of switzerland is incomplete for the current estimates
# the previous one is 15 years old
# the land use profile of wychely - brienzersee was used for walenstadt-wyss (more prairie, buildings less woods)
# the land use profile of grand-clos - lac-leman was used for other locations on walensee (more woods, less buildings, less praire and agg)
luse_wstdt = dfBeaches.loc['wycheley'][['population','% to buildings', '% to trans', '% to recreation', '% to agg', '% to woods']]
estimate_luse = dfBeaches.loc['grand-clos'][['population','% to buildings', '% to trans', '% to recreation', '% to agg', '% to woods']]

# seperate out the locations that aren't walenstadt
wlsnsee_locs_not_wstdt = ['gasi-strand', 'untertenzen', 'mols-rocks', 'seeflechsen', 'seemuhlestrasse-strand', 'muhlehorn-dorf', 'murg-bad', 'flibach-river-right-bank']

for a_param in estimate_luse.index:
    df.loc[df.location.isin(wlsnsee_locs_not_wstdt), a_param] = estimate_luse[a_param]
    df.loc['walensee_walenstadt_wysse', a_param] = luse_wstdt[a_param]
    
dfdt = df.groupby(use_these_cols[:-2], as_index=False).agg(agg_pcs_quantity)

# explanatory variables:
luse_exp = ['% to buildings', '% to recreation', '% to agg', '% to woods', 'streets km', 'intersects']

# chart the distribtuion of survey results with respect to the land use profile
fig, axs = plt.subplots(1, len(luse_exp), figsize=(14,4), sharey='row')

data=dfdt[(dfdt['survey year'] == '2017')].groupby(use_these_cols[:-2], as_index=False).agg({'p/100m':'sum', 'quantity':'sum'})
data2=dfdt[(dfdt['survey year'] == '2020')].groupby(use_these_cols[:-2], as_index=False).agg({'p/100m':'sum', 'quantity':'sum'})

for i, n in enumerate(luse_exp):
    ax=axs[i]
    the_data = ECDF(data[n].values)
    x, y = the_data.x, the_data.y
    
    the_data2 = ECDF(data2[n].values)
    x2, y2 = the_data2.x, the_data2.y
    
    
    sns.lineplot(x=x, y=y, ax=ax, color='magenta', label="SLR")
    sns.lineplot(x=x2, y=y2,ax=ax, color='dodgerblue', label="IQAASL")
    if i == 0:
        handles, labels=ax.get_legend_handles_labels() 
        ax.legend(handles, labels, loc='upper left')
        ax.set_ylabel("Percent of samples", **ck.xlab_k)
    else:
        ax.get_legend().remove()
    ax.set_xlabel(n, **ck.xlab_k)
    
handles, labels=ax.get_legend_handles_labels() 
ax.legend(handles, labels, loc='lower right')

plt.tight_layout()
plt.show()


# *Distribution of number of surveys results with respect to land use profile SLR - IQAASL* 
# <br></br>

# For both projects 50% of the samples had less than ~36% of land attributed to buildings,  less than ~5% attributed to recreation and less than ~10% attributed to woods or forest. In 2017 50% of the samples had less than ~25% of land attributed to agriculture versus ~14% for 2020. 
# 
# The length of the road network within the buffer zone differentiates between locations that have other wise similar land use characteristics. The range of the road network inside each 1500m buffer was 32km to 156km. In both years 50% of the samples came from locations that had 63km of roads or less within 1500m of the survey location. 
# 
# The number of river or canal intersections ranges from zero to 16, 50% of the surveys had 3 or fewer intersections within 1500m of the survey location in both years. The size of the intersecting river or canal was not taken into consideration. Survey locations on rivers have zero intersections.
# 
# The population (not shown) is taken from statpop 2018<sup>28</sup> and represents the population of the municipality surounding the survey location. The smallest population was 442 and the largest was 415,357. At least 50% of the samples came from municipalities with a population of ~13000 or less.
# 
# If % of land use attributed to agriculture is a sign of urbanization then the survey areas in 2020 were slightly more urban than 2017. 

# ## Results lakes and rivers

# Considering only the lakes and rivers that have samples in both years there were more samples and more trash was collected from fewer locations in 2017 than 2020. However, on a pieces per meter basis the mean, median and maximum were all higher in 2020. The difference is slight and in real terms is less than 30 pieces of trash per 100m, differences of this magnitude may not be immediately discernible to the casual observer.
# 
# Both sets of survey results are at their minimum in November through February(LOWS) and reach a maximum in April through July(HIGHS). This seasonality was noted previouslly in the SLR and in other studies outside of Switzerland. The monthly difference is greatest in August at 93pcs/100m. 

# ### Distribution of results 2017 and 2020

# *__Top Left:__ survey totals by date, __Top right:__ median monthly survey total* 

# In[5]:


# group by survey and sum all the objects for each survey AKA: survey total
data=df.groupby(['loc_date', 'date', 'survey year'], as_index=False)[unit_label].sum()

# get the ecdf for both projects
ecdf_2017 = ECDF(data[data['survey year'] == '2017'][unit_label].values)
ecdf_2020 = ECDF(data[data['survey year'] == '2020'][unit_label].values)

# convenience func and dict to display table values
change_names = {'count':'# samples', 'mean':F"average {unit_label}", 'std':'standard deviation', 'min':F"min {unit_label}",  '25%':'25%',  '50%':'50%', '75%':'75%', 'max':F"max {unit_label}", 'min':'min p/100', 'total objects':'total objects', '# locations':'# locations', 'survey year':'survey year'}

# group by survey year and use pd.describe to get basic stats
som_1720 = data.groupby('survey year')[unit_label].describe().round(2)

# add total quantity and number of unique locations
som_1720['total objects'] = som_1720.index.map(lambda x: df[df['survey year'] == x].quantity.sum())
som_1720['# locations'] = som_1720.index.map(lambda x: df[df['survey year'] == x].location.nunique())

# make columns names more descriptive
som_1720.rename(columns=(change_names), inplace=True)
ab = som_1720.reset_index()

# melt that on survey year
c_s = ab.melt(id_vars=['survey year'])

# pivot on survey year
combined_summary = c_s.pivot(columns='survey year', index='variable', values='value').reset_index()

# format for printing
combined_summary['2017'] = combined_summary['2017'].map(lambda x: F"{int(x):,}")
combined_summary['2020'] = combined_summary['2020'].map(lambda x: F"{int(x):,}")

# change the index to date
data.set_index('date', inplace=True)

# get the median monthly value
monthly_2017 = data.loc[data['survey year'] == '2017']['p/100m'].resample('M').median()
# change the date to the name of the month for charting
months_2017 = pd.DataFrame({'month':[dt.datetime.strftime(x, "%b") for x in monthly_2017.index], unit_label:monthly_2017.values})

# repeat for 2020
monthly_2020 = data.loc[data['survey year'] == '2020']['p/100m'].resample('M').median()
months_2020 = pd.DataFrame({'month':[dt.datetime.strftime(x, "%b") for x in monthly_2020.index], unit_label:monthly_2020.values})

# set the date intervas for the chart
months = mdates.MonthLocator(interval=1)
months_fmt = mdates.DateFormatter('%b')
years = mdates.YearLocator()

sns.set_style("whitegrid")

this_palette = {"2020":"dodgerblue", "2017":"magenta"}

the_90th = np.percentile(data['p/100m'], 95)

fig, ax = plt.subplots(2,2, figsize=(14,9), sharey=False)

axone=ax[0,0]
axtwo = ax[0,1]
axthree = ax[1,0]
axfour = ax[1,1]

axone.set_ylabel(unit_label, **ck.xlab_k14)
axone.xaxis.set_minor_locator(months)
axone.xaxis.set_major_locator(years)
axone.set_xlabel(" ")

axtwo.set_xlabel(" ")
axtwo.set_ylabel(unit_label, **ck.xlab_k14)
axtwo.set_ylim(-10, the_90th)

axthree.set_ylabel("# of samples", **ck.xlab_k14)
axthree.set_xlabel(unit_label, **ck.xlab_k)

axfour.set_ylabel("% of samples", **ck.xlab_k14)
axfour.set_xlabel(unit_label, **ck.xlab_k)

# histogram data:
data_long = pd.melt(data[['survey year', 'loc_date', unit_label]],id_vars=["survey year","loc_date"], value_vars=(unit_label,), value_name="survey total")
data_long['year_bin'] = np.where(data_long['survey year'] == '2017', 0, 1)

# scatter plot of surveys both years
sns.scatterplot(data=data, x='date', y='p/100m', color='red', s=34, ec='white',label="survey total", hue='survey year', palette= this_palette, ax=axone)
axone.legend(loc='upper center')

# monthly median
sns.lineplot(data=months_2017, x='month', y=unit_label, color='magenta', label=F"Monthly median:2017", ax=axtwo)
sns.lineplot(data=months_2020, x='month', y=unit_label, color='dodgerblue', label=F"Monthly median:2020", ax=axtwo)

# histogram
sns.histplot(data=data_long, x='survey total', hue='survey year', stat='count', multiple='stack',palette=this_palette, ax=axthree, bins=[x*20 for x in np.arange(80)])

# empirical cumulative distribution
sns.lineplot(x=ecdf_2017.x, y=ecdf_2017.y, ax=axfour, color='magenta', label="survey results 2017")
sns.lineplot(x=ecdf_2020.x, y=ecdf_2020.y, ax=axfour, color='dodgerblue', label="survey results 2020")

axfour.xaxis.set_major_locator(ticker.MultipleLocator(1000)) 
axfour.xaxis.set_minor_locator(ticker.MultipleLocator(100)) 

axfour.legend(loc="center right")
axfour.tick_params(which="both", bottom=True)
axfour.grid(b=True, which='minor',linewidth=0.5)

plt.show()


# *__bottom Left:__ number of samples with respect to the survey total, __bottom right:__ empirical cumulative distribution of survey totals* 

# ### Summary data and material types 2017 and 2020

# *__Left:__ summary of survey totals, __right:__ material type*

# In[6]:


# material totals
mat_total = df.groupby(['survey year', 'code'], as_index=False).quantity.sum()
# add material type:
mat_total['mat'] = mat_total.code.map(lambda x:code_material_map.loc[x])

# the most common codes for each year
mat_total = mat_total.groupby(['survey year', 'mat'], as_index=False).quantity.sum()

# get the % of total and fail rate for each object from each year
# add the yearly total column
mat_total.loc[mat_total['survey year'] == '2017', 'yt'] = mat_total[mat_total['survey year'] == '2017'].quantity.sum()
mat_total.loc[mat_total['survey year'] == '2020', 'yt'] = mat_total[mat_total['survey year'] == '2020'].quantity.sum()

# get % of total
mat_total['pt'] =((mat_total.quantity/mat_total.yt)*100).round(2)

# format for printing:
mat_total['pt'] = mat_total.pt.map(lambda x: F"{x}%")
mat_total['quantity'] = mat_total.quantity.map(lambda x: F"{x:,}")

m_t = mat_total[['survey year','mat', 'quantity', 'pt']].pivot(columns='survey year', index='mat', values='pt').reset_index()
m_t.rename(columns={'mat':'material', 'pt':'% of total'}, inplace=True)

# put that in a table
fig, axs = plt.subplots(1, 2, figsize=(10,6))

axone = axs[0]
axtwo= axs[1]

ut.hide_spines_ticks_grids(axone)
ut.hide_spines_ticks_grids(axtwo)

# summary data table
a_table = axone.table(cellText=combined_summary.values,  colLabels=combined_summary.columns, colWidths=[.5,.25,.25], loc='lower center', bbox=[0,0,1,1])
the_material_table_data = sut.make_a_summary_table(a_table,combined_summary,combined_summary.columns, s_et_bottom_row=True)

# material totals
a_table = axtwo.table(cellText=m_t.values,  colLabels=m_t.columns, colWidths=[.5,.25,.25], loc='lower center', bbox=[0,0,1,1])
the_material_table_data = sut.make_a_summary_table(a_table,m_t,m_t.columns, s_et_bottom_row=True)


plt.show()


#  

# ### The most common objects 2017 - 2020
# 
# The most common objects are any object that was found in at least 50% of all the surveys or whose total quantity is in the top ten of all objects. This accounts for 60% - 80% of all objects found. Note that the most common objects at the national level may not fully represent the most common objects in a specific region, though they usually have common elements. Here we compare the most common objects from 2017 - 2020.
# 
# *Glass pieces > 2.5cm* made the list in 2017 and *glass bottles* made the list in 2020. Alone, these 7 objects account for 57% of all objects found in 2017 and 52% in 2020.

# In[7]:


# code totals by project
c_totals = df.groupby(['survey year', 'code'], as_index=False).agg({'quantity':'sum', 'fail':'sum', unit_label:'median'})

# calculate the fail rate for each code and survey year
c_totals.loc[c_totals['survey year'] == '2017', 'fail rate'] = ((c_totals.fail/df[df['survey year'] == '2017'].loc_date.nunique())*100).astype('int')
c_totals.loc[c_totals['survey year'] == '2020', 'fail rate'] = ((c_totals.fail/df[df['survey year'] == '2020'].loc_date.nunique())*100).astype('int')

# calculate the % of total for each code and survey year
c_totals.loc[c_totals['survey year'] == '2017', '% of total'] = ((c_totals.quantity/df[df['survey year'] == '2017'].quantity.sum())*100).astype('int')
c_totals.loc[c_totals['survey year'] == '2020', '% of total'] = ((c_totals.quantity/df[df['survey year'] == '2020'].quantity.sum())*100).astype('int')

# get all the instances where the fail rate is > .4999
c_50 = c_totals.loc[c_totals['fail rate'] > 49.99]

ten_2017 = c_totals[c_totals['survey year'] == '2017'].sort_values(by='quantity', ascending=False)[:10].code.unique()
ten_2020 = c_totals[c_totals['survey year'] == '2020'].sort_values(by='quantity', ascending=False)[:10].code.unique()

mcom_2017 = list(set(c_50[c_50['survey year']=='2017'].code.unique())|set(ten_2017))
mcom_2020 = list(set(c_50[c_50['survey year']=='2020'].code.unique())|set(ten_2020))

com_2017 = c_totals[(c_totals['survey year'] == '2017')&(c_totals.code.isin(mcom_2017))]
com_2020 = c_totals[(c_totals['survey year'] == '2020')&(c_totals.code.isin(mcom_2020))]

# format values for table
table_data = []
chart_labels = ['2017', '2020']
for i, som_data in enumerate([com_2017, com_2020]):
    som_data = som_data.set_index('code')
    som_data.sort_values(by='quantity', ascending=False, inplace=True)
    som_data['item'] = som_data.index.map(lambda x: code_description_map.loc[x])
    som_data['% of total'] = som_data["% of total"].map(lambda x: F"{int(x)}%")
    som_data['quantity'] = som_data.quantity.map(lambda x: F"{int(x):,}")
    som_data['fail rate'] = som_data['fail rate'].map(lambda x: F"{int(x)}%")
    som_data[unit_label] = som_data[unit_label].map(lambda x: F"{int(np.ceil(x))}")    
    table_data.append({chart_labels[i]:som_data})

# the columns needed
cols_to_use = {'item':'Item','quantity':'Quantity', '% of total':'% of total', 'fail rate':'fail rate', unit_label:unit_label}


fig, axs = plt.subplots(1,2, figsize=(19,10*.8))

for i,this_table in enumerate(table_data):
    this_ax = axs[i]
    this_ax.set_title(chart_labels[i], **ck.title_k14)
    ut.hide_spines_ticks_grids(this_ax)
    the_first_table_data = this_ax.table(table_data[i][chart_labels[i]][cols_to_use.keys()].values,  colLabels=list(cols_to_use.values()), colWidths=[.48, .13,.13,.13, .13], bbox=[0, 0, 1, 1])
    a_summary_table_one = sut.make_a_summary_table(the_first_table_data,table_data[i][chart_labels[i]][cols_to_use.keys()].values,list(cols_to_use.values()), 'dodgerblue')

plt.show()

plt.close()


# ### A/B testing 2017 - 2020

# #### Difference of means: survey totals
# 
# Permutation test for the difference of means, n=5000, method=shuffle
# 
# *Null hypothesis:* The mean of the survey results from 2017 is the same as the survey results from 2020. The observed difference is due to chance.
# 
# *Alternate hypothesis:* The mean of the survey results from 2017 is not the same as the survey results from 2020. The observed difference in the samples is significant.

# In[8]:


# data for permutation testing
data=df.copy()

pre_shuffle = data.groupby(['survey year', 'loc_date'], as_index=False)[unit_label].sum()

observed_mean = pre_shuffle.groupby('survey year')[unit_label].mean()

observed_dif = observed_mean.loc["2020"] - observed_mean.loc["2017"]

new_means=[]
# permutation resampling:
for element in np.arange(5000):
    pre_shuffle['new_class'] = pre_shuffle['survey year'].sample(frac=1).values
    b=pre_shuffle.groupby('new_class').mean()
    new_means.append((b.loc['2020'] - b.loc['2017']).values[0])
emp_p = np.count_nonzero(new_means <= observed_dif )/ 5000

# chart the results
fig, ax = plt.subplots()

sns.histplot(new_means, ax=ax)
ax.set_title(F"$\u0394\mu$ = {np.round(observed_dif, 2)}, perm=5000, p={emp_p} ", **ck.title_k14)
ax.set_ylabel('permutations', **ck.xlab_k14)
ax.set_xlabel("$\mu$ 2020 - $\mu$ 2017", **ck.xlab_k14)
plt.show()


# #### Difference of means: most common objects
# 
# Permutation test for the difference of means, n=1000, method=shuffle
# 
# The condition is tested for each of the most common codes:
# 
# *Null hypothesis:* The mean of the of the survey results of the most common objects from 2017 is the same as 2020. The observed difference is due to chance.
# 
# *Alternate hypothesis:* The mean of the survey results of the most common objects from 2017 is different than 2020. The observed difference in the samples is significant.
# 
# 
# __Key:__
# 
# * if p>0.05 = white: there is no evidence to support the alternate hypothesis
# * if p < 0.05 = red: the difference is significant and positive
# * if p < 0.05 = yellow: the difference is significant and negative

# 

# In[9]:


# data for permutation testing
data=df.copy()

# the most common codes from both projects
common_codes_both_years = list(set([*mcom_2017, *mcom_2020]))

# data to resample
pre_shuffle = data[data.code.isin(common_codes_both_years)].groupby(['survey year', 'loc_date', 'code'], as_index=False)[unit_label].sum()

# the mean by survey year
observed_mean = pre_shuffle.groupby(['survey year', 'code'])[unit_label].mean()

# get the differences from one year to the next: check the inverse condtion
observed_dif = observed_mean.loc["2020"] - observed_mean.loc["2017"]
inv_diff = observed_mean.loc["2017"] - observed_mean.loc["2020"]

# how many permutations
perms = 1000

# keep the test statisitcs here
new_means=[]

# # permutation resampling:
for a_code in common_codes_both_years:
    
    # hypothese one
    cdif = []    
    # hypothesis two
    invdif=[]
    
    # get the data for the code
    c_data = pre_shuffle[pre_shuffle.code == a_code].copy()
    
    # shuffle
    for element in np.arange(perms):
        # creating new column for shuffled survey years
        c_data['new_class'] = c_data['survey year'].sample(frac=1).values
        # get the mean
        b=c_data.groupby('new_class').mean()
        # h1
        cdif.append((b.loc['2020'] - b.loc['2017']).values[0])
        # h2
        invdif.append((b.loc['2017'] - b.loc['2020']).values[0])
    # calculate p
    emp_p = np.count_nonzero(cdif <= (observed_dif.loc[a_code])) / perms
    inv_p = np.count_nonzero(invdif <= (inv_diff.loc[a_code])) / perms
    
    # store that result
    new_means.append({a_code:{'p':emp_p, 'invp':inv_p, 'difs':cdif}})

# chart the results
fig, axs = plt.subplots(3,5, figsize=(18,9))

for i,code in enumerate(common_codes_both_years):
    
    # assign columns and rows
    row = int(np.floor((i/5)%5))
    col =i%5
    ax=axs[row, col]
    
    # the data to plot
    data = new_means[i][code]['difs']
#     data_inv = new_means[i][code]['invdif']
    p=new_means[i][code]['p']
    invp=new_means[i][code]['invp']
    
    # set the face color according to p
    if invp < 0.05:
        ax.patch.set_facecolor('salmon')
        ax.patch.set_alpha(0.5)
    if p < 0.05:
        ax.patch.set_facecolor('palegoldenrod')
        ax.patch.set_alpha(0.5)        
     
    # plot that
    sns.histplot(data, ax=ax, color='dodgerblue')
 
    ax.set_title(code_description_map.loc[code], **ck.title_k)
    ax.set_xlabel(F"$\u0394\mu$={np.round(observed_dif.loc[code], 2)}, p={new_means[i][code]['p']}, invp={new_means[i][code]['invp']}", fontsize=12)

ut.hide_spines_ticks_grids(axs[2,3])
ut.hide_spines_ticks_grids(axs[2,4])

plt.subplots_adjust(hspace=0.25)
plt.tight_layout()

plt.show()


# However similar the results are, the difference in sampling conditions between rivers and lakes can not be overlooked nor the effects those conditions may have on survey totals. 

# ## Results lakes 2017 and 2020
# When possible the SLR locations were resampled in IQAASL, in most cases multiple times. The following lakes were sampled in both project years:
# 
# 1. Zurichsee
# 2. Bielersee
# 3. Neuenburgersee
# 4. Walensee
# 5. Lac Léman
# 6. Thunersee
# 
# When just the six lakes are considered there were more samples, more locations and more trash was collected in 2020, but the median and average were both lower with respect to 2017. 

# In[10]:


lks_df = df[df.water_name_slug.isin(these_lakes)].drop_duplicates().copy()

lks_dt = lks_df.groupby(['survey year', 'water_name_slug','loc_date','date', 'month'], as_index=False)[unit_label].sum()
com_locs_df = lks_df[lks_df.location.isin(both_years)].copy()
nsamps_com_locs = com_locs_df[com_locs_df['survey year'] == '2020'].groupby(['location'], as_index=True).loc_date.nunique()

com_locs_20 = com_locs_df[com_locs_df['survey year'] == '2020'].location.unique()
locs_lakes = lks_df[lks_df['survey year'] == '2020'].location.unique()


# ### Lakes: distribution of survey totals

# *__Top Left:__ survey totals by date, __Top right:__ median monthly survey total* 

# In[11]:


# the monthly average
data=lks_df.groupby(['loc_date', 'date', 'survey year'], as_index=False)['p/100m'].sum()
data.set_index('date', inplace=True)

months = mdates.MonthLocator(interval=1)
months_fmt = mdates.DateFormatter('%b')
years = mdates.YearLocator()

ecdf_2017 = ECDF(data[data['survey year'] == '2017']['p/100m'].values)
ecdf_2020 = ECDF(data[data['survey year'] == '2020']['p/100m'].values)
ecdf_2017_x, ecdf_2017_y = ecdf_2017.x, ecdf_2017.y
ecdf_2020_x, ecdf_2020_y = ecdf_2020.x, ecdf_2020.y

the_90th = np.percentile(data['p/100m'], 95)
just_2017 = data[data['survey year'] == '2017']['p/100m'].resample('M').median()
monthly_2017 = pd.DataFrame(just_2017)
monthly_2017.reset_index(inplace=True)
monthly_2017['month'] = monthly_2017.date.map(lambda x: dt.datetime.strftime(x, "%b"))

just_2020 = data[data['survey year'] == '2020']['p/100m'].resample('M').median()
monthly_2020 = pd.DataFrame(just_2020)
monthly_2020.reset_index(inplace=True)
monthly_2020['month'] = monthly_2020.date.map(lambda x: dt.datetime.strftime(x, "%b"))

data_long = pd.melt(data[['survey year', 'p/100m']],id_vars=["survey year"], value_vars=('p/100m',), value_name="survey total")
data_long['year_bin'] = np.where(data_long['survey year'] == '2017', 0, 1)
data_long = data_long[data_long["survey total"] < the_90th].copy()

fig, ax = plt.subplots(2,2, figsize=(14,9), sharey=False)
axone=ax[0,0]
axtwo = ax[0,1]
axthree = ax[1,0]
axfour = ax[1,1]

axone.set_ylabel("pieces of trash per 100m", **ck.xlab_k14)
axone.xaxis.set_minor_locator(months)
axone.xaxis.set_major_locator(years)
axone.set_xlabel(" ")

axtwo.set_xlabel(" ")
axtwo.set_ylabel("pieces of trash per 100m", **ck.xlab_k14)

axthree.set_ylabel("nummber of samples", **ck.xlab_k14)
axthree.set_xlabel("pieces of trash per 100m", **ck.xlab_k)

axfour.set_ylabel("percent of surveys", **ck.xlab_k14)
axfour.set_xlabel("pieces of trash per 100m", **ck.xlab_k)

sns.scatterplot(data=data, x='date', y='p/100m', color='red', s=34, ec='white',label="survey total", hue='survey year', palette= this_palette, ax=axone)

sns.lineplot(data=monthly_2017, x='month', y='p/100m', color='magenta', label=F"Monthly median:2017", ax=axtwo)
sns.lineplot(data=monthly_2020, x='month', y='p/100m', color='dodgerblue',label=F"Monthly median:2020",  ax=axtwo)

sns.histplot(data=data_long, x='survey total', hue='survey year', stat='count', multiple='stack', palette=this_palette, ax=axthree)

sns.lineplot(x=ecdf_2017_x, y=ecdf_2017_y, ax=axfour, color='magenta', label="survey results 2017")
sns.lineplot(x=ecdf_2020_x, y=ecdf_2020_y, ax=axfour, color='dodgerblue', label="survey results 2020")
axfour.xaxis.set_major_locator(ticker.MultipleLocator(1000)) 
axfour.xaxis.set_minor_locator(ticker.MultipleLocator(100)) 
axfour.legend(loc="center right")
axfour.tick_params(which="both", bottom=True)
axfour.grid(b=True, which='minor',linewidth=0.5)


axone.legend(loc='upper center')


axtwo.set_ylim(0, the_90th)
plt.show()


# *__bottom Left:__ number of samples with respect to the survey total, __bottom right:__ empirical cumulative distribution of survey totals* 

# ### Lakes: summary data and material types

# *__Left:__ summary of survey totals, __right:__ material type*

# In[12]:


# group by survey year and use pd.describe to get basic stats
som_1720 = lks_dt.groupby('survey year')[unit_label].describe().round(2)

# add total quantity and number of unique locations
som_1720['total objects'] = som_1720.index.map(lambda x: df[df['survey year'] == x].quantity.sum())
som_1720['# locations'] = som_1720.index.map(lambda x: df[df['survey year'] == x].location.nunique())

# make columns names more descriptive
som_1720.rename(columns=(change_names), inplace=True)
ab = som_1720.reset_index()

# melt that on survey year
c_s = ab.melt(id_vars=['survey year'])

# pivot on survey year
combined_summary = c_s.pivot(columns='survey year', index='variable', values='value').reset_index()

# format for printing
combined_summary['2017'] = combined_summary['2017'].map(lambda x: F"{int(x):,}")
combined_summary['2020'] = combined_summary['2020'].map(lambda x: F"{int(x):,}")

# change the index to date
data = lks_dt.set_index('date')

# get the median monthly value
monthly_2017 = data.loc[data['survey year'] == '2017']['p/100m'].resample('M').median()
# change the date to the name of the month for charting
months_2017 = pd.DataFrame({'month':[dt.datetime.strftime(x, "%b") for x in monthly_2017.index], unit_label:monthly_2017.values})

# repeat for 2020
monthly_2020 = data.loc[data['survey year'] == '2020']['p/100m'].resample('M').median()
months_2020 = pd.DataFrame({'month':[dt.datetime.strftime(x, "%b") for x in monthly_2020.index], unit_label:monthly_2020.values})


# material totals
mat_total = lks_df.groupby(['survey year', 'code'], as_index=False).quantity.sum()
# add material type:
mat_total['mat'] = mat_total.code.map(lambda x:code_material_map.loc[x])

# the most common codes for each year
mat_total = mat_total.groupby(['survey year', 'mat'], as_index=False).quantity.sum()

# get the % of total and fail rate for each object from each year
# add the yearly total column
mat_total.loc[mat_total['survey year'] == '2017', 'yt'] = mat_total[mat_total['survey year'] == '2017'].quantity.sum()
mat_total.loc[mat_total['survey year'] == '2020', 'yt'] = mat_total[mat_total['survey year'] == '2020'].quantity.sum()

# get % of total
mat_total['pt'] =((mat_total.quantity/mat_total.yt)*100).round(2)

# format for printing:
mat_total['pt'] = mat_total.pt.map(lambda x: F"{x}%")
mat_total['quantity'] = mat_total.quantity.map(lambda x: F"{x:,}")

m_t = mat_total[['survey year','mat', 'quantity', 'pt']].pivot(columns='survey year', index='mat', values='pt').reset_index()
m_t.rename(columns={'mat':'material', 'pt':'% of total'}, inplace=True)

# put that in a table
fig, axs = plt.subplots(1, 2, figsize=(10,8))

axone = axs[0]
axtwo= axs[1]

ut.hide_spines_ticks_grids(axone)
ut.hide_spines_ticks_grids(axtwo)

# summary data table
a_table = axone.table(cellText=combined_summary.values,  colLabels=combined_summary.columns, colWidths=[.5,.25,.25], loc='lower center', bbox=[0,0,1,1])
the_material_table_data = sut.make_a_summary_table(a_table,combined_summary,combined_summary.columns, s_et_bottom_row=True)

# material totals
a_table = axtwo.table(cellText=m_t.values,  colLabels=m_t.columns, colWidths=[.5,.25,.25], loc='lower center', bbox=[0,0,1,1])
the_material_table_data = sut.make_a_summary_table(a_table,m_t,m_t.columns, s_et_bottom_row=True)


plt.show()


# 

# ### Lakes: results most common objects
# 
# The most common objects make up 65% of all objects counted.

# In[13]:


lks_codes = lks_df[lks_df.code.isin(mcom_2017)].copy()
lks_codes = lks_df[lks_df.code.isin(mcom_2017)].groupby(['code', 'survey year'], as_index=False).agg({'p/100m':'median', 'quantity':'sum', 'fail':'sum', 'loc_date':'nunique'})
lks_codes.loc[lks_codes['survey year'] == '2020', 'fail rate'] = lks_codes.fail/lks_df[lks_df['survey year']=='2020'].loc_date.nunique()
lks_codes.loc[lks_codes['survey year'] == '2017', '% of total'] = lks_codes.quantity/lks_df[lks_df['survey year']=='2017'].quantity.sum()
lks_codes.loc[lks_codes['survey year'] == '2017', 'fail rate'] = lks_codes.fail/lks_df[lks_df['survey year']=='2017'].loc_date.nunique()
lks_codes.loc[lks_codes['survey year'] == '2020', '% of total'] = lks_codes.quantity/lks_df[lks_df['survey year']=='2020'].quantity.sum()

pivot_2017_2020 = lks_codes.pivot(columns='survey year', values=['p/100m', 'fail rate', '% of total'], index='code')
pivot_2017_2020['Item'] = pivot_2017_2020.index.map(lambda x: code_description_map.loc[x])
pivot_2017_2020.set_index('Item', inplace=True, drop=True)
pivot_2017_2020.sort_values(by=(unit_label,'2017'), ascending=False, inplace=True)


# In[14]:


# plot that
fig = plt.figure(figsize=(8, 12))

spec = GridSpec(ncols=8, nrows=2, figure=fig)
axone = fig.add_subplot(spec[:,1:3])
axtwo = fig.add_subplot(spec[:,3:5])
axthree = fig.add_subplot(spec[:,5:7])
an_order = pivot_2017_2020['p/100m'].sort_values(by='2017', ascending=False).index
axtwo_data = pivot_2017_2020['fail rate'].sort_values(by='2017', ascending=False).reindex(an_order)
axthree_data = pivot_2017_2020['% of total'].sort_values(by='2017', ascending=False).reindex(an_order)


sns.heatmap(pivot_2017_2020[unit_label], cmap=cmap2, annot=True, annot_kws={'fontsize':12},  ax=axone, square=True, cbar=False, linewidth=.05,  linecolor='white')
axone.tick_params(**dict(labeltop=True, labelbottom=True, pad=12, labelsize=12), **ck.no_xticks)
axone.set_xlabel(" ")
axone.set_title("median p/100m",**ck.title_k14r)

sns.heatmap(pivot_2017_2020['fail rate'], cmap=cmap2, annot=True, annot_kws={'fontsize':12}, fmt='.0%', ax=axtwo, square=True,  cbar=False, linewidth=.05,  linecolor='white')
axtwo.tick_params(**dict(labeltop=True, labelbottom=True, pad=12, labelsize=12), **ck.no_xticks)
axtwo.tick_params(labelleft=False, left=False)
axtwo.set_xlabel(" ")
axtwo.set_title("fail rate", **ck.title_k14r)

sns.heatmap(pivot_2017_2020['% of total'], cmap=cmap2, annot=True, annot_kws={'fontsize':12}, fmt='.0%', ax=axthree, square=True,  cbar=False, linewidth=.05,  linecolor='white')
axthree.tick_params(**dict(labeltop=True, labelbottom=True, pad=12, labelsize=12), **ck.no_xticks)
axthree.tick_params(labelleft=False, left=False)
axthree.set_xlabel(' ')
axthree.set_title("% of total", **ck.title_k14r)


axone.set_ylabel("")
axtwo.set_ylabel("")
axthree.set_ylabel("")


plt.subplots_adjust(wspace=0.3)
plt.show()


# ### Lakes monthly median common objects: 
# 
# All lakes were sampled in all months in both projects. In 2017 the minimum samples per month  was 12 and the maximum was 17 compared to a minimum of 17 and max of 34 in 2020.

# *Lakes 2017: monthly median result most common objects*

# In[15]:


top_ten_month = lks_df[(lks_df['survey year'] == '2017')&(lks_df.code.isin(mcom_2017))].groupby(['loc_date', 'date', 'code'], as_index=False)['p/100m'].sum()
top_ten_month['month'] = top_ten_month.date.dt.month

dts_date = top_ten_month.copy()
dts_date.set_index('date', inplace=True)
group_names =  mcom_2017

mgr = {}

for a_group in group_names:
    a_plot = dts_date[(dts_date.code==a_group)]['p/100m'].resample('M').mean().fillna(0)
    this_group = {a_group:a_plot}
    mgr.update(this_group)

# Median monthly results most common objects 2017

fig, ax = plt.subplots(figsize=(12,7))

colors_palette = {'G156':'dimgray', 'G178': 'teal',
    'G177': 'darkslategray',
    'G200': 'lightseagreen',
    'G27':'darkorange',
    'G30':'darkkhaki',
    'G67':'rosybrown',
    'G89': 'salmon',
    'G95':'magenta',
    'G82': 'maroon',
    'G79':'brown',
    'G208': 'turquoise',
    'G124':'indigo',
    'G25': 'chocolate',
    'G31': 'goldenrod',
    'G21': 'tan'    
}
months={
    0:'Jan',
    1:'Feb',
    2:'Mar',
    3:'Apr',
    4:'May',
    5:'Jun',
    6:'Jul',
    7:'Aug',
    8:'Sep',
    9:'Oct',
    10:'Nov',
    11:'Dec'
}

def new_month(x):
    if x <= 11:
        this_month = x
    else:
        this_month=x-12    
    return this_month

bottom = [0]*len(mgr['G27'])

hmm = lks_df[lks_df['survey year'] == '2017'].groupby(['loc_date', 'date'], as_index=False).agg({'p/100m':'sum', 'quantity':'sum'})
hmm.set_index('date', inplace=True)
hmmx2017 = hmm['p/100m'].resample('M').mean().fillna(0)

this_x = [i for i,x in  enumerate(hmmx2017.index)]
ax.bar(this_x, hmmx2017.to_numpy(), color='dodgerblue', alpha=0.1, linewidth=1, edgecolor='teal', width=1, label="Monthly survey average") 


for i, a_group in enumerate(group_names):
       
    
    this_x = [i for i,x in  enumerate(mgr[a_group].index)]
    this_month = [x.month for i,x in enumerate(mgr[a_group].index)]
    
    if i == 0:
        ax.bar(this_x, mgr[a_group].to_numpy(), label=a_group, color=colors_palette[a_group], linewidth=1, alpha=0.6 ) 
    else:
        bottom += mgr[group_names[i-1]].to_numpy()        
        ax.bar(this_x, mgr[a_group].to_numpy(), bottom=bottom, label=a_group, color=colors_palette[a_group], linewidth=1, alpha=0.8)

handles, labels = ax.get_legend_handles_labels()
ax.xaxis.set_major_locator(ticker.FixedLocator([i for i in np.arange(len(this_x))]))

axisticks = ax.get_xticks()
labelsx = [months[new_month(x-1)] for x in  this_month]
plt.xticks(ticks=axisticks, labels=labelsx)


new_labels = [code_description_map.loc[x] for x in labels[1:]]
new_labels = new_labels[::-1]
new_labels.insert(0,"Monthly survey average")

handles = [handles[0], *handles[1:][::-1]]
ax.set_title("")

    
plt.legend(handles=handles, labels=new_labels, bbox_to_anchor=(1, 1), loc="upper left",  fontsize=14)    
plt.show()


# *Lakes 2020: monthly median result most common objects*

# 

# In[16]:


top_ten_month = lks_df[(lks_df['survey year'] == '2020')&(lks_df.code.isin(mcom_2017))].groupby(['loc_date', 'date', 'code'], as_index=False)['p/100m'].sum()
top_ten_month['month'] = top_ten_month.date.dt.month

dts_date = top_ten_month.copy()
dts_date.set_index('date', inplace=True)

mgr2020 = {}

for a_group in group_names:
    a_plot = dts_date[(dts_date.code==a_group)]['p/100m'].resample('M').mean().fillna(0)
    this_group = {a_group:a_plot}
    mgr2020.update(this_group)
fig, ax = plt.subplots(figsize=(12,7))

bottom = [0]*len(mgr2020['G27'])

hmm = lks_df[lks_df['survey year'] == '2020'].groupby(['loc_date', 'date'], as_index=False).agg({'p/100m':'sum', 'quantity':'sum'})
hmm.set_index('date', inplace=True)
hmmx2020 = hmm['p/100m'].resample('M').mean().fillna(0)

this_x = [i for i,x in  enumerate(hmmx2020.index)]
ax.bar(this_x, hmmx2020.to_numpy(), color='dodgerblue', alpha=0.1, linewidth=1, edgecolor='teal', width=1, label="Monthly survey average") 

for i, a_group in enumerate(group_names):
       
    
    this_x = [i for i,x in  enumerate(mgr2020[a_group].index)]
    this_month = [x.month for i,x in enumerate(mgr2020[a_group].index)]
    
    if i == 0:
        ax.bar(this_x, mgr2020[a_group].to_numpy(), label=a_group, color=colors_palette[a_group], linewidth=1, alpha=0.6) 
    else:
        bottom += mgr2020[group_names[i-1]].to_numpy()
        
        ax.bar(this_x, mgr2020[a_group].to_numpy(), bottom=bottom, label=a_group, color=colors_palette[a_group], linewidth=1, alpha=0.8)

handles, labels = ax.get_legend_handles_labels()
ax.xaxis.set_major_locator(ticker.FixedLocator([i for i in np.arange(len(this_x))]))

axisticks = ax.get_xticks()
labelsx = [months[x-1] for x in  this_month]
plt.xticks(ticks=axisticks, labels=labelsx)


new_labels = [code_description_map.loc[x] for x in labels[1:]]
new_labels = new_labels[::-1]
new_labels.insert(0,"Monthly survey average")

handles = [handles[0], *handles[1:][::-1]]
ax.set_title("", **ck.title_k14)

    
plt.legend(handles=handles, labels=new_labels, bbox_to_anchor=(1, 1), loc="upper left",  fontsize=14)    
plt.show()


# ### Lakes: A/B testing 2017 - 2020

# #### Lakes: Difference of means survey totals
# 
# Permutation test for the difference of means, n=5000, method=shuffle
# 
# The following hypothesis was tested for the survey totals:
# 
# *Null hypothesis:* The mean of the survey results from 2017 is the same as 2020 for the surveys on the specified lakes. The observed difference is due to chance.
# 
# *Alternate hypothesis:* The mean of the survey results from 2017 is different than 2020 for the surveys on the specified lakes. The observed difference in the samples is significant.

# In[17]:


# data for permutation testing
data=df[df.water_name_slug.isin(these_lakes)].copy()

pre_shuffle = data.groupby(['survey year', 'loc_date'], as_index=False)[unit_label].sum()

observed_mean = pre_shuffle.groupby('survey year')[unit_label].mean()

observed_dif = observed_mean.loc["2020"] - observed_mean.loc["2017"]

new_means=[]
# permutation resampling:
for element in np.arange(5000):
    pre_shuffle['new_class'] = pre_shuffle['survey year'].sample(frac=1).values
    b=pre_shuffle.groupby('new_class').mean()
    new_means.append((b.loc['2020'] - b.loc['2017']).values[0])
emp_p = np.count_nonzero(new_means <= observed_dif )/ 5000

# chart the results
fig, ax = plt.subplots()

sns.histplot(new_means, ax=ax)
ax.set_title(F"$\u0394\mu$ = {np.round(observed_dif, 2)}, perm=5000, p={emp_p} ", **ck.title_k14)
ax.set_ylabel('permutations', **ck.xlab_k14)
ax.set_xlabel("$\mu$ 2020 - $\mu$ 2017", **ck.xlab_k14)
plt.show()


# #### Lakes: difference of means most common objects
# 
# Permutation test for the difference of means, n=1000, method=shuffle
# 
# The condition is tested for each of the most common codes:
# 
# *Null hypothesis:* The mean of the survey results of the most common objects from 2017 is the same as 2020 for the surveys on the specified lakes. The observed difference is due to chance.
# 
# *Alternate hypothesis:* The mean of the survey results of the most common objects from 2017 is different than 2020 for the surveys on the specified lakes. The observed difference in the samples is significant.
# 
# 
# __Key:__
# 
# * if p>0.05 = white: there is no evidence to support the alternate hypothesis
# * if p < 0.05 = red: the difference is significant and positive
# * if p < 0.05 = yellow: the difference is significant and negative

# In[18]:


# data for permutation testing
data=df[df.water_name_slug.isin(these_lakes)].copy()

common_codes_both_years = list(set([*mcom_2017, *mcom_2020]))

pre_shuffle = data[data.code.isin(common_codes_both_years)].groupby(['survey year', 'loc_date', 'code'], as_index=False)[unit_label].sum()

observed_mean = pre_shuffle.groupby(['survey year', 'code'])[unit_label].mean()

observed_dif = observed_mean.loc["2020"] - observed_mean.loc["2017"]
inv_diff = observed_mean.loc["2017"] - observed_mean.loc["2020"]

perms = 1000

new_means=[]
# # permutation resampling:
for a_code in common_codes_both_years:
    
    # store the test statisitc
    cdif = []
    invdif=[]
    
    # code data
    c_data = pre_shuffle[pre_shuffle.code == a_code].copy()
    for element in np.arange(perms):
        # shuffle labels
        c_data['new_class'] = c_data['survey year'].sample(frac=1).values
        b=c_data.groupby('new_class').mean()
        cdif.append((b.loc['2020'] - b.loc['2017']).values[0])
        invdif.append((b.loc['2017'] - b.loc['2020']).values[0])
    
    # calculate p
    emp_p = np.count_nonzero(cdif <= (observed_dif.loc[a_code])) / perms
    inv_p = np.count_nonzero(cdif >= (observed_dif.loc[a_code])) / perms
    new_means.append({a_code:{'p':emp_p, 'invp':inv_p, 'difs':cdif}})

# chart the results
fig, axs = plt.subplots(3,5, figsize=(18,9), sharey=True)

for i,code in enumerate(common_codes_both_years):
    
    # set up the ax
    row = int(np.floor((i/5)%5))
    col =i%5
    ax=axs[row, col]
    
    # data for charts
    data = new_means[i][code]['difs']
    
    # pvalues
    p=new_means[i][code]['p']
    invp=new_means[i][code]['invp']
    
    # set the facecolor based on the p value
    if invp < 0.05:
        ax.patch.set_facecolor('salmon')
        ax.patch.set_alpha(0.5)
    if p < 0.05:
        ax.patch.set_facecolor('palegoldenrod')
        ax.patch.set_alpha(0.5)        
    # plot that    
    sns.histplot(data, ax=ax, color='dodgerblue')
    
    ax.set_title(code_description_map.loc[code], **ck.title_k)
    ax.set_xlabel(F"$\u0394\mu$={np.round(observed_dif.loc[code], 2)}, p={new_means[i][code]['p']}, invp={new_means[i][code]['invp']}", fontsize=12)
    ax.set_ylabel('permutations')

# hide the unused axs
ut.hide_spines_ticks_grids(axs[2,3])
ut.hide_spines_ticks_grids(axs[2,4])

# get some space for xaxis label
plt.subplots_adjust(hspace=0.25)


plt.tight_layout()
plt.show()


# In[19]:


small = lks_df[lks_df.code.isin([ "G20", "G21", "G22", "G23"])].groupby(['code', 'survey year'], as_index=False).agg({'quantity':'sum', 'p/100m':'mean'})
ttl = combined_data.groupby('survey year').quantity.sum()
small.loc[small['survey year'] == '2017', 'p_t'] = small.quantity/ttl.loc['2017']
small.loc[small['survey year'] == '2020', 'p_t'] = small.quantity/ttl.loc['2020']
# print(small.groupby(['survey year','code']).sum())
# print(small.groupby(['survey year']).sum())


# ### Protocols matter
# 
# There was a key difference between the two protocols:
# 
# * The 2020 protocol counts all visible objects and classifies fragments by size
# * The 2017 protocol limited the object counts to items greater than or equal to 2.5cm in length
# 
# This difference in protocol effects the interpretation of the results for fragmented plastics and expanded foams from one year to the next.  Expanded foams and fragmented plastics are objects whose original use is unknown but the material can be distinguished. **Fragmented plastics and expanded foams of all sizes are 28% of the total survey results for the lakes in 2020 and half of which are unaccounted for in 2017**.  
# 
# __Surveyors paradox__
# 
# Size limitations increase the complexity of the survey process by introducing another step. If not carefully implemented limitations add a paradox that each surveyor must confront when objects that have been identified do not meet the size criteria of the protocol:
# 
# * either leave the material and not count it 
# * take it and not count it
# 
# The surveyor is being asked to either ignore objects that are there or remove the objects and not quantify them. Either way it does not fully describe the situation and it leaves work undone. A moral impass for the litter surveyor.
# 
# If their are size limits in the protocol then certain objects have to be measured. Whether an object is counted or not depends on if their is a category to place it in. The MSFD provides codes to classify objects as small as 5mm, the 2020 project takes advantage of this in order to account for as much material as possible. **Thus avoiding the paradox** and providing a more detailed survey.
# 
# __Plastic lids and plastic lids__
# 
# Plastic lids are seperated into three catgegories during the counting process:
# 
# 1. drink, food 
# 2. household cleaners etc..
# 3. unknown
# 
# As a group plastic lids make up 2% of the total objects in 2017 and 3% in 2020. Drink lids were ~51% of all lids found in 2017, 45% in 2020. On a pieces per meter basis there was a decrease in the amount of drink lids and an increase of non-drink lids.

# ### Land use profile: Spearmans ranked correlation
# 
# The land use features were previously calculated to compare the survey locations. The results of those calculations were also compared to the survey totals for each location. The survey totals and locations from both projects were considered as one group. The method used is the Spearman's rho or *Spearmans ranked correlation coefficient*<sup>20</sup>. The test results are evaluated at p<0.05 and 454 samples.
# 
# 1. Red/rose is a postitive association
# 2. yellow is negative
# 3. white means that p>0.05, there is no statisitical basis to assume a association
# 
# An association suggests that survey totals for that object will change in relation to the amount space attributed to that feature, or in the case of roads or river intersections, the quantity. The magnitude of the relationship is not defined and any association is not linear. 

# #### Results of Spearmans $\rho$

# In[20]:


corr_data = lks_df[(lks_df.code.isin(mcom_2017))].copy()

some_keys = {
    '% to buildings':'lu_build',
    '% to agg':'lu_agg',
    '% to woods':'lu_woods',
    '% to recreation':'lu_rec',
    '% to trans':'lu_trans',
    '% to meadow':'lu_m',
    'str_rank':'lu_trans',}
fig, axs = plt.subplots(len(mcom_2017),len(luse_exp), figsize=(len(luse_exp)+7,len(mcom_2017)+1), sharey='row')

for i,code in enumerate(mcom_2017):
    data = corr_data[corr_data.code == code]
    for j, n in enumerate(luse_exp):
        ax=axs[i, j]
        ax.grid(False)
        ax.tick_params(axis='both', which='both',bottom=False,top=False,labelbottom=False, labelleft=False, left=False)
       
        if i == 0:
            ax.set_title(F"{n}")
        else:
            pass
        
        if j == 0:
            ax.set_ylabel(F"{code_description_map[code]}", rotation=0, ha='right', **ck.xlab_k14)
            ax.set_xlabel(" ")
        else:
            ax.set_xlabel(" ")
            ax.set_ylabel(" ")
        _, corr, a_p = make_plot_with_spearmans(data, ax, n)
        
        if a_p < 0.05:
            if corr > 0:
                ax.patch.set_facecolor('salmon')
                ax.patch.set_alpha(0.5)
            else:
                ax.patch.set_facecolor('palegoldenrod')
                ax.patch.set_alpha(0.5)
# plt.tick_params(labelsize=14, which='both', axis='both')
plt.tight_layout()
plt.subplots_adjust(wspace=0, hspace=0)
plt.savefig(F"{project_directory}/test_one.jpg", dpi=300)
plt.show()


# #### Interpret Spearmans $\rho$
# 
# **Interpreting results for the most common objects** 
# 
# A positive association means that the land use attribute or feature had increased survey results when compared to other locations. This may be due to a covariance of attributes, either way **a positive association is a signal that the survey locations are near a zone of accumulation or a source**. This signal should be assessed along with the other key indicators of survey locations that have similar land use profiles. In general locations that fit the criteria could be considered as both a source and an area of accumulation for any objects that are positively associated.
# 
# A negative association means that the land use feature or attribute does not facilitate the accumulation of the object. This result is common for aggricultural areas and woods on the national level. **A negative association is a signal that the locations are not a zone of accumulation for the object**.
# 
# No or few association means that the land use features had no effect on the accumulation of that object. The survey results of the most common objects with no or few associations fall into two charateristics: 
# 
# 1. Ubiquitous: high fail rate, high pieces per meter. Found at consistent rates through out the survey area indifferent of land use
# 2. Transient: low fail rate, high quantity, high pieces per meter, few associations. Found occasionaly in large quantities at specific locations

# In[21]:


author = "roger@hammerdirt.ch"
my_message = "Love what you do. \u2764\ufe0f"
md(F"""
**This project was made possible by the Swiss federal office for the environment.**<br>

>{my_message}<br>

*{author}* pushed the run button on {today}.<br>
This document originates from https://github.com/hammerdirt-analyst/IQAASL-End-0f-Sampling-2021 all copyrights apply.<br>
""")


# ## Annex
# 
# ### IQAASL surveyors
# 
# Hammerdirt staff:
# 
# 1. Shannon Erismann, field operations manager
# 2. Helen Kurukulasuriya, surveyor
# 3. Débora Carmo, surveyor
# 4. Bettina Siegenthaler, surveyor
# 5. Roger Erismann, surveyor
# 
# Participating organizations:
# 
# 1. Precious plastic leman
# 2. Association pour la sauvetage du Léman
# 3. Geneva international School
# 4. Solid waste management: École polytechnique fédéral Lausanne

# <!-- [annex](#annex)<a id="notes"></a>
# 
# #### Notes:
# 
# <sup>1</sup> Marine debris in central California: Quantifying type and abundance of beach litter in Monterey Bay, CA. Available from: https://www.researchgate.net/publication/236053935_Marine_debris_in_central_California_Quantifying_type_and_abundance_of_beach_litter_in_Monterey_Bay_CA [accessed Jun 24 2021].
# 
# > Marginal heterogeneity was found between different types of litter across month and location. These results indicate litter type is significantly different among months and beach locations(p< 0.01). 
# 
# > Because the majority of Styrofoam observed in our surveys was broken-up (5 mm–5 cm), it was nearly impossibleto identify the whole source product from these fragments (i.e.,to-go containers, cups, plates, coolers, and commercial packingmaterial).
# 
# <sup>2</sup> S. Miladinova, D. Macias, A. Stips, E. Garcia-Gorriz, Identifying distribution and accumulation patterns of floating marine debris in the Black Sea, Marine Pollution Bulletin, Volume 153, 2020,110964,
# ISSN 0025-326X,https://doi.org/10.1016/j.marpolbul.2020.110964. (https://www.sciencedirect.com/science/article/pii/S0025326X20300825)
# 
# > Snowmelt and heavy rainfall during this period are thought to be key factors in carrying litter to the sea, as river discharge in this area is usually low at other times of the year.
# 
# > Monitoring of marine litter along the Bulgarian Black Sea coast (Simeonova et al., 2017) shows that the beaches are highly polluted due to local sources, where cigarette butts and filters (OSPAR-code 64) are dominant. Since the highest marine litter accumulation is observed in summer, one can conclude that the accumulation is probably a result of recreational activities, increased tourist flow and wild camping.
# 
# > Debris of terrestrial origin reaches the Black Sea mainly through runoff; via storm drains and waterways accessing areas where garbage is not adequately controlled
# 
# > We choose these two particle behaviours to calculate separately the litter accumulation zones when the litter does not accumulate on the beach (bouncing behaviour) and when the litter particles that reach the beach do not return back to the sea (beaching behaviour).
# 
# <sup>3</sup> van Emmerik, T., Strady, E., Kieu-Le, TC. et al. Seasonality of riverine macroplastic transport. Sci Rep 9, 13549 (2019). https://doi.org/10.1038/s41598-019-50096-1
# 
# > The abundance of plastics seems to be related to the concentration of organic material in the Saigon River. Most organic material was identified as water hyacinths. Water hyacinths often form large patches with plastic floating on its surface or trapped in the roots and thus seem to function as accumulation zones for plastic material.
# 
# <sup>4</sup> GESAMP. Sources, fate and effects of microplastics in the marine environment: part two of a global assessment (eds Kershaw, P. J. & Rochman, C. M.). (IMO/FAO/UNESCO-IOC/UNIDO/WMO/IAEA/UN/UNEP/UNDP Joint Group of Experts on the Scientific Aspects of Marine Environmental Protection). Rep. Stud. GESAMP 93, 220 (2016).
# 
# > Land-based sources, as opposed to marine-based sources, are considered the dominant input of plastics into oceans
# 
# <sup>5</sup> Lebreton, L., van der Zwet, J., Damsteeg, JW. et al. River plastic emissions to the world’s oceans. Nat Commun 8, 15611 (2017). https://doi.org/10.1038/ncomms15611
# 
# > Overall, observed plastic concentrations differ by several orders of magnitude in between sampled rivers, with studies suggesting that population density, levels of urbanization and industrialization within catchment areas, rainfall rates and the presence of artificial barriers such as weirs and dams play a significant role in resulting rates of river-based plastic inputs into the ocean.
# 
# <sup>6</sup> Wagner, M. et al. Microplastics in freshwater ecosystems: what we know and what we need to know. Environ. Sci. Eur. 26, 12 (2014).
# 
# <sup>7</sup> Spatio-temporal variability of beached macro-litter on remote islands of the North Atlantic, Noelia Ríosa,1, João P.G.L. Friasb,d,1, Yasmina Rodríguezc,d, Rita Carriçoc,d, Sofia M. Garciae,Manuela Julianoc, Christopher K. Pham
# 
# > For rocky and gravel beaches, plastic/polystyrenefragments between 2.5 and 50 cm were more prevalent. In opposition,plastic/polystyrene fragments between 2.1 and 2.5 cm were pre-dominant in sandy beaches while larger fragments (found to be morefrequent in gravel and rocky shores)
# 
# <sup>8</sup> Pascal Blarer, Gabriele Kull, The Swiss Litter Report, June 2108, Zurich, http://stoppp.org/research
# 
# > Between April 2017 and March 2018 1,052 measurements were made at 112 locations for the Swiss Litter Report. More than 150 trained volunteers collected and categorized 95,971 pieces of litter from the shores of the largest rivers and lakes in Switzerland. This makes the Swiss Litter Report one of the most comprehensive Citizen Science projects on this subject worldwide and for the first time gives us a nationwide view of the distribution of litter along the shores of Swiss waters.
# 
# > La densité moyenne des déchets diminue de 91 objets par 100m2en  été  à  47  en  hiver.  En janvier, une valeur légèrement plus élevée, imputable aux activités de Nouvel An et aux trois tempêtes survenues en 2018 pendant le mois en question, a été constatée.
# 
# > La densité mesurée des déchets est nettement plus élevée sur les rives des lacs (123) que le long des rivières   (38).   En   zone   urbaine, on   trouve   plus   de   déchets   (103)   que   dans l‘agglomération (56) et en zone rurale (53). Le nombre de visiteurs sur le site est un important facteur de densité des déchets.
# 
# > Le «Swiss Litter Report» recouvre de nombreux différents types de zones riveraines, ce qui fait que la densité de déchets varie fortement. Les densités de  déchets  mesurées  en  Suisse  sont  dans  le  spectre  de  celles  d’études internationales comparables•La  densité  moyenne  des  déchets  diminue  de  91  objets  par  100m2 en  été  à  47  en  hiver.  En janvier, une valeur légèrement plus élevée, imputable aux activités de Nouvel An et aux trois tempêtes survenues en 2018 pendant le mois en question, a été constatée.
# 
# > La densité mesurée des déchets est nettement plus élevée sur les rives des lacs (123) que le long   des   rivières   (38).   En   zone   urbaine,   on   trouve   plus   de   déchets   (103)   que   dans l‘agglomération (56) et en zone rurale (53). Le nombre de visiteurs sur le site est un important facteur de densité des déchets.
# 
# > Le «Swiss Litter Report» recouvre de nombreux différents types de zones riveraines, ce qui fait que la densité de déchets varie fortement.•Les  densités  de  déchets  mesurées  en  Suisse  sont  dans  le  spectre  de  celles  d’études internationales comparables
# 
# <sup>9</sup> Hanke, G. et al. Guidance on Monitoring of Marine Litter in European Seas. Publications Office of the European Union. JRC83985. (2013). https://doi.org/10.2788/99475.
# 
# <sup>10</sup> There is most likely more trash at the survey site, but certainly not less than what was recorded.
# 
# <sup>11</sup> Independent observations : [stats stackexchange](https://stats.stackexchange.com/questions/116355/what-does-independent-observations-mean)
# 
# <sup>12</sup> Van Loon, W., Hanke, G., Fleet, D., Werner, S., Barry, J., Strand, J., Eriksson, J., Galgani, F., Gräwe, D., Schulz, M., Vlachogianni, T., Press, M., Blidberg, E. and Walvoort, D., A European threshold value and assessment method for macro litter on coastlines, EUR 30347 EN, Publications Office of the European Union, Luxembourg, 2020, ISBN 978-92-76-21444-1 (online), doi:10.2760/54369 (online), JRC121707.
# 
# <sup>13</sup> Implementation of Anderson Darling k sampes test https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.anderson_ksamp.html
# 
# <sup>14</sup> Definition of Anderson Darling test https://en.wikipedia.org/wiki/Anderson%E2%80%93Darling_test
# 
# > The k-sample Anderson-Darling test is a nonparametric statistical procedure that tests the hypothesis that the populations from which two or more groups of data were drawn are identical. Each group should be an independent random sample from a population.
# 
# <sup>15</sup> IQAASL end of survey report https://github.com/hammerdirt-analyst/IQAASL-End-0f-Sampling-2021
# 
# <sup>16</sup> IQAASL key indicators of survey results https://github.com/hammerdirt-analyst/IQAASL-End-0f-Sampling-2021
# 
# <sup>17</sup> [Statistique suisse de superficie](https://www.bfs.admin.ch/bfs/fr/home/services/geostat/geodonnees-statistique-federale/sol-utilisation-couverture/statistique-suisse-superficie/utilisation-sol.assetdetail.4103545.html)
# 
# <sup>18</sup> [swissTLMRegio](https://www.swisstopo.admin.ch/de/geodata/landscape/tlmregio.html)
# 
# <sup>19</sup> IQAASL land use correlation https://github.com/hammerdirt-analyst/IQAASL-End-0f-Sampling-2021https://github.com/hammerdirt-analyst/IQAASL-End-0f-Sampling-2021
# 
# <sup>20</sup> Implementation of Spearmans rho :https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.spearmanr.html
# 
# <sup>21</sup> Fernando Pérez and Brian E. Granger. IPython: A System for Interactive Scientific Computing, Computing in Science & Engineering, 9, 21-29 (2007), DOI:10.1109/MCSE.2007.53
# 
# <sup>22</sup> Wes McKinney. Data Structures for Statistical Computing in Python, Proceedings of the 9th Python in Science Conference, 51-56 (2010)
# 
# <sup>23</sup> Harris et all, Array programming with NumPy, Nature, 585, 357–362 (2020), DOI:10.1038/s41586-020-2649-2 (publisher link)
# 
# <sup>24</sup> John D. Hunter. Matplotlib: A 2D Graphics Environment, Computing in Science & Engineering, 9, 90-95 (2007), DOI:10.1109/MCSE.2007.55
# 
# <sup>25</sup> Seabold, Skipper, and Josef Perktold. “statsmodels: Econometric and statistical modeling with python.” Proceedings of the 9th Python in Science Conference. 2010.
# 
# <sup>26</sup> Understanding Empirical Cumulative Distribution Functions, Clay Ford. University of Virginia Library https://data.library.virginia.edu/understanding-empirical-cumulative-distribution-functions/
# 
# <sup>27</sup>  Nonparametric statistics and model selection, Statistics for research projects, http://www.mit.edu/~6.s085/notes/lecture5.pdf
# 
# <sup>28</sup> Population and household statistics, https://www.bfs.admin.ch/bfs/en/home/statistics/population/surveys/statpop.html
#  -->

# <a id="gps"></a>
# #### [Survey locations](#annex)

# In[22]:


# display the survey locations
pd.set_option('display.max_rows', None)
disp_columns = ['latitude', 'longitude', 'water_name', 'city', 'is_2020']
disp_beaches = dfBeaches.loc[lks_df.location.unique()][disp_columns].sort_values(by='is_2020')
disp_beaches


# In[ ]:




