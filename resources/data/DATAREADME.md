# Data 

There are 7 .csv files labeled as follows:

1. before_2019.csv
2. after_2019.csv
3. after_may_2021.csv
4. alpes_ticino_to_add.csv
5. beaches.csv
6. codes.csv
7. new_landuse.csv

## Survey data

The suryvey data is contained in the following: before_2019.csv, after_2019.csv, after_may_2021.csv, alpes_ticino_to_add.csv.
The column names are as follows:

1. sample_id: a combination of date and location.
2. date: the date the sample was taken.
3. feature_name: the name of the park, river or lake where the sample was taken.
4. location: the name of the location as established by the person that made the observation.
5. code: the marine-litter-watch code from the 2013 guide to monitoring marine litter.
6. pcs/m: the pieces per meter for that code with that sample_id.
7. quantity: the number found. 
8. parent_boundary: The survey area or river bassin, could be park.
9. length: the number of meters surveyed.
10. groupname: the use case of the object (defined by code).
11. city: the name of the municipality.
12. feature_type: the type of feature (park, river, lake).

## Landuse and beach data

The landuse data is contained in the following: new_landuse.csv, beaches.csv. The new_landuse.csv file contains the following
columns: *location,buildings,wetlands,forest,public-services,recreation,undefined,streets,vineyards,cliffs,city-center,orchards,boulders*.
The location column is the key to join this data with the survey data and the beach data. The column values are the percentage of the
buffer zone that is covered by that landuse. The beaches.csv file contains the following columns:

1. slug: the location name
2. latitude,, longitude: the lat and lon
3. country: the two letter abbreviation
4. feature_type: lake river or park
5. display_feature_name: the name to display for the feature name
6. city_slug: the city in a code friendly format
7. feature_name: the name of the park, river or lake
8. city: the city of the survey location
9. parent_boundary: the river bassin or park
10. canton: the canton

## Codes and definitions

The codes.csv file contains the following columns:

1. code: the object codes from *A guide to monitioring European Seas* 
2. material: One of metal, plastic, paper, chemical, wood, glass, undefined
3. en: the english description
4. source: possible pathway to the beach
5. parent_code: if the code is local, then the parent code connects it back to the guide
6. single_use: whether it is single use or not
7. groupname: use case
8. fr: the french description of the object
9. de: the german description of the object