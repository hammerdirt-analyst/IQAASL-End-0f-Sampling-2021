# defining the feature data object
import pandas as pd
fd_var = {
    "start": "2020-03-01",
    "end": "2021-05-31",
    "unit_label": "p/100m",
    "a_fail_rate": 50
}

# set the different aggregation levels
# the aggregation level of interest is defined by level
# component are units of level
# top is all the data
# loi is the named feature(s) to be considered
# basin is the river bassin that the feature(s) are in
# top and bassin_label are used for charting

loc_var = {
    "wn_slug": "zurichsee",
    "name": "Zurichsee",
    "component": "city",
    "basin_slug": "linth",
    "basin_label": "Linth/Limmat survey area",
    "loi": ["zurichsee"],
    "top": "All survey areas",
    "level": "water_name_slug"
}

data_source = {
  "beachsource": "resources/beaches_with_land_use_rates.csv",
  "codesource": "resources/codes_with_group_names_2015.csv",
  "dimsource": "resources/corrected_dims.csv",
  "notaggsource": "resources/checked_before_agg_sdata_eos_2020_21.csv",
  "adatasource": "resources/checked_sdata_eos_2020_21.csv"
}

column_rename = {
    "% to agg": "% ag",
    "% to recreation": "% recreation",
    "% to woods": "% woods",
    "% to buildings": "% buildings"
}

def add_attributes(self, attributes):
    for k, v in attributes.items():
        setattr(self,key,value)


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


class FeatureData:
    def __init__(self, name: str = "Name on the title", level: str = "The aggregation level", component: str = "the smallest unit") -> None:
            self.name = name
            self.level = level
            self.component = component

    # use this method to add fd all the other variable attributes
    def add_attributes(self, attributes):
      for k, v in attributes.items():
        setattr(self, k, v)
    # the value of class attributes
    def inst_attributes(self):
        data = []
        for a,v in self.__dict__.items():
            data.append((a,v))
        return data





