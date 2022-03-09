.. role:: raw-html(raw)
    :format: html

============
Start here
============

The litter-sampler is a series of methods based on pandas 1.4 and python 3.7 that creates a complete report of litter survey results.
The litter survey results must be in long form, each row represents the survey result for each object. Data and report variables are managed using class
attributes. Check the :ref:`data-attributes` section for the required column names and details on loading and editing attributes.

Getting started is easy with the default data set (Switzerland 2020/2021):

.. code-block:: python
    :caption: Loading default values

    In [1]: import feature_data as fda
    In [2]: a = fda.load_defaults(fda.FeatureData())

The defaults load the data defined in the attributes and produces a set of standard reports for each region and the designated
sub-regions. The default data set is based on the survey results from Zurichsee. There are four reports generated when load_defaults
is called.

Available reports
=================

**Feature data summary**

.. code-block:: python
    :caption: Feature data summary example

    In [3]: a.fd_summary
    Out[3]:
    {'population': 504874.0,
     'sample': 56,
     'city': 7,
     'city_list': ['Rapperswil-Jona',
                   'Richterswil',
                   'Freienbach',
                   'Küsnacht (ZH)',
                   'Zürich',
                   'Stäfa',
                   'Schmerikon'
                   ],
     'location': 11,
     'location_list': ['rastplatz-stampf',
                      'zuerichsee_richterswil_benkoem_2',
                      'pfafikon-bad',
                      'zurichsee_kusnachterhorn_thirkell-whitej',
                      'zurichsee_wollishofen_langendorfm',
                      'zurcher-strand', 'zuerichsee_staefa_hennm',
                      'zuerichsee_waedenswil_colomboc_1',
                      'schmerikon-bahnhof-strand', 'aabach',
                      'strandbeiz'],
     'quantity': 5192}

The fd_summary is the top level summary and summarizes the effected population, the number of samples, the number of cities,
the names of the cities, the number of locations and their names as well as the number of objects
collected.

**Code totals**

The code totals report gives the total quantity of each object, the % of total with respect to the feature data,
the fail rate and the median survey value (using the unit of measurement provided in the attributes). This method
also provides the list of most common objects based on user defined criteria.

**Component summary**

The components are the lowest aggregation unit. In the current example, the city is the designated component. The component
summary details the number of samples, the median sample value (user defined units) and the quantity collected for each component.

**Survey summary**

The survey summary aggregates the total quantity and pieces of litter per unit of measure for each survey in the
feature-data. This produces a time series of survey results and the descriptive statistics for the time series.
