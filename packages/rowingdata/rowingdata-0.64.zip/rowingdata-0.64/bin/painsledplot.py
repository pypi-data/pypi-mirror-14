#! /usr/bin/python
import rowingdata
from sys import argv

readFile = argv[1]


row = rowingdata.rowingdata(readFile,rowtype="Indoor Rower")

row.plotmeters_erg()

print row.allstats()



print "done "+readFile
