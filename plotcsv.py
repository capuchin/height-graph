#!/usr/bin/env python

import csv
from optparse import OptionParser
import matplotlib.pyplot as plt


parser = OptionParser()
parser.add_option("-i", "--input-file", dest="input_file",
                  help="csv file to read from", metavar="FILE")
parser.add_option("-t", "--title", dest="title",
                  help="title text used on graphic", metavar="TITLE")

(options, args) = parser.parse_args()

csvreader = csv.reader(open(options.input_file), delimiter=',', quotechar='|')


x =[]
y = []
for row in csvreader:
	x.append(float(row[0]))
	y.append(float(row[1]))


plt.subplot(111, axisbg = 'lightblue' )
plt.fill_between(x, y, facecolor='lightgreen', color='darkgreen')
plt.axis([0, 10, 0, 450])
ttext = plt.title(options.title)
ytext = plt.ylabel('Elevation (m)')
xtext = plt.xlabel('Distance (km)')
plt.grid(True)
plt.setp(xtext, size='medium', name='courier', weight='bold', color='black')
plt.show()

