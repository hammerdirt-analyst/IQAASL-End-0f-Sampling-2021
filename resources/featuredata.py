import pandas as pd
import numpy as np
import scipy.stats as stats
from datetime import datetime
from babel.dates import get_month_names
from typing import Any

import reportlab
from reportlab.platypus.flowables import Flowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, ListFlowable, ListItem, KeepTogether
from reportlab.lib.pagesizes import A4
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import HexColor
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

date_format = "%Y-%m-%d"

group_names_de = {"waste water": "Abwasser",
                  "micro plastics (< 5mm)": "Mikroplastik (< 5mm)",
                  "infrastructure": "Infrastruktur",
                  "food and drink": "Essen und Trinken",
                  "agriculture": "Landwirtschaft",
                  "tobacco": "Tabakwaren",
                  "recreation": "Freizeit und Erholung",
                  "packaging non food": "Verpackungen ohne Lebensmittel/Tabak",
                  "plastic pieces": "Plastikfragmente",
                  "personal items": "Persönliche Gegenstände",
                  "unclassified": "nicht klassifiziert",
    
                  }
codes_to_change_de = [
    ["G704", "description", "Seilbahnbürsten"],
    ["Gfrags", "description", "Fragmentierte Kunststoffe"],
    ["G30", "description", "Snack-Verpackungen"],
    ["G124", "description", "Andere Kunststoff"],
    ["G87", "description", "Abdeckklebeband/Verpackungsklebeband"],
    ["G3", "description", "Einkaufstaschen, Shoppingtaschen"],
    ["G33", "description", "Einwegartikel; Tassen/Becher & Deckel"],
    ["G31", "description", "Schleckstengel, Stengel von Lutscher"],
    ["G211", "description", "Sonstiges medizinisches Material"],
    ["G904", "description", "Feuerwerkskörper; Raketenkappen"],
    ["G940", "description", "Schaumstoff EVA (flexibler Kunststoff)"],
    ["G178", "description", "Kronkorken, Lasche von Dose/Ausfreisslachen"],
    ["G74", "description", "Schaumstoffverpackungen/Isolierung"],
    ["G941", "description", "Verpackungsfolien, nicht für Lebensmittel"]
]

luse_de = {
    
    "% to buildings": "Gebäude",
    "% to recreation": "Aktivitäten im Freien",
    "% to agg": "Landwirtschaft",
    "% to woods": "Wald",
    "streets km": "Strassen km",
    "intersects": "Flussmündungen (Anzahl)",
    "% buildings": "Gebäude",
    "% recreation": "Aktivitäten im Freien",
    "% agg": "Landwirtschaft",
    "% woods": "Wald",
    "streets": "Strassen km",
    "population": "Bevölkerung"
}

river_basin_de = {
    "aare": "Aare",
    "linth": "Linth",
    "rhone": "Rhone",
    "ticino": "Ticino",
    "les-alpes": "Alpen und Jura"
}

dims_table_columns_de = {
    "samples":"Erhebungen",
    "quantity":"Objekte (St.)",
    "total_w":"Gesamtgewicht (Kg)",
    "mac_plast_w":"Plastik (Kg)",
    "area":"Fläche (m2)",
    "length":"Länge (m)"
}

sample_summary_table_de = {
    "material": "Material",
    "quantity": "Objekte (St.)",
    "% of total": "Anteil"
}

most_common_objects_table_de = {
    "item": "Objekte",
    "quantity": "Objekte (St.)",
    "% of total": "Anteil",
    "fail rate": "Häufigkeitsrate"
}

inventory_table_de = {
    "item": "Objekte",
    "groupname": "Gruppenname",
    "quantity": "Objekte (St.)",
    "% of total": "Anteil",
    "fail rate": "Häufigkeitsrate",
    "material": "Material"
}

default_land_use_columns = [
    "% buildings",
    "% recreation",
    "% agg",
    "% woods",
    "streets km",
    "intersects"
]

bassin_pallette = {
    "rhone": "dimgray",
    "aare": "salmon",
    "linth": "tan",
    "ticino": "steelblue",
    "reuss": "purple",
    "les-alpes": "darkcyan"
}

do_not_change = ["Alle Erhebungsgebiete", "All Survey areas"]

# colors for gradients
colorsx = ["beige", "navajowhite", "sandybrown", "salmon", "sienna"]
nodes = [0.0, 0.2, 0.6, 0.8, 1.0]
cmap2 = LinearSegmentedColormap.from_list("mycmap", list(zip(nodes, colorsx)))

xlab_k14 = {'labelpad':10, 'fontsize':14}

def defaultMapCaption(language: str = "de"):
    
    if language == "de":
        caption = [
            "Die Erhebungsorte sind für die Analyse nach Erhebungsgebiet ",
            "gruppiert. Die Grösse der Markierung gibt einen Hinweis auf die ",
            "Anzahl Abfallobjekte, die gefunden wurden."
            ]
    else:
        caption = [
            "Map of survey locations March 2020 - Mai 2021. ",
            "The language you requested is not available."
        ]
    return ''.join(caption)
    


def thousandsSeparator(aninteger: int, lang: str = "de"):
    # Replaces the comma with a space in integers >= 1000
    astring = "{:,}".format(aninteger)
    if lang == "de":
        astring = astring.replace(",", " ")
    
    return astring


def replaceDecimal(afloat: float, lang: str = "de"):
    # replaces the decimal with a comma for floats
    astring = str(afloat)
    if lang == "de":
        astring = astring.replace(".", ",")
    
    return astring


def fmtPctOfTotal(data: pd.DataFrame, label: str = "% of total", multiple: int = 100, around: int = 1):
    # Formats a float column to string with trailing % sign.
    # returns the dataframe with a new column using the label provided
    
    try:
        data[label] = (data[label] * multiple)
    except ValueError:
        print(f"Could not make {label} column")
        raise
    else:
        if around == 0:
            data[label] = data[label].map(lambda x: f"{int(x)}%")
        else:
            data[label] = data[label].map(lambda x: f"{round(x, around)}%")
            
    return data


def updatePlaceNames(x: str = None, column: str = 'water_name', a_map: Any = None, do_not_change: list = do_not_change):
    # If x is in tne index or is a key for a_map then the value of a_map for that key
    # is returned. Else value error is raised.
    
    if x in do_not_change:
        return x
    
    if isinstance(a_map, pd.DataFrame):
        try:
            x = a_map.loc[x, column]
        except ValueError:
            print(f'{x} is not a key for this index')
            raise
        else:
            return x
            
    if isinstance(a_map, dict):
        try:
            x = a_map[x]
        except ValueError:
            print(f'{x} x is not a key for this index')
            raise
        else:
            return x


def thereIsData(data: Any = None, atype: () = None):
    # checks that the provided data is a certain type
    if isinstance(data, atype):
        return data
    else:
        print(f"There is no data or it is not the right type: is_instance({data}, {atype}).")
        raise TypeError
    

def loadData(filename):
    # loads data from a .csv into a pandas dataframe
    filename = thereIsData(data=filename, atype=(str,))
    
    try:
        data = pd.read_csv(filename)
    except OSError:
        print("The file could not be read, is this the right file extension?")
        raise
    return data


def changeColumnNames(data, columns: {} = None):
    # changes the column names of a data frame
    data = thereIsData(data=data, atype=(pd.DataFrame,))
    columns = thereIsData(data=columns, atype=(dict,))
    
    try:
        data = data.rename(columns=columns)
    except ValueError:
        print("The columns did not go with the data")
        raise
    return data


def makeEventIdColumn(data, feature_level, these_features: str = " ", date_range: tuple = (),
                      index_name: str = "loc_date", index_prefix="location",
                      index_suffix="date", **kwargs):
    # Combines the location and date column into one str: "slug-date"
    # makes it possible to group records by event
    # converts string dates to timestamps and localizes to UTC
    data = thereIsData(data=data, atype=(pd.DataFrame,))
    feature_level = thereIsData(data=feature_level, atype=(str,))
    these_features = thereIsData(data=these_features, atype=(str, list))
    
    if feature_level == "all":
        data[index_name] = list(zip(data[index_prefix].values, data[index_suffix].values))
        data["date"] = pd.to_datetime(data["date"], format=date_format)
        temporal_mask = (data["date"] >= date_range[0]) & (data["date"] <= date_range[1])
        data = data[temporal_mask].copy()
        
    else:
        try:
            if isinstance(these_features, (list,)):
                mask = data[feature_level].isin(these_features)
            else:
                mask = data[feature_level] == these_features
            sliced_data = data[mask].copy()
            sliced_data[index_name] = list(zip(sliced_data[index_prefix].values, sliced_data[index_suffix].values))
            sliced_data["date"] = pd.to_datetime(sliced_data["date"], format=date_format).dt.tz_localize('UTC')
        
        except RuntimeError:
            print("The pandas implementation did not function")
            raise
        
        else:
            temporal_mask = (sliced_data["date"] >= date_range[0]) & (sliced_data["date"] <= date_range[1])
            data = sliced_data[temporal_mask].copy()
    
    return data


def featureData(filename: str = None, feature_level: str = None, language: str = None, date_range: () = None, these_features: str = None,
                columns: {} = None, unit_label: str = None, groupname: str = 'groupname'):
    
    f_data = loadData(filename)
    if isinstance(columns, dict):
        f_data = changeColumnNames(f_data, columns=columns)
    if language == "de":
        f_data[groupname] = f_data[groupname].map(lambda x: group_names_de[x])
        f_data.rename(columns={'p/100m': unit_label}, inplace=True)
        
    feature_data = makeEventIdColumn(f_data, feature_level, date_range=date_range, these_features=these_features)
    f_data["date"] = pd.to_datetime(f_data["date"], format=date_format).dt.tz_localize('UTC')
    temporal_mask = (f_data["date"] >= date_range[0]) & (f_data["date"] <= date_range[1])
    period_data = f_data[temporal_mask].copy()
    
    return feature_data, period_data


def convertCase(str_camelcase):
    # This function takes in a string in camelCase and converts it to snake_case
    str_camelcase = thereIsData(data=str_camelcase, atype=(str,))
    str_snake_case = ""
    for ele in list(str_camelcase):
        if ele.islower():
            str_snake_case = str_snake_case + ele
        else:
            str_snake_case = str_snake_case + "_" + ele.lower()
    return str_snake_case


def checkInitiateAttribute(data=False, check=False, atype=(list, np.ndarray), a_method=None, **kwargs):
    # check the data type of the requested element against the required data type
    # if check the data is returned, else <a_method> will be applied to <data>
    # and checked again.
    if isinstance(check, atype):
        return check
    else:
        try:
            new_data = a_method(data)
            check_again = checkInitiateAttribute(check=new_data, data=new_data, atype=atype, a_method=a_method,
                                                 **kwargs)
            return check_again
        
        except ValueError:
            print("neither the data nor the method worked")
            raise


def uniqueValues(data):
    # method to pass pd.series.unique as a variable
    return data.location.unique()


def dateToYearAndMonth(python_date_object, fmat='wide', lang=""):
    a_date = thereIsData(data=python_date_object, atype=(datetime,))
    amonth = a_date.month
    a_year = a_date.year
    amonth_foreign = get_month_names(fmat, locale=lang)[amonth]
    
    return f'{amonth_foreign} {a_year}'

def quarterlyOrMonthlyValues(data, feature, vals="p/100m", quarterly=["ticino"]):
    """Determines and then draws either quaterly or monthly resample
    of survey results depending on the value of quaterly.

    :param data: The data frame of interest
    :param feature: The current feature of interest
    :param vals: The column to resample
    :param quarterly: The names of the features that have quaterly samples
    :return: A data frame with eihther monthly or quarterly resamples and the designation
    """
    if feature in quarterly:
        plot = data[vals].resample("Q").median()
        rate = "quarterly"
    else:
        plot = data[vals].resample("M").median()
        rate = "monthly"
    
    return plot, rate

def createSummaryTableIndex(unit_label, language="en"):
    """Assigns the current units to the keys and creates
    custom key values based on language selection.

    :param unit_label: The current value of unit label
    :param language: the two letter abbreviation for the current language
    :return: the pd.describe dict with custom labels
    """
    
    if language == "en":
        new_data = {"count": "# samples",
                    "mean": f"average {unit_label}",
                    "std": "standard deviation",
                    "min": f"min {unit_label}",
                    "max": f"max {unit_label}",
                    "25%": "25%",
                    "50%": "50%",
                    "75%": "75%",
                    "total objects": "total objects",
                    "# locations": "# locations",
                    }
    elif language == "de":
        new_data = {"count": "Erhebungen",
                    "mean": f"Durchschnitt {unit_label}",
                    "std": "Standardabweichung",
                    "min": f"min {unit_label}",
                    "max": f"max {unit_label}",
                    "25%": "25%",
                    "50%": "50%",
                    "75%": "75%",
                    "total objects": "Abfallobjekte",
                    "# locations": "Anzahl der Standorte",
                    }
    else:
        print(f"ERROR {language} is not an option. Returning empty dictionary")
        new_data = {}
    
    return new_data


def changeSeriesIndexLabels(a_series: pd.Series = None, change_names: {} = None):
    """A convenience function to change the index labels of a series x.
    Change_names is keyed to the series index.

    :param a_series: A pandas series
    :param change_names: A dictionary that has keys = x.index and values = new x.index label
    :return: The series with the new labels
    """
    
    new_dict = {}
    for param in a_series.index:
        new_dict.update({change_names[param]: a_series[param]})
    return pd.Series(new_dict)


def make_table_values(data, col_nunique=["location", "loc_date", "city"], col_sum=["quantity"], col_median=[]):
    """Extracts particular aggregation values for different columns and returns a dictionary of values.

    :param data: The data frame that has the columns
    :param col_nunique: Counts the unique values of the columns
    :param col_sum: Sums the values of the columns
    :param col_median: Returns the median value for the array
    :return: A dictionary of values that corresponds to the requested aggregation
        for each column name
    """
    
    table_data = {}
    
    for col in col_nunique:
        table_data.update({col: data[col].nunique()})
    for col in col_sum:
        table_data.update({col: data[col].sum()})
    for col in col_median:
        table_data.update({col: data[col].median()})
    
    return table_data


def empiricalCDF(anarray):
    data = thereIsData(anarray, (list, np.ndarray))
    x = sorted(data)
    y = np.arange(1, len(data) + 1) / float(len(data))    
    
    return x, y


def ecdfOfAColumn(data, column=""):
    data = thereIsData(data, (pd.DataFrame,))
    col = thereIsData(column, str)
    
    anarray = data[col].values
    x, y = empiricalCDF(anarray)
    
    return {"column": col, "x": x, "y": y}


def columnsAndOperations(column_operations: list = None, columns: list = None, unit_label: str = None):
    if column_operations is None:
        column_operation = {unit_label: "median", "quantity": "sum"}
    else:
        column_operation = {x[0]: x[1] for x in column_operations}
    if columns is None:
        columns = ["loc_date", "groupname"]
    
    return columns, column_operation


def codeGroupTotals(data: pd.DataFrame = None, unit_label: str = None, column_operation: dict = {},
                    columns: list = None):
    codegroup_totals = data.groupby(columns, as_index=False).agg({unit_label: 'sum', 'quantity': 'sum'})
    codegroup_totals = codegroup_totals.groupby('groupname', as_index=False).agg(column_operation)
    
    # percent of total
    codegroup_totals["% of total"] = (codegroup_totals.quantity / codegroup_totals.quantity.sum()).round(2)
    
    # the code data comes from the feature data (survey results)
    # Add the description of the code and the material
    codegroup_totals.set_index("groupname", inplace=True)
    
    return codegroup_totals


class LandUseProfile:
    
    def __init__(self, data=None, index_column="loc_date", feature_level: str = None, these_features: str = None,
                 land_use_columns: list = default_land_use_columns, **kwargs):
        self.data = data
        self.land_use_columns = land_use_columns
        self.feature_level = feature_level
        self.index_column = index_column
        self.these_features = these_features
        super().__init__()
    
    def byIndexColumn(self):
       
        data = thereIsData(data=self.data, atype=(pd.DataFrame,))
        columns = [self.index_column, self.feature_level, *self.land_use_columns]
        d = data[columns].drop_duplicates()
        
        return d
    
    def featureOfInterest(self):
        d_indexed = self.byIndexColumn()
        if self.these_features == "all":
            all_features = d_indexed[self.feature_level].unique()
            d = [d_indexed[d_indexed[self.feature_level] == feature] for feature in all_features]
        else:
            d = [d_indexed[d_indexed[self.feature_level] == self.these_features]]
        return d


class Codes:
    de_codes_to_change = codes_to_change_de
    de_code_description = loadData("resources/codes_german_Version_1.csv")
    materials_ge = {"Metal": "Metall",
                    "Chemicals": "Chemikalien",
                    "Paper": "Papier",
                    "Glass": "Glas",
                    "Rubber": "Gummi",
                    "Wood": "Holz",
                    "Cloth": "Stoff",
                    "Unidentified": "Unbekannt",
                    "Undefined": "Unbestimmt",
                    "Plastic": "Plastik",
                    "Alu": "Alu",
                    }
    
    def __init__(self, code_data: pd.DataFrame = None, language: 'str' = 'en'):
        self.code_data = code_data
        self.language = language
        self.dfCodes = False
        self.dMap = False
        self.mMap = False
    
    def adjustForLanguage(self):
        if isinstance(self.dfCodes, pd.DataFrame):
            return self.dfCodes

        new_code_data = self.code_data.copy()
        
        if self.language == 'de':
            dmap = self.de_code_description[['code', 'german']].set_index('code')
            
            for code in new_code_data.index:
                new_code_data.loc[code, "description"] = dmap.loc[code, "german"]
            for code_def in self.de_codes_to_change:
                new_code_data.loc[code_def[0], code_def[1]] = code_def[2]
            
            new_code_data["material"] = new_code_data.material.map(lambda x: self.materials_ge[x])
        
        self.dfCodes = new_code_data
        self.mMap = new_code_data.material
        self.dMap = new_code_data.description


class PeriodResults:
    
    def __init__(self, period_data: pd.DataFrame = None, these_features: str = None,
                 feature_level: str = None, feature_parent: str = None, unit_label: str = None,
                 most_common: list = None, parent_level: str = None, period_name: str = None, **kwargs):
        self.period_data = period_data
        self.these_features = these_features
        self.feature_level = feature_level
        self.feature_parent = feature_parent
        self.parent_level = parent_level
        self.period_name = period_name
        self.unit_label = unit_label
        self.most_common = most_common
    
    def makeMask(self, parent: bool = True):
        if parent:
            return self.period_data[self.parent_level] == self.feature_parent
        else:
            return False
    
    def parentSampleTotals(self, parent: bool = True):
        
        mask = self.makeMask(parent=parent)
        
        if isinstance(mask, tuple):
            data = self.period_data[mask].copy()
            data = data.groupby(["loc_date", "date"], as_index=False)[self.unit_label].sum()
        
        else:
            data = self.period_data.groupby(["loc_date", "date"], as_index=False)[self.unit_label].sum()
            
        return data
    
    def parentMostCommon(self, parent: bool = True, percent: bool = False):
        
        mask = self.makeMask(parent=parent)
        
        if isinstance(mask, pd.Series):
            data = self.period_data[mask].copy()
            data = data[data.code.isin(self.most_common)]
            use_name = self.feature_parent
        else:
            data = self.period_data.copy()
            data = data[data.code.isin(self.most_common)]
            use_name = self.period_name
        
        if percent:
            data = data.groupby('code', as_index=False).quantity.sum()
            data.set_index('code', inplace=True)
            data[use_name] = (data.quantity / data.quantity.sum()).round(2)
            
            return data[use_name]
        
        else:
            data = data.groupby(["loc_date", 'code'], as_index=False)[self.unit_label].sum()
            data = data.groupby('code', as_index=False)[self.unit_label].median()
            data.set_index('code', inplace=True)
            data[use_name] = data[self.unit_label]
            
            return data[use_name]
    
    def parentGroupTotals(self, parent: bool = True, percent: bool = False):
        
        mask = self.makeMask(parent=parent)
        
        if isinstance(mask, pd.Series):
            data = self.period_data[mask].copy()
            use_name = self.feature_parent
        else:
            data = self.period_data.copy()
            use_name = self.period_name
        
        if percent:
            data = data.groupby('groupname', as_index=False).quantity.sum()
            data.set_index('groupname', inplace=True)
            data[use_name] = (data.quantity / data.quantity.sum()).round(2)
            
            return data[use_name]
        
        else:
            data = data.groupby(["loc_date", 'groupname'], as_index=False)[self.unit_label].sum()
            data = data.groupby('groupname', as_index=False)[self.unit_label].median()
            data.set_index('groupname', inplace=True)
            data[use_name] = data[self.unit_label]
            
            return data[use_name]
        
    def __str__(self):
        return f"Period data: {self.period_name}, features: {self.these_features}"


class FeatureData(Codes):
    
    def __init__(self, filename: str = "", feature_name: str = "", feature_level: str = "",
                 these_features: list = [], component: str = "", date_range: list = None, fail_rate: int = 0,
                 columns: list = False, language: str = "en", unit_label: str = "pcs/100m",
                 code_data: pd.DataFrame = None, water_type: str = None, **kwargs):
        super().__init__(code_data, language)
        self.filename = filename
        self.feature = feature_name
        self.feature_level = feature_level
        self.these_features = these_features
        self.feature_component = component
        self.columns = columns
        self.fail_rate = fail_rate
        self.date_range = date_range
        self.unit_label = unit_label
        self.water_type = water_type
        self.language = language
        self.feature_data = None
        self.period_data = None
        self.code_summary = None
        self.codegroup_summary = None
        self.material_summary = None
        self.most_common = None
        self.sample_totals = None
        self.sample_summary = None
    
    def makeFeatureData(self):
        
        if isinstance(self.feature_data, pd.DataFrame):
            return self.feature_data
        
        fd_kwargs = {
            "these_features": self.these_features,
            "columns": self.columns,
            "language": self.language,
            'date_range': self.date_range,
            'unit_label':self.unit_label
        }
        fd, period_data = featureData(self.filename, self.feature_level, **fd_kwargs)
        
        if self.water_type is None:
            self.feature_data = fd
            self.period_data = period_data
        else:
            self.feature_data = fd[fd.w_t == self.water_type]
            self.period_data = period_data[period_data.w_t == self.water_type]
    
    def locationSampleTotals(self, column_operations: list = None, columns: list = None):
        
        if isinstance(self.sample_totals, pd.DataFrame):
            return self.sample_totals
        
        if columns is None:
            columns = ["loc_date", "location", self.feature_component, "date"]
        
        cols_ops_kwargs = {
            "column_operations": [(self.unit_label, "sum"), ("quantity", "sum")],
            "columns": columns ,
            "unit_label": self.unit_label
        }

        columns, column_operation = columnsAndOperations(**cols_ops_kwargs)
        
        if not isinstance(self.feature_data, pd.DataFrame):
            self.makeFeatureData()
            
        self.sample_totals = self.feature_data.groupby(columns, as_index=False).agg(column_operation)
    
    def codeSummary(self, column_operations: list = None):
        
        if isinstance(self.code_summary, pd.DataFrame):
            return self.code_summary
        
        if column_operations is None:
            column_operations = {
                "column_operations": [(self.unit_label, "median"), ("quantity", "sum")],
                "columns": ["code"],
                "unit_label": self.unit_label
            }

        columns, column_operation = columnsAndOperations(**column_operations)
        
        # apply the column operations
        code_totals = self.feature_data.groupby(columns, as_index=False).agg(column_operation)
        
        # percent of total
        code_totals["% of total"] = ((code_totals.quantity / code_totals.quantity.sum()) * 100).round(2)
        
        # fail and fail-rate
        code_totals["fail"] = code_totals.code.map(lambda x: self.feature_data[
            (self.feature_data.code == x) & (self.feature_data.quantity > 0)].loc_date.nunique())
        code_totals["fail rate"] = ((code_totals.fail / self.feature_data.loc_date.nunique()) * 100).astype("int")
        
        # the code name comes from the feature data (survey results)
        # Add the description of the code and the material type
        code_totals.set_index(columns, inplace=True)
        code_totals["item"] = code_totals.index.map(lambda x: self.dMap[x])
        code_totals["material"] = code_totals.index.map(lambda x: self.mMap[x])
        
        code_totals = code_totals[["item", "quantity", "% of total", self.unit_label, "fail rate", "material"]]
        
        self.code_summary = code_totals
        
    def codeGroupSummary(self, column_operations=None):
        if isinstance(self.codegroup_summary, pd.DataFrame):
            return self.codegroup_summary
        
        cols_ops_kwargs = {
            "column_operations": None,
            "columns": None,
            "unit_label": self.unit_label
        }
        
        columns, column_operation = columnsAndOperations(**cols_ops_kwargs)

        code_group_kwargs = {
            "data": self.feature_data,
            "unit_label": self.unit_label,
            "column_operation": column_operation,
            "columns": columns
        }

        codegroup_totals = codeGroupTotals(**code_group_kwargs)
    
        self.codegroup_summary = codegroup_totals
    
    def materialSummary(self):
        
        if isinstance(self.material_summary, pd.DataFrame):
            return self.material_summary
        
        if not isinstance(self.code_summary, pd.DataFrame):
            self.codeSummary()
        
        a = self.code_summary.groupby("material", as_index=False).quantity.sum()
        a["% of total"] = a['quantity'] / a['quantity'].sum()
        b = a.sort_values(by="quantity", ascending=False)
        
        self.material_summary = b
    
    def mostCommon(self, fail_rate: int = None, limit: int = 10):
        
        if isinstance(self.most_common, pd.DataFrame):
            return self.most_common
        
        if not isinstance(self.code_summary, pd.DataFrame):
            self.codeSummary()
        if fail_rate is None:
            fail_rate = self.fail_rate
            
        # the top ten by quantity
        most_abundant = self.code_summary.sort_values(by="quantity", ascending=False)[:limit]
        
        # the most common
        most_common = self.code_summary[self.code_summary["fail rate"] >= fail_rate].sort_values(by="quantity",
                                                                                                 ascending=False)
        # merge with most_common and drop duplicates
        # it is possible (likely) that a code will be abundant and common
        m_common = pd.concat([most_abundant, most_common]).drop_duplicates()
        
        self.most_common = m_common
    
    def makeDailyTotalSummary(self):
        
        if isinstance(self.sample_summary, pd.Series):
            return self.sample_summary
        
        if not isinstance(self.sample_totals, pd.DataFrame):
            self.locationSampleTotals()
        
        # the summary of the dependent variable
        a = self.sample_totals[self.unit_label].describe().round(2)
        a["total objects"] = self.sample_totals.quantity.sum()
        
        # assign appropriate language to index names
        # retrieve the appropriate index names based on language
        table_index = createSummaryTableIndex(self.unit_label, language=self.language)
        
        # assign the new index
        summary_table = changeSeriesIndexLabels(a, table_index)
        
        self.sample_summary = summary_table
    
    def __str__(self):
        
        return f"{self.feature}, {self.feature_level}, {self.these_features}, {self.feature_component}"


class Components(FeatureData, Codes):
    
    def __init__(self, component_type: str = None, type_column: str = None, **kwargs):
        self.component_type = component_type
        self.type_column = type_column
        super().__init__(**kwargs)
    
    def componentMostCommonPcsM(self, columns: list = None, column_operations: list = None):
        
        codes = self.most_common.index
        
        if column_operations is None:
            column_operations = {
                "column_operations":  [(self.unit_label, "sum"), ("quantity", "sum")],
                "columns":  [self.feature_component, "loc_date", "code"],
                "unit_label": self.unit_label
            }
        
        columns, column_operation = columnsAndOperations(**column_operations)
        
        mask = self.feature_data.code.isin(codes)
        
        if isinstance(self.component_type, str):
            try:
                type_mask = self.feature_data[self.type_column] == self.component_type
            except ValueError:
                print("Type mask could not be executed using the type_column and component_type variables")
                raise
            mask = (mask & type_mask)
        
        a = self.feature_data[mask].groupby(columns, as_index=False).agg(column_operation)
        a = a.groupby([self.feature_component, "code"], as_index=False)[self.unit_label].median()
        
        # map the description to the code
        a["item"] = a.code.map(lambda x: self.dMap.loc[x])
        
        return a
    
    def componentCodeGroupResults(self, columns: []=None, column_operations: []=None):
        
        """Produces two arrays of the aggregated survey results by codegroup for each feature component. Rows are the
        feature component, columns are the codegroup. One array is % of total the other is median pcs/m.
        """
        if not isinstance(columns, list):
            # the results are aggregated at the sample level first
            columns = ["loc_date", "groupname"]
        if isinstance(column_operations, list):
            column_operation = {x[0]: x[1] for x in column_operations}
        else:
            column_operation = {self.unit_label: "sum", "quantity": "sum"}
        
        data = self.feature_data.copy()

        if isinstance(self.component_type, str):
            try:
                type_mask = self.feature_data[self.type_column] == self.component_type
            except ValueError:
                print("Type mask could not be executed using the type_column and component_type variables")
                raise
            data = data[type_mask]
        
        results = data.groupby([self.feature_component, *columns], as_index=False).agg(column_operation)
        
        # the total amount per component, used for % of total array
        cg_tq = results.groupby(self.feature_component).quantity.sum()
        
        # the median per survey per group and the total quantity
        agg_this = {self.unit_label: "median", "quantity": "sum"}
        results = results.groupby([self.feature_component, "groupname"], as_index=False).agg(agg_this)
        results["f_total"] = results[self.feature_component].map(lambda x: cg_tq.loc[x])
        results["% of total"] = (results.quantity / results.f_total).round(2)
        
        return results


class Beaches:
    """The dimendsional and geo data for each survey location"""
    
    def __init__(self, dfBeaches: pd.DataFrame = None):
        self.df_beaches = dfBeaches
        self.proper_feature_name = None
        
    def makeFeatureNameMap(self):
        a_map = self.df_beaches[["water_name_slug", "water_name"]].set_index("water_name_slug", drop=True)
        return a_map.drop_duplicates()
    
    def makeLocationFeatureMap(self):
        return self.df_beaches["water_name_slug"].copy()
    
    def makeCityFeatureMap(self):
        a_map = self.df_beaches[["city", "water_name_slug"]].set_index("city", drop=True)
        return a_map.drop_duplicates()
    
    def makeLocationCityMap(self):
        a_map = self.df_beaches[["location", "city"]].set_index('city', drop=True)
        return a_map.drop_duplicates()
    
    
class AdministrativeSummary(Beaches):
    col_nunique_qty = ["location", "loc_date", "city"]
    col_sum_qty = ["quantity"]
    col_population = ["city", "population"]
    col_sum_pop = ["population"]
    col_nunique_city = ["city"]
    
    def __init__(self, data: pd.DataFrame = None, dims_data: pd.DataFrame = None, feature_component: str = None,
                 label: str = None, date_range: () = None, **kwargs):
        super().__init__(**kwargs)
        self.feature_data = data
        self.label = label
        self.dims_data = dims_data
        self.feature_component = feature_component
        self.date_range = date_range
        self.component_labels = data[feature_component].unique()
        self.locations_of_interest = None
        self.lakes_of_interest = None
        self.rivers_of_interest = None
    
    def locationsOfInterest(self, **kwargs):
        data = thereIsData(self.feature_data, pd.DataFrame)
        locations = checkInitiateAttribute(check=self.locations_of_interest, data=data, atype=(list, np.ndarray),
                                           a_method=uniqueValues, **kwargs)
        
        self.locations_of_interest = locations
    
    def resultsObject(self, col_nunique=None, col_sum=None):
        data = thereIsData(self.feature_data, pd.DataFrame)
        
        if not col_nunique:
            col_nunique = self.col_nunique_qty
        if not col_sum:
            col_sum = self.col_sum_qty
        
        t = make_table_values(data, col_nunique=col_nunique, col_sum=col_sum)
        
        return t
    
    def populationKeys(self):
        data = thereIsData(self.feature_data, pd.DataFrame)
        locs = checkInitiateAttribute(check=self.locations_of_interest, data=data, atype=(list, np.ndarray),
                                      a_method=uniqueValues)
        
        try:
            popmap = self.df_beaches.loc[locs][self.col_population].drop_duplicates()
        except TypeError:
            print("that did not work")
            raise
        
        return popmap
    
    def lakesOfInterest(self):
        data = thereIsData(self.feature_data, pd.DataFrame)
        locs = checkInitiateAttribute(check=self.locations_of_interest, data=data, atype=(list, np.ndarray),
                                      a_method=uniqueValues)
        
        if not isinstance(self.lakes_of_interest, list):
            mask = (self.df_beaches.index.isin(locs)) & (self.df_beaches.water == "l")
            d = self.df_beaches.loc[mask]["water_name"].unique()
            self.lakes_of_interest = d
            return d
        else:
            return self.lakes_of_interest
    
    def riversOfInterest(self):
        data = thereIsData(self.feature_data, pd.DataFrame)
        locs = checkInitiateAttribute(check=self.locations_of_interest, data=data, atype=(list, np.ndarray),
                                      a_method=uniqueValues)
        
        if not isinstance(self.rivers_of_interest, list):
            mask = (self.df_beaches.index.isin(locs)) & (self.df_beaches.water == "r")
            d = self.df_beaches.loc[mask]["water_name"].unique()
            self.rivers_of_interest = d
            return d
        else:
            
            return self.rivers_of_interest
    
    def summaryObject(self):
        
        t = self.resultsObject()
        pop_values = make_table_values(self.populationKeys(), col_nunique=self.col_nunique_city,
                                           col_sum=self.col_sum_pop)
        if not isinstance(self.locations_of_interest, (list, np.ndarray)):
            self.locationsOfInterest()
        t["locations_of_interest"] = self.locations_of_interest
        
        t.update(pop_values)
        
        return t
    
    def dimensionalSummary(self):
        
        # map location to component name
        try:
            component_map = self.df_beaches[self.feature_component]
        except AttributeError:
            print("The beaches data frame is missing or the feature component is not valid")
            raise
            
        try:
            location_mask = (self.dims_data.location.isin(self.locations_of_interest))
        except AttributeError:
            print(
                "Unable to make location mask, either the dimensional data is missing or the locations of interest do not correspond")
            raise
        
        try:
            temporal_mask = (self.dims_data["date"] >= self.date_range[0]) & (
                        self.dims_data["date"] <= self.date_range[1])
        except AttributeError:
            print(
                "Unable to make temporal mask, either the dimensional data is missing or the of the date range variable is incorrect")
            raise
        
        try:
            dims_table = self.dims_data[location_mask & temporal_mask].copy()
        except AttributeError:
            print(
                "Unable to make dimensional data table, there is a problem with the either the data or location and temporal masks")
            raise
        
        # unique id for each survey
        dims_table["loc_date"] = list(zip(dims_table.location.values, dims_table["date"].values))
        
        # values of interest
        agg_dims = {"total_w": "sum", "mac_plast_w": "sum", "area": "sum", "length": "sum"}
        
        dims_table[self.feature_component] = dims_table.location.map(lambda x: component_map.loc[x])
        dims_table = dims_table.groupby([self.feature_component]).agg(agg_dims)
        
        # map the qauntity to the dimensional data
        q_map = self.feature_data.groupby(self.feature_component).quantity.sum()
        
        
        # collect the number of samples from the survey total data:
        for name in dims_table.index:
            if self.feature_component == "location":
                new_name = component_map[component_map == name].index[0]
                mask = self.feature_data[self.feature_component] == new_name
                dims_table.loc[name, "samples"] = self.feature_data[mask].loc_date.nunique()
                dims_table.loc[name, "quantity"] = q_map[new_name]
            else:
                mask = self.feature_data[self.feature_component] == name
                dims_table.loc[name, "samples"] = self.feature_data[mask].loc_date.nunique()
                
                dims_table.loc[name, "quantity"] = q_map[name]
                
        if self.feature_component == "water_name_slug":
            
            proper_names = self.makeFeatureNameMap()
            dims_table["water_name"] = dims_table.index.map(lambda x: proper_names.loc[x, "water_name"])
            dims_table.set_index("water_name", inplace=True, drop=True)
            
        # get the sum of all the features
        # print(dims_table)
        dims_table.loc[self.label] = dims_table.sum(numeric_only=True, axis=0)
        
        return dims_table

    
# style definitions for pdf report
# types
a_flowable_paragraph = reportlab.platypus.paragraph
a_flowable_image = reportlab.platypus.flowables.Image
# section and paragraph formatting
title_style = ParagraphStyle(**{"name": "title_style", "fontSize": 16, "fontName": "Helvetica"})
section_title = ParagraphStyle(**{"name": "section_title", "fontSize": 14, "fontName": "Helvetica"})
caption_style = ParagraphStyle(**{"name": "caption_style", "fontSize": 9, "fontName": "Times-Italic"})
subsection_title = ParagraphStyle(**{"name": "sub_section_title", "fontSize": 12, "fontName": "Helvetica"})
p_style = ParagraphStyle(**{"name": "content", "fontSize": 10, "fontName": "Times-Roman"})
bold_block = ParagraphStyle(**{"name": "bold_block", "fontSize": 10, "fontName": "Times-Bold"})
indented = ParagraphStyle(**{"name": "indented", "fontSize": 10, "fontName": "Times-Roman", "leftIndent":36})
block_quote_style = ParagraphStyle(**{"name": "list_item_style", "fontSize": 10, "fontName": "Times-Italic", "leading":15, "leftIndent":20})

# spacers
larger_space = Spacer(1, 1.5*cm)
large_space = Spacer(1, 1*cm)
small_space = Spacer(1, .5*cm)
smaller_space = Spacer(1, .25*inch)
smallest_space = Spacer(1, .2*cm)

# table cell definitions:
table_header = ParagraphStyle(**{"name": "table_header", "fontSize": 8, "fontName": "Helvetica", "alignment":1})
table_style = ParagraphStyle(**{"name": "table_style", "fontSize": 8, "fontName": "Helvetica"})
styled_table_header = ParagraphStyle(**{"name": "table_header", "fontSize": 8, "fontName": "Helvetica", "alignment":1})
table_style_centered = ParagraphStyle(**{"name": "table_style", "fontSize": 8, "fontName": "Helvetica", "alignment":1})
table_style_right = ParagraphStyle(**{"name": "table_style", "fontSize": 8, "fontName": "Helvetica", "alignment":2})
# lists
list_item_style = ParagraphStyle(
    **{"name": "list_item_style", "fontSize": 10, "fontName": "Times-Roman", "leftIndent": 5, "leading": 13,
       "bulletFont": "Times-Roman", "bulletFontSize": 6})


def makeAList(alistofstrings):
    group_list_items = [ListItem(Paragraph(x, list_item_style), leftIndent=25, bulletOffsetY=-3.2) for x in
                        alistofstrings]
    group_list = ListFlowable(group_list_items, bulletType='bullet', start="circle", bulletFontSize=6, leftIndent=5)
    
    return group_list

# table definitions
default_table_style = TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('INNERGRID', (1, 1), (-1, -1), 0.25, HexColor("#8b451330", hasAlpha=True)),
    ('ROWBACKGROUNDS', (1, 1), (-1, -1), [HexColor("#8b451320", hasAlpha=True), colors.white]),
    ('TOPPADDING', (0, 0), (-1, -1), 1),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 1)

])
figure_table_style = TableStyle([
    ('BOX', (0, 0), (-1, -1), .5, HexColor("#ffffff")),
    ('ALIGN', (0, 0), (0, 0), 'CENTER'),
    ('TOPPADDING', (0, 0), (0, 0), 8),
    ('BOTTOMPADDING', (0, 0), (0, 0), 8),
    ('LEFTPADDING', (1, 0), (1, 0), 8),
    ('RIGHTPADDING', (1, 0), (1, 0), 0),

])

side_by_side_style_figure_left = TableStyle([
    ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ('TOPPADDING', (0, 0), (0, 0), 0),
    ('TOPPADDING', (0, 1), (0, 1), 0),
    ('VALIGN', (0, 0), (-1, -1), "TOP"),
    ('VALIGN', (0, 0), (0, 0), "BOTTOM"),
    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
    ('LEFTPADDING', (0,0), (0, 0), 0),
    ('LEFTPADDING', (0,1), (0, 1), 8),
])

side_by_side_style_figure_right = TableStyle([
    ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ('TOPPADDING', (0, 0), (0, 0), 0),
    ('TOPPADDING', (0, 1), (0, 1), 0),
    ('VALIGN', (0, 0), (-1, -1), "TOP"),
    ('VALIGN', (0, 0), (0, 0), "TOP"),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('LEFTPADDING', (0, 0), (0, 0), 0),
    ('LEFTPADDING', (0, 1), (0, 1), 8),
])


def addToDoc(flowables, alist):
    
    doc_components = [*alist, *flowables]
    return doc_components

def combineString(a_list):
    return ''.join(a_list)
def makeAParagraph(alist_of_strings, style=p_style):
    p_text = combineString(alist_of_strings)
    return Paragraph(p_text, style)


def makeBibEntry(name: str = None, team: str = None, pub: str = None):
    anchor = f'<a name="{name}"/>{name}: <i>{team}</i> {pub}'
    return anchor


def sectionParagraphs(a_list_of_lists, smallspace=small_space, style=p_style):
    section = []
    for para in a_list_of_lists:
        p = makeAParagraph(para, style=style)
        section.append(p)
        section.append(KeepTogether(smallspace))
    return section


def adminFormatNumericInteger(func=thousandsSeparator, an_int: str=None, language: str=None):
    # uses the method defined by func to apply numeric formatting according to the language variable
    try:
        data = func(an_int, language)
    except OSError as err:
        print("The function provided did not work", err)
        raise
    else:
        return data


def stringStartEndDate(func=dateToYearAndMonth, date_format: str="%Y-%m-%d", lang: str = "de",  a_date: str=None,):
    # uses the method defined by func to apply date formatting according to the language variable
    
    try:
        data = func(datetime.strptime(a_date, date_format), lang=lang)
    except (TypeError, OSError) as err:
        print("Is the date formatted the same as the date_format? Are you sure of the method provided?", err)
    
    else:
        return data


def makeAdminSummaryStateMent(start, end, feature_name, language: str="de", admin_summary: dict=None,
                              all_lakes_and_rivers: bool=False):
    # the admin summary can be called from the admin class. It has a specific construction. 
    # use the data in the admin summary class to assemble string representation
    
    start_date = stringStartEndDate(a_date=start)
    end_date = stringStartEndDate(a_date=end)
    n_samples = adminFormatNumericInteger(an_int=admin_summary["loc_date"])
    total = adminFormatNumericInteger(an_int=admin_summary["quantity"])
    population = adminFormatNumericInteger(an_int=admin_summary["population"])
    
    if language != None:
        phrase_one = f"Im Zeitraum von {start_date}  bis {end_date} wurden im Rahmen von {n_samples} Datenerhebungen insgesamt {total} Objekte entfernt und identifiziert. "
        if all_lakes_and_rivers:
            phrase_two = f"Die Ergebnisse aller Erhebungsgebiete umfassen {admin_summary['location']} Orte, {admin_summary['city']} Gemeinden und eine Gesamtbevölkerung von etwa {population} Einwohnenden."
        else:
            phrase_two = f"Die Ergebnisse des {feature_name} umfassen {admin_summary['location']} Orte, {admin_summary['city']} Gemeinden und eine Gesamtbevölkerung von etwa {population} Einwohnenden."
        
        return f'{phrase_one} {phrase_two}'
    else:
        return 'Check the language variable'

    
def collectComponentLandMarks(admin_details, language="de"):
    # the column headers are dependent on the language.
    # using the admin_details class identify the component
    # features of interest and have a language appropriate
    # label.
    
    component_list = []
    
    if len(admin_details.lakesOfInterest()) > 0:
        
        if language == "de":
            header = "Seen"
        
        if language == "fr":
            header = "Lacs"
        
        else:
            header = "Lakes"
        
        components = ("Seen",  ", ".join(admin_details.lakes_of_interest))
        
        component_list.append(components)
    
    if len(admin_details.riversOfInterest()) > 0:
        if language == "de":
            header = "Fliessgewässer"
        
        if language == "fr":
            header = "Cours d'eaux"
        
        else:
            header = "Rivers"
        
        components = ("Fliessgewässer",  ", ".join(admin_details.rivers_of_interest))
        
        component_list.append(components)
        
    if language == "de":
        city_header = "Gemeinden"
        
    if language == "fr":
        city_header = "Communes"
        
    else:
        city_header = "Municipalities"
        
    munis = ("Gemeinden", ", ".join(sorted(admin_details.populationKeys()["city"])))
    
    component_list.append(munis)
    
    return component_list
 
    
class verticalText(Flowable):

    '''Rotates a text in a table cell.'''

    def __init__(self, text):
        Flowable.__init__(self)
        self.text = text

    def draw(self):
        canvas = self.canv
        canvas.rotate(90)
        fs = 8
        canvas.translate(1, -fs/1)  # canvas._leading?
        canvas.drawString(0, 0, self.text)

    def wrap(self, aW, aH):
        canv = self.canv
        fn, fs = canv._fontname, 8
        return canv._leading, 1 + canv.stringWidth(self.text, fn, fs)

  
def aStyledTable(data, header_style: Paragraph = styled_table_header, vertical_header: bool = False,
                 data_style: Paragraph = table_style_centered, colWidths: list = None, style: list = None,
                 gradient: bool = False, caption: str = None, caption_location: str = "BOTTOM", caption_style: () = caption_style):
    table_data = data.reset_index()
    # print(data.columns)
    # print(data.head())
    # print(table_data.columns)
    # print(table_data.head())
    if vertical_header:
        headers = [verticalText(x) for x in data.columns]
        headers = [verticalText(" "), *headers]
    else:
        headers = [Paragraph(str(x), header_style)  for x in data.columns]
        headers = [Paragraph(" ", table_style_centered) , *headers]
    
    if style is None:
        style = default_table_style

    new_rows = []
    for a_row in table_data.values.tolist():
        
        if isinstance(a_row[0], str):
            row_index = Paragraph(a_row[0], table_style_right)
            row_data = [Paragraph(str(x), data_style) for x in a_row[1:]]
            new_row = [row_index, *row_data]
            new_rows.append(new_row)
        else:
            row_data = [Paragraph(str(x), data_style) for x in a_row[1:]]
            new_rows.append(row_data)
        
    new_table = [headers, *new_rows]
    table = Table(new_table, style=style, colWidths=colWidths, repeatRows=1)
    # the width of the caption should match the width of the table
    table_width = sum(colWidths)/cm
    left_indent = round((21 - table_width)/2, 1)
    
    caption_kwargs = {
        "name": "caption_style",
        "fontSize": 9,
        "fontName": "Times-Italic",
       
    }
    new_caption_style = ParagraphStyle(**caption_kwargs)
    table_caption = Paragraph(caption, new_caption_style)
    
    if gradient:
        table_color_gradient = colorGradientTable(data)
        table.setStyle(table_color_gradient)
    table.hAlign = 'CENTER'
        
    if caption_location == "BOTTOM":
        
        return KeepTogether([table, smallest_space, table_caption])
    else:
        return KeepTogether([table_caption, smallest_space, table])


def aSingleStyledTable(data, header_style: Paragraph = styled_table_header, vertical_header: bool = False,
                       data_style: Paragraph = table_style_centered, colWidths: list = None, style: list = None,
                       gradient: bool = False):
    table_data = data.reset_index()
    
    
    if vertical_header:
        headers = [verticalText(x) for x in data.columns]
        headers = [verticalText(" "), *headers]
    else:
        headers = [Paragraph(str(x), header_style) for x in data.columns]
        headers = [Paragraph(" ", table_style_centered), *headers]
    
    if style is None:
        style = TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('INNERGRID', (1, 1), (-1, -1), 0.25, HexColor("#8b451330", hasAlpha=True)),
            ('ROWBACKGROUNDS', (1, 1), (-1, -1), [HexColor("#8b451320", hasAlpha=True), colors.white]),
            ('TOPPADDING', (0, 0), (-1, -1), 1),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
            ('VALIGN', (1, 0), (-1, -1), "MIDDLE")
        ])
    
    new_rows = []
    for a_row in table_data.values.tolist():
        
        
        if isinstance(a_row[0], str):
            row_index = Paragraph(a_row[0], table_style_right)
            row_data = [Paragraph(replaceDecimal(x), data_style) for x in a_row[1:]]
            new_row = [row_index, *row_data]
            new_rows.append(new_row)
        else:
            row_data = [Paragraph(replaceDecimal(x), data_style) for x in a_row[1:]]
            new_rows.append(row_data)
    
    if gradient:
        # print("This is a gradient")
        table_color_gradient = colorGradientTable(data)
        elements = [x for x in table_color_gradient.getCommands()]
        for element in elements:
            style.add(*element)
            
    
        
    
    new_table = [headers, *new_rows]
    # print(len(style.getCommands()))
    table = Table(new_table, style=style, colWidths=colWidths, hAlign="CENTER", repeatRows=1)
    
    return table


def tableAndCaption(table, caption, col_widths):
    table_and_caption_data = [[table], [caption]]
    
    colWidths = [sum(col_widths) + .25 * cm]
    # print("\n colWidths table and captions \n")
    # print(colWidths)
    
    table_and_caption = Table(table_and_caption_data, colWidths=colWidths, style=figure_table_style)
    
    return table_and_caption
def aStyledTableExtended(data, row_header: int=0, row_ends: int=-3, caption_prefix: str = None,
                         header_style: Paragraph = styled_table_header, vertical_header: bool = False,
                         data_style: Paragraph = table_style_centered, gradient: bool = False, colWidths: list = None,
                         style: list = None, caption_location: str = "BOTTOM"):
    
    table_data = data.reset_index()
    cols = table_data.columns

    first_col = cols[row_header]
    # print(first_col)
    last_cols = cols[row_ends:]
    start_data_cols = row_header+1
    # print(cols[start_data_cols])
    data_cols = cols[start_data_cols: row_ends]
    # print(data_cols)
    
    if len(data_cols)%2 == 0:
        first_table_stop = int(len(data_cols)/2)
        first_table_cols = cols[start_data_cols: first_table_stop]
        second_table_cols = cols[first_table_stop: row_ends]
        
    if len(data_cols)%2 == 1:
        first_table_stop = int((len(data_cols)+1)/2)+1
        first_table_cols = cols[start_data_cols: first_table_stop]
        second_table_cols = cols[first_table_stop:row_ends]
        # print(second_table_cols)
        
    first_table_data = table_data[[first_col, *first_table_cols, *last_cols]].set_index(first_col)
    second_table_data = table_data[[first_col, *second_table_cols, *last_cols]].set_index(first_col)
    # print(first_table_data.head())

    if style is None:
        style = default_table_style
    
    table_kwargs = {
        "header_style": header_style,
        "vertical_header": vertical_header,
        "data_style": data_style,
        "style": style,
        "caption_location": caption_location
    }
    
    table_kwargs.update({"colWidths": colWidths})
    
    table_one_caption = f'{caption_prefix}, {", ".join(first_table_cols)}'
    table_one_caption = Paragraph(table_one_caption, caption_style)
    col_widths = [colWidths[0], *[1.2 * cm] * len(first_table_data.columns)]
    table_one = aSingleStyledTable(first_table_data, colWidths=col_widths, gradient=True, vertical_header=vertical_header)
    table_one_and_caption = tableAndCaption(table_one, table_one_caption, col_widths)

    table_two_caption = f'{caption_prefix}, {", ".join(second_table_cols)}'
    table_two_caption = Paragraph(table_two_caption, caption_style)
    col_widths = [colWidths[0], *[1.2 * cm] * len(second_table_data.columns)]
    table_two = aSingleStyledTable(second_table_data, colWidths=col_widths, gradient=True, vertical_header=vertical_header)
    table_two_and_caption = tableAndCaption(table_two, table_two_caption, col_widths)
    
    return [table_one_and_caption, small_space, table_two_and_caption]
            
    

def colorGradient(x, cmap: str="YlOrBr", amin: int=0, amax: int=1):
    a_cmap = plt.cm.get_cmap(cmap)
    norm = mpl.colors.Normalize(vmin=amin, vmax=amax)
    color = a_cmap(norm(x))
    hex_color = mpl.colors.rgb2hex(color, keep_alpha=False)
    
    return hex_color

def stringifyValue(x):
    if isinstance(x, str):
        return x
    else:
        return str(x)
    
def colorGradientTable(data, color_gradient: callable=colorGradient, column: int=None):
    
    gradient_cells = TableStyle()
    a_min = data.min().min()
    a_max = data.max().max()
    change_font_color = a_max * .5
    
    if column is None:
        for i, row in enumerate(data.values):
            for j, element in enumerate(row):
                hex_color = colorGradient(element, amin=a_min, amax=a_max)
                gradient_cells.add('BACKGROUND', (j+1, i+1), (j+1, i+1), hex_color)
                if element > change_font_color:
                    gradient_cells.add('TEXTCOLOR', (j + 1, i + 1), (j + 1, i + 1), colors.white)
    
    elif isinstance(column, int) and column < len(data.values[0]):
        for i, row in enumerate(data.values):
            hex_color = colorGradient(row[column])
            gradient_cells.add('BACKGROUND', (column+1,i+1), (column+1,i+1), hex_color)
            if row[column] > change_font_color:
                gradient_cells.add('TEXTCOLOR', (column+1,i+1), (column+1,i+1), colors.white)
            
    else:
        print("ouch")
    
    return gradient_cells

def rotateText(x):
    return 'writing-mode: vertical-lr; transform: rotate(-180deg);  padding:10px; margins:0; vertical-align: baseline;'


def figureAndCaptionTable(image_file: str = None, caption: a_flowable_paragraph = None, desired_width: float = None,
                          caption_height: float = None, original_width: float = None, original_height: float = None,
                          style: list = figure_table_style,  hAlign: str = "CENTER"):
    if desired_width == original_width:
        height = (original_height + 0.5) * cm
    else:
        height = (desired_width * original_height / original_width + 0.5) * cm
    
    figure = Image(image_file, width=desired_width * cm, height=height, kind="proportional", hAlign=hAlign)
    
    if caption is None:
        return figure
        
    figure_and_caption_data = [[figure], [caption]]
    
    colWidths = [(desired_width + .05) * cm]
    rowHeights = [height, caption_height * cm]
    
    figure_and_caption = Table(figure_and_caption_data, colWidths=colWidths, rowHeights=rowHeights,
                               style=figure_table_style, hAlign=hAlign)
    
    return figure_and_caption


def aStyledTableWithTitleRow(data, header_style: Paragraph = styled_table_header, title: str = None,
                             data_style: Paragraph = table_style_centered, colWidths: list = None, style: list = None):
    table_data = data.reset_index()
    
    headers = [Paragraph(str(x), header_style) for x in data.columns]
    headers = [Paragraph(" ", data_style), *headers]
    
    if style is None:
        style = default_table_style
    
    new_rows = []
    for a_row in table_data.values.tolist():
        
        if isinstance(a_row[0], str):
            row_index = Paragraph(a_row[0], table_style_right)
            row_data = [Paragraph(str(x), data_style) for x in a_row[1:]]
            new_row = [row_index, *row_data]
            new_rows.append(new_row)
        else:
            row_data = [Paragraph(str(x), data_style) for x in a_row[1:]]
            new_rows.append(row_data)
    
    table_title_style = [
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('ROWBACKGROUND', (0, 0), (-1, -1), [colors.white]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3)
    
    ]
    
    table_title = Table([[title]], style=table_title_style, colWidths=sum(colWidths))
    new_table = [[table_title], headers, *new_rows]
    table = Table(new_table, style=style, colWidths=colWidths, repeatRows=2)
    
    return table


def splitTableWidth(data, caption_prefix: str = None, caption: str = None, gradient=False,
                    this_feature: str = None, vertical_header: bool = False,
                    colWidths=[4 * cm, *[None] * 4], rowends: int = -2):
    # print(len(data.columns))
    
    if len(data.columns) > 13:
        tables = aStyledTableExtended(data, gradient=gradient, caption_prefix=caption_prefix,
                                      vertical_header=vertical_header, colWidths=colWidths, row_ends=rowends)
    else:
        tables = aSingleStyledTable(data, vertical_header=vertical_header, gradient=gradient,
                                                colWidths=colWidths)
        table_cap = f'{caption_prefix}, {", ".join(data.columns)}'
        table_cap = Paragraph(table_cap, style=caption_style)
        tables = tableAndCaption(tables, table_cap, colWidths)
    
    return tables

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


def make_plot_with_spearmans(data, ax, n, unit_label="p/100m"):
    """Gets Spearmans ranked correlation and make A/B scatter plot. Must proived a
    matplotlib axis object.
    """
    corr, a_p = stats.spearmanr(data[n], data[unit_label])
    
    if a_p < 0.05:
        if corr > 0:
            ax.patch.set_facecolor("salmon")
            ax.patch.set_alpha(0.5)
        else:
            ax.patch.set_facecolor("palegoldenrod")
            ax.patch.set_alpha(0.5)
    
    return ax, corr, a_p
