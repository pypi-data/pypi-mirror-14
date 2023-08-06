#! /usr/bin/python
import rowingdata
from sys import argv

readFile = argv[1]

outfile = readFile+"_o.csv"

res = rowingdata.painsledDesktopParser(readFile)
res.write_csv(outfile)

row = rowingdata.rowingdata(outfile,rowtype="Indoor Rower")

row.plotmeters_erg()

print row.allstats()



print "done "+readFile
