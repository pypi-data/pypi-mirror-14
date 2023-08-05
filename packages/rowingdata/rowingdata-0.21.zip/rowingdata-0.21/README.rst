Rowingdata

-------------

To use with Painsled CSV data, simply do

>>> import rowingdata
>>> res = rowingdata.rowingdata("testdata.csv")
>>> res.plotmeters_erg()

To use with CrewNerd TCX data, simply do

>>> import rowingdata
>>> tcx = rowingdata.TCXParser("example.tcx")
>>> tcx.write_csv("example_data.csv")
>>> res = rowingdata.rowingdata("example_data.csv")
>>> res.plotmeters_otw()

To create the colorful plots as well as copy a text summary to the clipboard,
assuming you have a summary file from CrewNerd called 2016-03-25-0758.CSV and 
a TCX file called 2016-03-25-0758.TCX

>>> import otwplot
>>> otwplot.plotrowall("2016-03-25-0758")