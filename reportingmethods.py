"""
reportingmethods.py
-------------------
This is the collection of methods used to generate the IQAASL report. Originally their was a notebook per chapter much
of the code was duplicated. This is the refactored code that was used to automate reporting for future projects.

"""


import re
import unicodedata
import pandas as pd
import numpy as np
from pydantic import BaseModel, Field
from typing import List,Optional
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from prompts import  land_use_description, land_use_rates_description

# The following are the default values for the report
report_quantiles = [.05, .25, .5, .75, .95]
bin_labels = [1, 2, 3, 4, 5]

quantile_labels = ['5th', '25th', '50th', '75th', '95th']
object_of_interest = 'code'
location_label = 'location'
feature_variables = ['buildings', 'forest', 'public-services', 'recreation', 'undefined', 'streets']
info_columns = ['canton', 'city', 'feature_name', 'feature_type']

# indentify target variable and type
Y = 'pcs/m'
Q = 'quantity'

# distribution point estimate
tendencies = 'mean'
# these are the columns and methods used to aggregate the data at the sample level
# the sample level is the lowest level of aggregation. The sample level is the collection of all
# the records that share the same sample_id or loc_date. The loc_date is the unique identifier for each survey.
unit_agg = {
    Q: "sum",
    Y: "sum"
}

# Once the data is aggregated at the sample level, it is aggregated at the feature level. The pcs/m or pcs_m
# column can no longer be summed. We can only talk about the median, average or distribution of the pcs/m for the
# samples contained in each feature. The quantity column can still be summed. The median is used for reporting
# purposes. The median is less sensitive to outliers than the average. The median is also more intuitive than the
# average.
agg_groups = {
    Q: "sum",
    Y: tendencies
}

# css formatting for tables
format_kwargs = dict(precision=2, thousands="'", decimal=",")

header_row = {'selector':'th', 'props': 'background-color: #FFF; font-size:14px; text-align:left; width: auto; word-break: keep-all;'}
even_rows = {"selector": 'tr:nth-child(even)', 'props': 'background-color: rgba(139, 69, 19, 0.08);'}
odd_rows = {'selector': 'tr:nth-child(odd)', 'props': 'background: #FFF;'}
table_font = {'selector': 'tr', 'props': 'font-size: 12px;'}
table_data = {'selector': 'td', 'props': 'padding:4px; font-size:12px;text-align: center;'}
table_caption_top = {'selector': 'caption', 'props': 'caption-side: top; font-size:1em; text-align: left; margin-bottom: 10px;'}
table_border = {'selector': 'table, th, tr, td', 'props': 'border: 1px solid black; border-collapse: collapse;'}

table_css_styles = [even_rows, odd_rows, table_font, header_row, table_data, table_border, table_caption_top]

class ReportMeta(BaseModel):
    """
    The `ReportMeta` class contains the metadata needed to create a baseline report for a subset of data.

    Each report has an associated `ReportMeta` instance that defines the parameters for filtering and generating the report.
    The ReportMeta object can be .JSON object originally or a dictionary. The ReportMeta object is generated in the application
    through the parameter selection form.

    Attributes:
        start (Optional[str]): The start of the requested date range, string date in format YYYY-mm, e.g., 2020-01.
        end (Optional[str]): The end of the requested date range, string date in format YYYY-mm, e.g., 2020-01.
        name (Optional[str]): The name of the directory where the report components will be stored.
        report_codes (Optional[List[str]]): The objects of interest in OSPAR or JRC code, list of strings, e.g., ["G1", "G2"].
        code_types (Optional[List[str]]): The use category of the objects, e.g., personal-hygiene, construction.
        columns_of_interest (Optional[List[str]]): The feature columns for analysis, list of strings, e.g., ["column", "names"].
        info_columns (Optional[List[str]]): The possible subsets in a report, list of strings, e.g., ["column", "names"].
        feature_name (Optional[str]): The name of the lake or river if the report is about a lake or river.
        feature_type (Optional[str]): Designates the report as either river, lake, or both.
        boundary (Optional[str]): If the report is limited by administrative boundaries: canton, city, or survey area.
        boundary_name (Optional[str]): The name of the canton, city, or survey area.
        title_notes (Optional[str]): String for title notes.
        code_group_category (Optional[str]): The family descriptive name of the objects under consideration.
        roughdraft_name (Optional[str]): String for rough draft name.
        report_subtitle (str): String for report subtitle.
        author (str): The author of the report.
        local_directory (Optional[str]): The parent directory of the reports.

    Methods:
        file_name: Defines the local directory for report components.
        report_title: Builds the rough draft title from meta-data attributes.
        get: Retrieve the value of an attribute by name.
    """

    start: Optional[str] = Field(None,
                                 description="The start of the requested date range, string date in format YYYY-mm, e.g., 2020-01")
    end: Optional[str] = Field(None,
                               description="The end of the requested date range, string date in format YYYY-mm, e.g., 2020-01")
    name: Optional[str] = Field(None,
                                description="The name of the directory where the report components will be stored")
    report_codes: Optional[List[str]] = Field(None,
                                              description='The obects of interest in OSPAR or JRC code, list of strings, e.g., ["G1", "G2"]')
    code_types: Optional[List[str]] = Field(None,
                                            description='The use category of the objects ie. personal-hygiene, construction, list of strings, e.g., ["personal", "profesional"]')
    columns_of_interest: Optional[List[str]] = Field(None,
                                                     description='The feature columns for analysis list of strings, e.g., ["column", "names"]')
    info_columns: Optional[List[str]] = Field(None,
                                              description='The possible subsets in a report, list of strings, e.g., ["column", "names"]')
    feature_name: Optional[str] = Field(None,
                                        description="If the report is about a lake or river this is the name of the lake or river")
    feature_type: Optional[str] = Field(None, description="Designates the report as either river, lake or both")
    boundary: Optional[str] = Field(None,
                                    description="If the report is limited by adminstinstrative boundaries: canton, city or survey area")
    boundary_name: Optional[str] = Field(None, description="The name of the canton, city or survey area")
    title_notes: Optional[str] = Field('This is the default value of titles notes',
                                       description="String for title notes")
    code_group_category: Optional[str] = Field(None,
                                               description="The family descriptive name of the objects under consideration")
    roughdraft_name: Optional[str] = Field('rough_draft.md', description="String for rough draft name")
    report_subtitle: str = Field(
        "This is the roughdraft report of the observations of trash density along rivers and lakes",
        description="String for report subtitle")
    author: str = "AI reporter from hammerdirt"
    local_directory: str = Field(None, description="The parent directory of the reports")

    @property
    def file_name(self) -> Optional[str]:
        """Defines the local directory for report components"""

        if self.name and self.code_group_category and self.local_directory:
            the_directory = clean_string(self.name + self.code_group_category)
            the_location = f'{self.local_directory}/{the_directory}/'
            return the_location
        else:
            return None

    @property
    def report_title(self) -> Optional[str]:
        """Builds the rough draft title from meta-data attributes"""

        if self.name and self.boundary:
            aname = self.name.capitalize()
            return f'{aname} {self.boundary}'
        elif self.name and not self.boundary and self.feature_type:
            aname = self.name.capitalize()
            return f'{aname} {self.feature_type}'
        else:
            return None

    def get(self, attribute: str, default=None):
        """Retrieve the value of an attribute by name.

        Args:
            attribute (str): The name of the attribute to retrieve.
            default: The value to return if the attribute does not exist or is None.

        Returns:
            The value of the attribute or the default value if not found.
        """
        return getattr(self, attribute, default)

class SurveyReport:
    """
    The SurveyReport class is a container for the data and methods that are used to generate a report from a survey data set.

    The report is a summary of the data in the survey. The exact contents of the report should be defined by the stakeholders
    charged with the responsibility of interpreting the data. This has not happened in an official sense. Therefore, this report
    is the collection of methods used to describe the distribution of the target variables in relation to the distribution of the
    feature variables.

    Args:
        dfc (pd.DataFrame): The DataFrame containing the survey data.

    Methods:
        administrative_boundaries() -> list[dict]:
            Returns the name and number of unique Cantons and Cities in a report.
        feature_inventory() -> list[dict]:
            Returns the name and number of geographic boundaries in a report.
        date_range() -> dict:
            The date range of the selected results.
        inventory() -> pd.DataFrame:
            Returns the total quantity, median pcs/m, % of total and fail rate for each object code in the report.
        total_quantity() -> int:
            Returns the total quantity of the report.
        number_of_samples() -> int:
            Returns the number of unique sample_ids in the report.
        number_of_locations() -> int:
            Returns the number of unique locations in the report.
        material_report(code_material) -> list[dict]:
            Generate a report on the material composition of the samples.
        fail_rate(threshold: int = 1) -> pd.DataFrame:
            Calculate the fail rate for each object of interest.
        sample_results(df: pd.DataFrame = None, sample_id: str = None, labels: str = None, info_columns: list[str] = None, afunc: dict = None) -> pd.DataFrame:
            Calculate the sample totals by grouping the data based on sample ID, labels, and date.
        sampling_results_summary() -> list[dict]:
            Generate a summary of the sample totals.
        object_summary() -> list[dict]:
            Generate a summary of the object quantities and fail rates.
    """

    def __init__(self, dfc: pd.DataFrame):
        self.df = dfc
        self.administrative = [location_label, 'city', 'canton', 'parent_boundary']

    def administrative_boundaries(self) -> list[dict]:
        """
        Returns the name and number of unique Cantons and Cities in a report.

        This method calculates the number of unique Cantons and Cities in the survey data and returns a DataFrame
        with the counts and a dictionary with the names of the unique Cantons and Cities.

        Returns:
            list[dict]: A list containing a dictionary with a DataFrame of the count of unique Cantons and Cities,
                        and a dictionary with the names of the unique Cantons and Cities.

        Raises:
            ValueError: If the input DataFrame is empty.
        """
        if self.df.empty:
            raise ValueError("The input DataFrame is empty. Please provide a valid DataFrame.")

        result = {}
        boundary_names = {}
        for boundary in self.administrative:
            names = self.df[boundary].unique()
            boundary_names[boundary] = names
            if names.size == 0:
                result[boundary] = {'count': 0}
            else:
                result[boundary] = {'count': len(names)}
        result = pd.DataFrame(result).T

        result.loc['survey areas', 'count'] = result.loc['parent_boundary', 'count']
        result.drop('parent_boundary', inplace=True)

        boundary_names['survey_area'] = boundary_names['parent_boundary']
        boundary_names.pop('parent_boundary')
        section_label = f"**Administrative boundaries**"
        section_description = "The names of the cities, cantons and survey areas included in this report:\n\n"

        place_names = ""
        for a_label, a_list in boundary_names.items():
            if a_label != location_label:
                place_names += f"{a_label.capitalize()}: {', '.join(a_list)}\n\n"
        section_description = section_description + place_names

        return [{'dataframe': result, 'prompt': {'section_label': section_label, 'section_description': section_description}}]

    def feature_inventory(self) -> list[dict]:
        """
        Returns the name and number of geographic boundaries in a report.

        This method calculates the number of unique geographic boundaries (e.g., river basins, lakes, parks) in the survey data
        and returns a DataFrame with the counts and a dictionary with the names of the unique features.

        Returns:
            list[dict]: A list containing a dictionary with a DataFrame of the count of unique geographic boundaries,
                        and a dictionary with the prompt labels and descriptions in markdown.
        """
        if self.df.empty:
            raise ValueError("The input DataFrame is empty. Please provide a valid DataFrame.")

        result = {}
        feature_names = {}
        feature_type_labels = {'l': 'lake', 'r': 'river', 'p': 'park'}
        for feature_type in self.df.feature_type.unique():
            unique_features = self.df[self.df['feature_type'] == feature_type]['feature_name'].unique()
            ftype_label = feature_type_labels[feature_type]
            feature_names[ftype_label] = unique_features
            if unique_features.size > 0:
                result[feature_type] = {'count': len(unique_features)}
        result = pd.DataFrame(result)
        result.rename(columns={'l': 'lake', 'r': 'river', 'p': 'park'}, inplace=True)

        section_label = "**The named features in this report**"
        section_description = "The lakes, rivers or parks included in this report\n\n"

        place_names = ""
        for a_label, a_list in feature_names.items():
            if a_label != location_label:
                place_names += f"**{a_label.capitalize()}:** {', '.join(a_list)}\n\n"
        section_description = section_description + place_names.title()
        return [{'dataframe': result,
                 'prompt': {'section_label': section_label, 'section_description': section_description}}]

    @property
    def date_range(self) -> dict:
        """
        The date range of the selected results.

        Returns:
            dict: A dictionary with the start and end dates of the selected results.
        """
        start = self.df['date'].min()
        end = self.df['date'].max()
        return {'start': start, 'end': end}

    def inventory(self) -> pd.DataFrame:
        """
        Returns the total quantity, median pcs/m, % of total and fail rate for each object code in the report.

        Returns:
            pd.DataFrame: A DataFrame containing the total quantity, median pcs/m, % of total and fail rate for each object code.
        """
        tq = self.total_quantity
        object_totals = self.df.groupby([object_of_interest, 'en'], as_index=False).agg(agg_groups)
        object_totals['% of total'] = object_totals[Q] / tq
        object_totals.rename(columns={'en': 'object'}, inplace=True)

        return object_totals

    @property
    def total_quantity(self) -> int:
        """
        Returns the total quantity of the report.

        Returns:
            int: The total quantity of the report.
        """
        return self.df[Q].sum()

    @property
    def number_of_samples(self) -> int:
        """
        Returns the number of unique sample_ids in the report.

        Returns:
            int: The number of unique sample_ids in the report.
        """
        return self.df['sample_id'].nunique()

    @property
    def number_of_locations(self) -> int:
        """
        Returns the number of unique locations in the report.

        Returns:
            int: The number of unique locations in the report.
        """
        return self.df.location.nunique()

    def material_report(self, code_material) -> list[dict]:
        """
        Generate a report on the material composition of the samples.

        This method calculates the material composition of the samples in the survey data. It groups the data by material,
        calculates the total quantity for each material, and returns a DataFrame with the percentage of the total for each material.

        Args:
            code_material (pd.DataFrame): A DataFrame containing the material classification of the objects.

        Returns:
            list[dict]: A list containing a dictionary with a DataFrame of the material composition,
                        and a dictionary with the section label and description.

        Raises:
            ValueError: If the input DataFrame is empty.
        """
        if self.df.empty:
            raise ValueError("The input DataFrame is empty. Please provide a valid DataFrame.")

        inv = self.inventory()
        inv.set_index(object_of_interest, drop=True, inplace=True)
        inv = inv.merge(code_material, right_index=True, left_index=True)
        print('this is an m report\n')
        m_report = inv.groupby(['material']).quantity.sum()
        if sum(m_report) > 0:
            mr = m_report / sum(m_report)
        else:
            mr = m_report
        print('this is an mr\n')
        print(mr)
        mr = (mr * 100).astype(int)
        mr = pd.DataFrame(mr[mr >= 1])
        mr['% of total'] = mr.quantity.apply(lambda x: f'{x}%')
        mr = mr[['% of total']]
        section_label = "Material composition"
        section_description = "The proportion of each material type according to the material classification of the object\n\n"
        section_description = section_description + mr.to_markdown()

        return [{'dataframe': mr, 'prompt': {'section_label': section_label, 'section_description': section_description}}]

    def fail_rate(self, threshold: int = 1) -> pd.DataFrame:
        """
        Calculate the fail rate for each object of interest.

        This method calculates the fail rate for each object of interest in the survey data. The fail rate is defined as the
        number of samples where the quantity of the object is greater than or equal to the threshold, divided by the total
        number of samples for that object.

        Args:
            threshold (int, optional): The quantity threshold to consider a sample as a fail. Default is 1.

        Returns:
            pd.DataFrame: A DataFrame containing the fail rate for each object of interest.

        Raises:
            ValueError: If the input DataFrame is empty.
        """
        if self.df.empty:
            raise ValueError("The input DataFrame is empty. Please provide a valid DataFrame.")

        rates = self.df.groupby([object_of_interest])['sample_id'].nunique().reset_index()
        for anobject in rates[object_of_interest].unique():
            nfails = sum((self.df[object_of_interest] == anobject) & (self.df[Q] >= threshold))
            n_anobject = rates.loc[rates[object_of_interest] == anobject, 'sample_id'].values[0]
            rates.loc[rates[object_of_interest] == anobject, ['fails', 'rate']] = [nfails, nfails / n_anobject]

        return rates.set_index(object_of_interest, drop=True)

    def sample_results(self, df: pd.DataFrame = None, sample_id: str = None, labels: str = None,
                       info_columns: list[str] = None, afunc: dict = None) -> pd.DataFrame:
        """
        Calculate the sample totals by grouping the data based on sample ID, labels, and date.

        This function groups the data by sample ID, labels, and date, and applies the aggregation function to calculate
        the sample totals. If additional information columns are provided, they are included in the grouping.

        Args:
            df (pd.DataFrame, optional): The DataFrame containing the survey data. If not provided, the method uses the instance's DataFrame. Default is None.
            sample_id (str, optional): The column name representing the sample ID. Default is `index_label`.
            labels (str, optional): The column name representing the location labels. Default is `location_label`.
            info_columns (list[str], optional): Additional columns to include in the grouping. Default is None.
            afunc (dict, optional): The aggregation function to apply to the grouped data. Default is `unit_agg`.

        Returns:
            pd.DataFrame: A DataFrame containing the aggregated sample totals.

        Raises:
            ValueError: If the input DataFrame is empty.
        """
        if df is None:
            df = self.df
        if labels is None:
            labels = location_label
        if sample_id is None:
            sample_id = "sample_id"
        if afunc is None:
            afunc = unit_agg

        if df.empty:
            raise ValueError("The input DataFrame is empty. Please provide a valid DataFrame.")

        if not info_columns:
            return df.groupby([sample_id, labels, 'date'], as_index=False).agg(afunc)
        else:
            return df.groupby([sample_id, labels, 'date', *info_columns], as_index=False).agg(afunc)

    @property
    def sampling_results_summary(self) -> list[dict]:
        """
        Generate a summary of the sample totals.

        This property calculates the summary of the sample totals, including total quantity, number of samples, average,
        quantiles, standard deviation, maximum value, and date range.

        Returns:
            list[dict]: A list containing a dictionary with a DataFrame of the summary of the sample totals,
                        and a dictionary with the section label and description.

        Raises:
            ValueError: If the input DataFrame is empty.
        """
        if self.df.empty:
            raise ValueError("The input DataFrame is empty. Please provide a valid DataFrame.")

        data = self.sample_results()[Y].values
        qtiles = np.quantile(data, report_quantiles)
        q_labels = {quantile_labels[i]: qtiles[i] for i in range(len(qtiles))}

        asummary = {
            'quantity': self.total_quantity,
            'nsamples': self.number_of_samples,
            'average': np.mean(data),
            **q_labels,
            'std': np.std(data),
            'max': self.sample_results()[Y].max(),
            'start': self.date_range['start'],
            'end': self.date_range['end']
        }
        result = pd.DataFrame(asummary.values(), index=list(asummary.keys()), columns=['result'])

        section_label = "**Summary statistics**"
        section_description = ("The average pcs/m (objects per meter or trash per meter), standard deviation, "
                               "number of samples, date range, and the percentile distribution of the survey totals.\n\n")
        section_description = section_description + result.to_markdown() + '\n'

        return [{'dataframe': result,
                 'prompt': {'section_label': section_label, 'section_description': section_description}}]

    def object_summary(self) -> list[dict]:
        """
        Generate a summary of the object quantities and fail rates.

        This method calculates the total quantity and fail rate for each object of interest in the survey data. It filters
        out objects with zero quantity, sorts the objects by quantity in descending order, and merges the fail rate data.

        Returns:
            list[dict]: A list containing a dictionary with a DataFrame of the summary of object quantities and fail rates,
                        and a dictionary with the section label and description.

        Raises:
            ValueError: If the input DataFrame is empty.
        """
        if self.df.empty:
            raise ValueError("The input DataFrame is empty. Please provide a valid DataFrame.")

        qtys = self.inventory()
        qtys = qtys[qtys[Q] > 0]
        qtys = qtys.sort_values(Q, ascending=False)
        qtys.rename(columns={'sample_id': 'nsamples'}, inplace=True)
        df = qtys.merge(self.fail_rate(), right_on=object_of_interest, left_on=object_of_interest)
        df = df.rename(columns={'rate': 'fail rate'})
        df.drop(columns=['fails'], inplace=True)
        section_label = "**Inventory items**"
        section_description = "The quantity, average density, % of total and fail rate per object category\n\n"
        section_description = section_description + df.to_markdown()

        return [{'dataframe': df, 'prompt': {'section_label': section_label, 'section_description': section_description}}]

class LandUseReport:
    """
    A class to generate a report from survey data with respect to land use features.

    The `LandUseReport` class is a container for the data and methods used to generate a report from a survey data set.
    The report summarizes the data in the survey with respect to the land use features of the survey locations.

    Attributes
    ----------
    feature_variables : list of str
        A list of feature variables extracted from the features DataFrame.
    df_cont : pd.DataFrame
        A DataFrame containing the continuous data after merging the target and features DataFrames.
    df_cat : pd.DataFrame
        A DataFrame containing the categorized feature columns.

    Methods
    -------
    merge_land_use_to_survey_data()
        Merge the land use data with the survey data.
    categorize_columns(df: pd.DataFrame, feature_columns: list[str] = feature_variables) -> pd.DataFrame
        Categorize the feature columns in the DataFrame.
    n_samples_per_feature(df: pd.DataFrame = None, features: list[str] = None) -> pd.DataFrame
        Calculate the number of samples per feature.
    n_pieces_per_feature() -> pd.DataFrame
        Calculate the number of pieces per feature.
    locations_per_feature() -> pd.DataFrame
        Calculate the number of unique locations per feature.
    rate_per_feature(df: pd.DataFrame = None) -> pd.DataFrame
        Calculate the average rate per feature.
    correlation_matrix() -> pd.DataFrame
        Calculate the correlation matrix for the feature variables.
    """

    def __init__(self, df_target, features):
        self.df_cont = df_target
        self.feature_variables = features
        self.df_cat = self.categorize_columns(self.df_cont.copy())

    def categorize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Categorize the feature columns in the DataFrame.

        This method scales the 'streets' column and categorizes the specified feature columns into bins.

        Parameters
        ----------
        df : pd.DataFrame
            The DataFrame containing the feature data.

        Returns
        -------
        pd.DataFrame
            A DataFrame with the categorized feature columns.

        Raises
        ------
        ValueError
            If the input DataFrame is empty or if the feature columns are not found in the DataFrame.
        """
        return categorize_features(df, feature_columns=self.feature_variables)

    def n_samples_per_feature(self, df: pd.DataFrame = None, features: list[str] = None) -> list[dict]:
        """
        Calculate the number of samples per feature.

        This method calculates the number of samples for each specified feature in the DataFrame.

        Parameters
        ----------
        df : pd.DataFrame, optional
            The DataFrame containing the feature data. If not provided, the method uses `self.df_cat`.
        features : list of str, optional
            The list of features to calculate the number of samples for. If not provided, the method uses `session_config.feature_variables`.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing the number of samples per feature.

        Raises
        ------
        ValueError
            If the input DataFrame is empty or if the feature columns are not found in the DataFrame.
        """
        if df is None:
            df = self.df_cat.copy()
        else:
            df = df.copy()

        if features is None:
            features = self.feature_variables

        if df.empty:
            raise ValueError("Input DataFrame cannot be empty.")

        df_feature = {feature: df[feature].value_counts() for feature in features}

        df_concat = pd.concat(df_feature, axis=1)

        df_concat = df_concat.fillna(0).astype('int')

        d  = df_concat.sort_index()
        new_columns = pd.MultiIndex.from_product([["Proportion of samples collected"], d.columns])
        d.columns = new_columns
        d['proportion of buffer'] = ['0-20%', '20-40%', '40-60%', '60-80%', '80-100%']
        d.set_index('proportion of buffer', inplace=True, drop=True)
        d.replace(0, 'none', inplace=True)
        d = d.map(lambda x: f"{x * 100:.1f}%" if isinstance(x, (int, float)) else x)
        section_label = "Land use sampling stratification: proportion of buffer and proportion of samples"
        section_description = land_use_description + '\n' + d.to_markdown()

        return [{'dataframe': d, 'prompt': {'section_label': section_label, 'section_description': section_description}}]

    def n_pieces_per_feature(self) -> pd.DataFrame:
        """
        Calculate the number of pieces per feature.

        This method calculates the sum of pieces for each specified feature in the DataFrame.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing the number of pieces per feature.

        Raises
        ------
        ValueError
            If the input DataFrame is empty or if the feature columns are not found in the DataFrame.
        """
        if self.df_cat.empty:
            raise ValueError("Input DataFrame cannot be empty.")

        df_feature = {feature: self.df_cat.groupby(feature, observed=True)[Q].sum() for feature in
                      self.feature_variables}
        df_concat = pd.concat(df_feature, axis=1)


        return df_concat.fillna(0).astype('int')

    def locations_per_feature(self) -> pd.DataFrame:
        """
        Calculate the number of unique locations per feature.

        This method calculates the number of unique locations for each specified feature in the DataFrame.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing the number of unique locations per feature.

        Raises
        ------
        ValueError
            If the input DataFrame is empty or if the feature columns are not found in the DataFrame.
        """
        if self.df_cat.empty:
            raise ValueError("Input DataFrame cannot be empty.")

        df_feature = {feature: self.df_cat.groupby(feature, observed=True)[location_label].nunique() for feature in
                      self.feature_variables}
        df_concat = pd.concat(df_feature, axis=1)

        return df_concat.fillna(0).astype('int')

    def rate_per_feature(self, df: pd.DataFrame = None) -> list[dict]:
        """
        Calculate the average rate per feature.

        This method calculates the mean rate of the target variable for each category in the specified features.

        Parameters
        ----------
        df : pd.DataFrame, optional
            The DataFrame containing the feature data. If not provided, the method uses `self.df_cat`.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing the average rates per feature category.

        Raises
        ------
        ValueError
            If the input DataFrame is empty or if the feature columns are not found in the DataFrame.
        """
        if df is None:
            df = self.df_cat.copy()
        else:
            df = df.copy()

        if df.empty:
            raise ValueError("Input DataFrame cannot be empty.")

        avg_matrix = pd.DataFrame(index=feature_variables, columns=bin_labels)

        for column in self.feature_variables:
            for category in bin_labels:
                filtered = df[df[column] == category]
                avg_matrix.at[column, category] = filtered[Y].mean() if not filtered.empty else 0


        d = avg_matrix.round(2).T
        # d = d.round(2)
        new_columns = pd.MultiIndex.from_product([["Pieces of trash per meter"], d.columns])
        d.columns = new_columns
        d['proportion of buffer'] = ['0-20%', '20-40%', '40-60%', '60-80%', '80-100%']
        d.set_index('proportion of buffer', inplace=True, drop=True)
        # d = d.round(2)
        d.replace(0, 'none', inplace=True)
        section_label = "Lamd use sampling stratification: proportion of buffer and pcs/m"
        section_description = land_use_rates_description + '\n' + d.to_markdown()

        return [
            {'dataframe': d, 'prompt': {'section_label': section_label, 'section_description': section_description}}]

    def correlation_matrix(self) -> pd.DataFrame:
        """
        Calculate the correlation matrix for the feature variables.

        This method calculates the correlation matrix for the feature variables in the continuous DataFrame.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing the correlation matrix of the feature variables.

        Raises
        ------
        ValueError
            If the continuous DataFrame is empty or if the feature columns are not found in the DataFrame.
        """
        if self.df_cont.empty:
            raise ValueError("Continuous DataFrame cannot be empty.")

        missing_columns = [col for col in self.feature_variables if col not in self.df_cont.columns]
        if missing_columns:
            raise ValueError(f"Feature columns {missing_columns} not found in the DataFrame.")

        return self.df_cont[[*feature_variables, 'pcs/m']].corr()

def extract_roughdraft_text(aresult: list[dict]) -> str:
    """
    Extracts text results from a collection of dictionaries.

    This utility function iterates through a list of dictionaries, extracting the 'section_label' and 'section_description' from each dictionary's 'prompt' key. The extracted text is concatenated into a single string.

    Args:
        aresult (list[dict]): A list of dictionaries containing the text results to be extracted.

    Returns:
        str: A concatenated string of the extracted text results.
    """

    rough = ''
    for theresult in aresult:
        label = theresult['prompt']['section_label']
        description = theresult['prompt']['section_description']
        rough += label.capitalize() +'\n\n'+ description + '\n\n'
    return rough

def clean_string(text: str) -> str:
    """
    Removes accents, special characters, and spaces from a string.

    This function normalizes the input string to decompose accents, removes accents by keeping only ASCII characters,
    and removes special characters and spaces.

    Args:
        text (str): The input string to be cleaned.

    Returns:
        str: The cleaned string with accents, special characters, and spaces removed.
    """

    # normalize to decompose accents
    text = unicodedata.normalize("NFD", text)

    # remove accents by keeping only ASCII characters
    text = text.encode("ascii", "ignore").decode("utf-8")

    # remove special characters and spaces
    text = re.sub(r"[^a-zA-Z0-9]", "", text)

    return text

def categorize_features(df: pd.DataFrame, feature_columns: list[str] = None) -> pd.DataFrame:
    """
    Categorize the feature columns in the DataFrame.

    This function scales the 'streets' column and categorizes the specified feature columns into bins.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame containing the feature data.
    feature_columns : list of str, optional
        The list of feature columns to categorize. Default is `feature_variables`.

    Returns
    -------
    pd.DataFrame
        A DataFrame with the categorized feature columns.

    Raises
    ------
    ValueError
        If the input DataFrame is empty or if the feature columns are not found in the DataFrame.
    """
    if df.empty:
        raise ValueError("Input DataFrame cannot be empty.")

    bins = [-1, 0.2, 0.4, 0.6, 0.8, 1]
    #bin_labels = [1, 2, 3, 4, 5]

    scaler = MinMaxScaler()

    if 'streets' not in df.columns:
        raise ValueError("'streets' column not found in the DataFrame.")

    df['streets'] = scaler.fit_transform(df[['streets']])

    for column in feature_columns:
        if column not in df.columns:
            raise ValueError(f"Feature column '{column}' not found in the DataFrame.")
        df[column] = pd.cut(df[column], bins=bins, labels=bin_labels)

    return df

def survey_totals_boundary(survey_report: SurveyReport, info_columns: list) -> dict:
    """
    Generates a summary of sample results grouped by specified information columns.

    This function groups the survey data by the specified information columns, calculates the total quantity and pcs/m for each group, and sorts the results in descending order of pcs/m. It also capitalizes string columns and generates a section label and description for the report.

    Args:
        survey_report (SurveyReport): An instance of `SurveyReport` containing the survey data.
        info_columns (list): A list of column names to group the data by.

    Returns:
        dict: A dictionary containing the DataFrame of grouped sample results and a dictionary with the section label and description.
    """
    d = survey_report.sample_results(info_columns=info_columns)
    dt = d.groupby(info_columns, as_index=False).agg(agg_groups)
    dt = dt.sort_values(Y, ascending=False)
    string_columns = dt.select_dtypes(include='object').columns

    # Apply str.capitalize to all string columns
    dt[string_columns] = dt[string_columns].apply(lambda col: col.str.capitalize())
    the_theme = info_columns[0]
    if the_theme == 'parent_boundary':
        the_theme = 'survey area'
    section_label = f"**Sample results by {the_theme}**"
    section_description = f"The average sample total in pcs/m\n\n"
    section_description = section_description + dt.to_markdown()

    return {'dataframe': d, 'prompt': {'section_label': section_label, 'section_description': section_description}}

def survey_totals_for_all_info_cols(report_meta: ReportMeta, survey_report: SurveyReport) -> list[dict]:
    """
    Generates a summary of sample results for all specified information columns.

    This function iterates through the information columns specified in the `ReportMeta` object, groups the survey data by each column, calculates the total quantity and pcs/m for each group, and generates a section label and description for the report.

    Args:
        report_meta (ReportMeta): An instance of `ReportMeta` containing the metadata for filtering and generating the report.
        survey_report (SurveyReport): An instance of `SurveyReport` containing the survey data.

    Returns:
        list[dict]: A list of dictionaries, each containing a DataFrame of grouped sample results and a dictionary with the section label and description.
    """
    if 'boundary' in report_meta:
        these_cols = [x for x in report_meta.info_columns if x != report_meta['boundary']]
    else:
        these_cols = report_meta.info_columns

    results = []
    for col in these_cols:
        results.append(survey_totals_boundary(survey_report, [col]))

    return results

def translate_state_to_meta(state: dict, code_groups: pd.DataFrame, location: str, boundary: str = None) -> ReportMeta:
    """
    Converts the form state into a ReportMeta object. The ReportMeta object is used to filter the data and generate reports.

    Parameters
    ----------
    state : dict
        A dictionary containing the form state with keys such as 'start_date', 'end_date', 'feature_type', and 'codes'.
    code_groups : pd.DataFrame
        A DataFrame containing code group information.
    location : str
        The location name.
    boundary : str
        The boundary type (e.g., canton, city).

    Returns
    -------
    reportingmethods.ReportMeta
        A ReportMeta object with the necessary metadata for generating reports.
    """
    meta = {
        "name": location,
        "start": state['date_range']['start'].strftime('%Y-%m-%d'),
        "end": state['date_range']['end'].strftime('%Y-%m-%d'),
        "feature_type": state['feature_type'],
        "code_group_category": "Selected Codes",
        "boundary": boundary,
        "boundary_name": location if boundary else None,
        "feature_name": location if not boundary else None,
        "report_codes": state['selected_objects'],
        "info_columns": info_columns,
        "columns_of_interest": feature_variables
    }

    meta['report_title'] = f"{meta['name']} {boundary}"
    meta['report_subtitle'] = f"Lake, river or park: {meta['feature_type']}"
    meta['title_notes'] = "Proof of concept AI assisted reporting"
    meta['author'] = "hammerdirt analyst"
    meta['code_types'] = code_groups.loc[meta['report_codes']].groupname.unique()

    return ReportMeta(**meta)

def filter_dataframe_with_reportmeta(report_meta: ReportMeta, data: pd.DataFrame) -> pd.DataFrame:
    """
    Filters the DataFrame based on the conditions provided in the `ReportMeta` object.

    This function applies various filters to the survey data based on the metadata provided in the `ReportMeta` object.

    Args:
        report_meta (ReportMeta): An instance of `ReportMeta` containing the metadata for filtering the data.
        data (pd.DataFrame): The DataFrame containing the survey data.

    Returns:
        pd.DataFrame: The filtered DataFrame.
    """
    f_data = data.copy()
    print('\nfiltering data with report meta\n')
    print(report_meta)

    if report_meta.get('start'):
        f_data = f_data[f_data['date'] >= f"{report_meta.start}"]

    if report_meta.get('end'):
        f_data = f_data[f_data['date'] <= f"{report_meta.end}"]

    if report_meta.get('boundary') and report_meta.boundary_name:
        boundary = report_meta.boundary
        boundary_name = report_meta.boundary_name
        f_data = f_data[f_data[boundary] == boundary_name]

    if report_meta.get('feature_type'):
        if report_meta.feature_type == 'both':
            pass
        else:
            f_data = f_data[f_data['feature_type'] == report_meta.feature_type]

    if report_meta.get('feature_name'):
        f_data = f_data[f_data['feature_name'] == report_meta.feature_name]

    if report_meta.get('report_codes'):
        codes = report_meta.report_codes
        f_data = f_data[f_data['code'].isin(codes)]

    return f_data

def baseline_report_and_data(report_meta: ReportMeta, data: pd.DataFrame, material_spec: pd.DataFrame) -> str:
    """
    Produces a rough draft report from the survey data and report meta-data.

    This function filters the survey data based on the conditions provided in the `ReportMeta` object, generates various sections of the report, and concatenates them into a rough draft report.

    Args:
        report_meta (ReportMeta): An instance of `ReportMeta` containing the metadata for filtering and generating the report.
        data (pd.DataFrame): The DataFrame containing the survey data.
        material_spec (pd.DataFrame): A DataFrame containing the material classification of the objects.

    Returns:
        str: A concatenated string representing the rough draft report.
    """
    # report title section
    print(report_meta.boundary)
    title = "## " + report_meta.report_title + "\n"
    objectsoi = "**Objects:** " + ', '.join(report_meta.code_types) + "\n\n"
    notes = "**Notes:** " + report_meta.title_notes + "\n\n"
    author = "**Author:** " + report_meta.author + "\n\n"
    intro = f'{title}{objectsoi}{notes}{author}'

    df = filter_dataframe_with_reportmeta(report_meta, data)
    if df.empty:

        return intro + "No data available for the specified conditions."
    survey_report = SurveyReport(df)
    # baseline report sections
    admin_boundaries = extract_roughdraft_text(survey_report.administrative_boundaries())
    features = extract_roughdraft_text(survey_report.feature_inventory())
    summary_stats = extract_roughdraft_text(survey_report.sampling_results_summary)
    materials = extract_roughdraft_text(survey_report.material_report(material_spec))
    survey_totals = extract_roughdraft_text(survey_totals_for_all_info_cols(report_meta, survey_report))
    inventory = extract_roughdraft_text(survey_report.object_summary())



    # individual sections
    for section in [summary_stats, admin_boundaries, features, materials, survey_totals, inventory]:
        intro += section + "\n"

    return intro

def compute_similarity_matrix(dataframe, columns, id_column, column_to_normalize):
    """
    Computes a cosine similarity matrix for specified columns in a DataFrame.

    Parameters:
        dataframe (pd.DataFrame): The input DataFrame containing data.
        columns (list): List of columns to compute similarity on.
        id_column (str): Column name to use as row and column labels in the output matrix.
        column_to_normalize (str): Column that needs to be separately normalized.

    Returns:
        pd.DataFrame: A DataFrame representing the cosine similarity matrix.
    """
    # Create a copy of the DataFrame to avoid modifying the original
    df = dataframe.copy()

    # Normalize the specified column separately
    scaler = MinMaxScaler()
    df[column_to_normalize] = scaler.fit_transform(df[[column_to_normalize]])

    # Use the specified columns for similarity calculation
    features = df[columns]

    # Compute cosine similarity
    similarity_matrix = cosine_similarity(features)

    # Convert the matrix to a DataFrame for better readability
    similarity_df = pd.DataFrame(similarity_matrix,
                                 index=df[id_column],
                                 columns=df[id_column])
    return similarity_df

