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
import datetime as dt
from datetime import date, datetime, time
from babel.dates import format_date, format_datetime, format_time, get_month_names
import locale

# math packages:
import pandas as pd
import numpy as np
from math import pi

# charting:
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import ticker
from matplotlib.ticker import MultipleLocator
import seaborn as sns

# build report
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, ListFlowable, ListItem
from reportlab.lib.pagesizes import letter, A4
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.platypus import Table, Paragraph
from reportlab.lib import colors

# the module that has all the methods for handling the data
import resources.featuredata as featuredata

# home brew utitilties
import resources.chart_kwargs as ck
import resources.sr_ut as sut

# images and display
from IPython.display import Markdown as md
from myst_nb import glue

# chart style
sns.set_style("whitegrid")

# colors for gradients
cmap2 = ck.cmap2
colors_palette = ck.colors_palette

# border and row shading for tables
a_color = "saddlebrown"
table_row = "saddlebrown"

## !! Begin Note book variables !!

# There are two language variants: german and english
# change both: date_lang and language
date_lang =  'de_DE.utf8'
locale.setlocale(locale.LC_ALL, date_lang)

# the date format of the survey data is defined in the module
date_format = featuredata.date_format

# the language setting use lower case: en or de
# changing the language may require changing the unit label
language = "de"
unit_label = "p/100 m"

# the standard date format is "%Y-%m-%d" if your date column is
# not in this format it will not work.
# these dates cover the duration of the IQAASL project
start_date = "2020-03-01"
end_date ="2021-05-31"
start_end = [start_date, end_date]

# the fail rate used to calculate the most common codes is
# 50% it can be changed:
fail_rate = 50

# Changing these variables produces different reports
# Call the map image for the area of interest
bassin_map = "resources/maps/bielersee_scaled.jpeg"

# the label for the aggregation of all data in the region
top = "Alle Erhebungsgebiete"

# define the feature level and components
# the feature of interest is the Aare (aare) at the river basin (river_bassin) level.
# the label for charting is called 'name'
this_feature = {'slug':'bielersee', 'name':"Bielersee", 'level':'water_name_slug'}

# the lake is in this survey area
this_bassin = "aare"
# label for survey area
bassin_label = "Aare-Erhebungsgebiet"

# these are the smallest aggregated components
# choices are water_name_slug=lake or river, city or location at the scale of a river bassin 
# water body or lake maybe the most appropriate
this_level = 'city'

# identify the lakes of interest for the survey area
lakes_of_interest = ["bielersee"]    


# !! End note book variables !!
## data
# Survey location details (GPS, city, land use)
dfBeaches = pd.read_csv("resources/beaches_with_land_use_rates.csv")
# set the index of the beach data to location slug
dfBeaches.set_index("slug", inplace=True)

# Survey dimensions and weights
dfDims = pd.read_csv("resources/corrected_dims.csv")

# code definitions
dxCodes = pd.read_csv("resources/codes_with_group_names")
dxCodes.set_index("code", inplace=True)

# columns that need to be renamed. Setting the language will automatically
# change column names, code descriptions and chart annotations
columns={"% to agg":"% agg", "% to recreation": "% recreation", "% to woods":"% woods", "% to buildings":"% buildings", "p/100m":"p/100 m"}

# !key word arguments to construct feature data
# !Note the water type allows the selection of river or lakes
# if None then the data is aggregated together. This selection
# is only valid for survey-area reports or other aggregated data
# that may have survey results from both lakes and rivers.
fd_kwargs ={
    "filename": "resources/checked_sdata_eos_2020_21.csv",
    "feature_name": this_feature['slug'], 
    "feature_level": this_feature['level'], 
    "these_features": this_feature['slug'], 
    "component": this_level, 
    "columns": columns, 
    "language": 'de', 
    "unit_label": unit_label, 
    "fail_rate": fail_rate,
    "code_data":dxCodes,
    "date_range": start_end,
    "water_type": None,    
}

fdx = featuredata.Components(**fd_kwargs)

# call the reports and languages
fdx.adjustForLanguage()
fdx.makeFeatureData()
fdx.locationSampleTotals()
fdx.makeDailyTotalSummary()
fdx.materialSummary()
fdx.mostCommon()
fdx.codeGroupSummary()

# !this is the feature data!
fd = fdx.feature_data

# !keyword args to build period data
# the period data is all the data that was collected
# during the same period from all the other locations
# not included in the feature data. For a survey area
# or river bassin these_features = feature_parent and 
# feature_level = parent_level
period_kwargs = {
    "period_data": fdx.period_data,
    "these_features": this_feature['slug'],
    "feature_level":this_feature['level'],
    "feature_parent":this_bassin,
    "parent_level": "river_bassin",
    "period_name": bassin_label,
    "unit_label": unit_label,
    "most_common": fdx.most_common.index
}
period_data = featuredata.PeriodResults(**period_kwargs)

# the rivers are considered separately
# select only the results from rivers
# this can be done by updating the fd_kwargs
fd_rivers = fd_kwargs.update({"water_type":"r"})
fdr = featuredata.Components(**fd_kwargs)
fdr.makeFeatureData()

# collects the summarized values for the feature data
# use this to generate the summary data for the survey area
# and the section for the rivers
admin_kwargs = {
    "data":fd,
    "dims_data":dfDims,
    "label": this_feature["name"],
    "feature_component": this_level,
    "date_range":start_end,
    **{"dfBeaches":dfBeaches}
}
admin_details = featuredata.AdministrativeSummary(**admin_kwargs)
admin_summary = admin_details.summaryObject()

# update the admin kwargs with river data to make the river summary
admin_kwargs.update({"data":fdr.feature_data})
admin_r_details = featuredata.AdministrativeSummary(**admin_kwargs)
admin_r_summary = admin_r_details.summaryObject()


# pdf download is an option 
# reportlab is used to produce the document
# the arguments for the document are captured at run time
# capture for pdf content
pdfcomponents = []

def addToDoc(flowables, alist):
    
    doc_components = [*alist, *flowables]
    return doc_components

# style definitions for pdf report
title_style = ParagraphStyle(**{"name": "title_style", "fontSize": 18, "fontName": "Helvetica"})
section_title = ParagraphStyle(**{"name": "section_title", "fontSize": 16, "fontName": "Helvetica"})
caption_style = ParagraphStyle(**{"name": "caption_style", "fontSize": 9, "fontName": "Times-Italic"})
subsection_title = ParagraphStyle(**{"name": "sub_section_title", "fontSize": 12, "fontName": "Helvetica"})
p_style = ParagraphStyle(**{"name": "content", "fontSize": 10, "fontName": "Times-Roman"})
bold_block = ParagraphStyle(**{"name": "bold_block", "fontSize": 10, "fontName": "Times-Bold"})
larger_space = Spacer(1, .5*inch)
large_space = Spacer(1, .25*inch)
small_space = Spacer(1, .2*inch)
smaller_space = Spacer(1, .15*inch)
smallest_space = Spacer(1, .12*inch)
indented = ParagraphStyle(**{"name": "indented", "fontSize": 10, "fontName": "Times-Roman", "leftIndent":36})
table_header = ParagraphStyle(**{"name": "table_header", "fontSize": 8, "fontName": "Helvetica"})
table_style = ParagraphStyle(**{"name": "table_style", "fontSize": 8, "fontName": "Helvetica"})

def dfToTable(df: pd.DataFrame = None, table_header: ParagraphStyle=table_header, cell_style: ParagraphStyle= None, ):
    
    
    style=[
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('LINEBELOW',(0,0), (-1,0), 1, HexColor("#8b451330", hasAlpha=True)),
        ('INNERGRID', (0,0), (-1,-1), 0.25, HexColor("#8b451330", hasAlpha=True)),
        ('BOX', (0,0), (-1,-1), .5, HexColor("#8b451320", hasAlpha=True)),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [HexColor("#8b451320", hasAlpha=True), colors.white])
    ]
    
    
    if isinstance(cell_style, ParagraphStyle):
        
        header = [[Paragraph(col, table_header) for col in df.columns]]
        new_rows = []
        for a_row in df.values.tolist():



            new_row = [Paragraph(str(x), cell_style) for x in a_row]
            new_rows.append(new_row)

        new_rows = header + new_rows
        
        return Table(new_rows, style=style, hAlign = 'LEFT')
    
    else:    
    
        a_table = [[Paragraph(col, table_header) for col in df.columns]] + df.values.tolist()
      
        return Table(a_table, style=style, hAlign = 'LEFT')



# pdf title and map
pdf_title = Paragraph(this_feature["name"], title_style)
map_image =  Image(bassin_map, width=inch*5.8, height=inch*4.8, kind="proportional", hAlign= "LEFT")

pdfcomponents = addToDoc([
    pdf_title,    
    small_space,
    map_image
], pdfcomponents)


# (bielersee_de)=
# # Bielersee
# 
# 
# {download}`Download </resources/pdfs/bielersee.pdf>`

# In[2]:


class Caption:
    
    position=''
    figure_number=0
    captions=[]
    start_caption = ""
    end_caption = '*'
    paragraphs = []
    
    def buildCaption(self):
        start_caption = f'*__{self.position}:__'
        new_string=''
        for line in self.captions:
            new_string += line
        end_caption = self.end_caption
        
        return f'{start_caption} {new_string}{end_caption}'
    
    def buildParagraph(self):
        new_string=''
        for line in self.paragraphs:
            new_string += line
        
        return new_string
        
            
map_caption = Caption()
map_caption.position = "Unten"
map_caption.captions = [
    "Karte des Erhebungsgebiets März 2020 bis Mai 2021. ",
    "Der Durchmesser der Punktsymbole entspricht dem Median der",
    "Abfallobjekte pro 100 Meter (p/100 m) am jeweiligen Erhebungsort."
]

# pdf output
map_caption.paragraphs = map_caption.captions
a_paragraph = map_caption.buildParagraph()

# add those sections
pdfcomponents = addToDoc([Paragraph(a_paragraph, caption_style)], pdfcomponents)


# ```{figure} resources/maps/bielersee_scaled.jpeg
# ---
# name: bielersee_map
# ---
# ` `
# ```
# {numref}`Abbildung %s: <bielersee_map>` Karte des Erhebungsgebiets März 2020 bis Mai 2021.  Der Durchmesser der Punktsymbole entspricht dem Median der Abfallobjekte pro 100 Meter (p/100 m) am jeweiligen Erhebungsort.

# ## Erhebungsorte

# In[3]:


# add section to pdf file
pdfcomponents = addToDoc([large_space, Paragraph("Erhebungsort", section_title)], alist=pdfcomponents)


obj_string = featuredata.thousandsSeparator(admin_summary["quantity"], language)
surv_string = "{:,}".format(admin_summary["loc_date"])
pop_string = featuredata.thousandsSeparator(int(admin_summary["population"]), language)

# make strings
date_quantity_context = F"Im Zeitraum von {featuredata.dateToYearAndMonth(datetime.strptime(start_date, date_format), lang=date_lang)}  bis {featuredata.dateToYearAndMonth(datetime.strptime(end_date, date_format), lang= date_lang)} wurden im Rahmen von {surv_string} Datenerhebungen insgesamt {obj_string } Objekte entfernt und identifiziert."
geo_context = F"Die Ergebnisse des {this_feature['name']} umfassen {admin_summary['location']} Orte, {admin_summary['city']} Gemeinden und eine Gesamtbevölkerung von etwa {pop_string} Einwohnenden."

# lists of landmarks of interest
munis_joined = ", ".join(sorted(admin_details.populationKeys()["city"]))

admin_summary_section = Caption()
admin_summary_section.paragraph = [date_quantity_context, geo_context]
admin_summary_lists = admin_details.populationKeys()["city"]


cities_bold_block = Paragraph("Gemeinden:", bold_block),
cities = Paragraph(munis_joined, indented)

# add the admin summary to the pdf
pdfcomponents = addToDoc([
    small_space,
    Paragraph(f'{date_quantity_context} {geo_context}', p_style),   
    
], pdfcomponents)



# put that all together:
lake_string = F"""
{date_quantity_context} {geo_context }

*Gemeinden:*\n\n>{munis_joined}
"""
md(lake_string)


# ### Kumulative Gesamtmengen nach Gemeinden

# In[28]:


# add section to pdf
pdfcomponents = addToDoc([large_space, Paragraph("Kumulative Gesamtmengen nach Gemeinden", subsection_title)], pdfcomponents)

# save image of table to this directory
save_fig_prefix = "resources/output/"

# the arguments for formatting the image
dims_table_figure_kwargs = {
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


# make table sort and rename the columns
dims_table = admin_details.dimensionalSummary()
dims_table.sort_values(by=["quantity"], ascending=False, inplace=True)
dims_table.rename(columns=featuredata.dims_table_columns_de, inplace=True)

# put the weights to Kg
dims_table["Plastik (Kg)"] = dims_table["Plastik (Kg)"]/1000

# these columns need formatting for locale
thousands_separated = ["Fläche (m2)", "Länge (m)", "Erhebungen", "Objekte (St.)"]
replace_decimal = ["Plastik (Kg)", "Gesamtgewicht (Kg)"]
dims_table[thousands_separated] = dims_table[thousands_separated].applymap(lambda x: featuredata.thousandsSeparator(int(x), "de"))
dims_table[replace_decimal] = dims_table[replace_decimal].applymap(lambda x: featuredata.replaceDecimal(str(round(x,2))))

# figure caption
dims_table_caption = f'{this_feature["name"]}: kumulierten Gewichte  und Masse für die Gemeinden'
dtcap = dims_table_caption
glue("dims_table_caption",dtcap, display=False)


data = dims_table.reset_index()

d_chart = dfToTable(df=data, table_header=table_header, cell_style=table_style)
d_capt = Paragraph(dims_table_caption, caption_style)
pdfcomponents = addToDoc([small_space, d_chart, d_capt, PageBreak()], pdfcomponents)

colLabels = data.columns

fig, ax = plt.subplots(figsize=(len(colLabels)*2,len(data)*.7))

sut.hide_spines_ticks_grids(ax)
table_one = sut.make_a_table(ax, data.values, colLabels=colLabels, colWidths=[.18, .17, *[.13]*5], a_color=a_color)
table_one.get_celld()[(0,0)].get_text().set_text(" ")
table_one.set_fontsize(12)

figure_name = "bielersee_dimensional_summary"
dims_table_file_name = f'{save_fig_prefix}{figure_name}.jpeg'
dims_table_figure_kwargs.update({"fname":dims_table_file_name})

plt.tight_layout()
plt.savefig(**dims_table_figure_kwargs)
glue(figure_name, fig, display=False)
plt.close()


# ```{glue:figure} bielersee_dimensional_summary
# ---
# name: 'bielersee_dimensional_summary'
# ---
# ` `
# ```
# {numref}`Abbildung %s: <bielersee_dimensional_summary>` {glue:text}`dims_table_caption`

# ### Verteilung der Erhebungsergebnisse

# In[5]:


sample_total_notes = f'Links: {this_feature["name"]}, {featuredata.dateToYearAndMonth(datetime.strptime(start_date, date_format), lang=date_lang)} bis {featuredata.dateToYearAndMonth(datetime.strptime(end_date, date_format), lang=date_lang)}, n = {admin_summary["loc_date"]}. Rechts: empirische Verteilungsfunktion der Erhebungsergebnisse {this_feature["name"]}.'


dx = period_data.parentSampleTotals(parent=False)

months = mdates.MonthLocator(interval=1)
months_fmt = mdates.DateFormatter("%b")
days = mdates.DayLocator(interval=7)

# get the monthly or quarterly results for the feature
rsmp = fdx.sample_totals.set_index("date")
resample_plot, rate = featuredata.quarterlyOrMonthlyValues(rsmp, this_feature["name"], vals=unit_label)


fig, axs = plt.subplots(1,2, figsize=(10,5))

# the survey totals by day
ax = axs[0]

# feature surveys
sns.scatterplot(data=dx, x="date", y=unit_label, label=top, color="black", alpha=0.4,  ax=ax)
# all other surveys
sns.scatterplot(data=fdx.sample_totals, x="date", y=unit_label, label=this_feature["name"], color="red", s=34, ec="white", ax=ax)
# monthly or quaterly plot
sns.lineplot(data=resample_plot, x=resample_plot.index, y=resample_plot, label=F"{this_feature['name']}: monatlicher Medianwert", color="magenta", ax=ax)

y_lim = 95
y_limit = np.percentile(dx[unit_label], y_lim)
ax.set_ylabel(unit_label, **ck.xlab_k14)

ax.set_xlabel("")
ax.xaxis.set_minor_locator(days)
ax.xaxis.set_major_formatter(months_fmt)
# ax.margins(x=.05, y=.05)
ax.set_ylim(-50, 2000)

ax.legend()

# the cumlative distributions:
axtwo = axs[1]

# the feature of interest
feature_ecd = featuredata.ecdfOfAColumn(fdx.sample_totals, unit_label)    
sns.lineplot(x=feature_ecd["x"], y=feature_ecd["y"], color="darkblue", ax=axtwo, label=this_feature["name"])

# the other features
other_features = featuredata.ecdfOfAColumn(dx, unit_label)
sns.lineplot(x=other_features["x"], y=other_features["y"], color="magenta", label=top, linewidth=1, ax=axtwo)

axtwo.set_xlabel(unit_label, **ck.xlab_k14)
axtwo.set_ylabel("Verhältnis der Erhebungen", **ck.xlab_k14)
axtwo.set_xlim(0, 3000)

axtwo.xaxis.set_major_locator(MultipleLocator(500))
axtwo.xaxis.set_minor_locator(MultipleLocator(100))
axtwo.yaxis.set_major_locator(MultipleLocator(.1))
axtwo.grid(which="minor", visible=True, axis="x", linestyle="--", linewidth=1)

figure_name = "bielersee_sample_totals"
sample_totals_file_name = f'{save_fig_prefix}{figure_name}.jpeg'
dims_table_figure_kwargs.update({"fname":sample_totals_file_name})

plt.tight_layout()
plt.savefig(**dims_table_figure_kwargs)
glue("bielersee_sample_totals", fig, display=False)
plt.close()


# ```{glue:figure} bielersee_sample_totals
# ---
# name: 'bielersee_sample_totals'
# ---
# ` `
# ```
# {numref}`Abbildung %s: <bielersee_sample_totals>` Links: Bielersee, März 2020 bis Mai 2021, n = 38. Rechts: empirische Verteilungsfunktion der Erhebungsergebnisse Bielersee.

# ### Zusammengefasste Daten und Materialarten

# In[6]:


# figure caption
summary_of_survey_totals = f"""
Zusammenfassung der Daten aller Erhebungen am {this_feature["name"]}. Gefundene Materialarten am {this_feature["name"]} in Stückzahlen und als prozentuale Anteile (stückzahlbezogen).
"""
# md(summary_of_survey_totals)


# In[7]:


# add to pdf
s_totals = Image(sample_totals_file_name, width=inch*6, height=inch*4.8, kind="proportional", hAlign= "LEFT")
s_totals_caption = Paragraph(sample_total_notes, caption_style)
pdfcomponents = addToDoc([Paragraph("Verteilung der Erhebungsergebnisse", subsection_title), small_space, s_totals, s_totals_caption], pdfcomponents)

csx = fdx.sample_summary.copy()

combined_summary =[(x, featuredata.thousandsSeparator(int(csx[x]), language)) for x in csx.index]

# the materials table
fd_mat_totals = fdx.material_summary.copy()
fd_mat_totals = featuredata.fmtPctOfTotal(fd_mat_totals, around=0)

# applly new column names for printing
cols_to_use = {"material":"Material","quantity":"Objekte (St.)", "% of total":"Anteil"}
fd_mat_t = fd_mat_totals[cols_to_use.keys()].values
fd_mat_t = [(x[0], featuredata.thousandsSeparator(int(x[1]), language), x[2]) for x in fd_mat_t]

# make tables
fig, axs = plt.subplots(1,2)

# summary table
# names for the table columns
a_col = [this_feature["name"], "Total"]

axone = axs[0]
sut.hide_spines_ticks_grids(axone)

table_two = sut.make_a_table(axone, combined_summary,  colLabels=a_col, colWidths=[.75,.25],  bbox=[0,0,1,1], **{"loc":"lower center"})
table_two.get_celld()[(0,0)].get_text().set_text(" ")
table_two.set_fontsize(12)

# material table
axtwo = axs[1]
axtwo.set_xlabel(" ")
sut.hide_spines_ticks_grids(axtwo)

table_three = sut.make_a_table(axtwo, fd_mat_t,  colLabels=list(cols_to_use.values()), colWidths=[.4, .4,.2],  bbox=[0,0,1,1], **{"loc":"lower center"})
table_three.get_celld()[(0,0)].get_text().set_text(" ")
table_three.set_fontsize(12)
plt.tight_layout()
plt.subplots_adjust(wspace=0.2)
plt.margins(0, 0)
figure_name = "bielersee_sample_summaries"
sample_summaries_file_name = f'{save_fig_prefix}{figure_name}.jpeg'
dims_table_figure_kwargs.update({"fname":sample_summaries_file_name})

plt.savefig(**dims_table_figure_kwargs)


glue('bielersee_sample_material_tables', fig, display=False)
plt.close()


# ```{glue:figure} bielersee_sample_material_tables
# ---
# name: 'bielersee_sample_material_tables'
# ---
# ` `
# ```

# {numref}`Abbildung %s: <bielersee_sample_material_tables>`Links: Zusammenfassung der Daten aller Erhebungen am Bielersee. Rechts: Gefundene Materialarten am Bielersee in Stückzahlen und als prozentuale Anteile (stückzahlbezogen).

# ## Die am häufigsten gefundenen Objekte
# 
# Die am häufigsten gefundenen Objekte sind die zehn mengenmässig am meisten vorkommenden Objekte und/oder Objekte, die in mindestens 50 % aller Datenerhebungen identifiziert wurden (Häufigkeitsrate)

# In[8]:


# add summary tables to pdf
samp_mat_subsection = Paragraph("Zusammengefasste Daten und Materialarten", subsection_title)
samp_material_table = Image(sample_summaries_file_name , width=inch*6, height=inch*4.8, kind="proportional", hAlign= "LEFT")
samp_material_caption = Paragraph(summary_of_survey_totals, caption_style)
pdfcomponents = addToDoc([large_space, samp_mat_subsection, small_space, samp_material_table, samp_material_caption, PageBreak()], pdfcomponents)



# get percent of total
m_common_percent_of_total = fdx.most_common["quantity"].sum()/fdx.code_summary["quantity"].sum()
rb_string = f"""
Häufigste Objekte im {this_feature['name']}: d. h. Objekte mit einer Häufigkeitsrate von mindestens 50 % und/oder Top Ten nach Anzahl. Zusammengenommen machen die häufigsten Objekte {int(m_common_percent_of_total*100)}% aller gefundenen Objekte aus. Anmerkung: p/100 m = Medianwert der Erhebung.
"""


# In[9]:


# format values for table
m_common = fdx.most_common.copy()
m_common["item"] = m_common.index.map(lambda x: fdx.dMap.loc[x])
m_common["% of total"] = m_common["% of total"].map(lambda x: F"{int(x)}%")
m_common["quantity"] = m_common.quantity.map(lambda x:featuredata.thousandsSeparator(x, language))
m_common["fail rate"] = m_common["fail rate"].map(lambda x: F"{x}%")
m_common[unit_label] = m_common[unit_label].map(lambda x: featuredata.replaceDecimal(round(x,1)))

# format the table headers
cols_to_use = featuredata.most_common_objects_table_de
cols_to_use.update({unit_label:unit_label})
all_survey_areas = m_common[cols_to_use.keys()].values

pdf_mc_table = dfToTable(df=m_common[cols_to_use.keys()].copy(), table_header=table_header, cell_style=table_style)

fig, axs = plt.subplots(figsize=(10,len(m_common)*.7))

sut.hide_spines_ticks_grids(axs)

table_four = sut.make_a_table(axs, all_survey_areas,  colLabels=list(cols_to_use.values()), colWidths=[.49, .13,.11,.15, .12],  bbox=[0,0,1,1], **{"loc":"lower center"})
table_four.get_celld()[(0,0)].get_text().set_text(" ")
table_four.set_fontsize(12)
plt.tight_layout()

figure_name = "bielersee_most_common_table"
bielersee_most_common_table_file_name = f'{save_fig_prefix}{figure_name}.jpeg'
dims_table_figure_kwargs.update({"fname":bielersee_most_common_table_file_name})

plt.savefig(**dims_table_figure_kwargs)
glue('bielersee_most_common_tables', fig, display=False)
plt.close()


# In[10]:


m_common[cols_to_use.keys()]


# ```{glue:figure} bielersee_most_common_tables
# ---
# name: 'bielersee_most_common_tables'
# ---
# ` `
# ```

# {numref}`Abbildung %s: <bielersee_most_common_tables>` Häufigste Objekte im Bielersee: d. h. Objekte mit einer Häufigkeitsrate von mindestens 50 % und/oder Top Ten nach Anzahl. Zusammengenommen machen die häufigsten Objekte 73% aller gefundenen Objekte aus. Anmerkung: p/100 m = Medianwert der Erhebung.

# ### Die am häufigsten gefundenen Objekte nach Gemeinden

# In[11]:


# add new section pdf
mc_section_title = Paragraph("Die am häufigsten gefundenen Objekte", section_title)
para_g = "Die am häufigsten gefundenen Objekte sind die zehn mengenmässig am meisten vorkommenden Objekte und/oder Objekte, die in mindestens 50 % aller Datenerhebungen identifiziert wurden (Häufigkeitsrate)"
mc_section_para = Paragraph(para_g, p_style)
# mc_table = Image(bielersee_most_common_table_file_name, width=inch*6, height=inch*8, kind="proportional", hAlign= "LEFT")
mc_table_cap = Paragraph(rb_string, caption_style)
mc_heatmap_title = Paragraph("Die am häufigsten gefundenen Objekte nach Gemeinden", subsection_title)


new_components = [
    mc_section_title,
    small_space,
    mc_section_para,
    large_space,
    pdf_mc_table,
    mc_table_cap,
    PageBreak(),
    mc_heatmap_title,
    large_space
]
pdfcomponents = addToDoc(new_components, pdfcomponents)

rb_string = F"""
Median (p/100 m) der häufigsten Objekte am {this_feature["name"]}.
"""
# md(rb_string)


# In[12]:


# calling componentsMostCommon gets the results for the most common codes
# at the component level
components = fdx.componentMostCommonPcsM()

# pivot that and quash the hierarchal column index that is created when the table is pivoted
mc_comp = components[["item", unit_label, "city"]].pivot(columns="city", index="item")
mc_comp.columns = mc_comp.columns.get_level_values(1)

# the aggregated total of the feature is taken from the most common objects table
mc_feature = fdx.most_common[unit_label]
mc_feature = featuredata.changeSeriesIndexLabels(mc_feature, {x:fdx.dMap.loc[x] for x in mc_feature.index})

# aggregated totals of the parent this is derived from the arguments in kwargs
mc_parent = period_data.parentMostCommon(parent=True)
mc_parent = featuredata.changeSeriesIndexLabels(mc_parent, {x:fdx.dMap.loc[x] for x in mc_parent.index})

# the aggregated totals of all the period data
mc_period = period_data.parentMostCommon(parent=False)
mc_period = featuredata.changeSeriesIndexLabels(mc_period, {x:fdx.dMap.loc[x] for x in mc_period.index})

# add the feature, bassin_label and period results to the components table
mc_comp[this_feature["name"]]= mc_feature
mc_comp[bassin_label] = mc_parent
mc_comp[top] = mc_period

# chart that
fig, ax  = plt.subplots(figsize=(len(mc_comp.columns)*.7,len(mc_comp)*.8))
axone = ax

sns.heatmap(mc_comp, ax=axone, cmap=cmap2, annot=True, annot_kws={"fontsize":12}, fmt=".0f", square=True, cbar=False, linewidth=.1, linecolor="white")
axone.set_xlabel("")
axone.set_ylabel("")
axone.tick_params(labelsize=12, which="both", axis="y")

plt.setp(axone.get_xticklabels(), rotation=90)
plt.tight_layout()
plt.margins(0,0)

figure_name = "bielersee_most_common_heat_map"
bielersee_most_common_heat_map_name = f'{save_fig_prefix}{figure_name}.jpeg'
dims_table_figure_kwargs.update({"fname":bielersee_most_common_heat_map_name})

plt.savefig(**dims_table_figure_kwargs)

glue('bielersee_most_common_heat_map', fig, display=False)
plt.close()


# ```{glue:figure} bielersee_most_common_heat_map
# ---
# name: 'bielersee_most_common_heat_map'
# ---
# ` `
# ```

# {numref}`Abbildung %s: <bielersee_most_common_heat_map>` Median (p/100 m) der häufigsten Objekte am Bielersee.

# ### Die am häufigsten gefundenen Objekte im monatlichen Durchschnitt

# In[13]:


# add to pdf
mc_heat_map = Image(bielersee_most_common_heat_map_name, width=inch*6, height=inch*8, kind="proportional", hAlign= "LEFT")
mc_heat_map_caption = Paragraph(rb_string, caption_style)
mc_monthly_title = Paragraph("Die am häufigsten gefundenen Objekte im monatlichen Durchschnitt", subsection_title)
pdfcomponents = addToDoc([small_space,mc_heat_map, smallest_space, mc_heat_map_caption, PageBreak(), mc_monthly_title, small_space], pdfcomponents)

# collect the survey results of the most common objects
agg_pcs_quantity = {unit_label:"sum", "quantity":"sum"}
agg_pcs_median = {unit_label:"median", "quantity":"sum"}

m_common_m = fd[(fd.code.isin(m_common.index))].groupby(["loc_date","date","code", "groupname"], as_index=False).agg(agg_pcs_quantity)
m_common_m.set_index("date", inplace=True)

# set the order of the chart, group the codes by groupname columns
an_order = m_common_m.groupby(["code","groupname"], as_index=False).quantity.sum().sort_values(by="groupname")["code"].values

# a manager dict for the monthly results of each code
mgr = {}

# get the monhtly results for each code:
for a_group in an_order:
    # resample by month
    a_plot = m_common_m[(m_common_m.code==a_group)][unit_label].resample("M").mean().fillna(0)
    this_group = {a_group:a_plot}
    mgr.update(this_group)

# monthly_mc = F"""
# *__Below:__ {this_feature["name"]}, monatliche Durchschnittsergebnisse p/100 m.*
# """
# md(monthly_mc)

months={
    0:"Jan",
    1:"Feb",
    2:"Mar",
    3:"Apr",
    4:"May",
    5:"Jun",
    6:"Jul",
    7:"Aug",
    8:"Sep",
    9:"Oct",
    10:"Nov",
    11:"Dec"
}

# convenience function to label x axis
def new_month(x):
    if x <= 11:
        this_month = x
    else:
        this_month=x-12    
    return this_month

fig, ax = plt.subplots(figsize=(10,9))

# define a bottom
bottom = [0]*len(mgr["G27"])

# the monhtly survey average for all objects and locations
monthly_fd = fd.groupby(["loc_date", "date"], as_index=False).agg(agg_pcs_quantity)
monthly_fd.set_index("date", inplace=True)
m_fd = monthly_fd[unit_label].resample("M").mean().fillna(0)

# define the xaxis
this_x = [i for i,x in  enumerate(m_fd.index)]

# plot the monthly total survey average
ax.bar(this_x, m_fd.to_numpy(), color=table_row, alpha=0.2, linewidth=1, edgecolor="teal", width=1, label="Monthly survey average") 

# plot the monthly survey average of the most common objects
for i, a_group in enumerate(an_order): 
    
    # define the axis
    this_x = [i for i,x in  enumerate(mgr[a_group].index)]
    
    # collect the month
    this_month = [x.month for i,x in enumerate(mgr[a_group].index)]
    
    # if i == 0 laydown the first bars
    if i == 0:
        ax.bar(this_x, mgr[a_group].to_numpy(), label=a_group, color=colors_palette[a_group], linewidth=1, alpha=0.6 ) 
    # else use the previous results to define the bottom
    else:
        bottom += mgr[an_order[i-1]].to_numpy()        
        ax.bar(this_x, mgr[a_group].to_numpy(), bottom=bottom, label=a_group, color=colors_palette[a_group], linewidth=1, alpha=0.8)
        
# collect the handles and labels from the legend
handles, labels = ax.get_legend_handles_labels()

# set the location of the x ticks
ax.xaxis.set_major_locator(ticker.FixedLocator([i for i in np.arange(len(this_x))]))
ax.set_ylabel(unit_label, **ck.xlab_k14)

# label the xticks by month
axisticks = ax.get_xticks()
labelsx = [sut.months_de[new_month(x-1)] for x in  this_month]
plt.xticks(ticks=axisticks, labels=labelsx)

# make the legend
# swap out codes for descriptions
new_labels = [fdx.dMap.loc[x] for x in labels[1:]]
new_labels = new_labels[::-1]

# insert a label for the monthly average
new_labels.insert(0,"Monatsdurschnitt")
handles = [handles[0], *handles[1:][::-1]]
    

plt.tight_layout()
plt.legend(handles=handles, labels=new_labels, bbox_to_anchor=(.5, -.05), loc="upper center",  ncol=2, fontsize=12)

figure_name = "bielersee_most_common_monthly"
bielersee_most_common_monthly_name = f'{save_fig_prefix}{figure_name}.jpeg'
dims_table_figure_kwargs.update({"fname":bielersee_most_common_monthly_name })

plt.savefig(**dims_table_figure_kwargs)

glue("bielersee_monthly_results", fig, display=False)
plt.close()


# ```{glue:figure} bielersee_monthly_results
# ---
# name: 'bielersee_monthly_results'
# ---
# ` `
# ```

# {numref}`Abbildung %s: <bielersee_monthly_results>` Bielersee, monatliche Durchschnittsergebnisse p/100 m.

# ## Verwendungszweck der gefundenen Objekte
# 
# Der Verwendungszweck basiert auf der Verwendung des Objekts, bevor es weggeworfen wurde, oder auf der Artikelbeschreibung, wenn die ursprüngliche Verwendung unbestimmt ist. Identifizierte Objekte werden einer der 260 vordefinierten Kategorien zugeordnet. Die Kategorien werden je nach Verwendung oder Artikelbeschreibung gruppiert.
# 
# * Abwasser: Objekte, die aus Kläranlagen freigesetzt werden, sprich Objekte, die wahrscheinlich über die Toilette entsorgt werden
# * Mikroplastik (< 5 mm): fragmentierte Kunststoffe und Kunststoffharze aus der Vorproduktion
# * Infrastruktur: Artikel im Zusammenhang mit dem Bau und der Instandhaltung von Gebäuden, Strassen und der Wasser-/Stromversorgung
# * Essen und Trinken: alle Materialien, die mit dem Konsum von Essen und Trinken in Zusammenhang stehen
# * Landwirtschaft: Materialien z. B. für Mulch und Reihenabdeckungen, Gewächshäuser, Bodenbegasung, Ballenverpackungen. Einschliesslich Hartkunststoffe für landwirtschaftliche Zäune, Blumentöpfe usw.
# * Tabakwaren: hauptsächlich Zigarettenfilter, einschliesslich aller mit dem Rauchen verbundenen Materialien
# * Freizeit und Erholung: Objekte, die mit Sport und Freizeit zu tun haben, z. B. Angeln, Jagen, Wandern usw.
# * Verpackungen ausser Lebensmittel und Tabak: Verpackungsmaterial, das nicht lebensmittel- oder tabakbezogen ist
# * Plastikfragmente: Plastikteile unbestimmter Herkunft oder Verwendung
# * Persönliche Gegenstände: Accessoires, Hygieneartikel und Kleidung
# 
# Im Anhang (Kapitel 3.6.3) befindet sich die vollständige Liste der identifizierten Objekte, einschliesslich Beschreibungen und Gruppenklassifizierung. Das Kapitel [16 Codegruppen](codegroups) beschreibt jede Codegruppe im Detail und bietet eine umfassende Liste aller Objekte in einer Gruppe.

# In[14]:


monthly_results = Image(bielersee_most_common_monthly_name, width=inch*6, height=inch*8, kind="proportional", hAlign= "LEFT")
cone_group_subtitle = Paragraph("Verwendungszweck der gefundenen Objekte", section_title)

paragraph_one = [
    "Der Verwendungszweck basiert auf der Verwendung des Objekts, bevor es weggeworfen wurde, ",
    "oder auf der Artikelbeschreibung, wenn die ursprüngliche Verwendung unbestimmt ist. ",
    "Identifizierte Objekte werden einer der 260 vordefinierten Kategorien zugeordnet. ",
    "Die Kategorien werden je nach Verwendung oder Artikelbeschreibung gruppiert."
]

group_names_list = [
    "Abwasser: Objekte, die aus Kläranlagen freigesetzt werden, sprich Objekte, die wahrscheinlich über die Toilette entsorgt werden",
    "Mikroplastik (< 5 mm): fragmentierte Kunststoffe und Kunststoffharze aus der Vorproduktion",
    "Infrastruktur: Artikel im Zusammenhang mit dem Bau und der Instandhaltung von Gebäuden, Strassen und der Wasser-/Stromversorgung",
    "Essen und Trinken: alle Materialien, die mit dem Konsum von Essen und Trinken in Zusammenhang stehen",
    "Landwirtschaft: Materialien z. B. für Mulch und Reihenabdeckungen, Gewächshäuser, Bodenbegasung, Ballenverpackungen. Einschliesslich Hartkunststoffe für landwirtschaftliche Zäune, Blumentöpfe usw.",
    "Tabakwaren: hauptsächlich Zigarettenfilter, einschliesslich aller mit dem Rauchen verbundenen Materialien",
    "Freizeit und Erholung: Objekte, die mit Sport und Freizeit zu tun haben, z. B. Angeln, Jagen, Wandern usw.",
    "Verpackungen ausser Lebensmittel und Tabak: Verpackungsmaterial, das nicht lebensmittel- oder tabakbezogen ist",
    "Plastikfragmente: Plastikteile unbestimmter Herkunft oder Verwendung",
    "Persönliche Gegenstände: Accessoires, Hygieneartikel und Kleidung"
]

paragraph_three = [
    "Im Anhang (Kapitel 3.6.3) befindet sich die vollständige Liste der identifizierten Objekte, ",
    "einschliesslich Beschreibungen und Gruppenklassifizierung. ",
    "Das Kapitel [16 Codegruppen](codegroups) beschreibt jede Codegruppe im Detail und bietet eine ",
    "umfassende Liste aller Objekte in einer Gruppe."
]


code_group_para_one = ' '.join(paragraph_one)

name_list = [ListItem(Paragraph(x, p_style), bulletColor=HexColor("#000000")) for x in group_names_list]

cgroup_pone = Paragraph(code_group_para_one, p_style)
code_group_para_three = ''.join(paragraph_three)
cgroup_pthree = Paragraph(code_group_para_three, p_style)
a_list_groups = ListFlowable(name_list, bulletType='bullet', start="square", bulletFontSize=6)


pdfcomponents = addToDoc([monthly_results, PageBreak(), cone_group_subtitle, small_space, cgroup_pone, small_space, a_list_groups, small_space, cgroup_pthree], pdfcomponents)

cg_poft = F"""
Verwendungszweck oder Beschreibung der identifizierten Objekte in % der Gesamtzahl nach Gemeinden im Erhebungsgebiet {this_feature["name"]}. Fragmentierte Objekte, die nicht eindeutig identifiziert werden können, werden weiterhin nach ihrer Grösse klassifiziert.
"""
# md(cg_poft)


# In[15]:


components = fdx.componentCodeGroupResults()

# pivot that
pt_comp = components[["city", "groupname", '% of total' ]].pivot(columns="city", index="groupname")

# quash the hierarchal column index
pt_comp.columns = pt_comp.columns.get_level_values(1)

# the aggregated codegroup results from the feature
pt_feature = fdx.codegroup_summary["% of total"]
pt_comp[this_feature["name"]] = pt_feature

# the aggregated totals for the parent level
pt_parent = period_data.parentGroupTotals(parent=True, percent=True)
pt_comp[bassin_label] = pt_parent

# the aggregated totals for the period
pt_period = period_data.parentGroupTotals(parent=False, percent=True)
pt_comp[top] = pt_period


fig, ax = plt.subplots(figsize=(len(pt_comp.columns)*.9,len(pt_comp)*.8))

axone = ax

sns.heatmap(pt_comp , ax=axone, cmap=cmap2, annot=True,  annot_kws={"fontsize":12}, fmt=".0%", cbar=False, linewidth=.1, linecolor="white")

axone.set_ylabel("")
axone.set_xlabel("")
axone.tick_params(labelsize=12, which="both", axis="both", labeltop=False, labelbottom=True)

plt.setp(axone.get_xticklabels(), rotation=90, fontsize=14)
plt.setp(axone.get_yticklabels(), rotation=0, fontsize=14)

plt.tight_layout()
plt.margins(0,0)
figure_name = "bielersee_code_group_percent"
bielersee_code_group_percent = f'{save_fig_prefix}{figure_name}.jpeg'
dims_table_figure_kwargs.update({"fname": bielersee_code_group_percent})

plt.savefig(**dims_table_figure_kwargs)
glue('bielersee_codegroup_percent', fig, display=False)
plt.close()


# ```{glue:figure} bielersee_codegroup_percent
# ---
# name: 'bielersee_codegroup_percent'
# ---
# ` `
# ```
# {numref}`Abbildung %s: <bielersee_codegroup_percent>` Verwendungszweck oder Beschreibung der identifizierten Objekte in % der Gesamtzahl nach Gemeinden im Erhebungsgebiet Bielersee. Fragmentierte Objekte, die nicht eindeutig identifiziert werden können, werden weiterhin nach ihrer Grösse klassifiziert.

# In[16]:


cg_percent = Image(bielersee_code_group_percent, width=inch*6, height=inch*8, kind="proportional", hAlign= "LEFT")
cg_caption = Paragraph(cg_poft, caption_style)

cg_medpcm = F"""
Verwendungszweck der gefundenen Objekte Median p/100 m am {this_feature["name"]}. Fragmentierte Objekte, die nicht eindeutig identifiziert werden können, werden weiterhin nach ihrer Grösse klassifiziert.
"""
md(cg_medpcm)

# pivot that
grouppcs_comp = components[["city", "groupname", unit_label ]].pivot(columns="city", index="groupname")

# quash the hierarchal column index
grouppcs_comp.columns = grouppcs_comp.columns.get_level_values(1)

# the aggregated codegroup results from the feature
pt_feature = fdx.codegroup_summary[unit_label]
grouppcs_comp[this_feature["name"]] = pt_feature

# the aggregated totals for the parent level
pt_parent = period_data.parentGroupTotals(parent=True, percent=False)
grouppcs_comp[bassin_label] = pt_parent

# the aggregated totals for the period
pt_period = period_data.parentGroupTotals(parent=False, percent=False)
grouppcs_comp[top] = pt_period

fig, ax = plt.subplots(figsize=(len(pt_comp.columns)*.7,len(pt_comp)*.8))

axone = ax
sns.heatmap(grouppcs_comp , ax=axone, cmap=cmap2, annot=True, annot_kws={"fontsize":12}, fmt=".0f", cbar=False, linewidth=.1, square=True, linecolor="white")

axone.set_xlabel("")
axone.set_ylabel("")
axone.tick_params(labelsize=12, which="both", axis="both", labeltop=False, labelbottom=True)
plt.tight_layout()

plt.margins(0,0)
figure_name = "bielersee_code_group_pcsm"
bielersee_code_group_pcsm = f'{save_fig_prefix}{figure_name}.jpeg'
dims_table_figure_kwargs.update({"fname": bielersee_code_group_pcsm})

plt.savefig(**dims_table_figure_kwargs)
glue("bielersee_codegroup_pcsm", fig, display=False)
plt.close()


# ```{glue:figure} bielersee_codegroup_pcsm
# ---
# name: 'bielersee_codegroup_pcsm'
# ---
# ` `
# ```
# {numref}`Abbildung %s: <bielersee_codegroup_pcsm>` Verwendungszweck der gefundenen Objekte Median p/100 m am Bielersee. Fragmentierte Objekte, die nicht eindeutig identifiziert werden können, werden weiterhin nach ihrer Grösse klassifiziert.

# ## Anhang
# 
# ### Schaumstoffe und Kunststoffe nach Grösse
# 
# Die folgende Tabelle enthält die Komponenten «Gfoam» und «Gfrag», die für die Analyse gruppiert wurden. Objekte, die als Schaumstoffe gekennzeichnet sind, werden als Gfoam gruppiert und umfassen alle geschäumten Polystyrol-Kunststoffe > 0,5 cm. Kunststoffteile und Objekte aus kombinierten Kunststoff- und Schaumstoffmaterialien > 0,5 cm werden für die Analyse als Gfrags gruppiert.

# In[17]:


cg_pcsm = Image(bielersee_code_group_pcsm, width=inch*6, height=inch*8, kind="proportional", hAlign= "LEFT")
cgpcs_caption = Paragraph(cg_medpcm, caption_style)
annex_title = Paragraph("Anhang", section_title)
frag_sub_title = Paragraph("Schaumstoffe und Kunststoffe nach Grösse", subsection_title)

frag_paras = [
    "Die folgende Tabelle enthält die Komponenten «Gfoam» und «Gfrag», die für die Analyse gruppiert wurden. ",
    "Objekte, die als Schaumstoffe gekennzeichnet sind, werden als Gfoam gruppiert und umfassen alle geschäumten ",
    "Polystyrol-Kunststoffe > 0,5 cm. Kunststoffteile und Objekte aus kombinierten Kunststoff - und Schaumstoffmaterialien > 0,5 ",
    "cm werden für die Analyse als Gfrags gruppiert."
]

frag_p = "".join(frag_paras)
frag = Paragraph(frag_p, p_style)

new_components = [
    larger_space,
    cg_percent,
    smallest_space,
    cg_caption,
    larger_space,
    cg_pcsm,
    smallest_space,
    cgpcs_caption,
    PageBreak(),
    annex_title,
    small_space,
    frag_sub_title,
    smaller_space,
    frag,
    small_space
]

pdfcomponents = addToDoc(new_components, pdfcomponents)

frag_foams = f"""
Fragmentierte und geschäumte Kunststoffe nach Grösse am {this_feature["name"]},  Median p/100 m, Anzahl der gefundenen Objekte und Prozent der Gesamtmenge.
"""

# collect the data before aggregating foams for all locations in the survye area
# group by loc_date and code
# Combine the different sizes of fragmented plastics and styrofoam
# the codes for the foams
before_agg = pd.read_csv("resources/checked_before_agg_sdata_eos_2020_21.csv")
some_foams = ["G81", "G82", "G83", "G74"]
before_agg.rename(columns={"p/100m":unit_label}, inplace=True)

# the codes for the fragmented plastics
some_frag_plas = list(before_agg[before_agg.groupname == "plastic pieces"].code.unique())
mask = ((before_agg.code.isin([*some_frag_plas, *some_foams]))&(before_agg.location.isin(admin_summary["locations_of_interest"])))

fd_frags_foams = before_agg[mask].groupby(["loc_date","code"], as_index=False).agg(agg_pcs_quantity)
fd_frags_foams = fd_frags_foams.groupby("code").agg(agg_pcs_median)
fd_frags_foams["item"] = fd_frags_foams.index.map(lambda x: fdx.dMap.loc[x])
fd_frags_foams["% of total"] = (fd_frags_foams.quantity/fd.quantity.sum()*100).round(2)
fd_frags_foams["% of total"] = fd_frags_foams["% of total"].map(lambda x: f"{int(x)}%")
fd_frags_foams["quantity"] = fd_frags_foams["quantity"].map(lambda x: featuredata.thousandsSeparator(x, language))
fd_frags_foams[unit_label] = fd_frags_foams[unit_label].astype(int)
# table data
data = fd_frags_foams[["item",unit_label, "quantity", "% of total"]]
data.rename(columns={"quantity":"Objekte (St.)", "% of total":"Anteil"}, inplace=True)

fig, axs = plt.subplots(figsize=(len(data.columns)*2.1,len(data)*.7))

sut.hide_spines_ticks_grids(axs)

table_seven = sut.make_a_table(axs,data.values,  colLabels=data.columns, colWidths=[.6, .12, .15, .12], a_color=table_row)
table_seven.get_celld()[(0,0)].get_text().set_text(" ")
table_seven.set_fontsize(12)

plt.tight_layout()

figure_name = "bielersee_frags"
bielersee_frags = f'{save_fig_prefix}{figure_name}.jpeg'
dims_table_figure_kwargs.update({"fname": bielersee_frags})

plt.savefig(**dims_table_figure_kwargs)
glue('bielersee_fragmented_plastics', fig, display=False)
plt.close()


# ```{glue:figure} bielersee_fragmented_plastics
# ---
# name: 'bielersee_fragmented_plastics'
# ---
# ` `
# ```
# {numref}`Abbildung %s: <bielersee_fragmented_plastics>`  Fragmentierte und geschäumte Kunststoffe nach Grösse am Bielersee, Median p/100 m, Anzahl der gefundenen Objekte und Prozent der Gesamtmenge.

# ### Die Erhebungsorte

# In[18]:


frag_table = Image(bielersee_frags, width=inch*6, height=inch*8, kind="proportional", hAlign= "LEFT")
frag_caption = Paragraph(frag_foams, p_style)

pdfcomponents = addToDoc([frag_table, smallest_space, frag_caption], pdfcomponents)

# display the survey locations
disp_columns = ["latitude", "longitude", "city"]
disp_beaches = admin_details.df_beaches.loc[admin_summary["locations_of_interest"]][disp_columns]
disp_beaches.reset_index(inplace=True)
disp_beaches.rename(columns={"city":"stat", "slug":"standort"}, inplace=True)

# make this into a pdf table
location_subsection = Paragraph("Die Erhebungsorte", subsection_title)

pdf_table = dfToTable(df=disp_beaches, table_header=table_header)

pdfcomponents = addToDoc([small_space, location_subsection, small_space, pdf_table, PageBreak()], pdfcomponents)

disp_beaches.set_index("standort", inplace=True, drop=True)

disp_beaches


# ### Inventar der Objekte

# In[19]:


pd.set_option("display.max_rows", None)
complete_inventory = fdx.code_summary.copy()
complete_inventory["quantity"] = complete_inventory["quantity"].map(lambda x: featuredata.thousandsSeparator(x, language))
complete_inventory["% of total"] = complete_inventory["% of total"].astype(int)
complete_inventory[unit_label] = complete_inventory[unit_label].astype(int)
complete_inventory.rename(columns=featuredata.inventory_table_de, inplace=True)

complete_inventory.reset_index(inplace=True)

inventory_subsection = Paragraph("Inventar der Objekte", subsection_title)
inventory_table = dfToTable(df=complete_inventory, table_header=table_header, cell_style=table_style)

pdfcomponents = addToDoc([small_space, inventory_subsection, small_space, inventory_table], pdfcomponents)

complete_inventory.set_index("code", inplace=True, drop=True)

complete_inventory.sort_values(by="Objekte (St.)", ascending=False)


# In[20]:


# pdfcomponents = addToDoc([large_space, pdf_table], pdfcomponents)

doc = SimpleDocTemplate("bielersee.pdf", pagesize=A4, leftMargin=.5*inch, rightMargin=.5*inch, topMargin=.5*inch, bottomMargin=.5*inch)
pageinfo= f"IQAASL: {this_feature['name']} {start_date} bis {end_date}"

def myLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Italic',9)
    canvas.drawString(.5*inch, 0.25* inch, "S.%d %s" % (doc.page, pageinfo))
    canvas.restoreState()
    
doc.build(pdfcomponents,  onFirstPage=myLaterPages, onLaterPages=myLaterPages)


# In[ ]:




