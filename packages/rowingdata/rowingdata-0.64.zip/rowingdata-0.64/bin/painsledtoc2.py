#! /usr/bin/python
import rowingdata
from sys import argv

readFile = argv[1]

row = rowingdata.rowingdata(readFile)
row.uploadtoc2()



print "done "+readFile
