#! /usr/bin/python
import rowingdata
from sys import argv

readFile = argv[1]

tcxFile = readFile+".TCX"
csvsummary = readFile+".CSV"
csvoutput = readFile+"_data.CSV"

tcx = rowingdata.TCXParser(tcxFile)
tcx.write_csv(csvoutput,window_size=20)

res = rowingdata.rowingdata(csvoutput,rowtype="On-water")
res.plotmeters_otw()

sumdata = rowingdata.summarydata(csvsummary)
sumdata.shortstats()

sumdata.allstats()




print "done "+readFile
