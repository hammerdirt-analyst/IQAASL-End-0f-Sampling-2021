# Foreword

<a href="intro_de.html" > Deutsch </a>


The aim of this project was to collect data and develop the necessary infrastructure to accurately assess the composition and abundance of anthropogenic material along selected Swiss rivers and lakes and present those findings in a consolidated web-based report. 

## Assessment method

n 2008 the first international guide to monitoring beach-litter was published by the United Nations Environment Program (UNEP) and Intergovernmental Oceanographic Commission (IOC) {cite}`unepseas`. This method was reproduced by the OSPAR Commission in 2010 {cite}`ospard10`.  In 2013 the EU released Guidance on Monitoring of Marine Litter in European Seas (The guide) {cite}`mlwguidance`. Switzerland is a member of OSPAR and has over 1,400 samples using the methods described in The guide. 

*A beach-litter survey is the accounting of visible anthropogenic material identified within a delimited area that is bordered on one side by a lake, river or ocean.*

* Locations are defined by their GPS points 
* Length and width are measured for each survey area 
* Visible pollutants within the survey area are collected, classified, counted and weighed
* All items are classified based on code definitions included in _The guide_.

To identify objects of regional interest supplementary codes were added. For example, codes were developed for items such as pheromone bait containers and ski poles to account for the occurrence of these objects when identified in certain regions. Identifying and quantifying items allows researchers and stakeholders to determine probable sources and define reduction strategies targeting specific items. 

For more information: [Code groups](codegroups).


## Assessment metric

The median value (50th percentile) of the survey results is reported as the number of objects per 100m (p/100m) of shoreline. This is the method described in EU Marine Beach Litter Baselines {cite}`eubaselines` and is the standard used in this report. The 100-meter shoreline standard used in the marine environment is appropriate for coastal regions of the European continent. However, urbanization and topography present unique challenges when selecting locations suitable to safely conduct yearlong shoreline litter surveys.

Limiting surveys to 100 meters of exposed shoreline would have dramatically reduced the number of available survey locations as well as the use of preexisting data. Thus, the IQAASL reflects local topography with a median survey length of 45m, and an average of 51m. Surveys less than 10m were not considered in the baseline analysis. The survey results are converted to p/100m by multiplying the survey result by 100.


### Collecting data

A beach litter survey can be conducted by anybody at anytime. If the survey is conducted according to the method described in The Guide {cite}`mlwguidance` or [Beach litter baselines](threshhold) the result can be compared directly to the charts in this report. There is no need to enter the data into the system to compare results. 

__Collecting data__ for the report (or the next report) requires some on the job training and an evaluation. It usually takes 3-5 surveys to acclimate an individual to the task. Most of the time is spent identifying objects and the importance of maintaining a field notebook. The advantage to contributing data is that the reporting procedure is automated and there is always access to the results. 

## Using this report

It is important to understand the difference between the _median_ {cite}`mediandef` and the _average_ {cite}`meandeff` when interpreting the results. Except for monthly results the survey results are given as the __median__ p/100m for the location in question. 

As an example, consider the __median__ survey result for the most common objects on Thunersee and Brienzersee.


```{figure} resources/images/intro/tbexample.jpeg
---
width: 600px
name: mcommonforeword
---

` `

```

{numref}`Figure {number}: <mcommonforeword>` _Interpreting the survey results. The aggregated results from all survey areas are on the far-right column, preceded by the aggregated results from Thunersee and Brienzersee. The first six columns are the municipalities from where the samples were taken. This standard is maintained throughout the document. The number represents the median survey value for that object. If that object is not found in at least half of the surveys then the median value will be zero. The median value is a reasonable estimate of the number of objects likely to be found if a litter survey were repeated_. 

The results for plastic construction waste indicate that it was more prevalent in Bönigen (4.5p/100m) and Unterseen (1.5p/100m) versus the other municipalities where the median value is zero. However Industrial sheeting and cigarettes were identified at all municipalities in at least 1/2 the surveys. 

In practical terms there was a better chance of finding plastic construction waste on the beach in Bönigen and Unterseen than the other municipalities. However, the chances of finding industrial sheeting were approximately equal anywhere but the most might be found at at Brienze (67p/100m). 

The [key indicators](keyindicators) chapter gives a precise definition of each of the basic statistics that can be derived from the survey results and how they are used for identifying zones of accumulation and significant events. The methods used to calculate the different environmental variables are explained in [_The land use profile_](luseprofile). The codes and descriptions used to identify the items as well as the different economic groupings are covered in detail in [_Code groups_](codegroups). How samples are collected and the methods for identifying extreme values and calculating baselines for a region can be found in [_Beach litter baselines_](threshhold).

The results for each municipality are included with the lake or river to which they belong. A more detailed report can be produced for any municipality in this document. 

### Contributing to this report

This report is versioned therefore it is very easy to submit articles or analysis that correct, clarify or improve the content. The easiest way to contribute is to send a pull request to [end of sampling repo](https://github.com/hammerdirt-analyst/IQAASL-End-0f-Sampling-2021). Submissions are accepted in all official Swiss national languages.
