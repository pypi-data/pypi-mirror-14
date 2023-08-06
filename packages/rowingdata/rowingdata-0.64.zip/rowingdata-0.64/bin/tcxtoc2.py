#! /usr/bin/python
import rowingdata
from sys import argv

readFile = argv[1]

tcx = rowingdata.TCXParser(readFile)

file2 = readFile+"_o.csv"

tcx.write_csv(file2)

row = rowingdata.rowingdata(file2,rowtype="On-water")
row.uploadtoc2()



print "done "+readFile
