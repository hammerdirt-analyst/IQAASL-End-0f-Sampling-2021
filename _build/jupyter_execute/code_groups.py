#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# (codegroups)=
# # Code groups
# 
# <a href="baselines_de.html"> Deutsch </a>
# 
# The IQAASL project used the item codes and descriptions from the Marine Strategy Framework (MSFD) master list  {cite}`mlwguidance`.      Item identification follows the protocols from the MSFD Technical Subgroup on Marine Litter. The master list was developed based on the categories of items used in a series of programs and is one of the most detailed, representing established EU protocols. There are 217 identification codes to classify all objects collected from a survey. The item codes begin with G1 and end with G217. 
# 
# ## Accounting for regional objects
# 
# There are items identified regularly in Switzerland that do not appear in the master list. To account for this 43 codes were added to the master list under the parent code G124. These codes begin with G900 and end with G999. 
# 
# Some MSFD codes such as G124 other plastic/polystyrene items, identifiable allows for quantification of unlisted identifiable plastic items. An added item such as G913 pacifier can be quantified independently and linked to the MSFD code G124. This work is done at the server and the data can be analyzed using either form. 
# 
# Identifiable plastic objects were either attributed to an additional code such as G913, or if no other code described the item then G124 was used. Some codes were included to capture pandemic related items such as: 
# 
# * G901 Mask medical, synthetic (Parent code (G124) other plastic/polystyrene items identifiable)
# * G902 Mask medical, cloth (Parent code (G145) other textiles) 
# 
# __Codes and parent codes:__ accounting for regional differences. G902 is linked to G145 by the value in the column parent_code. G937 is linked to G124 by the parent code.

# In[2]:


# aggregated survey data
dfAgg = pd.read_csv("resources/checked_before_agg_sdata_eos_2020_21.csv")
dfAgg["date"] = pd.to_datetime(dfAgg["date"])

# get the data:
dfCodes = pd.read_csv("resources/codes_with_group_names_2015.csv")
dfCodes["parent_code"] = dfCodes.parent_code.where(dfCodes.parent_code != "Parent code", "none")

cols_to_display = ["code", "description","groupname",  "parent_code"]

dfCodes[dfCodes.code.isin(["G124", "G902", "G145","G937"])][cols_to_display].set_index("code")


# ### Modification of items by size and material descriptions
# 
# Several important size and material modifications were
# made specifically to the fragmented plastic and foamed
# plastic categories. Other modifications include expansion
# or narrowing of item descriptions.
# 
# * G96 sanitary towels, panty liners modified to include plastic tampon applicators.
# * G211 adhesive bandages modified from unclassified material to plastic.
# 
# To best identify and quantify micro plastics for this project 3 codes were modified by size from the _master list_.
# 
# Codes modified to account for objects less than 5mm:
# 
# * G75 Plastic/polystyrene pieces 0 - 2.5 cm modified to 0.5 cm - 2.5 cm
# * G78 Plastic pieces 0 - 2.5cm modified to 0.5cm - 2.5cm
# * G81 Polystyrene pieces 0 - 2.5cm modified to 0.5 cm - 2.5 cm
# 

# In[3]:


sut.display_image_ipython("resources/images/codegroups/20200819_080041.jpg", thumb=(700,1100), rotate=0)


# *Various sizes of plastic pieces*

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


# ### Foamed plastics: Gfoams
# 
# Expanded polystyrene G81, G82, G83 grouped as Gfoam, are light, friable, often white foamed plastics used for packaging or insulation. Foamed plastic items commonly used for take out food G10, sponge foams G73 and denser insulation foams G74 are categorized separately and not included in the expanded polystyrene group.
# 
# The foam packaging/insulation/polyurethane G74 was expanded in this study to include extruded polystyrenes (XPS) that are commonly used as insulation and conversely
# narrowed for G81, G82, and G83 polystyrene pieces to expanded polystyrene (EPS) larger than 0.5cm. These modification were to differentiate insulation foams from packaging foams although both are used for a variety of applications. The material modifications to the foamed plastics is grouped to the _parent code_ for analysis and recorded separately. A detailed inventory of the type and size of foam is provided with each report.
# 
# :::{note}
# Polystyrene beads less than 5mm, brand name Styrofoam® are grouped with micro plastics (G117) styrofoam < 5mm.
# :::

# In[5]:


wwcodes = dfCodes[dfCodes.code.isin(["G81", "G82", "G83"])][cols_to_display]
wwcodes.set_index("code", drop=True)


# In[6]:


sut.display_image_ipython("resources/images/codegroups/20210221CheyresFoam.jpg", thumb=(600,1000), rotate=360)


# *Various sizes of white expanded polystyrene and other foamed plastics*

# ### Not applicable or omitted items
# 
# Of the 217 MSFD codes available 176 of the items were identified in the 2020-2021 surveys. Several items are not applicable to Swiss waters as they pertain to marine aquaculture production:
# 
# * G207 octopus pots
# * G163 crab/lobster pots
# * G215 food waste/galley waste*
# 
# *All naturally biodegradable food waste as well as feces collection and quantification was omitted from this project*.

# In[7]:


sut.display_image_ipython("resources/images/codegroups/petite_plage_yverdon_lesBains15_02_2021.png", thumb=(800,1200), rotate=0)


# ## Objects grouped by use 
# 
# Individual item codes have been grouped to best describe usage and possible sources. It is acknowledged that some items in a group contribute to a percentage rather than the whole sum. Code grouping is a broad analysis method to evaluate the discarded materials found in water systems by economic sectors or physical properties. Items are also analyzed independently in this report. The grouping is derived from field observations and research to determine possible sources of various pollutants.
# 
# 1. wastewater: items released from water treatment plants includes items likely toilet flushed   
# 2. micro plastics (< 5mm): foams, plastic fragments and pre-production resins
# 3. infrastructure: items related to construction and maintenance of all buildings, roads and water/power supplies 
# 4. food/drink: primarily single use plastic items related to consuming food and drinks outdoors  
# 5. agriculture: mainly industrial sheeting for: mulch, row covers, greenhouses, soil fumigation and bale wraps includes hard plastics: agricultural fencing, plastic flower pots etc. 
# 6. tobacco: predominately cigarette filters, includes all smoking related material 
# 7. recreation: fishing, hunting, boating and beach related objects, excludes food, drink and tobacco   
# 8. packaging non food/drink: packaging or wrapping material not identifiable as food, drink nor tobacco related  
# 9. plastic pieces: plastic or foam/plastic composite pieces greater than 0.5 cm
# 10. personal items: personal use related; accessories, hygiene and clothing
# 11. Unclassified: ungrouped item codes
# 
# 

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
axone.set_title("Agriculture: industrial sheeting", **ck.title_k14)

axtwo=ax[0,1]
sut.hide_spines_ticks_grids(axtwo)
axtwo.imshow(img_b);
axtwo.set_title("Recreation: toys, fireworks, shotgun cartridge, fishing items", **ck.title_k14)

axthree=ax[1,0]
sut.hide_spines_ticks_grids(axthree)
axthree.imshow(img_c);
axthree.set_title("Infrastructure: construction plastics", **ck.title_k14)

axfour=ax[1,1]
sut.hide_spines_ticks_grids(axfour)
axfour.set_title("Wastewater and Personal items: bio filters, sanitary pad, syringe", **ck.title_k14)
axfour.imshow(img_d);

plt.tight_layout()
plt.show()


# *Material grouping examples*

# ### Wastewater treatment 
# 
# Wastewater treatment codes includes toilet flushed plastic items such as cotton swabs and direct use items such as biomass holders. 
# 
# :::{note}
# G98 includes diapers and wipes. Diapers are rarely found in Swiss water systems the quantities should be attributed to personal hygiene wipes.
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

wwcodes = dfCodes[dfCodes.code.isin(wastewater)][cols_to_display]
wwcodes.set_index("code", drop=True)


# ### Micro plastics 
# 
# Micro codes are all micro plastics and foams from the _master list_ items G103-G123. Not all codes have been identified in our data.  The objective of this project was to quantify observable litter which tends to be greater than 0.5 cm but the lower limit of natural visible detection when surveying a shore line is around 2 - 5mm. 
# Over the course of a survey, visible micro items are collected with the lager material and composition is generally identifiable. The IQAASL project did not include methods to specifically target items less than 5mm but all visible micro plastics collected during a survey were quantified, weighed and categorized using 20 codes available to classify plastics less than 5mm.

# *Plastic objects less than 5mm*

# In[10]:


# define group
codesmicro=["G112", "G106", "G117", "G103", "G104", "G105", "G107", "G108", "G109", "G110", "G111", "G113", "G114", "G115", "G116", "G118", "G119", "G120", "G121", "G122", "G123"]

# make table
wwcodes = dfCodes[dfCodes.code.isin(codesmicro)][cols_to_display]
wwcodes.set_index("code", drop=True)


# ### Infrastructure 
# 
# Infrastructure relates to all forms of construction, renovations and maintenance of public and private structures including roads, bridges and ports as well as power and water supplies. Important quanties of construction plastics and especially foamed plastics were identified along all lakes of study. See survey results 2020-2021 [All surveys areas](allsurveys)
# 
# The most common construction plastics are pieces of piping, flexible and rigid hosings and cable protectors as well as associated connectors, fittings and covers. Also common are plastics used in concrete forming such as dowels, anchors and spacers. Some items associated with plastic construction have unique codes such as G93: _cable ties_  or G17: _injection gun containers_.
# 
# Other items in the infrastrucutre group have a more general use case:
# 
# * G186 Industrial scrap
# * G194 Metal cables

# #### Infrastrucutre: foamed plastics
# 
# All foamed plastics associated with insulation applications are attributed to the infrastructure group. Extruded foams are relatively dense multi colored foam boards and spray foams greater than 0.5 cm. Expanded polystyrene is included as infrastructure related due to the common use as an exterior insulator for above ground applications.  Additional codes were created to quantify size variations of foams, G909 - G912. The modifications were to differentiate construction insulation foams from packaging foams although both are used for a variety of applications. The material modifications to the foamed plastics is grouped to the _parent code_ for analysis and recorded separately. A detailed inventory of the type and size of foam is provided with each report. 

# In[11]:


sut.display_image_ipython("resources/images/codegroups/fragfoam_450_600.jpg", thumb=(600, 1000), rotate=0)


# *Various sizes of foamed plastics; XPS, EPS, and spray foams SPF along Swiss shorelines*

# *Infrastructure group items*

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

wwcodes = dfCodes[dfCodes.code.isin(construction2)][cols_to_display]
wwcodes.set_index("code", drop=True)


# ### Food and drink 
# Includes all materials associated with eating and drinking. The greatest quantities are single use plastics (SUP) items related to outdoor or to go consumption. Packaging for candy and snacks items G30 and broken glass G200 are the most prevalent along Swiss shorelines. See survey results 2020-2021 [All surveys areas](allsurveys)

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

wwcodes = dfCodes[dfCodes.code.isin(foodstuff)][cols_to_display]
wwcodes.set_index("code", drop=True)


# ### Agriculture
# 
# Several codes were added to identify items pertaining to agriculture such as G937: _plastic pheromone baits_ commonly used in vineyards and G943: _plastic fencing_ associated with seasonal animal pasturing. The specific sheeting code G936: _greenhouse films and silage wrap_ was added for a particular type of product where the agriculture use is identifiable. 
# 
# Industrial sheeting (G67) is a broad category that includes plastic sheets and films that are flat pieces of plastic formed to a precise thickness for use in specific applications. Products differ in terms of materials, properties, and dimensions {cite}`globalspec`.
# Isolating agricultural plastic sheeting use is difficult as the same plastics are utilized extensively in the packaging and construction sectors. Predominately along Swiss shorelines plastic sheeting and films are extremely weathered and fragmented making definitive use and origin difficult to determine.
# 
# Industrial sheeting is attributed to the agriculture group due to continious exposure to physical elements and use in close proximity to  rivers, streams and canals. Industrial sheeting is also attributed to agriculture due to the continuously increasing use of plastic materials in agricultural applications commonly referred to as plasticulture.
# Plasticulture includes irrigation tubing, plastic nursery pots, and an extensive use of sheeting, wraps and films for horticultural, grain crops and dairy sectors {cite}`plasticulture`.
# 
# Plasticulture sheeting and films G67:
# 
# * mulch film
# * row coverings
# * polytunnels
# * plastic greenhouses
# * soil fumigation films
# * silage bale wrap
# 

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

wwcodes = dfCodes[dfCodes.code.isin(ag2)][cols_to_display]
wwcodes.set_index("code", drop=True) 


# ### Tobacco codes
# 
# All tobacco related items.

# In[15]:


tobac = [
    "G25",
    "G26",
    "G27",
    "G152"
    ]

wwcodes = dfCodes[dfCodes.code.isin(tobac)][cols_to_display]
wwcodes.set_index("code", drop=True)


# ### Recreation codes
# 
# The recreational group includes fishing, hunting, boating and beach related objects, excludes food, drink and tobacco. Plastic shotgun cartridges (G70) are found in surprising numbers considering hunting is not allowed along public beaches and maybe a key indicator of travel distances through the water systems.

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

wwcodes = dfCodes[dfCodes.code.isin(recreation)][cols_to_display]
wwcodes.set_index("code", drop=True)


# ### Packaging not related to food, drink, tobacco or unknown origin.
# All  packaging or wrapping material including paper, plastic and metal not identified as food, drink nor tobacco related. The packaging non food/drink group includes (G941) a code added  to differentiate thin packaging films from thicker industrial sheeting. The plastic packaging films (G941) are classified as non food, drink, nor tobacco related. Commonly the films are highly deteriorated and fragmented making the original use and source difficult to determine.
# 
# 
# 

# *Packaging not related to tobacco or food and drink or origin unknown*

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

wwcodes = dfCodes[dfCodes.code.isin(packaging)][cols_to_display]
wwcodes.loc[wwcodes.code == "G925", "description"] = "Dessicants/moisture absorbers"
wwcodes.set_index("code", drop=True)


# ### Fragmented plastics: Gfrags
# 
# The plastic fragments group (Gfrags for analysis) are all plastic and foam/plastic composite pieces greater than 0.5 cm. Plastic pieces found along Swiss shorelines are predominately small, hard, highly fragmented pieces of a pigmented item. The original use and source is principally undetermined. Individual plastic pieces were quantified by material and size:

# *Fragmented plastics code group, Gfrags*

# In[18]:


plasticpcs = [
    "G78",
    "G79",
    "G80",
    "G75", 
    "G76", 
    "G77" 
    ]

wwcodes = dfCodes[dfCodes.code.isin(plasticpcs)][cols_to_display]
wwcodes.set_index("code", drop=True)


# In[19]:


sut.display_image_ipython("resources/images/codegroups/Yverdon_lesBainsLacNeuchâtel15_02_2021.jpg", thumb=(800, 1200), rotate=0)


# *Various sizes of plastic pieces*

# ### Personal Items
# 
# Includes accessories, hygiene and clothing related items lost or discarded. Includes pandemic related items such as face masks as well as beach related items such as sunglasses and clothing.
# 
# Additional MSFD and IQAASL codes related to personal items:
# 
# * G923 tissue, toilet paper, napkins, paper towels Parent code (G158) Other paper items
# * G96 sanitary towels, pantyliners modified to include tampon applicators
# * G100 medical, pharmaceutical containers and tubes

# *Personal items*

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
wwcodes = dfCodes[dfCodes.code.isin(pi)][cols_to_display]
wwcodes.set_index("code", drop=True)


# ### Unclassified items 
# 
# The non grouped codes are predominately items that are ambiguous in origin, rarely identified, or do not pertain to shoreline surveillance of Swiss water systems. Many of the non grouped items have a total value of 0 for all survey data included in this report.
# 
# Notable exceptions are G20 and G23 plastic caps/lids unidentified which are found in significant quantities but use and origin are unknown.
# 
# Glass or ceramic fragments >2.5cm G208 is also unclassified in this report. Predominately ceramic pieces of unknown use or origin are identified frequently and in relatively high concentrations. The occurrence of ceramic fragments may be related to the sources of material for beach replenishing practices as well as natural transport and deposition processes rather than food and drink or other beach related activities. Identifiable glass drink bottles and pieces are classified as (G200) bottles and includes pieces, they are grouped with food and drink.

# In[21]:


wwcodes = dfCodes[dfCodes.groupname == "unclassified"][cols_to_display]
wwcodes.loc[wwcodes.code == "G38", "description"] = "Coverings sheeting for protecting large cargo items"
wwcodes.set_index("code", drop=True)


# ## List of additional codes

# *local codes added for Swiss water systems*

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

wwcodes = dfCodes[dfCodes.code.isin(addcodes)][cols_to_display]
wwcodes.loc[wwcodes.code == "G933", "description"] = "Bags cases for accesories"
wwcodes.loc[wwcodes.code == "G932", "description"] = "Biomass beads for waste water treatment"

wwcodes.set_index("code", drop=True)


# ## Local codes added for Swiss alps

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

wwcodes = dfCodes[dfCodes.code.isin(alpcodes)][cols_to_display]
wwcodes.loc[wwcodes.code == "G933", "description"] = "Bags cases for accesories"
wwcodes.loc[wwcodes.code == "G932", "description"] = "Biomass beads for waste water treatment"

wwcodes.set_index("code", drop=True)


# In[24]:


# hmm = dfAgg.copy()
# hmm = hmm[["code","quantity"]].groupby("code", as_index=False).quantity.sum()

# found = hmm[hmm.quantity > 0].code.unique()

# ahh=[code for code in dfCodes.code if code not in found]

# # saving to .json
# # push_this_to_json(filename=F"{project_directory}/codeNotfound.json", data=ahh)

# dfCodes[dfCodes.source_two == "cons"]
# figname = F"codes_with_groups.csv"
# filename=F"{output}/code_groups/{figname}"
# dfCodes.to_csv(filename, index=None) 


# In[ ]:




