"""
Utitlity functions for summarizing and analyzing data from the litter database. Used with a jupyter notebook.

Creates folder structures, groups data, creates graphs and outputs JSON format data.

See the repo @hammerdirt/three_year_final for the accompanying notebooks and intended use.

Contact roger@hammerdirt.ch or @hammerdirt

"""
import os
import json
import pandas as pd


def make_project_folder(here, project_name):
    """Makes a subdirectory with the specified 'project_name'
    in the directory specified by 'here'.

    Args:
        here: str: the home directory of the project
        project_name: str: the name of the project foler

    Returns:
        The directory of the project folder

    Used in all notebooks that read or write data.
    """
    project_folder = '{}/{}'.format(here, project_name)
    if os.path.isdir(project_folder):
        project_folder = project_folder
    else:
        os.mkdir(project_folder)
    return project_folder

def json_file_get(this_path):
    """Reads the local JSON in from the provided file path.
    Used in all notebooks that read in JSON data.

    Args:
        this_path: str:  a file path or url that returns a .JSON object

    Returns:
        a python object (list or dict) depending on the .JSON object requested
    """
    with open(this_path, 'r') as infile:
        data = json.load(infile)
        return data

def unpack_survey_results(survey_results):
    """Unpacks the surveys-results api-endpoint and adds the location name to each result dict.

    Used in notebooks that make an api call to 'https://mwshovel.pythonanywhere.com/api/surveys/daily-totals/code-totals/swiss/'
    """
    unpacked = []
    for location_data in survey_results:
        location = location_data['location']
        for each_dict in location_data['dailyTotals']:
            each_dict['location']=location
            unpacked.append(each_dict)
    return unpacked

def use_this_key(x, key, column='no column'):
    """Applies the variable x to a mapping object: key. Checks the data type of key and
    and applies x as a variable to the key in manner that is consistent with it's type.

    Args:
         x: str: the value that needs to be mapped
         key: object: dict, series or dataframe contains the desired value
         column: str: the column lable if required

    Returns:
        The paired value of x
    """
    this_type = type(key)
    if isinstance(key, tuple):
        x = [x]
    else:
        pass
    if isinstance(key, dict):
        try:
            data = key[x]
        except:
            data = 'bad key'
    elif this_type == pd.core.series.Series:
        try:
            data = key.loc[[x]]
            data = data[0]
        except:
            data = 'bad key'
    else:
        try:
            data = key.loc[x, column][0]
        except:
            data = 'bad key'

    return data
def hide_spines_ticks_grids(an_ax):
    """Removes spines, ticks and grid from matplotlib axis object

    Args:
        an_ax: object: matplotlib axis

    Returns:
          nothing

    """
    for spine in an_ax.spines.values():
        spine.set_visible(False)
    an_ax.tick_params(bottom=False, labelbottom=False, left=False, labelleft=False)
    an_ax.grid(False)

def push_this_to_json(filename="", data=[]):
    with open(filename, "w") as a_file:
        json.dump(data, a_file)