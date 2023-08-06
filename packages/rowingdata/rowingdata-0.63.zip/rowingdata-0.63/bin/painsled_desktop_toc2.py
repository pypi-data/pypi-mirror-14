#! /usr/bin/python
import rowingdata
from sys import argv

readFile = argv[1]


res = rowingdata.painsledDesktopParser(readFile)

file2 = readFile+"_o.csv"

res.write_csv(file2)

row = rowingdata.rowingdata(file2,rowtype="Indoor Rower")
row.uploadtoc2()



print "done "+readFile
