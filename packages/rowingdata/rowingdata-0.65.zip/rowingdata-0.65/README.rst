**************
Rowingdata
**************

Based on python code by Greg Smith (https://quantifiedrowing.wordpress.com/) 
and inspired by the RowPro Dan Burpee spreadsheet (http://www.sub7irc.com/RP_Split_Template.zip)

===============
To install 
===============

::

	$ easy_install rowingdata

Or ::

	$ pip install rowingdata


To upgrade: ::

$ pip install --upgrade rowingdata

or ::

$ easy_install --upgrade rowingdata

======================
Command Line Tools
======================

Beta. Use with caution.

The easiest way to use rowingdata is from the command line. 

First, create a rower data file (if you don't have one yet). Just run the 
following command and answer a few questions about yourself. If you don't 
know what heart rate bands are, check here http://www.freespiritsrowing.com/content/utilities/hr-bands/ : ::

	$ roweredit yourfilename.txt

You can omit the file name. This will create a file defaultrower.txt. 
You can always run the same command to change parameters (for example 
if you lost or gained weight, change the user name or password, etc.

Now you need the data files for your row. (The install comes with a few test 
files.) Get a TCX file (and a CSV summary file) from CrewNerd. TCX files from 
other tools should also work (not tested), as long as the TCX is valid.

Or get a CSV export from painsled. 


TCX files
-----------

Having a crewnerddata.csv (summary csv) and a crewnerddata.tcx, the following 
will create plots and spit out some summary text ::

	$ crewnerdplot crewnerddata yourrower.txt

The yourrower.txt argument is the file where you keep your rower data. 
This is optional. If you don't provide it, the tool will look for 
defaultrower.txt. If it doesn't find that, it will use some default values. 

The following will upload your row to the Concept2 logbook, and create a 
file crewnerddata.tcx_o.csv that looks like a painsled csv, for future use ::

	$ tcxtoc2 crewnerddata.tcx yourrower.txt

Again, yourrower.txt is optional.


Painsled
------------

Having painsled data in testdata.csv, the following will create plots and
spit out some summary text ::

	$ painsledplot testdata.csv yourrower.txt

The yourrower.txt argument is the file where you keep your rower data. 
This is optional. If you don't provide it, the tool will look for 
defaultrower.txt. If it doesn't find that, it will use some default values. 

The following will upload your row to the Concept2 logbook: ::

	$ painsledtoc2 testdata.csv yourrower.txt

Again, yourrower.txt is optional.

==============================
From Interactive python shell
==============================

Beta. Use with caution. 

Import
---------

Import the package

>>> from rowingdata import *

Your personal data
-----------------------

If you're not me (or have identical heart rate thresholds), 
you will have to change the default values for the rower. For example:

>>> john = rowingdata.rower(hrut2=100,hrut1=120,hrat=140,hrtr=150,hran=170,hrmax=180,c2username="johntherower",c2password="caughtacrab")

You can store this locally like this

>>> john.write("johnsdata.txt")

Then you can load this like this

>>> john = rowingdata.read_obj("johnsdata.txt")

Painsled
----------------

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

CrewNerd (and other TCX)
---------------------------

To use with CrewNerd TCX data, simply do

>>> tcx = rowingdata.TCXParser("2016-03-25-0758.tcx")
>>> tcx.write_csv("example_data.csv")
>>> row = rowingdata.rowingdata("example_data.csv",rower=myrower)
>>> row.plotmeters_otw()
>>> row.plottime_otw()
>>> print row.summary()

Other useful stuff
----------------------------

To get any data column as a numpy array, use (for example for HR data - 
see list below for other accessible data fields).

>>> row.getvalues[' HRCur (bpm)']

To create the colorful plots as well as copy a text summary to the clipboard,
assuming you have a summary file from CrewNerd called 2016-03-25-0758.CSV and 
a TCX file called 2016-03-25-0758.TCX

>>> rowingdata.dorowall("2016-03-25-0758")

Now you will have the summary data on your clipboard

>>> row.uploadtoc2()

This will upload your row to Concept2 logbook. It just simply fill the online 
form for you. So nothing more than total distance and duration, date, weight 
category and row type

==============
Data Fields
==============

The available data fields are

* 'Timestamp (sec)'
* ' Horizontal (meters)'
* ' Cadence (stokes/min'
* ' HRCur (bpm)'
* ' Stroke500mPace (sec/500m)'
* ' Power (watts)'
* ' DriveLength (meters)'
* ' StrokeDistance (meters)'
* ' DriveTime (ms)'
* ' StrokeRecoveryTime (ms)'
* ' AverageDriveForce (lbs)'
* ' PeakDriveForce (lbs)'
* 'cum_dist'



================
Release Notes:
================

0.65
------

- Expanded command line scripts with time plots
- Command line scripts now take a rower file as an optional second argument
- Command line script to change rower parameters easily

0.63
------

- Fixed a bug that caused unwanted forgetting of Concept2 username and password

0.62
-------

- Fixed the time plot bug which also let to errors in the Concept2 upload (needed to sort the painsled data by time)

0.6
-------

- Added command-line tools and some test data

0.52
-------

- Adding weight and row type to Concept2 upload
- Adding options to locally save concept2 username and password
- Added row type (e.g. "Indoor Rower" or "On-water") to rowingdata


0.51
-------

- Corrected some dependencies errors

0.5
-------

- Upload to Concept2 logbook is working!

0.45
--------

- Added saving and loading of rower data (so you can store your password and HR data)

0.43
--------

- Attempting to remove the dubious DataFrame copy errors using df.loc

0.42
--------
- Added RowPro CSV Parser
- Added summary statistics and interval statistics (also copies the output to clipboard)
- Interval statistics now (sort of) works for Desktop Painsled data



======================
Known bugs
======================

* The interval statistics from Painsled Desktop are not to be trusted
* Upload from Painsled Desktop includes "waiting" seconds - not ok for ranking pieces or verification codes
* getting "global name 'dateutil' is not defined error when using from interactive Python in any other directory than my development directory. The command line stuff works fine.

=======================
Future functionality
=======================



* Add support for other erg software tools (just need the csv/tcx and it will be easy)


