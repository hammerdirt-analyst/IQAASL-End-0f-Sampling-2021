# The Litter Surveyor Report

The _Litter Surveyor_ is a summary and analyis of the litter surveys conducted in Switzerland since 2017 and how those results relate to the experiences of our European neighbors.

## In this issue

1. Comparing the results from the 2017 - 2018 Swiss Litter Report
2. Implementing the EU recomendations for baseline calculations of beach litter survey results
3. Implementing the principle of causality: what role for beach litter survey results
4. A first look at litter surveys in les Alpes Valaisannes
5. Summary and baseline calculations for all survey areas and lakes surveyed in 2020-2021


:::{note}
This is version 0.5 _The review draft: causality_

__Content revisions__  are on ongoing if you were going to contribute now is the time. We will be asking for participant information and photos soon -- like the end of the week!

__To do__:

1. Finalize cartography
2. Finish executive summary
3. Finish image selection
4. Code revision

contact roger@hammerdirt.ch
:::

## Summary of all surveys

The sampling period (SP) was from April 01, 2020 - May 31, 2021. This date range overlaps with the start and end date of the Swiss Litter Report (SLR) {cite}`slr` the
last national level project to use the standard protocol described in the _Guide to monitoring beach litter_ or any other comparable method. 
<br></br>

_Map of survey locations. Locations grouped by survey area. April 2020 - May 2021_
:::{image} resources/maps/opening_map.jpeg
:alt: Map of IQAASL locations
:class: bg-primary mb-1
:width: 800px
:align: center
:::
_There were 385 samples from 143 locations in 77 different municipalities._

The median survey result was 158 pieces per 100 meters (p/100m), with a 95% confidence interval (CI) of 137p/100m - 188/p100m. This represents 54,713 recorded objects or
$\approx$ 306kg of trash including $\approx$ 96kg of plastic. The total linear distance surveyed was $\approx$ 20 km or a surface area of 9 hectares. The study was focussed on lakes, 331/385 samples come from 11 lakes. Both Geneva
and Zurich are included putting the total municipal population with a stake in this report at 1.7 million.

See the section [_All Survey areas_](allsurveys) for complete details.

 ---

## Trends from 2017

**When the lake and rivers with samples in both projects are considered** there was no statistical difference between the SLR results and IQAASL. The survey results
show that in 2020 there were fewer cigarettes, bottle tops and glass fragments and more cotton swabs, industrial sheeting and plastic construction waste.

**Comparison of survey results between SLR (2018) and IQAASL (2021)**

*Top Left: survey totals by date, Top right: median monthly survey total* 
:::{image} resources/images/slr_iqaasl_res.png
:alt: IQAASL and SLR charts
:class: bg-primary mb-1
:width: 1200px
:align: center
:::
*bottom Left: number of samples with respect to the survey total, bottom right: empirical cumulative distribution of survey totals* 
<br></br>

See the full report [_More and less trash since 2017_](slr-iqaasl)

 ---

## Principal of causality

According to the Law for the protection of the environment the pincipal of causality is defined as:

> The person who initiates a measure prescribed by this Act shall bear the costs thereof.

We use beach litter survey results to move up the causal chain to identify secondary sources of litter.

:::{image} resources/images/causality.jpeg
:alt: causality map
:class: bg-primary mb-1
:width: 1200px
:align: center
:::
*Identifying secondary sources of specific litter items. Consumers or handlers of plastic production pellets and probable fluvial route to survey location. Venoge and Thiele rivers.*

See the section [_Principle of causality_](transport)

 ---

## Baseline and extreme values

The proposed methods in the JRC Technical document _An Analysis of a pan-European 2012-2016 beach litter dataset_ are applied to the results from IQAASL. The baseline values are calculated for each survey area and examples are given of the the different methods to identify extreme values.

*Is this alot of trash to find at the beach?* 

:::{image} resources/codegroups/images/onethous40026pcs100m.jpg
:alt: IQAASL and SLR charts
:class: bg-primary mb-1
:width: 800px
:align: center
:::
<br></br>

See the section [_Calculating baseline values_](threshhold) for sample calculations and a detailed explanation.

 ---
 
## Sources

Economically the sources are determined by grouping the codes assigned to the objects according to use or description. Combined food and tobacco items make up 36% of the items found and infrastructure and agriculture are 24% of the total. Objects originating from waste water facilities or objects less than five millimeters make up another 10%. The relative amounts change for each survey area suggesting that local priorities may not always match regional priorities.

See the section [_Code groups_](codegroups) for a complete definition of how the codes were grouped.

 ---

## The structure and evolution of this document

The purpose is to provide a repeatable method and process to collect and evaluate beach-litter data at a scale that is appropriate to Switzerland and exploitable by
all stakeholders. The method and process need to reflect current advances in the field, the needs of stakeholders and faithfully report the survey results as collected
by the surveyor.

This document is a collection of scripts written in python and markdown contained in a series of notebooks designed specifically for completing data analysis. This
system has been in use for quite some time in the research community. Together those scripts make a book, or a [Jupyter Book](https://jupyterbook.org/intro.html).

The surveyor uses this application [plagespropres](https://www.plagespropres.ch/) to submit data and the report is processed here: [end of sampling repo](https://github.com/hammerdirt-analyst/IQAASL-End-0f-Sampling-2021).

Not all tasks have been automated. Land use data is calculated using QGIS and the method to automate this process has not been developed.

 ---
 

## Identification, quantification and analysis of observable anthropogenic debris along swiss river and lakes (IQAASL)

IQAASL is a project sponsored by the Swiss Federal Office for the Environment to quantify shoreline trash along swiss lakes and rivers. Multiple small scale **litter surveys** are completed at different locations within a designated survey area. For the year 2020/2021 the survey areas were defined by the municipalities that border the Aare, Rhône, Ticino and Linth/Limmat rivers and any lakes or rivers that contribute.
