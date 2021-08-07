import os
import pandas as pd
from resources.utility_functions import json_file_get
from matplotlib import colors


# def m_ap_code_to_description(data, key, func):
#   """Creates an 'item' column in a data frame. Uses specified key and method
#   to assign value to 'item'.
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
#   new_data['item'] = new_data.index.map(lambda x: func(x, key))
#   new_data.set_index('item', inplace=True)
#   return new_data


def get_the_file_extension(x):
  """Splits a string by the '.' , returns everything after the '.'"""
  split = x.split('.')[-1]
  return split


def add_a_grouping_column(x, a_dict, column_to_match="", new_column_name='river_bassin'):
  """Adds a new column to a dataframe. Matches values in column_to_match to values in a_dict

  Args:
    x: dataframe
    a_dict: dict k=desired value, v=list of membership
    column_to_match: str: column name
    new_column_name:str
  Returns:
    The original data frame with a new column
  """
  for k, v in a_dict.items():
    x.loc[x[column_to_match].isin(v), new_column_name] = k
  return x


def fo_rmat_date_column(x, a_format="%Y-%m-%d"):
  """Takes in a data frame and converts the date column to timestamp."""
  x['date'] = pd.to_datetime(x['date'], format=a_format)
  return x.copy()


def slic_eby_date(x, start_date, end_date):
  """ slices a data frame by the start and end date inclusive"""
  return x[(x.date >= start_date) & (x.date <= end_date)].copy()


def fo_rmat_and_slice_date(x, a_format="", start_date="", end_date=""):
  """Formats a date column in a dataframe and slices the data frame"""
  new_df = fo_rmat_date_column(x, a_format=a_format)
  new_df = slic_eby_date(new_df, start_date, end_date)
  return new_df


class SurveyData:
  """preprocesses data"""

  def __init__(self, data, beaches, these_cols=['loc_date', 'location', 'water_name_slug', 'river_bassin', 'date'],
               foams={'G82': ['G82', 'G912'], 'G81': ['G81', 'G911'], 'G74': ['G74', 'G910', 'G909']}, **kwargs):
    self.data = data
    self.these_cols = these_cols
    self.foams = foams
    self.beaches = beaches
    self.levels = kwargs['levels']
    self.exp_variables = kwargs['exp_variables']
    self.locations_in_use = data.location.unique()
    self.river_bassins = kwargs['river_bassins']
    self.code_maps = self.make_code_maps(self.data, self.these_cols, self.foams)
    self.codes_in_use = data.code.unique()
    self.group_names_locations = kwargs['code_group_data']
    self.code_groups = self.make_code_groups()
    self.code_group_map = self.make_group_map(self.code_groups)
    self.processed = self.add_exp_group_pop_locdate()
    self.survey_data = self.assign_code_groups_to_results(self.processed, self.code_group_map)
    self.daily_totals_all = self.survey_total_pcsm_q()
    self.median_daily_total = self.daily_totals_all.pcs_m.median()
    self.code_totals = self.survey_data.groupby('code').quantity.sum()
    self.code_pcsm_med = self.survey_data.groupby('code').pcs_m.median()

  def make_code_maps(self, data, these_cols, these_codes):
    """Returns a dictionary of the aggregated values of these_codes, grouped by these_cols.

      Args:
        data: dataframe
        these_cols: array: the columns to aggregate by
        these_codes: dict: keys=labels, values:list
      Returns:
        A dict of dataframes. Example based on the default value for foams:

        {"G82":dataframe of aggregated values, "G81":data frame of aggregated values}

      """
    wiw = {}
    for code in these_codes:
      a_map = data[data.code.isin(these_codes[code])].groupby(these_cols, as_index=False).agg(
        {'pcs_m': 'sum', 'quantity': 'sum'})
      a_map['code'] = code
      wiw.update({code: a_map})

    return wiw

  def agg_foams(self):
    """Combines the different code values for foams into the parent MLW code

      Aggregates each group of codes separately, removes original values from data and concatenates
      new values. Returns a new data frame.

      Args:
        self.foams: dict: the labels and codes to be aggregated.

      Returns:
        A new dataframe

      """
    accounted = [v for k, v in self.foams.items()]
    accounted = [item for a_list in accounted for item in a_list]
    remove_foam = self.data[~self.data.code.isin(accounted)].copy()
    foam = [v for k, v in self.code_maps.items()]
    newdf = pd.concat([remove_foam, *foam])
    # print("agg foams complet")
    return newdf

  def add_exp_group_pop_locdate(self):
    anewdf = self.agg_foams()
    anewdf['groupname'] = 'groupname'
    for beach in anewdf.location.unique():
      for variable in self.exp_variables:
        anewdf.loc[anewdf.location == beach, variable] = self.beaches.loc[beach][variable]
    anewdf['string_date'] = anewdf.date.dt.strftime('%Y-%m-%d')
    anewdf['loc_date'] = list(zip(anewdf.location, anewdf.string_date))
    # this_df = self.assign_regional_labels_to_data(anewdf)

    # print("added exp vs")
    return anewdf

  def make_code_groups(self):
    these_groups = {k: json_file_get(F"resources/codegroups/{v}") for k, v in self.group_names_locations.items()}
    accounted = [v for k, v in these_groups.items()]
    accounted = [item for a_list in accounted for item in a_list]
    the_rest = [x for x in self.codes_in_use if x not in accounted]
    these_groups.update({'not classified': the_rest})
    # print('made code groups')
    return these_groups

  def make_group_map(self, a_dict_of_lists):
    wiw = {}
    for group in a_dict_of_lists:
      keys = a_dict_of_lists[group]
      a_dict = {x: group for x in keys}
      wiw.update(**a_dict)
    # print('making group map')
    return wiw

  def assign_code_groups_to_results(self, data, code_group_map):
    data = data.copy()
    for code in data.code.unique():
      # print(code)
      data.loc[data.code == code, 'groupname'] = code_group_map[code]
    # print('assigned results to code groups')
    return data

  def tag_regional_label(self, x, beaches):
    try:
      a_label = beaches[x]
    except:
      a_label = "no data"
    return a_label

  # def assign_regional_labels_to_data(self, data):
  #   data = data.copy()
  #   for k, v in self.river_bassins.items():
  #     data.loc[data.water_name_slug.isin(v), 'river_bassin'] = k
  #   for beach in self.locations_in_use:
  #     data.loc[data.location == beach, 'city'] = self.beaches.loc[beach].city
  #
  #   # print('assigned regional labels')
  #   return data

  def survey_total_pcsm_q(self):
    anewdf = self.survey_data.groupby(['loc_date', 'location', 'water_name_slug', 'river_bassin', 'date'], as_index=False).agg({'pcs_m': 'sum', 'quantity': 'sum'})
    anewdf['string_date'] = anewdf.date.dt.strftime('%Y-%m-%d')
    anewdf['loc_date'] = list(zip(anewdf.location, anewdf.string_date))

    return anewdf


# def get_feature_component(data, feature_level, feature_component):
#   return data.loc[data[feature_level] == levels[feature_component]].copy()


def aggregate_a_group_of_codes(data, codes=[], groupby_column="", agg_columns={}):
  return data[data.code.isin(codes)].groupby(groupby_column, as_index=False).agg(agg_columns)


def replace_a_group_of_codes_with_one(data, new_code_values=[], codes_to_replace=[]):
  som_data = data[~data.code.isin(codes_to_replace)].copy()
  new_data = pd.concat(new_code_values, ignore_index=True)
  return_data = pd.concat([som_data, new_data], ignore_index=True)

  return return_data


def agg_a_group_of_codes_with_one_code(data, new_values, a_list_loc_dates=[], a_model_code=" ", a_new_code=""):
  # aggregate and assign a new code for the values:
  new_df_rows = []
  new_vals = new_values.set_index('loc_date', drop=True)
  for adate in a_list_loc_dates:
    gx = data.loc[(data.loc_date == adate) & (data.code == a_model_code)].copy()
    gx['code'] = a_new_code
    gx['quantity'] = new_vals.loc[[adate], 'quantity'][0]
    gx['pcs_m'] = new_vals.loc[[adate], 'pcs_m'][0]
    new_df_rows.append(gx)

  # create a data frame with the new values
  new_data = pd.concat(new_df_rows)

  return new_data, new_df_rows


def create_aggregate_groups(data, codes_to_agg=[], a_model_code="G79", a_new_code="Gfrags"):
  agretd = aggregate_a_group_of_codes(data, codes=codes_to_agg, groupby_column='loc_date',
                                      agg_columns={'quantity': 'sum', 'pcs_m': 'sum'})
  loc_dates = agretd.loc_date.unique()
  df, _ = agg_a_group_of_codes_with_one_code(data, agretd, a_list_loc_dates=loc_dates, a_model_code=a_model_code,
                                             a_new_code=a_new_code)

  return df


# new column names for display
# plain english for export and presentations
new_cols = {
  'total_time': 'time to survey',
  'length': 'meters surveyed',
  'area': 'm² surveyed',
  'total_w': 'total weight',
  'mac_plast_w': 'plastic > 5mm weight',
  'mic_plas_w': 'plastic < 5mm weight',
  'num_parts_staff': 'staff',
  'num_parts_other': 'help',
  'participants': 'groups',
  'loc_date': '# samples'
}

# columns to aggregate dimensional data
# common columns used to present the data
agg_this = {
  'meters surveyed': 'sum',
  'm² surveyed': 'sum',
  'total weight': 'sum',
  'plastic > 5mm weight': 'sum',
  'plastic < 5mm weight': 'sum',
  'staff': 'sum',
  'help': 'sum',
  '# samples': 'nunique'
}


def make_a_summary_table(ax, data, cols_to_use, a_color='dodgerblue', font_size=12, s_et_bottom_row=True):
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
  top_row = [(0, i) for i, x in enumerate(cols_to_use)]
  bottom_row = [(len(data), i) for i, x in enumerate(cols_to_use)]
  top_columns = top_row[1:]
  data_rows = [x for x in list(the_cells.keys()) if x not in top_row]
  odd_rows = [x for x in data_rows if x[0] % 2 > 0]
  first_column = [x for x in data_rows if x[1] == 0]

  # make the first cell a littel smaller than the others
  ax[0, 0].set_height(1 / (len(data)))
  ax[0, 0].set_text_props(**{'va': 'top'})

  for a_cell in top_row:
    ax[a_cell].visible_edges = 'B'
    ax[a_cell].set_text_props(**{'fontsize': font_size})
    ax[a_cell].set_edgecolor('white')
    ax[a_cell].PAD = .2

  for a_cell in top_columns:
    ax[a_cell].set_height((1.25 / (len(data))))
    ax[a_cell].set_text_props(**{'va': 'center'})

    ax[a_cell].set_edgecolor(line_color)
    ax[a_cell].visible_edges = 'T'

  for a_cell in odd_rows:
    ax[a_cell].set_facecolor(banded_color)

  for a_cell in data_rows:
    ax[a_cell].set_height(.75 / (len(data)))
    ax[a_cell].visible_edges = 'BTLR'
    ax[a_cell].set_text_props(**{'fontsize': font_size})
    ax[a_cell].set_edgecolor('white')
    ax[a_cell]._text.set_horizontalalignment('center')

  for a_cell in first_column:
    ax[a_cell]._text.set_horizontalalignment('right')
    ax[a_cell].PAD = .02

  if s_et_bottom_row is True:
    for a_cell in bottom_row:
      ax[a_cell].visible_edges = 'B'
      ax[a_cell].set_edgecolor(line_color)

  return ax


def add_a_new_code(a_name, a_model, a_dict_params, code_df):
  for param in a_dict_params:
    a_model[param] = a_dict_params[param]

  code_df.loc[a_name] = a_model

  return code_df


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
