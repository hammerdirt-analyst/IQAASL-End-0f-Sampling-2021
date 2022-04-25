import json
import pandas as pd
from scipy import stats
from matplotlib import colors
import seaborn as sns
import numpy as np
from IPython.display import display
from PIL import Image as PILImage
import locale



luse_exp = ["% to buildings", "% to recreation", "% to agg", "% to woods", "streets km", "intersects"]
# luse_ge = ["% zu Gebäude", "% zu Erholung", "% Landwirtschaft", "% zu Wald", "Strassen km", "kreuzt"]


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


def make_a_summary_table(ax, data, colLabels, a_color="saddlebrown", font_size=12):
    
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
    line_color = (*line_color[:-1], 0.3)
    banded_color = (*line_color[:-1], 0.08)

    # the different areas of formatting
    top_row = [(0, i) for i in np.arange(len(colLabels))]
    data_rows = [x for x in list(the_cells.keys()) if x not in top_row]
    odd_rows = [x for x in data_rows if x[0] % 2 > 0]
    first_column = [x for x in data_rows if x[1] == 0]

    for a_cell in top_row:
        ax[a_cell].set_height((1.1 / (len(data))))
        ax[a_cell].set_text_props(**{"fontsize": 14})
        ax[a_cell].set_edgecolor(line_color)
        ax[a_cell].PAD = .2

    for a_cell in odd_rows:
        ax[a_cell].set_facecolor(banded_color)

    for a_cell in data_rows:
        ax[a_cell].set_height(.75 / (len(data)))
        ax[a_cell].set_text_props(**{"fontsize": 14})
        ax[a_cell].set_edgecolor(line_color)
        ax[a_cell]._text.set_horizontalalignment("center")
        ax[a_cell].PAD = .1

    for a_cell in first_column:
        ax[a_cell]._text.set_horizontalalignment("right")
        ax[a_cell].PAD = .05


    return ax

def make_a_table(ax, data, colLabels=[], a_color="saddlebrown", colWidths=[.22, *[.13]*6], bbox=[0, 0, 1, 1],  **kwargs):
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

    a = ax.table(data,  colLabels=colLabels, colWidths=colWidths, bbox=bbox,  edges="closed")
    b = make_a_summary_table(a,data ,colLabels, a_color)
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
    and assigns the municipality to each record.
    
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
        new_data = {"count":"Anzahl Proben",
                "mean":f"Durchschnitt {unit_label}",
                "std":"Standardfehler", 
                "min":f"min {unit_label}",
                "max": f"max {unit_label}",
                "25%":"25%",
                "50%":"50%", 
                "75%":"75%",
                "total objects":"Abfallobjekte total",
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

def make_string_format(data, label="quantity", aformat="{:,}",
                       use_local=True):
    """Make string formats of values of a column in a dataframe. Returns the
    data frame
    """

    if use_local:
        data[label] = data[label].map(lambda x: f"{locale.format_string('%d', x, grouping=True)}")
    else:
        data[label] = data[label].map(lambda x: aformat.format(x))
    
    return data

def fmt_combined_summary(data, nf=[-1], fmt="{:,}", use_locale=True):
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

    if use_locale:
        new_data = [(x,  f"{locale.format_string('%d', data[x], grouping=True)}") for x in data.index[:]]
    
    elif len(nf):
        new_data = [(x, fmt.format(int(data[x]))) for x in data.index[:-1]]
        new_data.append((data.index[-1], int(data[-1])))
        
    else:
        new_data = [(x, fmt.format(int(data[x]))) for x in data.index]
    
    return new_data

def aggregate_to_group_name(data, unit_label="p/100m", column="groupname", name="afeaturename", val="pt"):
    """Convenience function, takes in a data frame and returns the aggregated values specified by <val> of <column> in
     a series labeled <name>.

    :param data: A pandas dataframe
    :type data: pd.core.frame.dataframe
    :param unit_label: The label for values that get a median
    :type unit_label: str,
    :param column: The label of the aggregation level
    :type column: str,
    :param name: The name of the new feature
    :type name: str,
    :param val: What type of operation is requested
    :type val: str,
    :return: Returns the aggregated value in series labeled <name>
    """

    try:
      if val == "pt":
          new_data = data.groupby(column, as_index=False).quantity.sum()
          new_data.set_index(column, inplace=True)
          new_data[name] = (new_data.quantity/new_data.quantity.sum()).round(2)
          data = new_data[name]
      else:
        if val == "med":
          new_data = data.groupby(["loc_date",column], as_index=False)[unit_label].sum()
          f_s_a = new_data.groupby(column, as_index=False)[unit_label].median()
          f_s_a.set_index(column, inplace=True)
          f_s_a[name] = f_s_a[unit_label]
          data = f_s_a[name]

    except:
      print("val is not defined as pt or med")
      data = ["an empty list"]

        
    
    return data

def aggregate_to_code(data, code_description_map, column="code", name="afeaturename", unit_label="p/100m"):



    f_s_a = data.groupby(column, as_index=False)[unit_label].median()

    try:
        f_s_a["item"] = f_s_a.code.map(lambda x: code_description_map.loc[x])
    except:
        f_s_a["item"] = f_s_a.code.map(lambda x: code_description_map[x])

    f_s_a.set_index("item", inplace=True)
    f_s_a[name] = f_s_a[unit_label]
    
    return f_s_a[name]

# german translations
luse_ge = {"% to buildings": "% zu Gebäuden",
           "% to recreation": "% zu Erholung",
           "% to agg": "% zu LWS",
           "% to woods": "% zu Wald",
           "streets km": "Strassen km",
           "intersects": "Flussmündung"
           }

mat_ge = {"Metal":"Metall", 
          "Chemicals":"Chemikalien",
          "Paper":"Papier",
          "Glass":"Glas",
          "Rubber":"Gummi",
          "Wood":"Holz",
          "Cloth":"Stoff",
          "Unidentified":"Unbekannt",
          "Undefined":"Unbestimmt",
          "Plastic":"Plastik"
         }

group_names_de =  {"waste water":"Abwasser",
                   "micro plastics (< 5mm)":"Mikroplastik (< 5mm)",
                   "infrastructure":"Infrastruktur",
                   "food and drink":"Essen und Trinken",
                   "agriculture":"Landwirtschaft",
                   "tobacco":"Tabakwaren",
                   "recreation":"Freizeit und Erholung",
                   "packaging non food":"Nicht-Lebensmittelverpackungen",
                   "plastic pieces":"Plastikfragmente",
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
      im.thumbnail(thumb)
      im.rotate(rotate)



    display(im)


def get_rid_of_ix(data, prefix=""):
  """Compares the components of <prefix> to the first n components
  of <data>, n=len(<prefix>). If there is a match <new_data> is
  returned minus the components of <prefix>.

  :param data: The object that may need to be trimmed
  :type data: array or str,
  :param prefix: The components to be removed
  :type prefix:  array or str
  :return: an array or str
  """
  test = len(prefix)

  if data[:test] == prefix[0:]:
    new_data = data[test:]
  else:
    new_data = data

  return new_data






