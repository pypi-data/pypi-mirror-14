#! /usr/bin/python
import rowingdata
from sys import argv


try:
    rowerFile = argv[1]
except IndexError:
    rowerFile = "defaultrower.txt"

print rowingdata.roweredit(rowerFile)

print "done"
