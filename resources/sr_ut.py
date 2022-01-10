import json
import pandas as pd
from scipy import stats
from matplotlib import colors
import seaborn as sns
import numpy as np
from IPython.display import display
from PIL import Image as PILImage



luse_exp = ["% to buildings", "% to recreation", "% to agg", "% to woods", "streets km", "intersects"]
luse_ge = ["% zu Gebäude", "% zu Erholung", "% Landwirtschaft", "% zu Wald", "Straßen km", "kreuzt"]


# columns needed
def shorten_the_value(an_array, a_df):
    """Change the value in a data frame column with an array of three values.

    Args:
    an_array: array: the index, column and the new value
    a_df: dataframe: the dataframe to change:

    Returns:
    The changed dataframe
    """
    a_df.loc[an_array[0], an_array[1]] = an_array[2]
    
    return a_df


def fo_rmat_date_column(x, a_format="%Y-%m-%d"):
    # takes in a a data frame and converts the date column to timestamp
    x["date"] = pd.to_datetime(x["date"], format=a_format)
    return x.copy()


def slic_eby_date(x, start_date, end_date):
    # slices a data frame by the start and end date inclusive
    return x[(x.date >= start_date) & (x.date <= end_date)].copy()


def fo_rmat_and_slice_date(x, a_format="", start_date="", end_date=""):
    # formats the date column and slices the data frame by the start and end date
    new_df = fo_rmat_date_column(x, a_format=a_format)
    new_df = slic_eby_date(new_df, start_date, end_date)
    return new_df


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


def json_file_get(this_path):
    """Reads the local JSON in from the provided file path.
    Used in all notebooks that read in JSON data.

    Args:
        this_path: str:  a file path or url that returns a .JSON object

    Returns:
        a python object (list or dict) depending on the .JSON object requested
    """
    with open(this_path, "r") as infile:
        data = json.load(infile)
        return data


def make_plot_with_spearmans(data, ax, n, unit_label="p/100m"):
    """Gets Spearmans ranked correlation and make A/B scatter plot. Must proived a
    matplotlib axis object.
    """
    sns.scatterplot(data=data, x=n, y=unit_label, ax=ax, color="black", s=30, edgecolor="white", alpha=0.6)
    corr, a_p = stats.spearmanr(data[n], data[unit_label])

    return ax, corr, a_p


def make_a_summary_table(ax, data, colLabels, a_color="dodgerblue", font_size=12, s_et_bottom_row=True):
    
    """ Makes a table of values with alternate row cololrs.

    Args:
    ax: object: matplotlib table object
    data: array: the 2d array used to generate the table object
    cols_to_use: array: the list of column names
    a_color: str: matplotlib named color, face and edgecolor of table cells
    font_size: int: the font size for the table cells
    s_et_bottom_row: bool: whether or not to draw bottom line on the last row

    Returns:
    The table object formatted.
    """

    ax.auto_set_font_size(False)
    the_cells = ax.get_celld()

    line_color = colors.to_rgba(a_color)
    banded_color = (*line_color[:-1], 0.1)

    # the different areas of formatting
    top_row = [(0, i) for i in np.arange(len(colLabels))]
    bottom_row = [(len(data), i) for i in np.arange(len(colLabels))]
    top_columns = top_row[1:]
    data_rows = [x for x in list(the_cells.keys()) if x not in top_row]
    odd_rows = [x for x in data_rows if x[0] % 2 > 0]
    first_column = [x for x in data_rows if x[1] == 0]

    # make the first cell a litte smaller than the others
    ax[0, 0].set_height(1 / (len(data)))
    ax[0, 0].set_text_props(**{"va": "top"})

    for a_cell in top_row:
        ax[a_cell].visible_edges = "B"
        ax[a_cell].set_text_props(**{"fontsize": font_size})
        ax[a_cell].set_edgecolor("white")
        ax[a_cell].PAD = .2

    for a_cell in top_columns:
        ax[a_cell].set_height((1.25 / (len(data))))
        ax[a_cell].set_text_props(**{"va": "center"})

        ax[a_cell].set_edgecolor(line_color)
        ax[a_cell].visible_edges = "T"

    for a_cell in odd_rows:
        ax[a_cell].set_facecolor(banded_color)

    for a_cell in data_rows:
        ax[a_cell].set_height(.75 / (len(data)))
        ax[a_cell].visible_edges = "BTLR"
        ax[a_cell].set_text_props(**{"fontsize": font_size})
        ax[a_cell].set_edgecolor("white")
        ax[a_cell]._text.set_horizontalalignment("center")

    for a_cell in first_column:
        ax[a_cell]._text.set_horizontalalignment("right")
        ax[a_cell].PAD = .02

    if s_et_bottom_row is True:
        
        for a_cell in bottom_row:
            ax[a_cell].visible_edges = "B"
            ax[a_cell].set_edgecolor(line_color)

    return ax

def make_a_table(ax, data, colLabels=[], a_color="dodgerblue", colWidths=[.22, *[.13]*6], bbox=[0, 0, 1, 1], bottom_row=True, *args, **kwargs):
    """Makes a table with banded rows from a matplotlib axes object.
    
    :param ax: An axes
    :type ax: matplotlib axes
    :param data: An array of the table values not including column names or labels
    :type data: array
    :param colLabels: The labels for the data table columns
    :type colLabels: array
    :param a_color: The row shading
    :type a_color: str
    :param colWidths: The width of each column in fractions of 1
    :type colWdiths: array, x < 1
    :param bbox: The location of the table in figure space
    :type bbox: array
    :return: A table on the provided axis
    :rtype: matplotlib.axes
    
    """
    
    a = ax.table(data,  colLabels=colLabels, colWidths=colWidths, bbox=bbox, **kwargs)
    b = make_a_summary_table(a,data ,colLabels, a_color, s_et_bottom_row=bottom_row)
    return b

def feature_data(data, feature_level, these_features=[], **kwargs):
    """Slices the data at the feature level for the features defined in these_features.
    Defines the data that all analysis is based on.
    
    :param data: A pandas data frame of survey results
    :type data: object: pandas.core.frame.DataFrame
    :param feature_level: The column name that contains
        the groups for the desired aggregation level.
    :type feature_level: str
    :param these_features: An array of values that are contained in feature_level
    :type feature_level: array
    :return: A sliced data frame with the date converted to datetime object
    :rtype: pandas.core.frame.DataFrame
    """
    
    sliced_data = data[data[feature_level].isin(these_features)].copy()
    
    # the loc_date is the unique indentifier for a survey
    sliced_data["loc_date"] = list(zip(sliced_data.location.values, sliced_data["date"].values))

    # ensure that the date is set to datetime
    sliced_data["date"] = pd.to_datetime(sliced_data["date"])
    
    return sliced_data


    
def the_aggregated_object_values(data, description_map={}, material_map={}, agg={}, obj="code", agg_level="groupname", material_totals="material", **kwargs):
    """Assigns description and material type to objects in the survey results. Defines the cumulative fail-rate, % of total
    and material totals for all the objects in data.
    
    :param data: The data frame that has the survey data
    :type data: object: pandas.core.frame.DataFrame
    :param obj: The column of interest, the highest aggregation element
    :type obj: string, column name, default=code
    :param agg_level: The next level of aggregateion, column of interest
    :type agg_level: string, column name, default=groupname
    :param agg: A dictionary of columns and aggregation functions
    :type agg: dictionary, example: {"columName":"an aggrgate function"}
    :param material_totals: Wether to include a material column or not
    :type material_totals: string, the name of the column, default=material
    :param description_map: A mapping of code value to the plain text description of the object
    :type description_map: dictionary or function that accpets code as an argument and returns a description
    :param material_map: A mapping of code value to the material composition of the object
    :type material_map: dictionary or function that accpets code as an argument and returns a material
    :return: A pandas data frame of the cumulative results for each object in obj
    :rtype: pandas.core.frame.DataFrame
    """
    
    code_totals = data.groupby([obj, agg_level], as_index=False).agg(agg)
    
    # percent of total
    code_totals["% of total"] = ((code_totals.quantity/code_totals.quantity.sum())*100).round(2)
    
    # fail and fail-rate
    code_totals["fail"] = code_totals.code.map(lambda x: data[(data.code == x) & (data.quantity > 0)].loc_date.nunique())
    code_totals["fail rate"] = ((code_totals.fail/data.loc_date.nunique())*100).astype("int")
    code_totals.set_index("code",inplace=True)
    code_totals["item"] = code_totals.index.map(lambda x: description_map[x])
    
    if material_totals:
        
        code_totals[material_totals] = code_totals.index.map(lambda x: material_map[x])
        
    
    return code_totals

def the_ratio_object_to_total(data, obj="material", measure="quantity", metric="% of total"):    
    """Makes a ratio column of one column to another. The instance quantity is divided by the total quantity.
    
    :param data: The data frame that has the comlumns
    :type data: pandas.core.frame.DataFrame
    :param obj: The object or column for which the ratio is required
    :type obj: str, the column name of the object of interest
    :param measure: The number or value of which the ratio is comprised
    :type measure: str, the name of the column that has the numerical values
    :param metric: The name of the new column
    :type metric: str,
    :return: A sorted data frame
    :rtype: pandas.core.frame.DataFrame    
    """
    
    # group the code_totals df by material and get the quantity
    a = data[[obj, measure]].groupby(obj, as_index=False)[measure].sum()
    a[metric] = a[measure]/a[measure].sum()
    b = a.sort_values(by=measure, ascending=False)
    
    return b

def make_table_values(data, col_nunique=["location", "loc_date", "city"], col_sum=["quantity"], col_median=[]):
    """Extracts particular aggregation values for different columns and returns a dictionary of values
    keyed to the column name.
    
    :param data: The data frame that has the columns
    :type data: pandas.core.frame.DataFrame
    :param col_unique: Counts the unique values of the columns
    :type col_unique: array
    :param col_sum: Sums the values of the columns
    :type col_unique: array
    :param col_median: Returns the median value for the array
    :type col_unique: array
    :return: A dictionary of values that corresponds to the requested aggregation
        for each column name
    :rtype: dictionary    
    """
    
    table_data = {}
    
    for col in col_nunique:
        table_data.update({col:data[col].nunique()})
    for col in col_sum:
        table_data.update({col:data[col].sum()})
    for col in col_median:
        table_data.update({col:data[col].median()})
    
    return table_data

def gather_dimensional_data(dimsData, this_level="city", locations=[], start_end=[], city_map=[], agg_dims={}):
    """Gathers the dimensional data by the designated locations and dates. Initiates a loc_date column
    and assigns the municpality to each record.
    
    :param data: The data frame that has the dimensional data
    :type data: pandas.core.frame.DataFrame
    :param locations: The survey locations of interest, fd.locaction.unique()
    :type locations: array or series, survey location names
    :param start_end: The start and end dates of the slice
    :type start_end: string, dates in string format "%Y-%m-%d"
    :param city_map: A mapping from location name to to city or any other mapping
    :type city_map: pandas.core.frame.DataFrame, index=survey_location
    :param agg: Aggregates the data by level according to the parameters of agg
    :type agg: dicytionary of column names and aggregation types
    """
    
    a = dimsData[(dimsData.location.isin(locations))&(dimsData["date"] >= start_end[0])&(dimsData["date"] <= start_end[1])].copy()
    a["loc_date"] = list(zip(a.location.values, a["date"].values))
    
    if len(city_map):
        try:
            a[this_level] = a.location.map(lambda x: city_map.loc[x])
        except:
            print("the cities could not be mapped to the dims data")
            pass
    if agg_dims:
        try:
            a = a.groupby([this_level]).agg(agg_dims)
        except:
            print("the dimensional data could not be aggregated")
            pass
            
        
    
    return a

def update_dictionary(a_dict, updates={}):
    """Convenience function for updating a dictionary
    
    :param a_dict: A dictionary of column names and new names
    :type a_dict: dict,
    :param updates: A dictionary of updates to a_dict
    :type updates: dict
    :return: A dictionary of old column names to new column names
    :rtype: dict
    """
    if updates:
        a_dict.update(updates)
    return a_dict

# column headers for printed Dimenesional data summary
dims_table_columns = {"samples":"samples",
                      "quantity":"items",
                      "total_w":"total kg",
                      "mac_plast_w":"plastic kg",
                      "area":"m²",
                      "length":"meters"
                     }

def group_these_columns(data, these_columns=[], agg_this={}):
    """Convenience method for grouping operations
    
    :param data: The data frame that has the columns
    :type data: pandas.core.frame.DataFrame
    :param these_columns: The array of columns that are being grouped
        in the sequential order of grouping
    :type these_columns: array, column names
    :param agg_this: A dictionary of column names and aggregate functions
    :type agg_this: dictionary
    :return: The grouped data
    :rtype: pandas.core.frame.DataFrame
    """
    
    try:
        new_data = data.groupby(these_columns, as_index=False).agg(agg_this)
        new_data.set_index("date", inplace=True)
    
    except:        
        print("could not aggregate the data")
        new_data = data
        pass
    return new_data

def the_other_surveys(data, level_to_exclude="string", components_to_exclude=[]):
    """Returns a data frame without the components to exclude
    
    :param data: The data frame of interest
    :type data: pandas.core.frame.DataFrame 
    :param level_to_exclde: The hierarchal level of the excluded objects
    :type level_to_exclude: string, column name
    :param components_to_exclude: An array of values from level_to_exclude that
        should be removed.
    :type components_to_exclude: array
    :return: A data frame
    :rtype: pandas.core.frame.DataFrame
    """
    
    try:
        a = data[~data[level_to_exclude].isin(components_to_exclude)].copy()
    except:
        print("the surveys could not be excluded")
        a = data
              
    return a

def quarterly_or_monthly_values(data, feature, vals="p/100m", quarterly=["ticino"]):
    """Determines and then draws either quaterly or monthly resample of
    of survey results depending on the value of quaterly.
    
    :param data: The data frame of interest
    :type data: pandas.core.frame.DataFrame 
    :param feature: The current feature of interest
    :type feature: string, name of the feature
    :param vals: The column to resample
    :type vals: string
    :param quarterly: The names of the features that have quaterly samples
    :type quarterly: array
    :return: A data frame with eihther monthly or quarterly resamples and the designation
    :rtype: pandas.core.frame.DataFrame 
    
    """
    if feature in quarterly:
        plot = data[vals].resample("Q").median()
        rate = "quarterly"
    else:
        plot = data[vals].resample("M").median()
        rate = "monthly"
    
    return plot, rate

# convenience function to change the index names in a series
def change_series_index_labels(x, change_names):
    """A convenience funtion to change the index labels of a series x.
    Change_names is keyed to the series index.
    
    :param x: A pandas series
    :type x: pandas.series
    :param change_names: A dictionary that has keys = x.index and
        values = new x.index label
    :type change_names: dict
    :return: The series with the new labels
    :rtype: pandas.series    
    """
    
    new_dict = {}
    for param in x.index:
        new_dict.update({change_names[param]:x[param]})
    return pd.Series(new_dict)

def create_summary_table_index(unit_label, lang="EN"):
    """Assigns the current units to the keys and creates
    custom key values for tables of summary statistics.
    
    :param unit_label: The current value of unit label
    :type unti_label: string
    :param lang: the two letter abbreviation for the current language
    :type lang: string DE, EN
    :return: A dictionary that for the summary tables
    :rtype: dict   
    """
    
    if lang == "EN":
        new_data = {"count":"# samples",
             "mean":f"average {unit_label}",
             "std":"standard deviation", 
             "min":f"min {unit_label}",
             "max":f"max {unit_label}",
             "25%":"25%",
             "50%":"50%", 
             "75%":"75%",
             "total objects":"total objects",
             "# locations":"# locations",
         }
    elif lang == "DE":
        new_data = {"count":"# Proben", 
                "mean":f"Durchschnitt {unit_label}",
                "std":"Standardfehler", 
                "min":f"min {unit_label}",
                "max": f"max {unit_label}",
                "25%":"25%",
                "50%":"50%", 
                "75%":"75%",
                "total objects":"Totalobjekte",
                "# locations":"Anzahl der Standorte",
               }
    else:
        print(f"ERROR {lang} is not an option")
        new_data = {}
              
    
    return new_data

def fmt_pct_of_total(data, label="% of total", fmt=True, multiple=100, around=1):
    """Multiplies the value of the objects with label=label by multiple.
    
    :param data: A pandas data frame of survey results
    :type data: object: pandas.core.frame.DataFrame
    :param label: The column name to treat
    :type label: string
    :param fmt: Wehther or not the values should be foramtted to string
    :type fmt: boolean
    :param multiple: The number to multiply by
    :type mulitple: int or float
    :param round: The number of decimal places to round too
    :type round: int
    :return: The data frame
    :rtype: pandas.core.frame.DataFrame
    """
    
    data[label] = (data[label]*multiple).round(around)
    
    if fmt:
        data[label] = data[label].map(lambda x: f"{x}%")
    
    return data

def make_string_format(data, label="quantity", aformat="{:,}"):
    """Make string formats of values of a column in a dataframe. Returns the
    data frame
    """
    
    data[label]=data[label].map(lambda x: aformat.format(x))
    
    return data

def fmt_combined_summary(data, nf=[-1], fmt="{:,}"):
    """Convenience function for formatting the values of the combined
    summary. Accepts a series and returns an array of tuples of the
    index label and the formatted value
    
    :param data:A pandas series of values that need to be formatted
    :type data: pandas.core.series.Series
    :param nf: Index of objects not to format
    :type nf: array
    :param fmt: The formatting to be applied to each value
    :type fmt: string
    :return: An aray of tuples (<index label>, <formatted value>)
    :rtype: array    
    """
    
    if len(nf):
        new_data = [(x, fmt.format(int(data[x]))) for x in data.index[:-1]]
        new_data.append((data.index[-1], int(data[-1])))
        
    else:
        new_data = [(x, fmt.format(int(data[x]))) for x in data.index]
    
    return new_data

def aggregate_to_group_name(data, unit_label="p/100m", column="groupname", name="afeaturename", val="pt"):
    f_s_a = data.groupby(column, as_index=False)[unit_label].agg({unit_label:"median", "quantity":"sum"})
    if val == "pt":
        f_s_a["pt"] = (f_s_a.quantity/f_s_a.quantity.sum()).round(2)
        f_s_a.set_index(column, inplace=True)
        f_s_a[name] = f_s_a["pt"]
        data = f_s_a[name]
    elif val == "med":
        f_s_a.set_index(column, inplace=True)
        f_s_a[name] = f_s_a[unit_label]
        data = f_s_a[name]
    else:
        print("val is not defined as pt or med")
        data = ["an empty list"]
        
    
    return data

def aggregate_to_code(data, code_description_map, column="code", name="afeaturename", unit_label="p/100m"):
    
    f_s_a = data.groupby(column, as_index=False)[unit_label].median()
    f_s_a["item"] = f_s_a.code.map(lambda x: code_description_map.loc[x])
    f_s_a.set_index("item", inplace=True)
    f_s_a[name] = f_s_a[unit_label]
    
    return f_s_a[name]

# german translations
luse_ge = {"% to buildings": "% zu Gebäude",
           "% to recreation": "% zu Erholung",
           "% to agg": "% zu agg",
           "% to woods": "% zu Wald",
           "streets km": "Straßen km",
           "intersects": "kreuzt"
           }

mat_ge = {"Metal":"Metall", 
          "Chemicals":"Chemikalien",
          "Paper":"Papier",
          "Glass":"Glas",
          "Rubber":"Gummi",
          "Wood":"Holz",
          "Cloth":"Stoff",
          "Unidentified":"Ubekannt",
          "Undefined":"Unbestimmt",
          "Plastic":"Plastick"
         }

group_names_de =  {"waste water":"Abwasser",
                   "micro plastics (< 5mm)":"Mikrokunstoffe",
                   "infrastructure":"Infrastruktur",
                   "food and drink":"Lebensmittel und Getränke",
                   "agriculture":"Landwirtschaft",
                   "tobacco":"Tabak",
                   "recreation":"Freizeit",
                   "packaging non food":"Verpackungen nicht Lebensmitteln und Getränken",
                   "plastic pieces":"Kunststoffteile",
                   "personal items": "Persönliche Gegenstände",
                   "unclassified":"nicht klassifiziert",
                  
                  }
months_de={
    0:"Jan",
    1:"Feb",
    2:"Mär",
    3:"Apr",
    4:"Mai",
    5:"Jun",
    6:"Jul",
    7:"Aug",
    8:"Sep",
    9:"Okt",
    10:"Nov",
    11:"Dez"
}


def display_image_ipython(file_location, thumb=(1200, 700), rotate=0):
    """Convenience method to use PIL and Ipython to display images.

    :param file_location: The location of the file relative location of the file
    :type file_location: string
    :param thumb: The size of the image
    :type thumb: tuple, integers
    :return: displays the image or a message that the image could not be displayed
    :rtype: displayed image
    """

    try:
        im = PILImage.open(file_location)

    except:
        print(f"could not load image {file_location} ")

    if rotate == 0:
      im.thumbnail(thumb)




    else:
      print("rotate")
      im.thumbnail(thumb)
      im.rotate(rotate)



    display(im)


# def m_ap_code_to_description(data, key, func):
#   """Creates an "item" column in a data frame. Uses specified key and method
#   to assign value to "item".
#
#   Args:
#     data: pandas data frame
#     key: dictionary or array
#     func: method
#
#   returns:
#     dataframe
#   """
#   new_data = data.copy()
#   new_data["item"] = new_data.index.map(lambda x: func(x, key))
#   new_data.set_index("item", inplace=True)
#   return new_data


# def get_the_file_extension(x):
#   """Splits a string by the "." , returns everything after the ".""""
#   split = x.split(".")[-1]
#   return split


# def add_a_grouping_column(x, a_dict, column_to_match="", new_column_name="river_bassin"):
#   """Adds a new column to a dataframe. Matches values in column_to_match to values in a_dict

#   Args:
#     x: dataframe
#     a_dict: dict k=desired value, v=list of membership
#     column_to_match: str: column name
#     new_column_name:str
#   Returns:
#     The original data frame with a new column
#   """
#   for k, v in a_dict.items():
#     x.loc[x[column_to_match].isin(v), new_column_name] = k
#   return x


# def fo_rmat_date_column(x, a_format="%Y-%m-%d"):
#   """Takes in a data frame and converts the date column to timestamp."""
#   x["date"] = pd.to_datetime(x["date"], format=a_format)
#   return x.copy()


# def slic_eby_date(x, start_date, end_date):
#   """ slices a data frame by the start and end date inclusive"""
#   return x[(x.date >= start_date) & (x.date <= end_date)].copy()


# def fo_rmat_and_slice_date(x, a_format="", start_date="", end_date=""):
#   """Formats a date column in a dataframe and slices the data frame"""
#   new_df = fo_rmat_date_column(x, a_format=a_format)
#   new_df = slic_eby_date(new_df, start_date, end_date)
#   return new_df


# class SurveyData:
#   """preprocesses data"""

#   def __init__(self, data, beaches, these_cols=["loc_date", "location", "water_name_slug", "river_bassin", "date"],
#                foams={"G82": ["G82", "G912"], "G81": ["G81", "G911"], "G74": ["G74", "G910", "G909"]}, **kwargs):
#     self.data = data
#     self.these_cols = these_cols
#     self.foams = foams
#     self.beaches = beaches
#     self.levels = kwargs["levels"]
#     self.exp_variables = kwargs["exp_variables"]
#     self.locations_in_use = data.location.unique()
#     self.river_bassins = kwargs["river_bassins"]
#     self.code_maps = self.make_code_maps(self.data, self.these_cols, self.foams)
#     self.codes_in_use = data.code.unique()
#     self.group_names_locations = kwargs["code_group_data"]
#     self.code_groups = self.make_code_groups()
#     self.code_group_map = self.make_group_map(self.code_groups)
#     self.processed = self.add_exp_group_pop_locdate()
#     self.survey_data = self.assign_code_groups_to_results(self.processed, self.code_group_map)
#     self.daily_totals_all = self.survey_total_pcsm_q()
#     self.median_daily_total = self.daily_totals_all.pcs_m.median()
#     self.code_totals = self.survey_data.groupby("code").quantity.sum()
#     self.code_pcsm_med = self.survey_data.groupby("code").pcs_m.median()
  
#   def make_code_maps(self, data, these_cols, these_codes):
#     """Returns a dictionary of the aggregated values of these_codes, grouped by these_cols.

#       Args:
#         data: dataframe
#         these_cols: array: the columns to aggregate by
#         these_codes: dict: keys=labels, values:list
#       Returns:
#         A dict of dataframes. Example based on the default value for foams:

#         {"G82":dataframe of aggregated values, "G81":data frame of aggregated values}

#       """
#     wiw = {}
#     for code in these_codes:
#       a_map = data[data.code.isin(these_codes[code])].groupby(these_cols, as_index=False).agg(
#         {"pcs_m": "sum", "quantity": "sum"})
#       a_map["code"] = code
#       wiw.update({code: a_map})

#     return wiw

#   def agg_foams(self):
#     """Combines the different code values for foams into the parent MLW code

#       Aggregates each group of codes separately, removes original values from data and concatenates
#       new values. Returns a new data frame.

#       Args:
#         self.foams: dict: the labels and codes to be aggregated.

#       Returns:
#         A new dataframe

#       """
#     accounted = [v for k, v in self.foams.items()]
#     accounted = [item for a_list in accounted for item in a_list]
#     remove_foam = self.data[~self.data.code.isin(accounted)].copy()
#     foam = [v for k, v in self.code_maps.items()]
#     newdf = pd.concat([remove_foam, *foam])
#     # print("agg foams complet")
#     return newdf

#   def add_exp_group_pop_locdate(self):
#     anewdf = self.agg_foams()
#     anewdf["groupname"] = "groupname"
#     for beach in anewdf.location.unique():
#       for variable in self.exp_variables:
#         anewdf.loc[anewdf.location == beach, variable] = self.beaches.loc[beach][variable]
#     anewdf["string_date"] = anewdf.date.dt.strftime("%Y-%m-%d")
#     anewdf["loc_date"] = list(zip(anewdf.location, anewdf.string_date))
#     # this_df = self.assign_regional_labels_to_data(anewdf)

#     # print("added exp vs")
#     return anewdf

#   def make_code_groups(self):
#     these_groups = {k: json_file_get(F"resources/codegroups/{v}") for k, v in self.group_names_locations.items()}
#     accounted = [v for k, v in these_groups.items()]
#     accounted = [item for a_list in accounted for item in a_list]
#     the_rest = [x for x in self.codes_in_use if x not in accounted]
#     these_groups.update({"not classified": the_rest})
#     # print("made code groups")
#     return these_groups

#   def make_group_map(self, a_dict_of_lists):
#     wiw = {}
#     for group in a_dict_of_lists:
#       keys = a_dict_of_lists[group]
#       a_dict = {x: group for x in keys}
#       wiw.update(**a_dict)
#     # print("making group map")
#     return wiw

#   def assign_code_groups_to_results(self, data, code_group_map):
#     data = data.copy()
#     for code in data.code.unique():
#       # print(code)
#       data.loc[data.code == code, "groupname"] = code_group_map[code]
#     # print("assigned results to code groups")
#     return data

#   def tag_regional_label(self, x, beaches):
#     try:
#       a_label = beaches[x]
#     except:
#       a_label = "no data"
#     return a_label

  # def assign_regional_labels_to_data(self, data):
  #   data = data.copy()
  #   for k, v in self.river_bassins.items():
  #     data.loc[data.water_name_slug.isin(v), "river_bassin"] = k
  #   for beach in self.locations_in_use:
  #     data.loc[data.location == beach, "city"] = self.beaches.loc[beach].city
  #
  #   # print("assigned regional labels")
  #   return data

#   def survey_total_pcsm_q(self):
#     anewdf = self.survey_data.groupby(["loc_date", "location", "water_name_slug", "river_bassin", "date"], as_index=False).agg({"pcs_m": "sum", "quantity": "sum"})
#     anewdf["string_date"] = anewdf.date.dt.strftime("%Y-%m-%d")
#     anewdf["loc_date"] = list(zip(anewdf.location, anewdf.string_date))

#     return anewdf


# def get_feature_component(data, feature_level, feature_component):
#   return data.loc[data[feature_level] == levels[feature_component]].copy()


# def aggregate_a_group_of_codes(data, codes=[], groupby_column="", agg_columns={}):
#   return data[data.code.isin(codes)].groupby(groupby_column, as_index=False).agg(agg_columns)


# def replace_a_group_of_codes_with_one(data, new_code_values=[], codes_to_replace=[]):
#   som_data = data[~data.code.isin(codes_to_replace)].copy()
#   new_data = pd.concat(new_code_values, ignore_index=True)
#   return_data = pd.concat([som_data, new_data], ignore_index=True)

#   return return_data


# def agg_a_group_of_codes_with_one_code(data, new_values, a_list_loc_dates=[], a_model_code=" ", a_new_code=""):
#   # aggregate and assign a new code for the values:
#   new_df_rows = []
#   new_vals = new_values.set_index("loc_date", drop=True)
#   for adate in a_list_loc_dates:
#     gx = data.loc[(data.loc_date == adate) & (data.code == a_model_code)].copy()
#     gx["code"] = a_new_code
#     gx["quantity"] = new_vals.loc[[adate], "quantity"][0]
#     gx["pcs_m"] = new_vals.loc[[adate], "pcs_m"][0]
#     new_df_rows.append(gx)

#   # create a data frame with the new values
#   new_data = pd.concat(new_df_rows)

#   return new_data, new_df_rows


# def create_aggregate_groups(data, codes_to_agg=[], a_model_code="G79", a_new_code="Gfrags"):
#   agretd = aggregate_a_group_of_codes(data, codes=codes_to_agg, groupby_column="loc_date",
#                                       agg_columns={"quantity": "sum", "pcs_m": "sum"})
#   loc_dates = agretd.loc_date.unique()
#   df, _ = agg_a_group_of_codes_with_one_code(data, agretd, a_list_loc_dates=loc_dates, a_model_code=a_model_code,
#                                              a_new_code=a_new_code)

#   return df


# new column names for display
# plain english for export and presentations
# new_cols = {
#   "total_time": "time to survey",
#   "length": "meters surveyed",
#   "area": "m² surveyed",
#   "total_w": "total weight",
#   "mac_plast_w": "plastic > 5mm weight",
#   "mic_plas_w": "plastic < 5mm weight",
#   "num_parts_staff": "staff",
#   "num_parts_other": "help",
#   "participants": "groups",
#   "loc_date": "# samples"
# }

# # columns to aggregate dimensional data
# # common columns used to present the data
# agg_this = {
#   "meters surveyed": "sum",
#   "m² surveyed": "sum",
#   "total weight": "sum",
#   "plastic > 5mm weight": "sum",
#   "plastic < 5mm weight": "sum",
#   "staff": "sum",
#   "help": "sum",
#   "# samples": "nunique"
# }



# def add_a_new_code(a_name, a_model, a_dict_params, code_df):
#     for param in a_dict_params:
#     `a_model[param] = a_dict_params[param]

#   code_df.loc[a_name] = a_model

#   return code_df



