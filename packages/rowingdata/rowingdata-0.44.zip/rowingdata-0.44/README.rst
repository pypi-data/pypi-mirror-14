==============
Rowingdata
==============

Based on python code by Greg Smith (https://quantifiedrowing.wordpress.com/) 
and inspired by the RowPro Dan Burpee spreadsheet (http://www.sub7irc.com/RP_Split_Template.zip)

To install 
===============

$ easy_install rowingdata

Or

$ pip install rowingdata


To upgrade:

$ pip install --upgrade rowingdata

or 

$ easy_install --upgrade rowingdata

Release Notes:
================

0.43
--------

- Attempting to remove the dubious DataFrame copy errors using df.loc

0.42
--------
- Added RowPro CSV Parser
- Added summary statistics and interval statistics (also copies the output to clipboard)
- Interval statistics now (sort of) works for Desktop Painsled data


To Use 
==================

Beta. Use with caution. 

Import the package

>>> from rowingdata import *


If you're not me (or have identical heart rate thresholds), 
you will have to change the default values for the rower. For example:

>>> myrower = rowingdata.rower(hrut2=100,hrut1=120,hrat=140,hrtr=150,hran=170,hrmax=180)

To use with Painsled CSV data, simply do

>>> row = rowingdata.rowingdata("testdata.csv",rower=myrower)
>>> row.plotmeters_erg()
>>> print row.allstats()

To use with RowPro CSV data, simply do

>>> rp = rowingdata.RowProParser("RP_testdata.csv")
>>> rp.write_csv("example_data.csv")
>>> row = rowingdata.rowingdata("example_data.csv")
>>> row.plotmeters_erg()
>>> row.plottime_erg()
>>> print row.summary()

To use with CrewNerd TCX data, simply do

>>> tcx = rowingdata.TCXParser("2016-03-25-0758.tcx")
>>> tcx.write_csv("example_data.csv")
>>> row = rowingdata.rowingdata("example_data.csv",rower=myrower)
>>> row.plotmeters_otw()
>>> row.plottime_otw()
>>> print row.summary()

To get any data column as a numpy array, use (for example for HR data - 
see list below for other accessible data fields).

>>> row.getvalues[' HRCur (bpm)']

To create the colorful plots as well as copy a text summary to the clipboard,
assuming you have a summary file from CrewNerd called 2016-03-25-0758.CSV and 
a TCX file called 2016-03-25-0758.TCX

>>> from rowingdata import *
>>> otwplot.plotrowall("2016-03-25-0758")

Now you will have the summary data on your clipboard


Data Fields
==============

The available data fields are

* 'Timestamp (sec)'
* ' Horizontal (meters)'
* ' Cadence (stokes/min'
* 'HRCur (bpm)'
* ' Stroke500mPace (sec/500m)'
* ' Power (watts)'
* ' DriveLength (meters)'
* ' StrokeDistance (meters)'
* ' DriveTime (ms)'
* ' StrokeRecoveryTime (ms)'
* ' AverageDriveForce (lbs)'
* ' PeakDriveForce (lbs)'
* 'cum_dist'

Known bugs
=======================

* Something wrong with the time values when imported from RowPro 

Future functionality
=======================

* Add upload to concept2 logbook (would be great but very difficult as I haven't found an API and not much experience with the network protocols)
* Add support for other erg software tools (just need the csv/tcx and it will be easy)
* Add some command line tools to do the most common stuff


