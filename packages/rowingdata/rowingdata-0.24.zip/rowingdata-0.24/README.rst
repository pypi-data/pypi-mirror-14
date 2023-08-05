Rowingdata
--------------

To install 

easy_install rowingdata

Or

$ pip install rowingdata

--------------

To use with Painsled CSV data, simply do

>>> from rowingdata import *
>>> res = rowingdata.rowingdata("testdata.csv")
>>> res.plotmeters_erg()

To use with CrewNerd TCX data, simply do

>>> from rowingdata import *
>>> tcx = rowingdata.TCXParser("2016-03-25-0758.tcx")
>>> tcx.write_csv("example_data.csv")
>>> res = rowingdata.rowingdata("example_data.csv")
>>> res.plotmeters_otw()

To create the colorful plots as well as copy a text summary to the clipboard,
assuming you have a summary file from CrewNerd called 2016-03-25-0758.CSV and 
a TCX file called 2016-03-25-0758.TCX

>>> from rowingdata import *
>>> otwplot.plotrowall("2016-03-25-0758")

Now you will have the summary data on your clipboard

The test data files are in the testdata folder in the install 