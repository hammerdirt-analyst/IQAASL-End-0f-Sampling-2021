# Description of the content in the resources directory

This does not include the images and maps. The map names are self explanatory and the images are under the directory of the document where it can be seen.


## .CSV files: 

__resources/agg_results_with_land_use_2015.csv:__

Contains all the records since November 2015, including the land use rates calculated to 1500m.  The records ARE not aggregated to GFRAGS or MLW 

Columns: 'loc_date', 'date', 'water_name_slug', 'location', 'code', 'pcs_m', 'quantity', 'river_bassin', 'length', 'ilength', 'groupname', 'city', 'population', 'intersects', 'fail', '% to buildings', '% to trans', '% to recreation', '% to agg', '% to woods', '% to water', '% to unproductive', 'streets' 

__resources/alpes_dims.csv:__

The weights, measures and times for the surveys in the Alps 

Columns: 'survey_key', 'date', 'length', 'area', 'mac_plast_w', 'mic_plas_w', 'total_w', 'est_weight', 'num_parts_staff', 'num_parts_other', 'time_minutes', 'participants', 'project', 'is_2020', 'location', 'loc_date', 'water_name_slug', 'river_bassin', 'survey area' 

__resources/beaches_with_land_use_rates.csv:__

All the information that is specific to a survey location, includes land use, BNS number and city. 

Columns: 'slug', 'location', 'latitude', 'longitude', 'post', 'country', 'water', 'water_name', 'city_slug', 'water_name_slug', 'is_2020', 'city', 'bfsnum', 'population', 'streets', 'intersects', 'river_bassin', 'industrial', 'residential', 'government', 'agg_buildings', 'unk_building', 'roads', 'railways', 'airports', 'special', 'recreational', 'orchards', 'vineyards', 'horticulture', 'arable', 'meadows', 'farmpastures', 'alpinemeadows', 'aplinepasteurs', 'closed_forest', 'open_forest', 'brush_forest', 'woods', 'lakes', 'rivers', 'unproductive', 'bareland', 'glaciers', 'luse_total', 'water_value', 'adjusted_land_use', 'part_industrial', 'part_residential', 'part_government', 'part_agg_buildings', 'part_unk_building', 'part_roads', 'part_railways', 'part_airports', 'part_special', 'part_recreational', 'part_orchards', 'part_vineyards', 'part_horticulture', 'part_arable', 'part_meadows', 'part_farmpastures', 'part_alpinemeadows', 'part_aplinepasteurs', 'part_closed_forest', 'part_open_forest', 'part_brush_forest', 'part_woods', 'part_lakes', 'part_rivers', 'part_unproductive', 'part_bareland', 'part_glaciers', '% to buildings', '% to trans', '% to recreation', '% to agg', '% to woods', '% to water', '% to unproductive', 'is_slr', 'is_mcbp', 'both' 

__resources/checked_alpes_survey_data_be.csv__

The unaggregated data from the Alps surveys 

Columns: 'date', 'code', 'pcs_m', 'quantity', 'location', 'loc_date', 'water_name_slug', 'river_bassin', 'length', 'ilength', 'groupname', 'city', 'population', 'intersects', 'fail', '% to buildings', '% to trans', '% to recreation', '% to agg', '% to woods', '% to water', '% to unproductive', 'streets', 'month', 'eom', 'material', 'w_t', 'streets km', 'p/100m' 

__resources/checked_alpes_survey_data.csv__

Records are aggregated to Gfrags and Gfoams 

Columns: 'date', 'code', 'pcs_m', 'quantity', 'location', 'loc_date', 'water_name_slug', 'river_bassin', 'length', 'ilength', 'groupname', 'city', 'population', 'intersects', 'fail', '% to buildings', '% to trans', '% to recreation', '% to agg', '% to woods', '% to water', '% to unproductive', 'streets', 'month', 'eom', 'material', 'w_t', 'streets km', 'p/100m', 'area' 

__resources/checked_before_agg_sdata_eos_2020_21.csv__

The unaggregated data from the IQAASL project 

Columns: 'date', 'code', 'pcs_m', 'quantity', 'location', 'loc_date', 'water_name_slug', 'river_bassin', 'length', 'ilength', 'groupname', 'city', 'population', 'intersects', 'fail', '% to buildings', '% to trans', '% to recreation', '% to agg', '% to woods', '% to water', '% to unproductive', 'streets', 'month', 'eom', 'material', 'w_t', 'streets km', 'p/100m' 

__resources/checked_sdata_eos_2020_21.csv__

The data used for the report. Codes aggregated to Gfrags and Gfoam 

Columns: 'date', 'code', 'pcs_m', 'quantity', 'location', 'loc_date', 'water_name_slug', 'river_bassin', 'length', 'ilength', 'groupname', 'city', 'population', 'intersects', 'fail', '% to buildings', '% to trans', '% to recreation', '% to agg', '% to woods', '% to water', '% to unproductive', 'streets', 'month', 'eom', 'material', 'w_t', 'streets km', 'p/100m', 'area' 

__resources/codes_german_Version_1.csv__

The English to German code description translations 

Columns: 'code', 'description', 'german' 

__resources/codes_with_group_names_2015.csv__

The code definition file has columns to apply different explanatory variables.  

Columns: 'code', 'material', 'description', 'source', 'source_two', 'source_three', 'parent_code', 'direct', 'single_use', 'micro', 'ospar_code', 'groupname' 

__resources/corrected_dims.csv__ 

The dimensional data from the IQAASL project. 

Columns: 'survey_key', 'date', 'length', 'area', 'mac_plast_w', 'mic_plas_w', 'total_w', 'est_weight', 'num_parts_staff', 'num_parts_other', 'time_minutes', 'participants', 'project', 'is_2020', 'location', 'loc_date', 'water_name_slug', 'river_bassin', 'survey area' 

## .JSON files 

__resources/river_basins.json__

Defines the membership of a location to a survey area. Beach names are stored in an array keyed to the name of a survey area. 

__resources/french_code_translations.json__ 

Keys the Gcode to the the french description. 
