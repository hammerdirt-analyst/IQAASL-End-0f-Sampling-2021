# Identification, quantification and analysis of observable anthropogenic debris along swiss river and lakes (IQAASL)

IQAASL is a project sponsored by the Swiss Federal Office for the Environment to quantify shoreline trash along swiss lakes and rivers. Multiple small scale **litter surveys** are completed at different locations within a designated survey area. For the year 2020/2021 the survey areas were defined by the municipalities that border the Aare, Rhône, Ticino and Linth/Limmat rivers and any lakes or rivers that contribute.

:::{note}

This is version 0.02 _The review draft: cartography_

__Content revisions__ I have received a few comments and will address them during this version. The numerical results will not change, unless somebody finds a mistake!

We are adding the following during this review:

* lake and city results
* images

and wrapping up the summary

contact roger@hammerdirt.ch
:::

## The Litter Surveyor Report

This report uses the techniques developed in Switzerland and the European Union (EU) to identify the most common litter objects, their relative abundance and where they accumulate
in the vast network of Swiss rivers and lakes. This is done using a harmonized data collection protocol and measuring scheme that has been in use and in active development
in Switzerland since 2015 and internationally for decades. {cite}`mlwguidance` {cite}`slr` {cite}`eubaselines`. 

Current research suggests that inland lakes are transition points for garbage transported by rivers, some of that trash goes on to the next lake (or the ocean) 
and some of it remains and degrades in the lake where it was deposited. For Switzerland that means our lakes could be _sinks_ or _dumps_ for garbage and that it
does not all go the ocean. {cite}`Kooi2018`

In September 2020 the EU adopted a common benchmarking method using data collected following the same protocol used in Switzerland. The value of the benchmarks set by the EU are not
as important as __the definition of a common method to compare results from beach litter surveys from one period to the next__. This has been lacking and has left
administrators and stakeholders with no objective, standardized method to assess performance of litter mitigation strategies. 

The _Litter Surveyor Report_ attempts to integrate the methods proposed by the EU as a set of tools to interpret current beach litter survey results from the national to
the municipal level. The results from past and present beach litter surveys are presented in an objective way and in the context of current events.

## Summary

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

### Trends from 2017

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

The comparison of survey results from both projects also shows that **a positive statistically relevant association** can be attributed to items related to the consumption
of food or tobacco products and the level and type of economic development within 1500m of the survey location. Confirming observations in the SLR that litter
survey results were increased in urban and suburban environments.

Other objects like fragmented plastics, fragmented foams and industrial sheeting have few if any positive associations in either project year and the observed
levels remained within the range encountered in the SLR.

See the full report [_More and less trash since 2017_](slr-iqaasl)

 ---

### Local versus regional

Beach litter surveys are collections of many individual surveys. Here we compare the results of two different groups of items under two opposite land use conditions
(see [_The land use profile_](luseprofile)). In one group the use case is well known and the connection to human behavior and the land use is uncontested: tobacco and
snacks, this group is called _contributed_. The other group includes fragmented objects of different densities, specific objects less than 5mm and construction plastics,
none of which show any association to measurable land use features, this group is called distributed

The results of the test show that the distributed objects are found at similar rates regardless of land use class. Suggesting that there is another mechanism of transport
and deposition for these objects that is not directly associated with behavior. The presence of high density plastics in this group and the numerous river or canal discharge
sites within 1500 meters of every survey location support previous observations that these objects are being transported to the survey site and a portion of them are sinking
or beaching within proximity of the survey site.

See the section [_Transport an empirical approach_](transport)

 ---

### Baseline and extreme values

The proposed methods in the JRC Technical document _An Analysis of a pan-European 2012-2016 beach litter dataset_ are applied to the results from IQAASL. The baseline values are calculated for each survey area and the different methods of calculation are explained and included with the survey results.

*Section 7.3 identifying extreme values: __left__ comparison of simulated survey results to observed values. __right__: distribution of simulated survey results with detail of IQR and expected $90^{th}$ percentile* 
:::{image} resources/images/intro_baselines.png
:alt: IQAASL and SLR charts
:class: bg-primary mb-1
:width: 800px
:align: center
:::
*MOM - method of moments Scipy implementation, MLE - Maximum likelihood estimation, observed - the survey results* 
<br></br>

In general survey results were higher in the Rhône survey area (RSA) than the other survey areas, both in terms of the median survey totals and the median totals of the most common objects. 

See the section [_Calculating baseline values_](threshhold) for sample calculations and a detailed explanation.

 ---
 
### Sources

Geographically a potential source can be determined based on the median survey result of an object in relation to its distance from a probable source. An example
of this is given in the section _Key Statistical Indicators_. Certain objects, like pre-production plastic pellets (GPI), cigarette ends or cable-ties are easy to 
identify and changes in the relative amounts these objects are easy to spot. This is a benefit of using the median value as a baseline.

On a regional basis any stream/river/canal should be considered a source of fragmented plastics and construction plastics. They have a tendency to
sink after they transition from river to lake, as result they accumulate near where they are deposited. The communities nearest the hydrological exchanges
tend to have increased survey results with a wider variety of objects.

Economically the sources are determined by grouping the codes assigned to the objects according to use or description. Combined food and tobacco items make up 36%
of the items found and infrastructure and agriculture are 24% of the total. Objects originating from waste water facilities or objects less than five millimeters 
make up another 10%. The relative amounts change for each survey area suggesting that local priorities may not always match regional priorities.

See the section [_Code groups_](codegroups) for a complete definition of how the codes were grouped.

 ---

### The structure and evolution of this document

The purpose is to provide a repeatable method and process to collect and evaluate beach-litter data at a scale that is appropriate to Switzerland and exploitable by
all stakeholders. The method and process need to reflect current advances in the field, the needs of stakeholders and faithfully report the survey results as collected
by the surveyor.

This document is a collection of scripts written in python and markdown contained in a series of notebooks designed specifically for completing data analysis. This
system has been in use for quite some time in the research community. Together those scripts make a book, or a [Jupyter Book](https://jupyterbook.org/intro.html).

The surveyor uses this application [plagespropres](https://www.plagespropres.ch/) to submit data and the report is processed here: [end of sampling repo](https://github.com/hammerdirt-analyst/IQAASL-End-0f-Sampling-2021).

Not all tasks have been automated. Land use data is calculated using QGIS and the method to automate this process has not been developed.