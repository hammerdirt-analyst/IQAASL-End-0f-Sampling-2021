# Identification, quantification and analysis of observable anthropogenic debris along swiss river and lakes (IQAASL)

[![DOI](https://zenodo.org/badge/382063409.svg)](https://zenodo.org/badge/latestdoi/382063409)

IQAASL was a project sponsored by the Swiss Federal Office for the Environment to quantify shoreline trash along swiss lakes and rivers. Multiple small scale litter surveys are completed at different locations within a designated survey area. For the year 2020/2021 the survey areas were defined by the municipalities that border the Aare, Rhône, Ticino and Linth/Limmat rivers and any lakes or rivers that are within the catchment area.

The following components (currently being refactored), were developed specifically to manage the data collected:

* REST API with Django REST framework: https://github.com/hammerdirt-dev/hammerdirt_api
* Front end with ReactJS: https://github.com/hammerdirt-dev/plages_prop

Develpment of these two tools stopped for two years while we were out in the field collecting samples. The new version of the API and frontend will incorporate language support and additional functionality in the survey form.

hammerdirt staff maintain the repo for the report, the API and the front end.

## Contents

### report

1. A .pynb file each survey area, lake and any chapter that had calculations
2. The  .md file for all other chapters
3. The \_toc.yml and \_config.yml file for each language version

### resources
5. All the images and maps for the report
6. ALL the data including explanatory variables [ readme_data ](https://github.com/hammerdirt-analyst/IQAASL-End-0f-Sampling-2021/blob/main/resources/readme_data.md).

### docs

The complete html version of the report in German and English you can see that here [Litter Surveyor Report](https://hammerdirt-analyst.github.io/IQAASL-End-0f-Sampling-2021/titlepage.html)

### \_build

Any other available build formats

### tocs

The table of content files for different configurations

### templates

A series of operations that produces a standardized report.


## Contributing

This report was the inspiration for three manuscripts in devlopment and could serve as an initiation to data science and computing. Specifically for those interested in discrete, `random` observations or count data methods this repo may provide you with a new challenge.

The REST API for the new application is in development here [IQALS](https://github.com/hammerdirt-analyst/iqals)

Currently there is a team working on the application of a simple machine learning model that describes the probability of finding an object given the data. Development has also begun on a more complex model that predicts the range of probable values that a person may encounter.

The methods and formatting used in this report are being refactored for use in the [ litter surveyor ](https://www.plagespropres.ch/) as the evolution of that application continues.

There are ample oportunities to learn, teach and contribute.

#### more information

analyst@hammerdirt.ch or dev@hammerdirt.ch
> :heart: what you do 
