.. role:: raw-html(raw)
    :format: html

===============
Feature Data
===============

.. automodule:: feature_data

**Key points**

1. The attributes define the source of the data, the region of analysis, the units and the date range of the report
2. The attributes are dictionaries that can be loaded from the module or command line
3. The attributes can be changed at anytime

Attributes
_____________

**Dimensional**

There are three types of required attributes: dimensional, location and surveydata. The dimensional
attributes define the start and end date, the units (meters), the fail rate (%) and the unit
length (meters).

.. code-block:: python
  :caption: Default dimensional attributes

  fd_var = {
      "sdate": "2020-03-01",
      "edate": "2021-05-31",
      "unit_label": "p/100m",
      "a_fail_rate": 50,
      "a_unit_length": 100
  }

The unit_label attribute refers to a column in the existing data and will be used as an axis label and
column head for all outputs. If a different unit-length and unit_label are required then the column
must be created before the data is added to the class. The default attributes will slice the data by the
start and end dates and generate summaries based on pieces per 100 meters (p/100m) and a fail rate >/= 50%.

**Location**

The location attributes define the geographic bounds of the summary. Each survey location has at least
three different location definitions (columns in the data-frame): city, water-body and river basin. The summary
structure is set by defining the level and component attributes. The level attribute is the region of interest,
the component attribute defines the smallest hierarchical unit of the summary.

.. code-block:: python
  :caption: Default location attributes

  loc_var = {
      "name": "Zurichsee", # the title of the report
      "component": "city", # the smallest unit
      "basin_slug": "linth", # the river basin identifier
      "basin_label": "Linth/Limmat survey area", # the label for the river bassin
      "loi": ["zurichsee"], # these resolve to values in <level>
      "top": "All survey areas", # the top level aggregation
      "level": "water_name_slug" # the column name where <loi> values can be found
  }

The example above will produce the data for a report that summarizes the survey results
from Zurichsee and the cities that are on Zurichsee. The results will include the summarized values
for (i) the linth river bassin and (ii) all the data.

The baseline values and most common objects are defined by the data from the <level> attribute. The results can then
be compared from the context of the region of interest both up and down the hierarchical chain.

Data attributes
----------------

The data attributes define the file names (location) of the data. Three data sources are required; (i) survey data, (ii)
location data and (iii) code or object data.

For each set of data there are required columns and data types. The



.. code-block:: python
   :caption: The data attribute

    data_source = {
      "codes": "file-name.csv",
      "locations": "file-name.csv",
      "surveys": "file-name.csv"
    }

**Survey data**

The survey data is the actual counts per object and survey. The survey data must be in long form so that each row is an
object count with the date, location, code, quantity, shoreline length and unit_label value.

.. table:: Example long form survey data
  :widths: 20,20,10,10,10,20

  +-------------+---------------+--------+-----+--------+--------+-------------------------------+
  |     date    | location      | code   | qty | length | p/100m |        loc_date               |
  +=============+===============+========+=====+========+========+===============================+
  | 20-08-13    |  mullermatte  |  G95   | 20  |    40  |    50  | ("mullermatte", "2020-08-12") |
  +-------------+---------------+--------+-----+--------+--------+-------------------------------+

The example above is the count of cotton-swabs found at a survey at mullermatte on August 13, 2020. A survey
would contain several of these rows.

**Code data**

The code data contains the definition of each code, the material classification and any group labels
that are in use. The code data is related to the survey value by the "code" field.

.. table:: Example code data
  :widths: 10,40,30,20

  +------+--------------+----------+---------+
  | code | description  | material | group   |
  +======+==============+==========+=========+
  | G95  | cotton swabs | plastic  | hygiene |
  +------+--------------+----------+---------+

The description field is used as labels for all charts and tables that display the data after the
aggregated results are defined. The material field is used to calculate the material percentages from
survey totals.

**Location data**

The location data contains the reference values for the *location* attributes. Specifically the city, water-body and river
basin labels. If a differentiation between rivers and lakes is desired the column must exist in the location data.

.. table:: Example location data
  :widths: 20,20,20,20,20

  +-------------+-------------+------------+-------------+---------+
  | location    | city        | water body | river basin | ETC...  |
  +=============+=============+============+=============+=========+
  | mullermatte | biel        | bielersee  | aare        | etc..   |
  +-------------+-------------+------------+-------------+---------+

The data provided must have at least the columns defined above for the FeatureData class to function.

Loading attributes
------------------

The attributes are added once a FeatureData object has been instantiated. Attributes can be added one at a time or as a
group. The preferred method is to load all the attributes at once from a dictionary. This method works extremely well if
there are multiple summaries to create and all the survey data is in one file. Once the data sources are assigned, the location
and dimensional attributes can be changed as needed.

.. code-block:: python
  :caption: Example initiating a FeatureData class and loading dimensional attributes


  In [1]: import feature_data as fda
  In [2]: a = fda.FeatureData()
  In [3]: fd_var = {
      "sdate": "2020-03-01",
      "edate": "2021-05-31",
      "unit_label": "p/100m",
      "a_fail_rate": 50,
      "a_unit_length": 100}
  In [4]: a.add_attributes(fd_var)

**Check the status of attributes**

The status of all the attributes can be accessed by calling .inst_attributes() on the current instance
of the class.

.. code-block:: python
  :caption: Checking the status of the class attributes

  In [5]: a.inst_attributes()
  Out[5]:
  {'name': NoneType,
   'level': NoneType,
   'component': NoneType,
   'min_att': list,
   'sdate': str,
   'edate': str,
   'unit_label': str,
   'a_fail_rate': int,
   'a_unit_length': int}

In this example there are no data sources or location attributes. The class will not function and throw an
error. Calling feature_data.load_defaults(<class instance>) with the current instance as the argument loads a
set of attributes that include all the data from Switzerland.

.. code-block:: python
  :caption: Loading the default values:

    In [6]: fda.load_defaults(a)
    In [7]: a.inst_attributes()
    Out[7]:
    {'name': str,
     'level': str,
     'component': str,
     'min_att': list,
     'sdate': str,
     'edate': str,
     'unit_label': str,
     'a_fail_rate': int,
     'a_unit_length': int,
     'basin_slug': str,
     'basin_label': str,
     'loi': list,
     'top': str,
     'beachsource': str, # location data
     'codesource': str, # code data
     'dimsource': str, # additional data sources
     'notaggsource': str, # additional data sources
     'fd': str}

All the required attributes are available and there are additional data sources that can be used. The
min_att attribute is loaded automatically. If the current attributes do not have all the elements of the min_att
attribute no operations can be performed.

Editing attributes
------------------

Attributes can be edited or added at anytime. Once attributes are changed, any report that was run prior to the
change needs to be update with the new values. Notice that the add_attributes() method is used for both adding and
editing.

.. code-block:: python
  :caption: Editing attribute values

  In [1]: import feature_data as fda
  In [2]: a = fda.FeatureData()
  In [3]: fd_var = {
      "sdate": "2020-03-01",
      "edate": "2021-05-31",
      "unit_label": "p/100m",
      "a_fail_rate": 50,
      "a_unit_length": 100}
  In [4]: a.add_attributes(fd_var)
  In [5]: a.sdate
  Out[5]: '2020-03-01'
  In [6]: new_dates = {"sdate": "2021-01-01", "edate": "2021-06-01"}
  In [7]: a.add_attributes(new_dates)
  In [8]: a.sdate
  Out[8]: '2021-01-01'

Once the attributes are set the different reports can be generated from the module.

The attribute methods
_____________________

:raw-html:`<br />`

.. py:method:: FeatureData.add_attributes()

    Updates the attributes of the class

    Can be used to create new attributes or modify existing ones. The
    keys of the dictionary become class attributes with the
    corresponding value.

    :param attributes: Key, value pairs of {"attribute label": "value"}
    :type attributes: dict
    :return: Values get added to class attributes
    :rtype: None

:raw-html:`<br />`

.. py:method:: FeatureData.check_for_these_attributes()

    Checks the current instance for the required attribute

    This compares the requested attributes for a method against the
    current attributes. Returns True or False and the array of missing
    attributes. Called internally for each method.

    :param attributes: A list of required attributes
    :type attributes: list
    :return: True or False and an array of missing values.
    :rtype: boolean, list

:raw-html:`<br />`

.. py:method:: FeatureData.inst_attributes()

    Displays the current class attributes

    Provides a dict of all the current class attributes and the data
    types.

    :param self: Calls an instance of self
    :return: A dictionary of all the current attributes and data type
    :rtype: dict

:raw-html:`<br />`

.. py:method:: feature_data.load_defaults(x, def_vals: list=[fd_var, loc_var, data_source])

    Loads a list of dictionaries to  the class attributes

    All the attributes can be loaded at once, by providing a list of
    dictionaries. The keys become the class attribute labels.

    :param x: The class instance
    :type x: class
    :param def_vals: The array of class attributes
    :type def_vals: list
    :return: The attributes are updated with the dictionaries
    :rtype: None














































