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

# home brew utitilties
import resources.utility_functions as ut
import resources.chart_kwargs as ck
import resources.sr_ut as sut

# images and display
import base64, io, IPython
from PIL import Image as PILImage
from IPython.display import Markdown as md

# set some parameters:
today = dt.datetime.now().date().strftime("%Y-%m-%d")
start_date = '2020-03-01'
end_date ='2021-05-31'
a_fail_rate = .5

unit_label = 'pcs_m'

# name of the output folder:
name_of_project = 'land_use_correlation_method'

# add the folder to the directory tree:
project_directory = ut.make_project_folder('output', name_of_project)

# get your data:
survey_data = pd.read_csv('resources/results_with_land_use_2015.csv')
river_bassins = ut.json_file_get("resources/river_basins.json")
dfBeaches = pd.read_csv("resources/beaches_with_land_use_rates.csv")
dfCodes = pd.read_csv("resources/codes_with_group_names_2015.csv")
dfDims = pd.read_csv("resources/dims_data.csv")

# set the index of the beach data to location slug
dfBeaches.set_index('slug', inplace=True)

# set the code index and edit descriptions for display:
dfCodes.set_index('code', inplace=True)

# make a map to the code descriptions
code_description_map = dfCodes.description

# these descriptions need to be shortened for display
dfCodes = sut.shorten_the_value(["G74", "description", "Insulation: includes spray foams"], dfCodes)
dfCodes = sut.shorten_the_value(["G940", "description", "Foamed EVA for crafts and sports"], dfCodes)
dfCodes = sut.shorten_the_value(["G96", "description", "Sanitary-pads/panty liners/tampons"], dfCodes)
dfCodes = sut.shorten_the_value(["G178", "description", "Metal bottle caps and lids"], dfCodes)


# # The land use profile
# 
# *The land use mix* or *the land use profile* is a numerical representation of the type and amplititude of econmic activity around the survey location.
# 
# Trash is a collection of objects found in the natural environment. The object type and the context in which it is found gives plenty of indicators as to its origin geographically and economically. How the land is used in proximity to the survey location is an important context to consider when evaluating survey results. {cite}`aydin` {cite}`grelaud`
# 
# In September 2020 the European Union issued beach-litter baselines and target values. After considering the many factors, including the transparency of the calculation method the EU decided that the median value of survey results would be used to compare surveys. **This has incited interest in communities to better indentify and quantify point sources of trash as they attempt to find the most efficient way to meet target values**. Identifying relevant land use patterns and features is an essential element in the process. {cite}`threshholdeu` {cite}`eubaselines` {cite}`vanemmerick`
# 
# Here we propose a method to evaluate the results of beach-litter-surveys with respect to the land use profile within 1500m of the survey location. The survey results of the most common objects are tested for association against the measured land use features using Spearmans $\rho$ or *Spearmans ranked correlation*, a non paramatetric test of association. {cite}`defspearmans` {cite}`spearmansexplained`
# 
# ## Assessing land use
# 
# The land use profile is comprised of the measurable properties that are geolocated and can be extracted from the current versions of *Statistique Suisse de la superficie* and *swissTlmRegio*. {cite}`superficie` {cite}`tlmregio`. 
# 
# The following values were calculated within a radius of 1500m of each survey location:
# 
# 1. \% of surface area attributed to buildings
# 2. \% of surface area left to woods
# 3. \% of surface area attributed to outdoor activities
# 4. \% of surface area attributed to aggriculture
# 5. length in kilometers of all roads and trails (railways not included)
# 6. number of river discharge intersections
# 
# **Calculating the land use profile**
# 
# The Office fédéral de la statistique provides the 'Statistique de superficie', a grid of points 100m x 100m that covers Switzerland. Each point is assigned one of 27 different land use categories defined by  standard classification of 2004. This grid serves as the basis for calculating how the land is used around the survey area. For this study the land use categories were aggregated into seven groups from the twenty seven available categories.
# 
# *The aggregated values and the corresponding land use categories*
# 
# * buildings: (1, 2, 3, 4, 5, 9)
# * transprotation:(6, 7, 8)
# * recreation: (10)
# * aggriculture: (11, 12, 13, 14, 15, 16, 18)
# * woods: (17, 19, 20, 21, 22)
# * water: (23, 24)
# * unproductive: (25, 26, 27)
# 
# For each location the cumulaltive sum and the cumulative sum of each group was calculated within the 1500m buffer. The amount allocated to *water* was substracted from the cumulative sum, the result was used to calculate the percent of land use attributed for each category.
# 
# The category *recreation* includes diverse public use applications. Uses range from sports fields to cemeteries, this captures all areas set aside for social activities.
# 
# **Calculating street length**
# 
# The street length was calculated by intersecting the map layer swissTLM3D_TLM_STRASSE with the 1500m buffer of each survey location. All the streets and pathways were combined into one line (QGIS: dissolve) and the length of that line is the reported value of kilometers of streets.
# 
# **Counting riverine inputs**
# 
# For locations on lakes, the number of intersecting river/canal discharges was calculated within 1500m of each survey location. The map layer swissTLM3D_TLM_FLIESSGEWAESSER (rivers) was intersected with swissTLM3D_TLM_STEHENDES_GEWAESSER (lakes), (QGIS: "line intersections"),  and the number of intersections per 1500m buffer was counted, (QGIS: "count points in polygon"). The lakes map layer was extended by 100 meters to capture any discharge points or streams that terminated in close proximity to the lake. {cite}`qgis_software` {cite}`tlmregio`

# *Map layers used to calculate the land use profile. __Top left:__ all measureable values within 1500m. __Top right:__ streets and river intersections within 1500m. __Bottom right:__ land use points used to calculate \% of total and total.*

# In[2]:


output = io.BytesIO()
a_map=PILImage.open("resources/maps/explain_landuse/land_use_dispaly_20.jpeg")
a_map.thumbnail((1200, 800))
a_map.save(output, format='PNG')
encoded_string = base64.b64encode(output.getvalue()).decode()

html = '<img src="data:image/png;base64,{}"/>'.format(encoded_string)
IPython.display.HTML(html)


# _Calculated Land use profile of hauterive-petite-plage, NE._
# 
#     *  to builidings: 32.7%
#     *  to recreation: 9.9%
#     *  to aggriculture: 18.9%
#     *  to woods: 24.3%
#     *  kilometers of streets 85
#     *  river of intersects: 2
# 
# 
# 

# In[3]:


# # get the location
# data = dfBeaches.loc["hauterive-petite-plage"][['% to buildings', '% to recreation', '% to agg', '% to woods', 'population', 'streets', 'intersects']]

# # pretty foramtting
# data[['% to buildings', '% to recreation', '% to agg',  '% to woods']] = data[['% to buildings', '% to recreation', '% to agg', '% to woods']].apply(lambda x: F"{round((x*100),1)}%")

# # scale streets and format population
# data['streets'] = (data['streets']/1000).astype('int')
# data['population'] = F"{data['population']:,}"

# # make all that horzontal and put location as index
# newdf = {x:[data.loc[x]] for x in data.index}
# newdf.update({"location":"hauterive-petite-plage"})

# df = pd.DataFrame(newdf)
# df = df[[df.columns[-1], *df.columns[:-1]]]

# df.set_index('location', drop=True, inplace=True)
# df


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

# <br></br>
# ### Land use profile of the project
# 
# The land use is reported as the percent of total area attributed to each land use category within a 1500m radius of the survey location. The ratio of the number of samples completed at the different land use profiles gives a good *objective* indicator of the envrionmental conditions the samples were taken.

# *Distribution of the number of surveys for the different land use attributes, n=354 samples* 

# In[4]:


# explanatory variables:
luse_exp = ['% to buildings', '% to recreation', '% to agg', '% to woods', 'streets km', 'intersects']

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

use_these_args = (survey_data.water_name_slug != 'walensee')&(survey_data.date >= start_date)&(survey_data.date <= end_date)
survey_data = survey_data[use_these_args].copy()
survey_data.rename(columns={'str_rank':'street rank'}, inplace=True)
survey_data['streets km'] = survey_data.streets/1000
survey_data['date'] = pd.to_datetime(survey_data.date)

a_data = survey_data.copy()

# Combine the different sizes of fragmented plastics and styrofoam
# the codes for the foams
some_foams = ['G81', 'G82', 'G83']

# the codes for the fragmented plastics
some_frag_plas = list(a_data[a_data.groupname == 'plastic pieces'].code.unique())

the_plast_rows = sut.create_aggregate_groups(a_data, codes_to_agg=some_frag_plas,a_model_code="G79", a_new_code="Gfrags")
the_foam_rows = sut.create_aggregate_groups(a_data, codes_to_agg=some_foams, a_model_code="G82", a_new_code="Gfoam")

# the foam codes and fragmented plastic codes have been aggregated in to Gfrags and Gfoam
new_som_data = sut.replace_a_group_of_codes_with_one(a_data, new_code_values=[the_plast_rows, the_foam_rows], codes_to_replace=[*some_frag_plas, *some_foams])

# survey totals
dfdt = new_som_data.groupby(use_these_cols[:-2], as_index=False).agg({unit_label:'sum', 'quantity':'sum'})

# method to get the ranked correlation of pcs_m to each explanatory variable
def make_plot_with_spearmans(data, ax, n):
    sns.scatterplot(data=data, x=n, y=unit_label, ax=ax, color='black', s=30, edgecolor='white', alpha=0.6)
    corr, a_p = stats.spearmanr(data[n], data[unit_label])
    return ax, corr, a_p

# group the explanatory variables and count the number of surveys for the different landuse values
sns.set_style("whitegrid")
fig, axs = plt.subplots(1,len(luse_exp), figsize=(14,3), sharey=True)

data = dfdt.copy()

for i, n in enumerate(luse_exp):
    ax=axs[i]
    the_data = ECDF(data[n].values)
    x, y = the_data.x, the_data.y   
    
    sns.lineplot(x=x, y=y, ax=ax, color='dodgerblue', label="% of surface area" )
    # get the median from the data
    the_median = data[n].median()
    
    # plot the median and drop horzontal and vertical lines
    ax.scatter([the_median], 0.5, color='red',s=50, linewidth=2, zorder=100, label="the median")
    ax.vlines(x=the_median, ymin=0, ymax=0.5, color='red', linewidth=2)
    ax.hlines(xmax=the_median, xmin=0, y=0.5, color='red', linewidth=2)
    
    #remove the legend from ax   
    ax.get_legend().remove()
    
    if i == 0:
        ax.set_ylabel("Percent of samples", **ck.xlab_k)
    else:
        pass
    ax.set_title(F"The median: {(round(the_median, 2))}",fontsize=12, loc='left')
    ax.set_xlabel(n, **ck.xlab_k)
    
# handles, labels=ax.get_legend_handles_labels() 


plt.tight_layout()
# fig.legend(handles, labels, bbox_to_anchor=(1,1.1), loc='upper right', ncol=2)
plt.show()


# **The land use** around the survey locations had a higher attribution to buildings as opposed to agriculture and woods. For example, half of all the surveys had at least  37\% of land use devoted to buildings as opposed to 19\% for agriculture or woods. Land use devoted to recreation was at least 6% for half of all samples. 
# 
# **The length of the road network** within the buffer zone differentiates between locations that have other wise similar land use characteristics. The length of road per buffer ranges from 13km to 212km, 50% of the surveys had less than 67km of road network.
# 
# **The number of intersections** ranges from zero to 23, 50% of the surveys had 3 or fewer intersections within 1500m of the survey location. The size of the intersecting river or canal was not taken into consideration. Survey locations on rivers have zero intersections.
# 
# **The population** (not shown) is taken from statpop 2018 and represents the population of the municipality surounding the survey location. The smallest population was 442 and the maximum was 415,367, 50% of the surveys come from municipalities with a population of at least 12,812.

# ### Choosing survey sites
# 
# The survey locations were chosen based on the following criteria:
# 
# 1. Data from previous surveys (SLR, MCBP)
# 2. Year round safe access
# 3. Within 30 minutes walking distance from nearest public transport
# 
# **The survey locations represent the land use conditions accesible by public transport to $\approx$ 1.7 million people**. For more information see the document *Survey site selection and criteria*.

# ## Associating land use to survey results
# 
# ### The data
# 
# There are 354 surveys from 134 locations. This includes rivers and lakes. The results from Walensee are excluded, the data was incomplete for that part of Switzerland. The mean was more than twice the median, reflecting the extreme values that are typical of beach-litter-surveys. 

# In[5]:


# set the date intervas for the chart
months = mdates.MonthLocator(interval=1)
months_fmt = mdates.DateFormatter('%b')
days = mdates.DayLocator(interval=7)

# set the grid for the chart
sns.set_style("whitegrid")
fig, ax = plt.subplots(1,2, figsize=(10,6), sharey=False)

axone=ax[0]
axtwo = ax[1]

axone.set_ylabel(unit_label, **ck.xlab_k14)
axone.xaxis.set_minor_locator(days)
axone.xaxis.set_major_formatter(months_fmt)
axone.set_xlabel(" ")

axtwo.set_ylabel("% of samples", **ck.xlab_k14)
axtwo.set_xlabel(unit_label, **ck.xlab_k)

# time series plot of the survey results
sns.scatterplot(data=dfdt, x='date', y=unit_label, color='dodgerblue', s=34, ec='white', ax=axone)

# ecdf of the survey results
this_ecdf = ECDF(dfdt.pcs_m.values)

# plot the cumulative disrtibution
sns.lineplot(x=this_ecdf.x,y=this_ecdf.y, ax=axtwo, label='emprical cumulative distribution')
# get the median and mean from the data
the_median = data[unit_label].median()
the_mean = data.pcs_m.mean()

# get the percentile ranking of the mean
p_mean = this_ecdf(the_mean)

# plot the median and drop horzontal and vertical lines
axtwo.scatter([the_median], 0.5, color='red',s=50, linewidth=2, zorder=100, label="the median")
axtwo.vlines(x=the_median, ymin=0, ymax=0.5, color='red', linewidth=1)
axtwo.hlines(xmax=the_median, xmin=0, y=0.5, color='red', linewidth=1)

# plot the mean and drop horzontal and vertical lines
axtwo.scatter([the_mean], p_mean, color='magenta',s=50, linewidth=2, zorder=100, label="the mean")
axtwo.vlines(x=the_mean, ymin=0, ymax=p_mean, color='magenta', linewidth=1)
axtwo.hlines(xmax=the_mean, xmin=0, y=p_mean, color='magenta', linewidth=1)

handle, labels = axtwo.get_legend_handles_labels()

plt.legend(handle,labels)

plt.tight_layout()

plt.show()


# *Survey results and cumulative distribution all lakes and rivers (Walensee excluded).*
# 
# *Number of samples: 354, number of locations: 134, median:2.04 pcs/m, mean:4.11 pcs/m*

# ### Spearmans $\rho$ an example
# 
# Spearmans ranked correlation tests for a statistically significant monotonic relationship or association between two variables. The hypothesis is that there is no association between the land use profile and the survey results. 
# 
# The test results relate the direction ($\rho$) of an association and whether or not that association is likely due to chance (p-value). For a test to be considered significant the p-value needs to be less than 0.05.
# 
# It does not provide any information about the magnitude of the relationship. As an example consider the relationship of the survey results of cigarette ends with respect to the amount of land attributed to buildings or aggriculture.

# *__Left:__ survey totals cigarette ends with respect to % of land to buildings. $\rho$= 0.39, p-value < .001*

# In[6]:


# data for the example
data = new_som_data[new_som_data.code == "G27"].groupby(["loc_date","% to buildings", "% to agg"], as_index=False)[unit_label].sum()

# run the test
sprmns_b = stats.spearmanr(data["% to buildings"], data[unit_label])
sprmns_a = stats.spearmanr(data["% to agg"], data[unit_label])

fig, axs = plt.subplots(1,2, figsize=(9,6), sharey=True)

# plot the survey results with respect to the land use profile
sns.scatterplot(data=data, x="% to buildings", y=unit_label, ax=axs[0], color='magenta')
sns.scatterplot(data=data, x="% to agg", y=unit_label, ax=axs[1], color='dodgerblue')

axs[0].set_xlabel("% to buildings", **ck.xlab_k14)
axs[1].set_xlabel("% to agg", **ck.xlab_k14)

axs[0].set_ylabel(unit_label, **ck.xlab_k14)

plt.tight_layout()
plt.show()


# *__Right:__ survey totals cigarette ends with respect to % of land to aggriculture. $\rho$= -0.31, p-value < .001*

# The test results confirm what appears to be an association between the quantity of cigarette ends found and the percent of land attributed to aggriculture or buildings. A non conclusive test means that we can assume that there is no association between the land use profile and the survey results. 

# ### Association of survey totals to land use

# *Results of Spearmans ranked correlation test: survey totals with respect to land use profile*

# In[7]:


# correlation  of survey total to land use attributes:

fig, axs = plt.subplots(1,len(luse_exp), figsize=(14,3), sharey=True)

for i, n in enumerate(luse_exp):
    ax=axs[i]
    ax, corr, a_p = make_plot_with_spearmans(dfdt, ax, n)
    if i == 0:
        ax.set_ylabel('pieces per meter', **ck.xlab_k)
    ax.set_xlabel(n, **ck.xlab_k)
    if a_p <= .001:
        title_str = "p < .001"
    else:
        title_str = F"p={round(a_p, 3)}"
    
    ax.set_title(rF"$\rho={round(corr,4)}$, {title_str}")
    
    if a_p < 0.05:
        if corr > 0:
            ax.patch.set_facecolor('salmon')
            ax.patch.set_alpha(0.5)
        else:
            ax.patch.set_facecolor('palegoldenrod')
            ax.patch.set_alpha(0.5)

            plt.ylabel('pieces per meter', **ck.xlab_k)
plt.tight_layout()
plt.show()


# In general a positive relationship can be assumed between survey results and percent of land to buildings or recreation, and a negative association with woods and agriculture. 

# ### Association of most common objects to land use
# 
# **The most common objects are** all objects that were either the ten most abundant by quantity or any object that was indentified in at least 50% of all the surveys. In this way we are accounting for $\approx 68$% of all objects found and counted. These lists are not the same, not all objects that were found 50% of the time are found in large enough quantities to make the "top ten list".

# In[8]:


# the number of times an object was found at least once
code_fails = new_som_data.groupby('code').fail.sum()

# the ratio of found/not found
code_fail_rate = code_fails/new_som_data.loc_date.nunique()

# all codes with a fail rate > fail rate
better_than_50 = code_fail_rate[code_fail_rate > a_fail_rate]

some_keys = {
    '% to buildings':'lu_build',
    '% to agg':'lu_agg',
    '% to woods':'lu_woods',
    '% to recreation':'lu_rec',
    '% to trans':'lu_trans',
    '% to meadow':'lu_m',
    'str_rank':'lu_trans',}

code_totals = new_som_data.groupby('code').quantity.sum()

t_ten = code_totals.sort_values(ascending=False)[:10]
tlist = list(t_ten.index)

for code in better_than_50.index:
    if code in t_ten.index:
        pass
    else:
        tlist.append(code)
        

abundant_codes = tlist

total_acodes = new_som_data[new_som_data.code.isin(abundant_codes)].quantity.sum()
ptotal_acodes = total_acodes/new_som_data.quantity.sum()
# print(ptotal_acodes)

display_codes = ",\n".join([F"{i+1}. {x}: {code_description_map[x]}" for i,x in enumerate(abundant_codes)])

md(F"The most common objects:\n{display_codes}")


# #### Results Spearmans $\rho$
# 
# From the first figure a positive correlation can be assumed between the amount of trash found and the percent of land attributed to buildings and recreation.  The inverse is true for the percent of land attributed to aggriculture and woods, there is no statisitical basis to assume a correlation with the length of streets or the number of river intersections.
# 
# The result of  Spearman's rho on the most abundant objects gives context to the results in the preceding figure and changes the assumption that neither river intersections or streets plays a role in beach-litter-survey-results.

# In[9]:



fig, axs = plt.subplots(len(abundant_codes),len(luse_exp), figsize=(len(luse_exp)+7,len(abundant_codes)+6), sharey='row')

for i,code in enumerate(abundant_codes):
    data = new_som_data[new_som_data.code == code]
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

plt.tick_params(labelsize=14, which='both', axis='both')
plt.tight_layout()
plt.subplots_adjust(wspace=0, hspace=0)
plt.savefig(F"{project_directory}/test_one.jpg", dpi=300)
plt.show()


# ### Interpreting Spearmans $\rho$
# 
# A positive association means that the land use attribute or feature had increased survey results when compared to other locations. This may be due to a covariance of attributes, either way **a positive association is a signal that the survey locations are near a zone of accumulation or a source**. This signal should be assessed along with the other key indicators of survey locations that have similar land use profiles. In general locations that fit the criteria could be considered as both a source and an area of accumulation for any objects that are positively associated.
# 
# A negative association means that the land use feature or attribute does not facilitate the accumulation of the object. This result is common for aggricultural areas and woods on the national level. **A negative association is a signal that the locations are not a zone of accumulation for the object**.
# 
# No or few association means that the land use features had no effect on the accumulation of that object. The survey results of the most common objects with no or few associations fall into two charateristics: 
# 
# 1. Ubiquitous: high fail rate, high pieces per meter. Found at consistent rates through out the survey area indifferent of land use
# 2. Transient: low fail rate, high quantity, high pieces per meter, few associations. Found occasionaly in large quantities at specific locations
# 
# 
# ### Conclusions
# 
# Overall, surveys at locations with more buildings and more recreation sites had more trash (all objects considered). However, when the most common objects are considered, only five out of the twelve were found at higher rates in the presence of more buildings. Of those objects: cigarette ends, candy wrappers, glass drink bottles and metal drink lids are likely related to food or tobacco consumption. Objects associated with food consumption or smoking are found at higher rates in locations that have more space attributed to human interaction as opposed to space devoted to farming or forestry, this has been observed in other studies indifferent of the statistical method.  
# 
# Several of the most objects that have less than two associations:
# 
# 1.  objects that have high fail rate and few associations
#     * plastic conststruction waste
#     * fragmented plastics
#     * industrial sheeting
#     * expanded polystyrene
#     
# 2. few associations, low fail rate, high pcs/m
#    * industrial pellets
# 
# The objects in the first group are just as likely to be found indifferent of the location, in general they make up 30% - 40% of the total trash found.
# 
# Industrial pellets (group 2) are found in only 1/3 surveys, their presence in the most common objects indicates they have been found in important quantities at select locations. An association with land attributed to recreaction means that the locations where they were found had a higher percent of land attributed to recreation.
# 
# Each survey area is independent of the other, therfore it is expected that the association results will look different for each survey area where this analysis is applied. The association of an object with a particular land use profile should be considered along with all the relevant key indicators and the specific context of the survey area in question.

# In[10]:


author = "roger@hammerdirt.ch"
my_message = "Love what you do. \u2764\ufe0f"
md(F"""
**This project was made possible by the Swiss federal office for the environment.**<br>

>{my_message}<br>

*{author}* pushed the run button on {today}.<br>
This document originates from https://github.com/hammerdirt-analyst/IQAASL-End-0f-Sampling-2021 all copyrights apply.<br>
""")


# In[ ]:




