"""
The feature data module contains all the process used to generate the
survey area and water body reports in ver 1.0 of the end-of-sampling report.

The FeatureData class is the base component of the module. When instantiated
the class has no valid attributes. The attributes define the units of
measurement, start and end dates, fail rates and the location labels to
create a hierarchical summary of survey results.

The class produces numerical results that can be in the form of a numpy
array, dictionary or a pandas data-frame. Intended to be used with the
data visualization modules, the default output for each method integrates
directly into the current visualization options.
"""
import pandas as pd
fd_var = {
    "sdate": "2020-03-01",
    "edate": "2021-05-31",
    "unit_label": "p/100m",
    "a_fail_rate": 50,
    "a_unit_length": 100
}

# set the different aggregation levels
# the aggregation level of interest is defined by level
# component are units of level
# top is all the data
# loi is the named feature(s) to be considered
# basin is the river bassin that the feature(s) are in
# top and bassin_label are used for charting

loc_var = {
    "name": "Zurichsee",
    "component": "city",
    "basin_slug": "linth",
    "basin_label": "Linth/Limmat survey area",
    "loi": ["zurichsee"],
    "top": "All survey areas",
    "level": "water_body"
}

data_source = {
  "beachsource": "resources/beaches_with_land_use_rates.csv",
  "codesource": "resources/codes_with_group_names_2015.csv",
  "dimsource": "resources/corrected_dims.csv",
  "notaggsource": "resources/checked_before_agg_sdata_eos_2020_21.csv",
  "fd_data": "resources/checked_sdata_eos_2020_21.csv"
}

column_rename = {
    "% to agg": "% ag",
    "% to recreation": "% recreation",
    "% to woods": "% woods",
    "% to buildings": "% buildings",
    "loc_date": "sample",
    "water_name_slug": "water_body",
    "river_bassin": "basin"
    }

columns = [
    "sample", "location",
    "city", "water_body",
    "date", "quantity", "population"
    ]

explanatory_variables = [
    "% buildings", "% recreation",
    "% ag", "% woods", "streets km",
    "intersects"
    ]

dim_to_agg = {
    'length': 'sum',
    'area': 'sum',
    'mac_plast_w': 'sum',
    'mic_plas_w': 'sum',
    'total_w': 'sum'
}


def load_defaults(x, def_vals: list = [fd_var, loc_var, data_source]):
    """Loads a list of dictionaries to  the class attributes

    All the attributes can be loaded at once, by providing a list of
    dictionaries.

    :param x: The class instance
    :type x: class
    :param def_vals: The array of class attributes
    :type def_vals: list
    :return: The attributes are updated with the dictionaries
    :rtype: None
    """

    for atts in def_vals:
        x.add_attributes(atts)


def add_attributes(a, attributes):
    """Adds the key, value pairs from a dict as attributes to a class

    :param a: An instance of FeatureData
    :type a: class
    :param attributes: The attributes to be added to the class instance
    :type attributes: dict
    :return: The attributes are added to the class instance
    :rtype: None
    """

    for k, v in attributes.items():
        setattr(a, k, v)


def feature_data(data, level: str = None, loi: list = [],
                 slice_data: bool = True):
    """Slices the data at the feature level for the features in loi.

    :param data: A pandas data frame of survey results
    :type data: object: pandas.core.frame.DataFrame
    :param level: Column name that has will be aggregated on
    :type level: str
    :param loi: An array of values that are contained in feature_level
    :type loi: array
    :param slice_data: Indicate whether the data needs to be sliced
    :type slice_data: bool
    :return: A sliced data frame with the date converted to datetime object
    :rtype: pandas.core.frame.DataFrame
    """

    if slice_data:
        sliced_data = data[data[level].isin(loi)].copy()
    else:
        sliced_data = data.copy()
    # the sample is the unique indentifier for a survey
    sliced_data["sample"] = list(zip(sliced_data.location.values,
                                     sliced_data["date"].values)
                                   )

    # ensure that the date is set to datetime
    sliced_data["date"] = pd.to_datetime(sliced_data["date"])

    return sliced_data


# check that the required attribute is present for a requested operation
def check_for_these_attributes(aninstance, attributes: list = []):
    """Checks the current instance for the required attribute

    This compares the requested attributes for a method against the
    current attributes. Returns True or False and the array of missing
    attributes. Called internally for each method.

    :param aninstance: An valid class instance
    :type aninstance: class
    :param attributes: A list of required attributes
    :type attributes: list
    :return: True or False and an array of missing values, empty if
    none missing.
    :rtype: boolean, list
    """
    current = aninstance.inst_attributes()
    not_current = [x for x in attributes if x not in current.keys()]
    if len(not_current):
        proceed = False
    else:
        proceed = True

    return proceed, not_current


def check_attribute_of_this(aninstance, this: str = None, atype: str = None):
    """Checks the current instance for the required attribute and type

    This compares the required attributes for a method against the
    current class attributes. If the required attribute exists its
    type is compared to the required type at that instance.

    :param aninstance: An valid class instance
    :type aninstance: class
    :param this: A class attribute that is required
    :type this: str
    :param atype: A valid python data type
    :type atype: Can be any type
    :return: True or False, if the proposed attributed exists and it
    matches the data type required by the method.
    :rtype: boolean
    """
    stat, _ = check_for_these_attributes(aninstance, attributes=[this])

    # if the attribute exists in this instance
    if stat:
        # fetch it and see that it matches the requirement
        # for the current mehtod
        data = getattr(aninstance, this)
        is_an_inst = isinstance(data, atype)
        # if true proceed
        if is_an_inst:
            proceed = True
        else:
            proceed = False
    else:
        proceed = False
    return proceed


class FeatureData:
    """The FeatureData class slices the data by user defined variables.

    The class creates two different sets, one with all the data the other
    with just the results from the loi. The summary statistics for the loi
    and all the data are available as attributes of the class.
    """

    def __init__(self, name: str = None, level: str = None,
                 component: str = None,
                 min_att: list = ["level", "loi", "sdate", "edate"]
                 ) -> None:
        self.name = name
        self.level = level
        self.component = component
        self.min_att = min_att

    # use this method to add attributes to the class
    def add_attributes(self, attributes: dict = {}):
        """Updates the attributes of the class

        Can be used to create new attributes or modify existing ones. The
        keys of the dictionary become class attributes with the
        corresponding value.

        :param attributes: Key, value pairs of {"attribute label": "value"}
        :type attributes: dict
        :return: Values get added to class attributes
        :rtype: None
        """
        for k, v in attributes.items():
            setattr(self, k, v)

    # the value of class attributes
    def inst_attributes(self):
        """Displays the current class attributes

        Provides a dict of all the current class attributes and the data
        types.

        :param self: Calls an instance of self
        :return: A dictionary of all the current attributes and data type
        :rtype: dict
        """
        data = {k: type(v) for k, v in self.__dict__.items()}
        return data



    def make_fd(self, sources: list = [],
                new_column_names : dict = column_rename):
        """Applies the user defined variables to construct the feature data

        Make_fd is the base method for this class. It assigns a unique id for
        each survey, slices the data by start and end dates and applies
        self.level and self.loi to slice the data by hierarchical types.

        Provides two sets of data for each source. One set has all the
        data within the date range, the other is a slice with just the data
        from the loi attribute.

        :param sources: A list that has the attribute name for the data source
        :type sources: list
        :param new_column_names: The map from old names to new names
        :type new_column_names: dict, gets passed to df.rename
        :return: Results are added as attributes to the class
        :rtype: None
        """

        # check for the required attributes
        # source of data, locations of interest
        status, labels = check_for_these_attributes(
            self, attributes = [*self.min_att, *sources])

        if status:
            # if all the attributes are present
            # make the feature data, add as class attribute
            for x in sources:
                # the location of the file is an attribute of the class
                location = getattr(self, x)
                # get the data
                a = pd.read_csv(location)
                # format the unique survey id
                if new_column_names:
                    a.rename(columns=new_column_names, inplace=True)

                a["sample"] = list(zip(a["location"], a["date"]))
                # set to datetime
                a["date"] = pd.to_datetime(a["date"])
                # slice by start and end
                aslice = (a["date"] >= self.sdate) & (a["date"] <= self.edate)
                ad = a[aslice].copy()

                # assign all the data as an attribute
                new_name = f"a_data_fd"
                setattr(self, new_name, ad)

                # slice the data by the location attributes
                fd = feature_data(ad, self.level, loi=self.loi)
                # assign the feature data as an attribute
                setattr(self, "fd", fd)

        else:
            # if not identify the missing attributes
            # print to console
            print("The following attributes are undefined", labels)

    def change_column_names(self, attname: str = "fd", renames: dict =
                            column_rename):
        """User defined column names are added here"""
        status, labels = self.check_for_these_attributes([attname])
        if status:
            data = getattr(self, attname)
            if isinstance(data, pd.core.frame.DataFrame):
                data.rename(columns=renames, inplace=True)
                setattr(self, attname, data)
            else:
                print("that attribute is not a dataframe")
        else:
            print("there is no attribute with that name")

    def summary(self, attname: str = "fd"):
        """The summary of samples, cities and population in the data.

        If the columns are present in the survey data attribute: summarizes
        the number of locations, samples, cities, population and quantity for
        the provided data.

        :param attname: An instance attribute that is a dataframe
        :type attname: str
        :return: Results are added as attributes to the class instance
        :rtype: None
        """
        # the required columns
        required = ["population", "sample",
                    self.component, "location",
                    "quantity"
                    ]

        # retrieve the attribute that has the data
        atype = pd.core.frame.DataFrame
        # check the type against the required
        proceed = check_attribute_of_this(self, this = attname, atype = atype)

        if proceed:
            somdata = getattr(self, attname)
            # if somdata resolves to a data frame
            cols = [x for x in required if x in somdata.columns]
            # this holds the summary values if len(cols) > 0
            # gets added as an attribute of the class instance
            asummary = dict()

            if len(cols):
                # provide a summary of the different column values
                for acol in cols:
                    if acol in ["sample", self.component, "location"]:
                        asummary.update({acol: somdata[acol].nunique()})
                    if acol in [self.component, "location"]:
                        asummary.update({
                            f"{acol}_list": somdata[acol].unique()
                        })
                    if acol == "quantity":
                        asummary.update({acol: somdata.quantity.sum()})
                    if acol == "population":
                        popd = somdata[
                            ["city", "population"]
                        ].drop_duplicates()
                        population = popd.population.sum()
                        asummary.update({acol: population})
                # set the asummary dict as an attribute of the instance
                setattr(self, f"{attname}_summary", asummary)
            else:
                # the summary cannot be completed
                print("The required columns are not in the dataframe")
        else:
            # either use a different attribute or load the data
            print("That attribute does not resolve to a dataframe")


    def code_totals(self, attname: str = "fd"):
        """ The cumulative values of the codes for the requested data.

        The total number of each object code identified. The % of the total
        numer of objects, the fail rate and the median unit_label value is
        also calculated. The results are added as attributes to the class
        instance.

        :param attname: An instance attribute that is a dataframe
        :type attname: str
        :return: Results are added as attributes to the class instance
        :rtype: None
        """

        atype = pd.core.frame.DataFrame
        proceed = check_attribute_of_this(self, this = attname, atype = atype)

        if proceed:
            somdata = getattr(self, attname)
            required = ["sample", "code", "quantity", self.unit_label]
            cols = [x for x in required if x in somdata.columns]

            if len(cols) == len(required):
                # per sample numbers
                g_one = ["sample", "code"]
                agg_this = {self.unit_label: "sum", "quantity": "sum"}
                a = somdata.groupby(g_one, as_index=False).agg(agg_this)

                # count the number of times none were found
                a["fail"] = a.quantity > 0
                aggthat = {"fail": "sum",
                           "quantity": "sum",
                           self.unit_label: "median"}

                b = a.groupby("code").agg(aggthat)
                b["% of total"] = b.quantity/b.quantity.sum()
                b["fail rate"] = b.fail/somdata["sample"].nunique()

                setattr(self, f"{attname}_codetotals", b)
            else:
                print("The required columns are not in the dataframe")
        else:
            print("That is not a valid attribute for this method")

    def survey_summary(self, attname: str = "fd"):
        """Aggregates the total for each survey and summarizes the results.

        Survey summary aggregates the unit_label variable to the unique
        survey id. Producing the survey total for each survey. The summary
        is the default of pands.series.describe. The results (the time
        series data of survey results and the summary) are
        added as attributes to the class instance.

        :param attname: An instance attribute that is a dataframe
        :type attname: str
        :return: Results are added as attributes to the class instance
        :rtype: None
        """
        atype = pd.core.frame.DataFrame
        proceed = check_attribute_of_this(self, this = attname, atype = atype)

        if proceed:
            somdata = getattr(self, attname)
            required = ["sample", "date", self.unit_label]
            cols = [x for x in required if x in somdata.columns]
            if len(cols) == len(required):
                sids = ["sample", "date"]
                a = somdata.groupby(sids, as_index=False)[
                    self.unit_label
                    ].sum()
                setattr(self, f"{attname}_surveytotals", a)

                asummary = a[self.unit_label].describe()
                setattr(self, f"{attname}_surveysummary", asummary)

            else:
                print("The required columns are not in the dataframe")
        else:
            print("That is not a valid attribute for this method")

    def component_summary(self, attname: str = 'fd'):
        """Aggregates survey results of the components

        Provides the number of samples, the total number of objects and the
        median unit_label value for each of the components.

        :param attname: An instance attribute that is a dataframe
        :type attname: str
        :return: Results are added as attributes to the class instance
        :rtype: None
        """

        atype = pd.core.frame.DataFrame
        proceed = check_attribute_of_this(self, this = attname, atype = atype)

        if proceed:

            somdata = getattr(self, attname)
            required = ["sample", "date",
                        self.unit_label,
                        self.component,
                        "quantity"]
            cols = [x for x in required if x in somdata.columns]

            if len(cols) == len(required):
                sids = [self.component, "sample"]
                agg_this = {self.unit_label: "sum", "quantity": "sum"}
                a = somdata.groupby(sids, as_index=False).agg(agg_this)
                asum = {self.unit_label: "median", "quantity": "sum",
                        "sample": "nunique"}
                b = a.groupby(self.component, as_index=False).agg(asum)
                setattr(self, f"{attname}_components", b)

            else:
                print("The required columns are not in the dataframe")
        else:
            print("That attribute does not resolve to a dataframe")

    def make_complete_summary(self, attname: str = "fd_data"):
        """Calls all the methods to create a summary"""

        self.make_fd([attname])
        self.summary()
        self.code_totals()
        self.survey_summary()
        self.component_summary()


class DimensionalData:
    def __init__(self, atts: object = None, to_aggregate: dict = dim_to_agg):

        if atts:
            self.is_valid_instance(atts, required=self.required)
            self.to_aggregate = to_aggregate

        else:
            print("This requires an instance of .make_complete_summary()")

    required = [
        "dimsource", "fd_summary", "beachsource", "name",
        "fd_components", "sdate", "edate", "component"
    ]

    def is_valid_instance(self, atts, required: list = required):
        proceed = check_for_these_attributes(atts, attributes=required)
        if proceed:
            for aname in required:
                this_att = getattr(atts, aname)
                setattr(self, aname, this_att)
        else:
            print("The class instance does not have the required attributes")



    def make_dims_data(self):
        """The dimensional data for an instance of FeatureData

        The attributes are defined by an instance of FeatureData that has
        a value for <class instance>.fd_components.

        :return:
        """

        # slice the dimensional data by the attributes
        # provided by the class instance
        somdata = pd.read_csv(self.dimsource)
        somdata["date"] = pd.to_datetime(somdata["date"])

        # start and end dates
        by_date = ((somdata["date"] >= self.sdate) &
                   (somdata["date"] <= self.edate)
                   )
        # the sample locations
        by_location = (somdata.location.isin(
            self.fd_summary["location_list"])
        )

        # the dimensional data
        ddata = somdata[by_date & by_location].copy()

        # map the slug/location to the correct component value
        beachdata = pd.read_csv(self.beachsource)
        component_map = beachdata[["slug", self.component]].set_index("slug")

        # assign the value to the dimensional data
        ddata[self.component] = ddata.location.map(
            lambda x: component_map.loc[x][self.component]
        )

        # assign as attributes to the current instance

        setattr(self, "dims_data", ddata)
        setattr(self, "beach_data", beachdata)

    def make_component_summary(self):
        """Summarizes the cumulative values of the components

        Includes the values from FeatureData.component_summary().
        """

        a = self.dims_data.groupby(self.component).agg(self.to_aggregate)
        b = self.fd_components.set_index(self.component, drop = True)

        dim_summary = pd.concat([a,b], axis=1)
        dim_summary.loc[self.name] = dim_summary.iloc[:, :-1].sum()

        setattr(self, "dims_summary", dim_summary)


