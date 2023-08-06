import math
import numpy as np
import pylab
import scipy
import matplotlib
import matplotlib.pyplot as plt
import os
import pickle
import getpass
import mechanize
import pandas as pd

import time
import datetime

import dateutil

from lxml import objectify
from math import sin,cos,atan2,sqrt
from numpy import isnan,isinf
from matplotlib.pyplot import grid
from pandas import Series, DataFrame
from Tkinter import Tk
from matplotlib.ticker import MultipleLocator,FuncFormatter,NullFormatter


__version__ = "0.70.4"

namespace = 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'

def main():
    print("Executing rowingdata version %s." % __version__)

def write_obj(obj,filename):
    """ Save an object (e.g. your rower) to a file
    """
    pickle.dump(obj,open(filename,"wb"))

def read_obj(filename):
    """ Read an object (e.g. your rower, including passwords) from a file
        Usage: john = rowingdata.read_obj("john.txt")
    """
    res = pickle.load(open(filename))
    return res

def getrower(fileName="defaultrower.txt"):
    """ Read a rower object

    """

    try:
	r = pickle.load(open(fileName))
    except (IOError,ImportError):
	print "Default rower file doesn't exist. Create new rower"
	r = rower()

    return r


def getrowtype():
    rowtypes = dict([
	('Indoor Rower',['1']),
	('Indoor Rower with Slides',['2']),
	('Dynamic Indoor Rower',['3']),
	('SkiErg',['4']),
	('Paddle Adapter',['5']),
	('On-water',['6']),
	('On-snow',['7'])
	])
    
    return rowtypes

def movingaverage(interval, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')

def interval_string(nr,totaldist,totaltime,avgpace,avgspm,
		    avghr,maxhr,avgdps,
		    separator='|'):
    """ Used to create a nifty text string with the data for the interval
    """

    stri = "{nr:0>2.0f}{sep}{td:0>5.0f}{sep}{inttime:0>5}{sep}".format(
	nr = nr,
	sep = separator,
	td = totaldist,
	inttime = format_pace(totaltime)
	)

    stri += "{tpace:0>7}{sep}{tspm:0>4.1f}{sep}{thr:3.1f}".format(
	tpace=format_pace(avgpace),
	sep=separator,
	tspm=avgspm,
	thr = avghr
	)

    stri += "{sep}{tmaxhr:3.1f}{sep}{tdps:0>4.1f}".format(
	sep = separator,
	tmaxhr = maxhr,
	tdps = avgdps
	)


    stri += "\n"
    return stri

def summarystring(totaldist,totaltime,avgpace,avgspm,avghr,maxhr,avgdps,
		  readFile="",
		  separator="|"):
    """ Used to create a nifty string summarizing your entire row
    """

    stri1 = "Workout Summary - "+readFile+"\n"
    stri1 += "--{sep}Total{sep}-Total-{sep}--Avg--{sep}Avg-{sep}-Avg-{sep}-Max-{sep}-Avg\n".format(sep=separator)
    stri1 += "--{sep}Dist-{sep}-Time--{sep}-Pace--{sep}SPM-{sep}-HR--{sep}-HR--{sep}-DPS\n".format(sep=separator)

    pacestring = format_pace(avgpace)

    stri1 += "--{sep}{dtot:0>5.0f}{sep}{tottime:7}{sep}{pacestring:0>7}".format(
	sep = separator,
	dtot = totaldist,
	tottime = format_time(totaltime),
	pacestring = pacestring
	)

    stri1 += "{sep}{avgsr:2.1f}{sep}{avghr:3.1f}{sep}".format(
	avgsr = avgspm,
	sep = separator,
	avghr = avghr
	)

    stri1 += "{maxhr:3.1f}{sep}{avgdps:0>4.1f}\n".format(
	sep = separator,
	maxhr = maxhr,
	avgdps = avgdps
	)

    return stri1

def geo_distance(lat1,lon1,lat2,lon2):
    """ Approximate distance between two points defined by lat1,lon1 and lat2,lon2
    This is a slight underestimate but is close enough for our purposes,
    We're never moving more than 10 meters between trackpoints
    """
    
    # radius of earth in km
    R = 6373.0

    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    lon1 = math.radians(lon1)
    lon2 = math.radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance

def format_pace_tick(x,pos=None):
	min=int(x/60)
	sec=int(x-min*60.)
	sec_str=str(sec).zfill(2)
	template='%d:%s'
	return template % (min,sec_str)

def format_pace(x,pos=None):
    if isinf(x) or isnan(x):
	x=0
	
    min=int(x/60)
    sec=(x-min*60.)

    str1 = "{min:0>2}:{sec:0>4.1f}".format(
	min = min,
	sec = sec
	)

    return str1

def format_time(x,pos=None):

    min = int(x/60.)
    sec = int(x-min*60)

    str1 = "{min:0>2}:{sec:0>4.1f}".format(
	min=min,
	sec=sec,
	)

    return str1

def format_dist_tick(x,pos=None):
	km = x/1000.
	template='%6.3f'
	return template % (km)

def format_time_tick(x,pos=None):
	hour=int(x/3600)
	min=int((x-hour*3600.)/60)
	min_str=str(min).zfill(2)
	template='%d:%s'
	return template % (hour,min_str)

class summarydata:
    """ This is used to create nice summary texts from CrewNerd's summary CSV

    Usage: sumd = rowingdata.summarydata("crewnerdsummary.CSV")

           sumd.allstats()

	   sumd.shortstats()

	   """
    
    def __init__(self, readFile):
	self.readFile = readFile
	sumdf = pd.read_csv(readFile)
	self.sumdf = sumdf

	# prepare Work Data
	# remove "Just Go"
	s2 = self.sumdf[self.sumdf['Workout Name']<>'Just Go']
	s3 = s2[~s2['Interval Type'].str.contains("Rest")]
	self.workdata = s3

    def allstats(self,separator="|"):



	stri2 = "Workout Details\n"
	stri2 += "#-{sep}SDist{sep}-Split-{sep}-SPace-{sep}SPM-{sep}AvgHR{sep}MaxHR{sep}DPS-\n".format(
	    sep = separator
	    )

	avghr = self.workdata['Avg HR'].mean()
	avgsr = self.workdata['Avg SR'].mean()
	maxhr = self.workdata['Max HR'].mean()
	maxsr = self.workdata['Max SR'].mean()
	totaldistance = self.workdata['Distance (m)'].sum()
	avgspeed = self.workdata['Avg Speed (m/s)'].mean()
	totalstrokes = self.workdata['Strokes'].sum()
	avgpace = 500/avgspeed


	min=int(avgpace/60)
	sec=int(10*(avgpace-min*60.))/10.
	pacestring = str(min)+":"+str(sec)


	nr_rows = self.workdata.shape[0]

	totmin = 0
	totsec = 0

	
	for i in range(nr_rows):
	    inttime = self.workdata['Time'].iloc[i]
	    thr = self.workdata['Avg HR'].iloc[i]
	    td = self.workdata['Distance (m)'].iloc[i]
	    tpace = self.workdata['Avg Pace (/500m)'].iloc[i]
	    tspm = self.workdata['Avg SR'].iloc[i]
	    tmaxhr = self.workdata['Max HR'].iloc[i]
	    tstrokes = self.workdata['Strokes'].iloc[i]

	    tdps = td/(1.0*tstrokes)
				 

	    t = time.strptime(inttime, "%M:%S")
	    totmin = totmin+t.tm_min
	    totsec = totsec+t.tm_sec
	    if (totsec > 60):
		totsec = totsec - 60
		totmin = totmin+1


	    stri2 += "{nr:0>2}{sep}{td:0>5}{sep} {inttime:0>5} {sep}".format(
		nr = i+1,
		sep = separator,
		td = td,
		inttime = inttime
		)

	    stri2 += "{tpace:0>7}{sep}{tspm:0>4.1f}{sep}{thr:3.1f}".format(
		tpace=tpace,
		sep=separator,
		tspm=tspm,
		thr = thr
		)

	    stri2 += "{sep}{tmaxhr:3.1f}{sep}{tdps:0>4.1f}".format(
		sep = separator,
		tmaxhr = tmaxhr,
		tdps = tdps
		)


	    stri2 += "\n"

	

	tottime = "{totmin:0>2}:{totsec:0>2}".format(
	    totmin = totmin,
	    totsec = totsec)

	totaltime = totmin*60+totsec
	
	avgdps = totaldistance/(1.0*totalstrokes)
	if isnan(avgdps):
	    avgdps = 0

	stri1 = summarystring(totaldistance,totaltime,avgpace,avgsr,
			     avghr,maxhr,avgdps,
			     readFile=self.readFile,
			     separator=separator)

	
	print stri1+stri2

	# Copy to clipboard for pasting into blog
	r = Tk()
	r.withdraw()
	r.clipboard_clear()
	r.clipboard_append(stri1+stri2)
	r.destroy

    def shortstats(self):
	avghr = self.workdata['Avg HR'].mean()
	avgsr = self.workdata['Avg SR'].mean()
	maxhr = self.workdata['Max HR'].mean()
	maxsr = self.workdata['Max SR'].mean()
	totaldistance = self.workdata['Distance (m)'].sum()
	avgspeed = self.workdata['Avg Speed (m/s)'].mean()
	avgpace = 500/avgspeed

	min=int(avgpace/60)
	sec=int(10*(avgpace-min*60.))/10.
	pacestring = str(min)+":"+str(sec)


	nr_rows = self.workdata.shape[0]

	totmin = 0
	totsec = 0

	
	for i in range(nr_rows):
	    inttime = self.workdata['Time'].iloc[i]

	    t = time.strptime(inttime, "%M:%S")
	    totmin = totmin+t.tm_min
	    totsec = totsec+t.tm_sec
	    if (totsec > 60):
		totsec = totsec - 60
		totmin = totmin+1

	stri =  "=========WORK DATA=================\n"
	stri = stri+"Total Time     : "+str(totmin)+":"+str(totsec)+"\n"
	stri = stri+ "Total Distance : "+str(totaldistance)+" m\n"
	stri = stri+"Average Pace   : "+pacestring+"\n"
	stri = stri+"Average HR     : "+str(int(avghr))+" Beats/min\n"
	stri = stri+"Average SPM    : "+str(int(10*avgsr)/10.)+" /min\n"
	stri = stri+"Max HR         : "+str(int(maxhr))+" Beats/min\n"
	stri = stri+"Max SPM        : "+str(int(10*maxsr)/10.)+" /min\n"
	stri = stri+"==================================="

	print stri
	
	# Copy to clipboard for pasting into blog
	r = Tk()
	r.withdraw()
	r.clipboard_clear()
	r.clipboard_append(stri)
	r.destroy

class RowProParser:
    """ Parser for reading CSV files created by RowPro

    Use: data = rowingdata.RowProParser("RPdata.csv")

         data.write_csv("RPdata_out.csv")

	 """
    
    def __init__(self,RPfile="RPtest.csv",skiprows=14,skipfooter=24):
	self.RP_df = pd.read_csv(RPfile,skiprows=skiprows,skipfooter=skipfooter)

    def write_csv(self,writeFile="example.csv"):
	""" Exports RowPro data to the CSV format that I use in rowingdata
	"""

	# Time,Distance,Pace,Watts,Cals,SPM,HR,DutyCycle,Rowfile_Id

	unixtimes = self.RP_df['Time']
	dist2 = self.RP_df['Distance']
	spm = self.RP_df['SPM']
	pace = self.RP_df['Pace']*500.0
	power = self.RP_df['Watts']



	hr = self.RP_df['HR']
	nr_rows = len(spm)

	# Create data frame with all necessary data to write to csv
	data = DataFrame({'TimeStamp (sec)':unixtimes,
			  ' Horizontal (meters)': dist2,
			  ' Cadence (stokes/min)':spm,
			  ' HRCur (bpm)':hr,
			  ' Stroke500mPace (sec/500m)':pace,
			  ' Power (watts)':power,
			  ' DriveLength (meters)':np.zeros(nr_rows),
			  ' StrokeDistance (meters)':np.zeros(nr_rows),
			  ' DriveTime (ms)':np.zeros(nr_rows),
			  ' StrokeRecoveryTime (ms)':np.zeros(nr_rows),
			  ' AverageDriveForce (lbs)':np.zeros(nr_rows),
			  ' PeakDriveForce (lbs)':np.zeros(nr_rows),
			  ' lapIdx':np.zeros(nr_rows)
			  })
	
	data.sort(['TimeStamp (sec)'],ascending=True)

	return data.to_csv(writeFile,index_label='index')
	

class painsledDesktopParser:
    """ Parser for reading CSV files created by Painsled (desktop version)

    Use: data = rowingdata.painsledDesktopParser("sled_data.csv")

         data.write_csv("sled_data_out.csv")

	 """
    
    def __init__(self, sled_file="sled_test.csv"):
	df = pd.read_csv(sled_file)
	# remove "00 waiting to row"
	self.sled_df = df[df[' stroke.endWorkoutState'] != ' "00 waiting to row"']



    def time_values(self):
	""" Converts painsled style time stamps to Unix time stamps	"""
	
	# time stamps (ISO)
	timestamps = self.sled_df.loc[:,' stroke.driveStartMs'].values
	
	# convert to unix style time stamp
	unixtimes = np.zeros(len(timestamps))

	# there may be a more elegant and faster way with arrays 
	for i in range(len(timestamps)):
	    tt = dateutil.parser.parse(timestamps[i],fuzzy=True)
	    unixtimes[i] = time.mktime(tt.timetuple())

	return unixtimes


    def write_csv(self,writeFile="example.csv"):
	""" Exports Painsled (desktop) data to the CSV format that
	I use in rowingdata
	"""
	

	unixtimes = self.time_values()

	
	dist2 = self.sled_df[' stroke.startWorkoutMeter']
	spm = self.sled_df[' stroke.strokesPerMin']
	pace = self.sled_df[' stroke.paceSecPer1k']/2.0
	power = self.sled_df[' stroke.watts']
	ldrive = self.sled_df[' stroke.driveMeters']
	strokelength2 = self.sled_df[' stroke.strokeMeters']
	tdrive = self.sled_df[' stroke.driveMs']
	trecovery = self.sled_df[' stroke.slideMs']
	hr = self.sled_df[' stroke.hrBpm']
	intervalcount = self.sled_df[' stroke.intervalNumber']

	nr_rows = len(spm)

	# Create data frame with all necessary data to write to csv
	data = DataFrame({'TimeStamp (sec)':unixtimes,
			  ' Horizontal (meters)': dist2,
			  ' Cadence (stokes/min)':spm,
			  ' HRCur (bpm)':hr,
			  ' Stroke500mPace (sec/500m)':pace,
			  ' Power (watts)':power,
			  ' DriveLength (meters)':ldrive,
			  ' StrokeDistance (meters)':strokelength2,
			  ' DriveTime (ms)':tdrive,
			  ' StrokeRecoveryTime (ms)':trecovery,
			  ' AverageDriveForce (lbs)':np.zeros(nr_rows),
			  ' PeakDriveForce (lbs)':np.zeros(nr_rows),
			  ' lapIdx':intervalcount
			  })

	data.sort(['TimeStamp (sec)'],ascending=True)

	

	return data.to_csv(writeFile,index_label='index')

	
class TCXParser:
    """ Parser for reading TCX files, e.g. from CrewNerd

    Use: data = rowingdata.TCXParser("crewnerd_data.tcx")

         data.write_csv("crewnerd_data_out.csv")

	 """

    
    def __init__(self, tcx_file):
        tree = objectify.parse(tcx_file)
        self.root = tree.getroot()
        self.activity = self.root.Activities.Activity

# need to select only trackpoints with Cadence, Distance, Time & HR data 
	self.selectionstring = '//ns:Trackpoint[descendant::ns:HeartRateBpm]'
	self.selectionstring +='[descendant::ns:Cadence]'
	self.selectionstring +='[descendant::ns:DistanceMeters]'
	self.selectionstring +='[descendant::ns:Time]'

        
    def hr_values(self):
        return self.root.xpath(self.selectionstring
			       +'//ns:HeartRateBpm/ns:Value',
			       namespaces={'ns': namespace})

    def distance_values(self):
        return self.root.xpath(self.selectionstring
			       +'/ns:DistanceMeters',
			       namespaces={'ns': namespace})

    def spm_values(self):
        return self.root.xpath(self.selectionstring
			       +'/ns:Cadence',
			       namespaces={'ns': namespace})

    def time_values(self):
	# time stamps (ISO)
	timestamps = self.root.xpath(self.selectionstring
				    +'/ns:Time',
				    namespaces={'ns': namespace})
	
	# convert to unix style time stamp
	unixtimes = np.zeros(len(timestamps))

	# there may be a more elegant and faster way with arrays 
	for i in range(len(timestamps)):
	    s = str(timestamps[i])
	    tt = dateutil.parser.parse(s)
	    unixtimes[i] = time.mktime(tt.timetuple())

	return unixtimes

    def lat_values(self):
	return self.root.xpath(self.selectionstring
			       +'/ns:Position/ns:LatitudeDegrees',
			       namespaces={'ns':namespace})

    def long_values(self):
	return self.root.xpath(self.selectionstring
			       +'/ns:Position/ns:LongitudeDegrees',
			       namespaces={'ns':namespace})
    

    def all_values(self):
	t = self.root.xpath(self.selectionstring
			    +'/ns:Time',
			     namespaces={'ns': namespace})
	d = self.root.xpath(self.selectionstring+'/ns:DistanceMeters',
			     namespaces={'ns': namespace})
	spm = self.root.xpath(self.selectionstring
			      +'/ns:Cadence',
			     namespaces={'ns': namespace})
	
	hr = self.root.xpath(self.selectionstring
			       +'//ns:HeartRateBpm/ns:Value',
			       namespaces={'ns': namespace})

	return [t,d,spm,hr]

    def write_csv(self,writeFile='example.csv',window_size=20):
	""" Exports TCX data to the CSV format that
	I use in rowingdata
	"""

	# Time stamps 
	unixtimes = self.time_values()


	# Distance Meters
	d = self.distance_values()

	# Stroke Rate
	spm = self.spm_values()
	
	# Heart Rate
	hr = self.hr_values()

	long = self.long_values()
	lat = self.lat_values()

	nr_rows = len(spm)
	velo = np.zeros(nr_rows)
	dist2 = np.zeros(nr_rows)
	strokelength = np.zeros(nr_rows)

	for i in range(nr_rows-1):
	    dl = 1000.*geo_distance(lat[i],long[i],lat[i+1],long[i+1])
	    dist2[i+1]=dist2[i]+dl
	    velo[i+1] = dl/(1.0*(unixtimes[i+1]-unixtimes[i]))
	    strokelength[i] = dl*60/spm[i]



	velo2 = movingaverage(velo,window_size)
	strokelength2 = movingaverage(strokelength,window_size)
	pace = 500./velo2



	# Create data frame with all necessary data to write to csv
	data = DataFrame({'TimeStamp (sec)':unixtimes,
			  ' Horizontal (meters)': dist2,
			  ' Cadence (stokes/min)':spm,
			  ' HRCur (bpm)':hr,
			  ' longitude':long,
			  ' latitude':lat,
			  ' Stroke500mPace (sec/500m)':pace,
			  ' Power (watts)':np.zeros(nr_rows),
			  ' DriveLength (meters)':np.zeros(nr_rows),
			  ' StrokeDistance (meters)':strokelength2,
			  ' DriveTime (ms)':np.zeros(nr_rows),
			  ' StrokeRecoveryTime (ms)':np.zeros(nr_rows),
			  ' AverageDriveForce (lbs)':np.zeros(nr_rows),
			  ' PeakDriveForce (lbs)':np.zeros(nr_rows),
			  ' lapIdx':np.zeros(nr_rows)
			  })
	
	return data.to_csv(writeFile,index_label='index')

    def write_nogeo_csv(self,writeFile='example.csv',window_size=5):
	""" Exports TCX data without position data (indoor)
	to the CSV format that
	I use in rowingdata
	"""

	# Time stamps 
	unixtimes = self.time_values()


	# Distance Meters
	d = self.distance_values()

	# Stroke Rate
	spm = self.spm_values()
	
	# Heart Rate
	hr = self.hr_values()


	nr_rows = len(spm)
	velo = np.zeros(nr_rows)

	strokelength = np.zeros(nr_rows)

	for i in range(nr_rows-1):
	    dl = d[i+1]-d[i]
	    if (unixtimes[i+1]<>unixtimes[i]):
		velo[i+1] = dl/(unixtimes[i+1]-unixtimes[i])
	    else:
		velo[i+1]=0

	    if (spm[i]<>0):
		strokelength[i] = dl*60/spm[i]
	    else:
		strokelength[i] = 0.


	

	velo2 = movingaverage(velo,window_size)
	strokelength2 = movingaverage(strokelength,window_size)
	pace = 500./velo2



	# Create data frame with all necessary data to write to csv
	data = DataFrame({'TimeStamp (sec)':unixtimes,
			  ' Horizontal (meters)': d,
			  ' Cadence (stokes/min)':spm,
			  ' HRCur (bpm)':hr,
			  ' Stroke500mPace (sec/500m)':pace,
			  ' Power (watts)':np.zeros(nr_rows),
			  ' DriveLength (meters)':np.zeros(nr_rows),
			  ' StrokeDistance (meters)':strokelength2,
			  ' DriveTime (ms)':np.zeros(nr_rows),
			  ' StrokeRecoveryTime (ms)':np.zeros(nr_rows),
			  ' AverageDriveForce (lbs)':np.zeros(nr_rows),
			  ' PeakDriveForce (lbs)':np.zeros(nr_rows),
			  ' lapIdx':np.zeros(nr_rows)
			  })
	
	return data.to_csv(writeFile,index_label='index')


class rower:
    """ This class contains all the personal data about the rower

    * HR threshold values

    * C2 logbook username and password

    * weight category

    """
    
    def __init__(self,hrut2=142,hrut1=146,hrat=160,
		 hrtr=167,hran=180,hrmax=192,
		 c2username="",
		 c2password="",
		 weightcategory="hwt"):
	self.ut2=hrut2
	self.ut1=hrut1
	self.at=hrat
	self.tr=hrtr
	self.an=hran
	self.max=hrmax
	self.c2username=c2username
	self.c2password=c2password
	if (weightcategory <> "hwt") and (weightcategory <> "lwt"):
	    print "Weightcategory unrecognized. Set to hwt"
	    weightcategory = "hwt"
	    
	self.weightcategory=weightcategory

    def write(self,fileName):
	res = write_obj(self,fileName)


def roweredit(fileName="defaultrower.txt"):
    """ Easy editing or creation of a rower file.
    Mainly for using from the windows command line

    """

    try:
	r = pickle.load(open(fileName))
    except IOError:
	print "File does not exist. Reverting to defaultrower.txt"
	r = getrower()
    except ImportError:
	print "File is not valid. Reverting to defaultrower.txt"
	r = getrower()

    print "Heart Rate Training Bands"
    # hrmax
    print "Your HR max is set to {hrmax} bpm".format(
	hrmax = r.max
	)
    strin = raw_input('Enter HR max (just ENTER to keep {hrmax}):'.format(hrmax=r.max))
    if (strin <> ""):
	try:
	    r.max = int(strin)
	except ValueError:
	    print "Not a valid number. Keeping original value"

    
    # hrut2, hrut1
    print "UT2 zone is between {hrut2} and {hrut1} bpm ({percut2:2.0f}-{percut1:2.0f}% of max HR)".format(
	hrut2 = r.ut2,
	hrut1 = r.ut1,
	percut2 = 100.*r.ut2/r.max,
	percut1 = 100.*r.ut1/r.max
	)
    strin = raw_input('Enter UT2 band lower value (ENTER to keep {hrut2}):'.format(hrut2=r.ut2))
    if (strin <> ""):
	try:
	    r.ut2 = int(strin)
	except ValueError:
    	    print "Not a valid number. Keeping original value"

    strin = raw_input('Enter UT2 band upper value (ENTER to keep {hrut1}):'.format(hrut1=r.ut1))
    if (strin <> ""):
	try:
	    r.ut1 = int(strin)
	except ValueError:
    	    print "Not a valid number. Keeping original value"

    
    print "UT1 zone is between {val1} and {val2} bpm ({perc1:2.0f}-{perc2:2.0f}% of max HR)".format(
	val1 = r.ut1,
	val2 = r.at,
	perc1 = 100.*r.ut1/r.max,
	perc2 = 100.*r.at/r.max
	)

    strin = raw_input('Enter UT1 band upper value (ENTER to keep {hrat}):'.format(hrat=r.at))
    if (strin <> ""):
	try:
	    r.at = int(strin)
	except ValueError:
    	    print "Not a valid number. Keeping original value"

    
    print "AT zone is between {val1} and {val2} bpm ({perc1:2.0f}-{perc2:2.0f}% of max HR)".format(
	val1 = r.at,
	val2 = r.tr,
	perc1 = 100.*r.at/r.max,
	perc2 = 100.*r.tr/r.max
	)

    strin = raw_input('Enter AT band upper value (ENTER to keep {hrtr}):'.format(hrtr=r.tr))
    if (strin <> ""):
	try:
	    r.tr = int(strin)
	except ValueError:
    	    print "Not a valid number. Keeping original value"

    
    
    print "TR zone is between {val1} and {val2} bpm ({perc1:2.0f}-{perc2:2.0f}% of max HR)".format(
	val1 = r.tr,
	val2 = r.an,
	perc1 = 100.*r.tr/r.max,
	perc2 = 100.*r.an/r.max
	)

    strin = raw_input('Enter TR band upper value (ENTER to keep {hran}):'.format(hran=r.an))
    if (strin <> ""):
	try:
	    r.an = int(strin)
	except ValueError:
    	    print "Not a valid number. Keeping original value"


    print ""

    # weightcategory    
    print "Your weight category is set to {weightcategory}.".format(
	weightcategory = r.weightcategory
	)
    strin = raw_input('Enter lwt for Light Weight, hwt for Heavy Weight, or just ENTER: ')
    if (strin <> ""):
	if (strin == 'lwt'):
	    r.weightcategory = strin
	    print "Setting to "+strin
	elif (strin == 'hwt'):
	    r.weightcategory = strin
	    print "Setting to "+strin
	else:
	    print "Value not recognized"

    print ""

    # c2username
    if (r.c2username <> ""):
	print "Your Concept2 is set to {c2username}.".format(
	    c2username = r.c2username
	)
	strin = raw_input('Enter new username (or just ENTER to keep): ')
	if (strin <> ""):
	    r.c2username = strin


    # c2password
    if (r.c2username == ""):
	print "We don't know your Concept2 username"
	strin = raw_input('Enter new username (or ENTER to skip): ')
	r.c2username = strin

    if (r.c2username <> ""):
	if (r.c2password <> ""):
	    print "We have your Concept2 password."
	    changeyesno = raw_input('Do you want to change/erase your password (y/n)')
	    if changeyesno == "y":
		strin1 = getpass.getpass('Enter new password (or ENTER to erase):')
		if (strin1 <> ""):
		    strin2 = getpass.getpass('Repeat password:')
		    if (strin1 == strin2):
			r.c2password = strin1
		    else:
			print "Error. Not the same."
		if (strin1 == ""):
			print "Forgetting your password"
			r.c2password = ""
	elif (r.c2password == ""):
	    print "We don't have your Concept2 password yet."
	    strin1 = getpass.getpass('Concept2 password (or ENTER to skip):')
	    if (strin1 <> ""):
		strin2 = getpass.getpass('Repeat password:')
		if (strin1 == strin2):
		    r.c2password = strin1
		else:
		    print "Error. Not the same."
    
    


    r.write(fileName)
    
    print "Done"
    return 1


class rowingdata:
    """ This is the main class. Read the data from the csv file and do all
    kinds
    of cool stuff with it.

    Usage: row = rowingdata.rowingdata("testdata.csv",rowtype = "Indoor Rower")
           row.plotmeters_all()
	   
    The default rower looks for a defaultrower.txt file. If it is not found,
    it reverts to some arbitrary rower.
    

    """
    
    def __init__(self,readFile="testdata.csv",
		 rower=rower(),
		 rowtype="Indoor Rower"):
	
	self.readFile = readFile
	self.rower = rower
	self.rowtype = rowtype
	
	sled_df = pd.read_csv(readFile)

	# get the date of the row
	starttime = sled_df.loc[0,'TimeStamp (sec)']
	# using UTC time for now
	self.rowdatetime = datetime.datetime.utcfromtimestamp(starttime)
	
	    	
	# remove the start time from the time stamps
	sled_df['TimeStamp (sec)']=sled_df['TimeStamp (sec)']-sled_df['TimeStamp (sec)'][0]

	number_of_columns = sled_df.shape[1]
	number_of_rows = sled_df.shape[0]


	# define an additional data frame that will hold the multiple bar plot data and the hr 
	# limit data for the plot, it also holds a cumulative distance column
	# Sander: changed the first row of next line (compared to Greg)
	# Sander: so it will work with my TCX to CSV parsed files
	hr_df = DataFrame({'key': sled_df['TimeStamp (sec)'],
			   'hr_ut2': np.zeros(number_of_rows),
			   'hr_ut1': np.zeros(number_of_rows),
			   'hr_at': np.zeros(number_of_rows),
			   'hr_tr': np.zeros(number_of_rows),
			   'hr_an': np.zeros(number_of_rows),
			   'hr_max': np.zeros(number_of_rows),
			   'lim_ut2': self.rower.ut2,
			   'lim_ut1': self.rower.ut1,
			   'lim_at': self.rower.at,
			   'lim_tr': self.rower.tr,
			   'lim_an': self.rower.an,
			   'lim_max': self.rower.max,
			   'cum_dist':np.zeros(number_of_rows)
			   })

				   
	# merge the two dataframes together
	df = pd.merge(sled_df,hr_df,left_on='TimeStamp (sec)',right_on='key')

	# create the columns containing the data for the colored bar chart
	# attempt to do this in a way that doesn't generate dubious copy warnings
	mask = df[' HRCur (bpm)']<=self.rower.ut2
	df.loc[mask,'hr_ut2'] = df.loc[mask,' HRCur (bpm)']

	mask = (df[' HRCur (bpm)']<=self.rower.ut1)&(df[' HRCur (bpm)']>self.rower.ut2)
	df.loc[mask,'hr_ut1'] = df.loc[mask,' HRCur (bpm)']

	mask = (df[' HRCur (bpm)']<=self.rower.at)&(df[' HRCur (bpm)']>self.rower.ut1)
	df.loc[mask,'hr_at'] = df.loc[mask,' HRCur (bpm)']

	mask = (df[' HRCur (bpm)']<=self.rower.tr)&(df[' HRCur (bpm)']>self.rower.at)
	df.loc[mask,'hr_tr'] = df.loc[mask,' HRCur (bpm)']

	mask = (df[' HRCur (bpm)']<=self.rower.an)&(df[' HRCur (bpm)']>self.rower.tr)
	df.loc[mask,'hr_an'] = df.loc[mask,' HRCur (bpm)']

	mask = (df[' HRCur (bpm)']>self.rower.an)
	df.loc[mask,'hr_max'] = df.loc[mask,' HRCur (bpm)']


	# The following calls generated dubious copy warnings
#	df['hr_ut2'][df[' HRCur (bpm)']<self.rower.ut2] = df[' HRCur (bpm)'] 
#	df['hr_ut1'][df[' HRCur (bpm)']>=self.rower.ut2] = df[' HRCur (bpm)'] 
#	df['hr_ut1'][df[' HRCur (bpm)']>self.rower.ut1] = 0
#	df['hr_at'][df[' HRCur (bpm)']>=self.rower.ut1] = df[' HRCur (bpm)'] 
#	df['hr_at'][df[' HRCur (bpm)']>self.rower.at] = 0
#	df['hr_tr'][df[' HRCur (bpm)']>=self.rower.at] = df[' HRCur (bpm)'] 
#	df['hr_tr'][df[' HRCur (bpm)']>self.rower.tr] = 0
#	df['hr_an'][df[' HRCur (bpm)']>=self.rower.tr] = df[' HRCur (bpm)'] 
#	df['hr_an'][df[' HRCur (bpm)']>self.rower.an] = 0
#	df['hr_max'][df[' HRCur (bpm)']>=self.rower.an] = df[' HRCur (bpm)'] 
#	df['hr_max'][df[' HRCur (bpm)']>self.rower.max] = 0

	# fill cumulative distance column with cumulative distance
	# ignoring resets to lower distance values
	df['cum_dist'] = np.cumsum(df[' Horizontal (meters)'].diff()[df[' Horizontal (meters)'].diff()>0])

	# Remove the NaN values from the data frame (in the cum_dist column)
	self.df = df.fillna(method='ffill')

    def getvalues(self,keystring):
	""" Just a tool to get a column of the row data as a numpy array

	You can also just access row.df[keystring] to get a pandas Series

	"""
	
	return self.df[keystring].values

    def intervalstats(self,separator='|'):
	""" Used to create a nifty text summary, one row for each interval

	Also copies the string to the clipboard (handy!)

	Works for painsled (both iOS and desktop version) because they use
	the lapIdx column

	"""
	
	df = self.df

	intervalnrs = pd.unique(df[' lapIdx'])

	stri = "Workout Details\n"
	stri += "#-{sep}SDist{sep}-Split-{sep}-SPace-{sep}SPM-{sep}AvgHR{sep}MaxHR{sep}DPS-\n".format(
	    sep = separator
	    )


	for idx in intervalnrs:
	    td = df[df[' lapIdx'] == idx]
	    avghr = td[' HRCur (bpm)'].mean()
	    maxhr = td[' HRCur (bpm)'].max()
	    avgspm = td[' Cadence (stokes/min)'].mean()
	    
	    intervaldistance = td['cum_dist'].max()-td['cum_dist'].min()
	    intervalduration = td['TimeStamp (sec)'].max()-td['TimeStamp (sec)'].min()
	    intervalpace = 500.*intervalduration/intervaldistance
	    avgdps = intervaldistance/(intervalduration*avgspm/60.)
	    if isnan(avgdps) or isinf(avgdps):
		avgdps = 0

	    stri += interval_string(idx,intervaldistance,intervalduration,
				    intervalpace,avgspm,
				    avghr,maxhr,avgdps,
				    separator=separator)
	    

	# Copy to clipboard for pasting into blog
	r = Tk()
	r.withdraw()
	r.clipboard_clear()
	r.clipboard_append(stri)
	r.destroy

	return stri

    def summary(self,separator='|'):
	""" Creates a nifty text string that contains the key data for the row
	and copies it to the clipboard

	"""
	
	df = self.df

	# total dist, total time, avg pace, avg hr, max hr, avg dps

	totaldist = df['cum_dist'].max()
	totaltime = df['TimeStamp (sec)'].max()
	avgpace = 500*totaltime/totaldist
	avghr = df[' HRCur (bpm)'].mean()
	maxhr = df[' HRCur (bpm)'].max()
	avgspm = df[' Cadence (stokes/min)'].mean()
	avgdps = totaldist/(totaltime*avgspm/60.)
	
	stri = summarystring(totaldist,totaltime,avgpace,avgspm,
			     avghr,maxhr,avgdps,
			     readFile=self.readFile,
			     separator=separator)

	# Copy to clipboard for pasting into blog
	r = Tk()
	r.withdraw()
	r.clipboard_clear()
	r.clipboard_append(stri)
	r.destroy


	return stri

    def allstats(self,separator='|'):
	""" Creates a nice text summary, both overall summary and a one line
	per interval summary

	Works for painsled (both iOS and desktop)

	Also copies the string to the clipboard (handy!)

	"""

	stri = self.summary(separator=separator)+self.intervalstats(separator=separator)
	# Copy to clipboard for pasting into blog
	r = Tk()
	r.withdraw()
	r.clipboard_clear()
	r.clipboard_append(stri)
	r.destroy


	return stri

    def plotmeters_erg(self):
	""" Creates two images containing interesting plots

	x-axis is distance

	Used with painsled (erg) data
	

	"""
	
	df = self.df
	fig1 = plt.figure(figsize=(12,10))
	fig_title = "Input File:  "+self.readFile+" --- HR / Pace / Rate / Power"

	# First panel, hr
	ax1 = fig1.add_subplot(4,1,1)
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_ut2'],color='gray', ec='gray')
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_ut1'],color='y',ec='y')
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_at'],color='g',ec='g')
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_tr'],color='blue',ec='blue')
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_an'],color='violet',ec='violet')
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_max'],color='r',ec='r')
	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_ut2'],color='k')
	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_ut1'],color='k')
	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_at'],color='k')
	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_tr'],color='k')
	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_an'],color='k')
	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_max'],color='k')
	ax1.text(5,self.rower.ut2+1.5,"UT2",size=8)
	ax1.text(5,self.rower.ut1+1.5,"UT1",size=8)
	ax1.text(5,self.rower.at+1.5,"AT",size=8)
	ax1.text(5,self.rower.tr+1.5,"TR",size=8)
	ax1.text(5,self.rower.an+1.5,"AN",size=8)
	ax1.text(5,self.rower.max+1.5,"MAX",size=8)

	end_dist = int(df.ix[df.shape[0]-1,'cum_dist'])

	ax1.axis([0,end_dist,100,1.1*self.rower.max])
	ax1.set_xticks(range(1000,end_dist,1000))
	ax1.set_ylabel('BPM')
	ax1.set_yticks(range(110,200,10))
	ax1.set_title(fig_title)

	grid(True)

	# Second Panel, Pace
	ax2 = fig1.add_subplot(4,1,2)
	ax2.plot(df.ix[:,'cum_dist'],df.ix[:,' Stroke500mPace (sec/500m)'])
	ax2.axis([0,end_dist,150,90])
	ax2.set_xticks(range(1000,end_dist,1000))
	ax2.set_ylabel('(sec/500)')
	ax2.set_yticks(range(145,95,-5))
	grid(True)
	majorTickFormatter = FuncFormatter(format_pace_tick)
	majorLocator = (5)
	ax2.yaxis.set_major_formatter(majorTickFormatter)

	# Third Panel, rate
	ax3 = fig1.add_subplot(4,1,3)
	ax3.plot(df.ix[:,'cum_dist'],df.ix[:,' Cadence (stokes/min)'])
	ax3.axis([0,end_dist,14,40])
	ax3.set_xticks(range(1000,end_dist,1000))
	ax3.set_ylabel('SPM')
	ax3.set_yticks(range(16,40,2))

	grid(True)

	# Fourth Panel, watts
	ax4 = fig1.add_subplot(4,1,4)
	ax4.plot(df.ix[:,'cum_dist'],df.ix[:,' Power (watts)'])
	ax4.axis([0,end_dist,100,500])
	ax4.set_xticks(range(1000,end_dist,1000))
	ax4.set_xlabel('Dist (km)')
	ax4.set_ylabel('Watts')
	ax4.set_yticks(range(150,450,50))
	grid(True)
	majorKmFormatter = FuncFormatter(format_dist_tick)
	majorLocator = (1000)
	ax4.xaxis.set_major_formatter(majorKmFormatter)

	plt.subplots_adjust(hspace=0)
	
	fig2 = plt.figure(figsize=(12,10))
	fig_title = "Input File:  "+self.readFile+" --- Stroke Metrics"
	
	# Top plot is pace
	ax5 = fig2.add_subplot(4,1,1)
	ax5.plot(df.ix[:,'cum_dist'],df.ix[:,' Stroke500mPace (sec/500m)'])
	ax5.axis([0,end_dist,180,90])
	ax5.set_xticks(range(1000,end_dist,1000))
	ax5.set_ylabel('(sec/500)')
	ax5.set_yticks(range(175,95,-10))
	grid(True)
	ax5.set_title(fig_title)
	majorFormatter = FuncFormatter(format_pace_tick)
	majorLocator = (5)
	ax5.yaxis.set_major_formatter(majorFormatter)
	
	# next we plot the drive length
	ax6 = fig2.add_subplot(4,1,2)
	ax6.plot(df.ix[:,'cum_dist'],df.ix[:,' DriveLength (meters)'])
	ax6.axis([0,end_dist,1.3,1.6])
	ax6.set_xticks(range(1000,end_dist,1000))
	ax6.set_ylabel('Drive Len(m)')
	ax6.set_yticks(np.arange(1.35,1.6,0.05))
	grid(True)

	# next we plot the drive time and recovery time
	ax7 = fig2.add_subplot(4,1,3)
	ax7.plot(df.ix[:,'cum_dist'],df.ix[:,' DriveTime (ms)']/1000.)
	ax7.plot(df.ix[:,'cum_dist'],df.ix[:,' StrokeRecoveryTime (ms)']/1000.)
	ax7.axis([0,end_dist,0.0,3.0])
	ax7.set_xticks(range(1000,end_dist,1000))
	ax7.set_ylabel('Drv / Rcv Time (s)')
	ax7.set_yticks(np.arange(0.2,3.0,0.2))
	grid(True)

	# Peak and average force
	ax8 = fig2.add_subplot(4,1,4)
	ax8.plot(df.ix[:,'cum_dist'],df.ix[:,' AverageDriveForce (lbs)'])
	ax8.plot(df.ix[:,'cum_dist'],df.ix[:,' PeakDriveForce (lbs)'])
	ax8.axis([0,end_dist,0,300])
	ax8.set_xticks(range(1000,end_dist,1000))
	ax8.set_xlabel('Dist (m)')
	ax8.set_ylabel('Force (lbs)')
	ax8.set_yticks(range(25,300,25))
	grid(True)
	majorLocator = (1000)
	ax8.xaxis.set_major_formatter(majorKmFormatter)
	

	plt.subplots_adjust(hspace=0)

	plt.show()
	print "done"
    
    def plottime_erg(self):
	""" Creates two images containing interesting plots

	x-axis is time

	Used with painsled (erg) data
	

	"""

	df = self.df
	fig1 = plt.figure(figsize=(12,10))
	fig_title = "Input File:  "+self.readFile+" --- HR / Pace / Rate / Power"

	# First panel, hr
	ax1 = fig1.add_subplot(4,1,1)
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_ut2'],color='gray', ec='gray')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_ut1'],color='y',ec='y')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_at'],color='g',ec='g')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_tr'],color='blue',ec='blue')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_an'],color='violet',ec='violet')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_max'],color='r',ec='r')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_ut2'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_ut1'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_at'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_tr'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_an'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_max'],color='k')
	ax1.text(5,self.rower.ut2+1.5,"UT2",size=8)
	ax1.text(5,self.rower.ut1+1.5,"UT1",size=8)
	ax1.text(5,self.rower.at+1.5,"AT",size=8)
	ax1.text(5,self.rower.tr+1.5,"TR",size=8)
	ax1.text(5,self.rower.an+1.5,"AN",size=8)
	ax1.text(5,self.rower.max+1.5,"MAX",size=8)

	end_time = int(df.ix[df.shape[0]-1,'TimeStamp (sec)'])
	ax1.axis([0,end_time,100,1.1*self.rower.max])
	ax1.set_xticks(range(0,end_time,300))
	ax1.set_ylabel('BPM')
	ax1.set_yticks(range(110,190,10))
	ax1.set_title(fig_title)
	timeTickFormatter = NullFormatter()
	ax1.xaxis.set_major_formatter(timeTickFormatter)

	grid(True)

	# Second Panel, Pace
	ax2 = fig1.add_subplot(4,1,2)
	ax2.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,' Stroke500mPace (sec/500m)'])
	end_time = int(df.ix[df.shape[0]-1,'TimeStamp (sec)'])
	ax2.axis([0,end_time,150,90])
	ax2.set_xticks(range(0,end_time,300))
	ax2.set_ylabel('(sec/500)')
	ax2.set_yticks(range(145,90,-5))
	# ax2.set_title('Pace')
	grid(True)
	majorFormatter = FuncFormatter(format_pace_tick)
	majorLocator = (5)
	ax2.xaxis.set_major_formatter(timeTickFormatter)
	ax2.yaxis.set_major_formatter(majorFormatter)

	# Third Panel, rate
	ax3 = fig1.add_subplot(4,1,3)
	ax3.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,' Cadence (stokes/min)'])
	rate_ewma = pd.ewma
	ax3.axis([0,end_time,14,40])
	ax3.set_xticks(range(0,end_time,300))
	ax3.set_xlabel('Time (sec)')
	ax3.set_ylabel('SPM')
	ax3.set_yticks(range(16,40,2))
	# ax3.set_title('Rate')
	ax3.xaxis.set_major_formatter(timeTickFormatter)
	grid(True)

	# Fourth Panel, watts
	ax4 = fig1.add_subplot(4,1,4)
	ax4.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,' Power (watts)'])
	ax4.axis([0,end_time,100,500])
	ax4.set_xticks(range(0,end_time,300))
	ax4.set_xlabel('Time (h:m)')
	ax4.set_ylabel('Watts')
	ax4.set_yticks(range(150,450,50))
	# ax4.set_title('Power')
	grid(True)
	majorTimeFormatter = FuncFormatter(format_time_tick)
	majorLocator = (15*60)
	ax4.xaxis.set_major_formatter(majorTimeFormatter)

	plt.subplots_adjust(hspace=0)
	
	fig2 = plt.figure(figsize=(12,10))
	fig_title = "Input File:  "+self.readFile+" --- Stroke Metrics"

	# Top plot is pace
	ax5 = fig2.add_subplot(4,1,1)
	ax5.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,' Stroke500mPace (sec/500m)'])
	end_time = int(df.ix[df.shape[0]-1,'TimeStamp (sec)'])
	ax5.axis([0,end_time,150,90])
	ax5.set_xticks(range(0,end_time,300))
	ax5.set_ylabel('(sec/500)')
	ax5.set_yticks(range(145,90,-5))
	grid(True)
	ax5.set_title(fig_title)
	majorFormatter = FuncFormatter(format_pace_tick)
	majorLocator = (5)
	ax5.xaxis.set_major_formatter(timeTickFormatter)
	ax5.yaxis.set_major_formatter(majorFormatter)

	# next we plot the drive length
	ax6 = fig2.add_subplot(4,1,2)
	ax6.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,' DriveLength (meters)'])
	ax6.axis([0,end_time,1.3,1.6])
	ax6.set_xticks(range(0,end_time,300))
	ax6.set_xlabel('Time (sec)')
	ax6.set_ylabel('Drive Len(m)')
	ax6.set_yticks(np.arange(1.35,1.6,0.05))
	ax6.xaxis.set_major_formatter(timeTickFormatter)
	grid(True)

	# next we plot the drive time and recovery time
	ax7 = fig2.add_subplot(4,1,3)
	ax7.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,' DriveTime (ms)']/1000.)
	ax7.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,' StrokeRecoveryTime (ms)']/1000.)
	ax7.axis([0,end_time,0.0,3.0])
	ax7.set_xticks(range(0,end_time,300))
	ax7.set_xlabel('Time (sec)')
	ax7.set_ylabel('Drv / Rcv Time (s)')
	ax7.set_yticks(np.arange(0.2,3.0,0.2))
	ax7.xaxis.set_major_formatter(timeTickFormatter)
	grid(True)

	# Peak and average force
	ax8 = fig2.add_subplot(4,1,4)
	ax8.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,' AverageDriveForce (lbs)'])
	ax8.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,' PeakDriveForce (lbs)'])
	ax8.axis([0,end_time,0,300])
	ax8.set_xticks(range(0,end_time,300))
	ax8.set_xlabel('Time (h:m)')
	ax8.set_ylabel('Force (lbs)')
	ax8.set_yticks(range(25,300,25))
	# ax4.set_title('Power')
	grid(True)
	majorTimeFormatter = FuncFormatter(format_time_tick)
	majorLocator = (15*60)
	ax8.xaxis.set_major_formatter(majorTimeFormatter)


	plt.subplots_adjust(hspace=0)

	plt.show()
	print "done"

    def plottime_hr(self):
	""" Creates a HR vs time plot

	"""
	
	df = self.df
	fig1 = plt.figure(figsize=(12,10))
	fig_title = "Input File:  "+self.readFile+" --- HR "

	# First panel, hr
	ax1 = fig1.add_subplot(1,1,1)
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_ut2'],color='gray', ec='gray')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_ut1'],color='y',ec='y')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_at'],color='g',ec='g')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_tr'],color='blue',ec='blue')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_an'],color='violet',ec='violet')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_max'],color='r',ec='r')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_ut2'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_ut1'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_at'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_tr'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_an'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_max'],color='k')
	ax1.text(5,self.rower.ut2+1.5,"UT2",size=8)
	ax1.text(5,self.rower.ut1+1.5,"UT1",size=8)
	ax1.text(5,self.rower.at+1.5,"AT",size=8)
	ax1.text(5,self.rower.tr+1.5,"TR",size=8)
	ax1.text(5,self.rower.an+1.5,"AN",size=8)
	ax1.text(5,self.rower.max+1.5,"MAX",size=8)

	end_time = int(df.ix[df.shape[0]-1,'TimeStamp (sec)'])
	ax1.axis([0,end_time,100,1.1*self.rower.max])
	ax1.set_xticks(range(0,end_time,300))
	ax1.set_ylabel('BPM')
	ax1.set_yticks(range(110,190,10))
	ax1.set_title(fig_title)
	timeTickFormatter = NullFormatter()
	ax1.xaxis.set_major_formatter(timeTickFormatter)

	grid(True)

    def plotmeters_otw(self):
	""" Creates two images containing interesting plots

	x-axis is distance

	Used with OTW data (no Power plot)
	

	"""

	df = self.df
	fig1 = plt.figure(figsize=(12,10))
	fig_title = "Input File:  "+self.readFile+" --- HR / Pace / Rate "

	# First panel, hr
	ax1 = fig1.add_subplot(3,1,1)
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_ut2'],color='gray', ec='gray')
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_ut1'],color='y',ec='y')
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_at'],color='g',ec='g')
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_tr'],color='blue',ec='blue')
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_an'],color='violet',ec='violet')
	ax1.bar(df.ix[:,'cum_dist'],df.ix[:,'hr_max'],color='r',ec='r')
	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_ut2'],color='k')
	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_ut1'],color='k')
	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_at'],color='k')
	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_tr'],color='k')
	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_an'],color='k')
	ax1.plot(df.ix[:,'cum_dist'],df.ix[:,'lim_max'],color='k')
	ax1.text(5,self.rower.ut2+1.5,"UT2",size=8)
	ax1.text(5,self.rower.ut1+1.5,"UT1",size=8)
	ax1.text(5,self.rower.at+1.5,"AT",size=8)
	ax1.text(5,self.rower.tr+1.5,"TR",size=8)
	ax1.text(5,self.rower.an+1.5,"AN",size=8)
	ax1.text(5,self.rower.max+1.5,"MAX",size=8)

	end_dist = int(df.ix[df.shape[0]-1,'cum_dist'])

	ax1.axis([0,end_dist,100,1.1*self.rower.max])
	ax1.set_xticks(range(1000,end_dist,1000))
	ax1.set_ylabel('BPM')
	ax1.set_yticks(range(110,200,10))
	ax1.set_title(fig_title)

	grid(True)

	# Second Panel, Pace
	ax2 = fig1.add_subplot(3,1,2)
	ax2.plot(df.ix[:,'cum_dist'],df.ix[:,' Stroke500mPace (sec/500m)'])
	ax2.axis([0,end_dist,180,90])
	ax2.set_xticks(range(1000,end_dist,1000))
	ax2.set_ylabel('(sec/500)')
	ax2.set_yticks(range(175,95,-10))
	grid(True)
	majorTickFormatter = FuncFormatter(format_pace_tick)
	majorLocator = (5)
	ax2.yaxis.set_major_formatter(majorTickFormatter)

	# Third Panel, rate
	ax3 = fig1.add_subplot(3,1,3)
	ax3.plot(df.ix[:,'cum_dist'],df.ix[:,' Cadence (stokes/min)'])
	ax3.axis([0,end_dist,14,40])
	ax3.set_xticks(range(1000,end_dist,1000))
	ax3.set_xlabel('Distance (m)')
	ax3.set_ylabel('SPM')
	ax3.set_yticks(range(16,40,2))

	grid(True)


	plt.subplots_adjust(hspace=0)
	
	fig2 = plt.figure(figsize=(12,10))
	fig_title = "Input File:  "+self.readFile+" --- Stroke Metrics"
	
	# Top plot is pace
	ax5 = fig2.add_subplot(2,1,1)
	ax5.plot(df.ix[:,'cum_dist'],df.ix[:,' Stroke500mPace (sec/500m)'])
	ax5.axis([0,end_dist,180,90])
	ax5.set_xticks(range(1000,end_dist,1000))
	ax5.set_ylabel('(sec/500)')
	ax5.set_yticks(range(175,95,-10))
	grid(True)
	ax5.set_title(fig_title)
	majorFormatter = FuncFormatter(format_pace_tick)
	majorLocator = (5)
	ax5.yaxis.set_major_formatter(majorFormatter)
	
	# next we plot the stroke distance
	ax6 = fig2.add_subplot(2,1,2)
	ax6.plot(df.ix[:,'cum_dist'],df.ix[:,' StrokeDistance (meters)'])
	ax6.axis([0,end_dist,5,12])
	ax6.set_xlabel('Distance (m)')
	ax6.set_xticks(range(1000,end_dist,1000))
	ax6.set_ylabel('Stroke Distance (m)')
	ax6.set_yticks(np.arange(5.5,11.5,0.5))
	grid(True)
	

	plt.subplots_adjust(hspace=0)

	plt.show()
	print "done"
    

    def plottime_otw(self):
	""" Creates two images containing interesting plots

	x-axis is time

	Used with OTW data (no Power plot)
	

	"""

	df = self.df
	fig1 = plt.figure(figsize=(12,10))
	fig_title = "Input File:  "+self.readFile+" --- HR / Pace / Rate "

	# First panel, hr
	ax1 = fig1.add_subplot(3,1,1)
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_ut2'],color='gray', ec='gray')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_ut1'],color='y',ec='y')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_at'],color='g',ec='g')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_tr'],color='blue',ec='blue')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_an'],color='violet',ec='violet')
	ax1.bar(df.ix[:,'TimeStamp (sec)'],df.ix[:,'hr_max'],color='r',ec='r')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_ut2'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_ut1'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_at'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_tr'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_an'],color='k')
	ax1.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,'lim_max'],color='k')
	ax1.text(5,self.rower.ut2+1.5,"UT2",size=8)
	ax1.text(5,self.rower.ut1+1.5,"UT1",size=8)
	ax1.text(5,self.rower.at+1.5,"AT",size=8)
	ax1.text(5,self.rower.tr+1.5,"TR",size=8)
	ax1.text(5,self.rower.an+1.5,"AN",size=8)
	ax1.text(5,self.rower.max+1.5,"MAX",size=8)

	end_time = int(df.ix[df.shape[0]-1,'TimeStamp (sec)'])
	ax1.axis([0,end_time,100,1.1*self.rower.max])
	ax1.set_xticks(range(0,end_time,300))
	ax1.set_ylabel('BPM')
	ax1.set_yticks(range(110,190,10))
	ax1.set_title(fig_title)
	timeTickFormatter = NullFormatter()
	ax1.xaxis.set_major_formatter(timeTickFormatter)

	grid(True)

	# Second Panel, Pace
	ax2 = fig1.add_subplot(3,1,2)
	ax2.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,' Stroke500mPace (sec/500m)'])
	end_time = int(df.ix[df.shape[0]-1,'TimeStamp (sec)'])
	ax2.axis([0,end_time,180,90])
	ax2.set_xticks(range(0,end_time,300))
	ax2.set_ylabel('(sec/500)')
	ax2.set_yticks(range(175,90,-5))
	# ax2.set_title('Pace')
	grid(True)
	majorFormatter = FuncFormatter(format_pace_tick)
	majorLocator = (5)
	ax2.xaxis.set_major_formatter(timeTickFormatter)
	ax2.yaxis.set_major_formatter(majorFormatter)

	# Third Panel, rate
	ax3 = fig1.add_subplot(3,1,3)
	ax3.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,' Cadence (stokes/min)'])
	rate_ewma = pd.ewma
	ax3.axis([0,end_time,14,40])
	ax3.set_xticks(range(0,end_time,300))
	ax3.set_xlabel('Time (sec)')
	ax3.set_ylabel('SPM')
	ax3.set_yticks(range(16,40,2))
	# ax3.set_title('Rate')
	ax3.xaxis.set_major_formatter(timeTickFormatter)
	grid(True)


	majorTimeFormatter = FuncFormatter(format_time_tick)
	majorLocator = (15*60)
	ax3.set_xlabel('Time (h:m)')
	ax3.xaxis.set_major_formatter(majorTimeFormatter)
	plt.subplots_adjust(hspace=0)
	
	fig2 = plt.figure(figsize=(12,10))
	fig_title = "Input File:  "+self.readFile+" --- Stroke Metrics"

	# Top plot is pace
	ax5 = fig2.add_subplot(2,1,1)
	ax5.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,' Stroke500mPace (sec/500m)'])
	end_time = int(df.ix[df.shape[0]-1,'TimeStamp (sec)'])
	ax5.axis([0,end_time,180,90])
	ax5.set_xticks(range(0,end_time,300))
	ax5.set_ylabel('(sec/500)')
	ax5.set_yticks(range(175,90,-5))
	grid(True)
	ax5.set_title(fig_title)
	majorFormatter = FuncFormatter(format_pace_tick)
	majorLocator = (5)
	ax5.xaxis.set_major_formatter(timeTickFormatter)
	ax5.yaxis.set_major_formatter(majorFormatter)

	# next we plot the drive length
	ax6 = fig2.add_subplot(2,1,2)
	ax6.plot(df.ix[:,'TimeStamp (sec)'],df.ix[:,' StrokeDistance (meters)'])
	ax6.axis([0,end_time,5,12])
	ax6.set_xticks(range(0,end_time,300))
	ax6.set_xlabel('Time (sec)')
	ax6.set_ylabel('Stroke Distance (m)')
	ax6.set_yticks(np.arange(5.5,11.5,0.5))
	ax6.xaxis.set_major_formatter(timeTickFormatter)
	grid(True)


	majorTimeFormatter = FuncFormatter(format_time_tick)
	majorLocator = (15*60)
	ax6.set_xlabel('Time (h:m)')
	ax6.xaxis.set_major_formatter(majorTimeFormatter)
	plt.subplots_adjust(hspace=0)

	plt.show()
	print "done"

    def uploadtoc2(self,
		   comment="uploaded by rowingdata tool\n",
		   rowerFile="defaultrower.txt"):
	""" Upload your row to the Concept2 logbook

	Will ask for username and password if not known
	Will offer to store username and password locally for you.
	This is not mandatory

	This just fills the online logbook form. It may break if Concept2
	changes their website. I am waiting for a Concept2 Logbook API

	"""

	comment+=self.readFile

	# prepare the needed data
	# Date
	datestring = "{mo:0>2}/{dd:0>2}/{yr}".format(
	    yr = self.rowdatetime.year,
	    mo = self.rowdatetime.month,
	    dd = self.rowdatetime.day
	    )

	rowtypenr = [1]
	weightselect = ["L"]

	# row type
	availabletypes = getrowtype()
	try:
	    rowtypenr = availabletypes[self.rowtype]
	except KeyError:
	    rowtypenr = [1]


	# weight
	if (self.rower.weightcategory.lower()=="lwt"):
	    weightselect = ["L"]
	else:
	    weightselect = ["H"]

	df = self.df

	# total dist, total time, avg pace, avg hr, max hr, avg dps

	totaldist = df['cum_dist'].max()
	totaltime = df['TimeStamp (sec)'].max()
	avgpace = 500*totaltime/totaldist
	avghr = df[' HRCur (bpm)'].mean()
	maxhr = df[' HRCur (bpm)'].max()
	avgspm = df[' Cadence (stokes/min)'].mean()
	avgdps = totaldist/(totaltime*avgspm/60.)

	hour=int(totaltime/3600)
	min=int((totaltime-hour*3600.)/60)
	sec=int((totaltime-hour*3600.-min*60.))
	tenth=int(10*(totaltime-hour*3600.-min*60.-sec))

	# log in to concept2 log, ask for password if it isn't known
	print "login to concept2 log"
	save_user = "y"
	save_pass = "y"
	if self.rower.c2username == "":
	    save_user = "n"
	    self.rower.c2username = raw_input('C2 user name:')
	    save_user = raw_input('Would you like to save your username (y/n)? ')
	    
	if self.rower.c2password == "":
	    save_pass = "n"
	    self.rower.c2password = getpass.getpass('C2 password:')
	    save_pass = raw_input('Would you like to save your password (y/n)? ')

	# try to log in to logbook
	br = mechanize.Browser()
	loginpage = br.open("http://log.concept2.com/login")

	# the login is the first form
	br.select_form(nr=0)
	# set user name
	usercntrl = br.form.find_control("username")
	usercntrl.value = self.rower.c2username

	pwcntrl = br.form.find_control("password")
	pwcntrl.value = self.rower.c2password

	response = br.submit()
	if "Incorrect" in response.read():
	    print "Incorrect username/password combination"
	    print ""
	else:
	    # continue
	    print "login successful"
	    print ""
	    br.select_form(nr=0)

	    br.form['type'] = rowtypenr
	    print "setting type to "+self.rowtype

	    datecntrl = br.form.find_control("date")
	    datecntrl.value = datestring
	    print "setting date to "+datestring

	    distcntrl = br.form.find_control("distance")
	    distcntrl.value = str(int(totaldist))
	    print "setting distance to "+str(int(totaldist))

	    hrscntrl = br.form.find_control("hours")
	    hrscntrl.value = str(hour)
	    mincntrl = br.form.find_control("minutes")
	    mincntrl.value = str(min)
	    secscntrl = br.form.find_control("seconds")
	    secscntrl.value = str(sec)
	    tenthscntrl = br.form.find_control("tenths")
	    tenthscntrl.value = str(tenth)

	    print "setting duration to {hour} hours, {min} minutes, {sec} seconds, {tenth} tenths".format(
		hour = hour,
		min = min,
		sec  = sec,
		tenth = tenth
		)

	    br.form['weight_class'] = weightselect

	    print "Setting weight class to "+self.rower.weightcategory+"("+weightselect[0]+")"

	    commentscontrol = br.form.find_control("comments")
	    commentscontrol.value = comment
	    print "Setting comment to:"
	    print comment

	    print ""

	    res = br.submit()

	    if "New workout added" in res.read():

		# workout added
		print "workout added"
	    else:
		print "something went wrong"

	if save_user == "n":
	    self.rower.c2username = ''
	    print "forgetting user name"
	if save_pass == "n":
	    self.rower.c2password = ''
	    print "forgetting password"


	if (save_user == "y" or save_pass == "y"):
	    self.rower.write(rowerFile)
	    

	print "done"


def dorowall(readFile="testdata",window_size=20):
    """ Used if you have CrewNerd TCX and summary CSV with the same file name

    Creates all the plots and spits out a text summary (and copies it
    to the clipboard too!)

    """

    tcxFile = readFile+".TCX"
    csvsummary = readFile+".CSV"
    csvoutput = readFile+"_data.CSV"

    tcx = rowingdata.TCXParser(tcxFile)
    tcx.write_csv(csvoutput,window_size=window_size)

    res = rowingdata.rowingdata(csvoutput)
    res.plotmeters_otw()

    sumdata = rowingdata.summarydata(csvsummary)
    sumdata.shortstats()

    sumdata.allstats()
