#!/usr/bin/env python
# coding: utf-8

# In[1]:


# sys, file and nav packages:
import datetime as dt


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
start_date = '2020-03-01'
end_date ='2021-05-31'

a_fail_rate = 50

# the city, lake and river bassin we are aggregating to
# the keys are column names in the survey data
levels = {"city":"Biel/Bienne","water_name_slug":'bielersee', "river_bassin":'aare'}
level_names = [levels['city'], "Bielersee","Aare survey area"]

# name of the output folder:
name_of_project = 'key_indicators_report'

# colors for gradients
colors = ['beige', 'navajowhite', 'sandybrown', 'salmon', 'sienna']
nodes = [0.0, 0.2, 0.6, 0.8, 1.0]
cmap2 = LinearSegmentedColormap.from_list("mycmap", list(zip(nodes, colors)))

# add the folder to the directory tree:
project_directory = ut.make_project_folder('output', name_of_project)


# # Key statistical indicators
# 
# The key indicators provide answers to the most frequent questions about the state of litter in the natural environment. The key indicators are:
# 
# 1. number of samples
# 2. pass-fail rate (fail-rate)
# 3. pieces of trash per meter (pcs/m or pcs/m²)
# 4. percent of total trash (% of total)
# 
# Easy to calculate and taken directly from the survey results the key indicators are essential to identifying zones of accumulation within the watershed. When combined with specific knowledge of the surrounding area the key indicators help identify potential sources.{cite}`mlwguidance`
# 
# __Indicators for the most frequent questions__
# 
# Assessments of beach-litter surveys describe the location, abundance and composition of the objects found {cite}`eubaselines`. The key indicators answer the following questions:
# 
# 1. What do you find?
# 2. How often do you find it?
# 3. How much do you find?
# 4. Where do you find the most?
# 
# These questions could apply to almost every environmental monitoring procedure that rely on observations to estimate populations. Examples include the populations of migrating birds or the prescence of native plant species. Similar to counting birds or wildflowers a litter-surveyor has to find the quarry and then identify it, this process is well documented and has been tested under many conditions{cite}`Ryan2015` {cite}`Rech`.
# 
# __Assumptions of the key indicators:__
# 
# The reliability of these indicators is based on the following assumptions:
# 
# 1. The more trash there is on the ground the more a person is likely to find
# 2. The survey results represent the minimum amount of trash at that site
# 3. The surveyors are following the protocol and recording findings accurately
# 4. For each survey: finding one item does not effect the chance of finding another {cite}`iid`
# 
# __Using the key indicators__
# 
# The key indicators of the most common objects are given with every data summary at each aggregation level. If the previous assumptions are maintained then the number of samples in the region of interest should be considered first before applying any weight to conclusions that may be drawn from the survey results.

# In[2]:


# get your data:
survey_data = pd.read_csv('resources/results_with_land_use_2015.csv')
river_bassins = ut.json_file_get("resources/river_basins.json")
dfBeaches = pd.read_csv("resources/beaches_with_land_use_rates.csv")
dfCodes = pd.read_csv("resources/codes_with_group_names_2015.csv")
dfDims = pd.read_csv("resources/dims_data.csv")

# set the index of the beach data to location slug
dfBeaches.set_index('slug', inplace=True)

# map locations to feature names
location_wname_key = dfBeaches.water_name_slug

# map water_name_slug to water_name
wname_wname = dfBeaches[['water_name_slug','water_name']].reset_index(drop=True).drop_duplicates()
wname_wname.set_index('water_name_slug', inplace=True)
        
# def make_plot_with_spearmans(data, ax, n):
#     sns.scatterplot(data=data, x=n, y='pcs_m', ax=ax, color='black', s=30, edgecolor='white', alpha=0.6)
#     corr, a_p = stats.spearmanr(data[n], data['pcs_m']).correlation
#     return ax, corr, a_p

# make changes to code def for display
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


# ## The data for this example

# In[3]:


dfSurveys = ac.fo_rmat_and_slice_date(survey_data.copy(), a_format="%Y-%m-%d", start_date=start_date, end_date=end_date)

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
biel_fail = biel.loc[biel.quantity > 0]
biel_nfail = len(biel_fail.code.unique())

# print(F"\n Results for all surveys between {start_date} and {end_date} from the following catchment areas:\n\n  {trb.river_bassin.unique()}")
md(F"\n\nThe data is from the Aare survey area between 2020-03-01 and 2020-05-31. There were {'{:,}'.format(num_obj)} objects collected from {num_samps} surveys.\n")


# In[4]:


bassin_map = PILImage.open("resources/maps/aare_scaled.jpeg")

bassin_map.thumbnail((800, 1200))


output = io.BytesIO()
bassin_map.save(output, format='PNG')
encoded_string = base64.b64encode(output.getvalue()).decode()

html = '<img src="data:image/png;base64,{}"/>'.format(encoded_string)
IPython.display.HTML(html)


# In[5]:


# this is a convenience function for the abundance class
# the fail rate needs to be recalculated at each aggregation level
fail_rates_df = ac.agg_fail_rate_by_city_feature_basin_all(dfSurveys, levels, group='code')
fail_rates_df['item'] = fail_rates_df.index.map(lambda x: ut.use_this_key(x, code_description_map))
fail_rates_df.set_index('item', drop=True, inplace=True)

# keep the list of top ten:
the_top_ten = fail_rates_df.sort_values(by='Biel/Bienne',ascending=False)[:10].index

# the labels for the summary table:
unit_label= 'pcs_m'
change_names = {'count':'# samples', 
                'mean':F"average {unit_label}",
                'std':'standard deviation', 
                'min p/50m':'min', '25%':'25%',
                '50%':'50%', '75%':'75%',
                'max':F"max {unit_label}", 'min':F"min {unit_label}",
                'total objects':'total objects',
                '# locations':'# locations',
                'survey year':'survey year'
               }

# convenience function to change the index names in a series
def anew_dict(x):
    new_dict = {}
    for param in x.index:
        new_dict.update({change_names[param]:x[param]})
    return new_dict  

# select data
data = trb.groupby(['loc_date','location',  'date'], as_index=False).agg({'pcs_m':'sum', 'quantity':'sum'})

# get the basic statistics from pd.describe
desc_biel = data['pcs_m'].describe().round(2)

# add project totals
desc_biel['total objects'] = data.quantity.sum()
desc_biel['# locations'] = data.location.nunique()

# change the names
combined_summary = pd.Series(anew_dict(desc_biel))

# format the output for printing:
not_formatted = combined_summary[-1]
combined_summary = [(x, "{:,}".format(int(combined_summary[x]))) for x in combined_summary.index[:-1]]
combined_summary.append((desc_biel.index[-1], int(not_formatted) ))

# format for time series
months = mdates.MonthLocator(interval=1)
months_fmt = mdates.DateFormatter('%b')
days = mdates.DayLocator(interval=7)

# get the data
dt_all = trb.groupby(['loc_date', 'date'], as_index=False).pcs_m.sum()
monthly_plot = dt_all.set_index('date', drop=True).pcs_m.resample('M').median()

fig = plt.figure(figsize=(12, 6))

spec = GridSpec(ncols=8, nrows=2, figure=fig)
axone = fig.add_subplot(spec[:,0:5])
axtwo = fig.add_subplot(spec[:,5:8])

sns.scatterplot(data=dt_all, x='date', y='pcs_m', color='black', alpha=0.2, label="All survey areas", ax=axone)
sns.lineplot(data=monthly_plot, x=monthly_plot.index, y=monthly_plot, color='magenta', label=F"Monthly median:{level_names[2]}", ax=axone)

the_90th = np.percentile(dt_all.pcs_m, 99)

not_included = F"Values greater than the 99th percentile ({round(the_90th, 2)}) not shown."

axone.set_ylabel("Pieces of trash per meter", **ck.xlab_k14)
axone.set_ylim(0,the_90th )
axone.set_title(F"{level_names[2]}, {start_date[:7]} through {end_date[:7]}, n={num_samps}\n{not_included}",  **ck.title_k)
axone.xaxis.set_minor_locator(days)
axone.xaxis.set_major_formatter(months_fmt)
axone.set_xlabel("")

axtwo.set_xlabel(" ")
ut.hide_spines_ticks_grids(axtwo)

a_col = ['Aare survey area', 'total']
a_table = axtwo.table(cellText=combined_summary,  colLabels=a_col, colWidths=[.4, .3,.3], loc='lower center', bbox=[0,0,1,1])
the_material_table_data = sut.make_a_summary_table(a_table,combined_summary,a_col, s_et_bottom_row=False)

plt.show()


# ## The key indicators

# ### The number of samples
# 
# The number of samples is the simplest and most important statistic to consider. The more samples there are the easier it is to spot irregularities or departures from the norm.

# ### The fail rate: how often an object was found
# 
# The pass-fail rate is the number of times that an object was found at least once divided by the number of surveys.
# 
# **What does it mean?** The fail rate describes the percent of times that a category **was** identified in relation to the amount of surveys conducted.
# 
# > Use the fail rate to determine how frequently an object is found within a geographic range. Items can be differentiated by the fail rate. Use the fail rate and pcs/m to identify objects that are found infrequently but in important quantities.

# __Different fail rates at different levels__
# 
# The fail rate can be calculated for any lake, municipality or river bassin _provided you have a sufficient quantity of reliable data_ for the location of interest.
# 
# __Biel/Bienne the ten items with the highest fail rate__
# 
# Compare the fail-rates of the ten most common items from the 16 surveys in Biel to the pass-fail-rates of those same items for Bielersee the Aare and all other survey areas.

# In[6]:


# this is a convenience function for the abundance class
# the fail rate needs to be recalculated at each aggregation level

fail_rates_df = ac.agg_fail_rate_by_city_feature_basin_all(dfSurveys, levels, group='code')
fail_rates_dfx = fail_rates_df.copy()
fail_rates_dfx['item'] = fail_rates_dfx.index.map(lambda x: code_description_map.loc[x])
fail_rates_dfx.set_index('item', drop=True, inplace=True)

# keep the list of top ten:
the_top_ten = fail_rates_df.sort_values(by='Biel/Bienne',ascending=False)[:10].index

# plot that
fig, ax = plt.subplots(figsize=(8,8))
# axone.tick_params(labelsize=14, which='both', axis='both')
sns.heatmap(fail_rates_dfx.sort_values(by="Biel/Bienne", ascending=False)[:10], cmap=cmap2, annot=True, annot_kws={'fontsize':12}, fmt='.0%', ax=ax, square=True, cbar=False, linewidth=.05,  linecolor='white')
ax.tick_params(**ck.xlabels_top, **ck.no_xticks)

ax.set_ylabel("")
ax.set_xlabel(" ")
plt.setp(ax.get_xticklabels(), rotation=90)
        
plt.tight_layout()
plt.show()


# With the exception of industrial sheeting the fail rate was greater in Biel/Bienne than the rest of the lake, the river bassin and nationally. This means that, in general, there was a greater chance of finding those objects at Biel/Bienne than most other places.
# 
# The pass-fail rate is the  most likely estimate (MLE) of the probability of finding one object. **A 100% fail rate does not mean that you are guaranteed to find the object**, it means that the object was identified in all previous samples and you should expect to find the object at the next survey. The inverse is also true. In some cases an object may be remarked by its abscence as opposed to its quantity.

# ### Pieces per meter: number of objects found per length of shoreline
# 
# Pieces per meter is the number of objects found at each survey divided by the length of the survey.
# 
# **What does it mean?** Pieces per meter describes the quantity of an object that was found for each meter of shoreline surveyed. Using pieces per meter allows survey results to be compared indifferent of the size of the survey.
# 
# > Use pieces per meter to find the objects that were found in the greatest quantities. Use pieces per meter to identify zones of accumulation.
# 
# _Why not use the surface area?_ The international norm is to report the results as quantity of objects per length of shoreline surveyed, usually 100 meters. You can use either one, however if you are looking for comparable data sets your choices may be limited if using the surface area is a requirement. The example here is given in pieces per meter.
# 
# 
# __Biel/Bienne: the ten objects with the highest median pieces per meter per survey__

# In[7]:


top_ten_pcsm = ac.agg_pcs_m_by_city_feature_basin_all(
    dfSurveys,
    levels,
    level_names=level_names,
    agg_cols={"pcs_m":"median"},
    national=True,
    **{"bassin_summary":False}
)

top_ten_pcsm['item'] = top_ten_pcsm.index.map(lambda x: code_description_map.loc[x])
tt_pcsm = top_ten_pcsm.set_index('item', drop=True).sort_values(by=levels['city'], ascending=False)[:10]

fig, ax = plt.subplots(figsize=(8,8))

sns.heatmap(tt_pcsm.sort_values(by=levels['city'], ascending=False), cmap=cmap2, annot=True, annot_kws={'fontsize':12}, fmt='.3', ax=ax, square=True, cbar=False, linewidth=.05, linecolor='white')
ax.tick_params(**ck.xlabels_top, **ck.no_xticks)
plt.setp(ax.get_xticklabels(), rotation=90)
ax.set_ylabel("")
ax.set_xlabel(" ")
        
plt.tight_layout()
plt.show()


# The ten objects that are found most frequently are not the same as the ten objects that are found in the greatest quantity. There are two objects, *foil wrappers* and *lolypop sticks*, that are found in approximately 75% of all surveys but not in quantities sufficient to make the top ten. 
# 
# Of those objects that had the greatest quantities, *nonfood packaging* and *styrofoam < 5mm*, were not identified as frequently as the other items but were found in quantities sufficient to place in the top ten.
# 
# #### Definition: the most common objects:
# 
# The most common objects are those objects that have a fail rate greater than 50% and/or are in the top-ten by quantity or pieces/m for any defined geographic area.

# In[8]:


fail_rate_ten = fail_rates_dfx.sort_values(by="Biel/Bienne", ascending=False)[:10].index
pcs_m_ten = tt_pcsm.index

accounted = set([*top_ten_pcsm['Biel/Bienne'].sort_values(ascending=False)[:10].index, *the_top_ten])
accounted_total = dfSurveys[(dfSurveys.city == 'Biel/Bienne')&(dfSurveys.code.isin(accounted))].quantity.sum()

per_cent_all_biel = F"""

*Combined, the most abundant objects and the objects found most frequently account for {np.ceil((accounted_total/biel_t)*100)}% of all objects found in Biel.*
"""

md(per_cent_all_biel)


# ### Percent of total: the compostion of the objects found
# 
# The percent of total is the amount of an object found divided by the total amount of all objects found for a defined location/region and date range.
# 
# **What does it mean?** The percent of total describes the quantity of objects found in relation to each other and the total amount of trash identified.
# 
# > Use the percent of total to define the principal trash objects. Use percent of total to identify priorities on a regional scale
# 
# The percent of total should always be evaluated with the pass-fail rate and the number of samples. Similar to pieces per meter, if an object has a low pass-fail rate and an elevated % of total it is a signal that objects are possibly being deposited in large quantities at irregular intervals: dumping or leaking.

# In[9]:


new_dfs = []
for level in levels:
    a_newdf = dfSurveys[dfSurveys[level] == levels[level]].groupby('code').agg({'quantity':'sum'})
    a_newdf[levels[level]] = a_newdf/a_newdf.sum()
    new_dfs.append(a_newdf[levels[level]])

all_survey_areas = dfSurveys.groupby('code').agg({'quantity':'sum'})
all_survey_areas['All survey areas'] = all_survey_areas/all_survey_areas.sum()
new_dfs.append(all_survey_areas['All survey areas'])
percent_of_total = pd.concat(new_dfs, axis=1)

percent_of_total['item'] = percent_of_total.index.map(lambda x: code_description_map.loc[x])
p_t = percent_of_total.loc[accounted].sort_values(by=levels['city'], ascending = False)
p_t.set_index('item', inplace=True, drop=True)

fig, ax = plt.subplots(figsize=(8,9))

sns.heatmap(p_t, cmap=cmap2, annot=True, annot_kws={'fontsize':12},fmt='.0%', ax=ax, square=True, cbar=False, linewidth=.05, linecolor='white')
ax.tick_params(**ck.xlabels_top, **ck.no_xticks)
plt.setp(ax.get_xticklabels(), rotation=90)
ax.set_ylabel("")
ax.set_xlabel(" ")
        
plt.tight_layout()
plt.show()


# ### Describe the survey results using the key indicators
# 
# Objects that are directly related to consumption (food, drinks, tobacco) are found at a rate that exceeds the median for the survey area, these objects represent 36% of the trash collected compared to 24% for all survey areas. Objects not directly related to consumption (insulation, expanded polystyrene, insultation) are found at a rate that exceeds the median for the survey area, these objects represent 22% of the total trash collected compared to 27% for all survey areas.
# 
# Biel/Bienne is most likely a source of expanded polystyrene, cigarette ends and food wrappers given the elevated pcs/m and pass-fail rate when compared to the lake, the survey area or all survey areas. Expanded polystyrene is used as an exterior insulation envelope for buildings (new construction and renovations) and to protect component objects during transportation. Biel has a strong industrial base and an active construction industry, including many projects within 1.5km of the survey locations.
# 
# In contrast, industrial sheeting and fragmented plastics have a pass-fail rate and median pcs/m value very similar to the rest of the lake, indicating that these values should be expected at other locations in the region. Thus, ruling out Biel/Bienne as a primary source of these two objects but definitely a zone of accumulation given the proximity of the Aare outflow and Suze inflow.
# 
# __What about the rest?__
# 
# The twelve objects indentified in the previous example account for approximately 66% (2019/3067) of all objects found in Biel/Bienne. That leaves 1048 objects that have not been accounted for. Of the 260 available object categories 114 were identified and 12 of those account for 66% of all the data. Therefore, there are 102 categories to describe the 1048 remaining objects, all of which are found less than 10% of the time and constitute a small protion of the total.

# ### Practical excercise
# 
# Plastic industrial pellets are the primary material used to produce plastic objects they are used extensively in Switzerland. They are disc or pellet shaped with a diameter of ~5mm.
# 
# Given the following survey results, the map of survey locations and maintaining the assumptions presented at the begining of this article answer the following questions:
# 
# 1. Where are the best chances of finding at least one?
# 2. If a survey of 50 meters is conducted what is the probable minimum amount of pellets would you find?
# 3. Why did you pick that location or locations? How sure are you of your choices?

# In[10]:


aggs = {'loc_date':'nunique', 'fail':'sum', 'pcs_m':'mean', "quantity":"sum"}
new_col_names = {"loc_date":"# of samples", "fail":"# fail", "pcs_m":"median pcs/m", "quantity":"#found"}


biel_g95 = dfSurveys[(dfSurveys.water_name_slug == levels['water_name_slug'])&(dfSurveys.code == 'G112')].groupby(['location']).agg(aggs)
biel_g95.rename(columns=new_col_names, inplace=True)

biel_g95


# <br></br>

# In[11]:


bassin_map = PILImage.open("resources/maps/bielersee_scaled.jpeg")

# image = PImage.open('demo_image.jpg')
bassin_map.thumbnail((800, 1200))
# image.save('image_thumbnail.jpg')

output = io.BytesIO()
bassin_map.save(output, format='PNG')
encoded_string = base64.b64encode(output.getvalue()).decode()

html = '<img src="data:image/png;base64,{}"/>'.format(encoded_string)
IPython.display.HTML(html)


# In[12]:


author = "roger@hammerdirt.ch"
my_message = "Love what you do. \u2764\ufe0f"
md(F"""
**This project was made possible by the Swiss federal office for the environment.**<br>

>{my_message}<br>

*{author}* pushed the run button on {today}.<br>
This document originates from https://github.com/hammerdirt-analyst/IQAASL-End-0f-Sampling-2021 all copyrights apply.<br>
""")

