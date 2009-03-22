#!/usr/bin/env python

import csv
from optparse import OptionParser
import matplotlib.pyplot as plt

parser = OptionParser()
parser.add_option("-i", "--input-file", dest="input_file",
                  help="csv file to read from", metavar="FILE")
parser.add_option("-s", "--sections-file", dest="sections_file",
                  help="csv file to read section titles from", metavar="FILE")
parser.add_option("-t", "--title", dest="title",
                  help="title text used on graphic", metavar="TITLE")

(options, args) = parser.parse_args()

csvreader = csv.reader(open(options.input_file), delimiter=',', quotechar='|')
x =[]
y = []
for row in csvreader:
	x.append(float(row[0]))
	y.append(float(row[1]))

csvreader = csv.reader(open(options.sections_file), delimiter=',', quotechar='|')
titles =[]
distances = []
for row in csvreader:
	titles.append(row[0])
	distances.append(float(row[1]))

plt.subplot(111, axisbg = 'lightblue' )
plt.fill_between(x, y, facecolor='lightgreen', color='darkgreen')
##plt.axvline(x=3.5, ymax=250, linewidth=1, color='black')

accm_dist = 0
for i in range(0, len(titles)):	
	plt.text(accm_dist + distances[i]/2, 10, titles[i], rotation = 'vertical', fontsize=10)
	accm_dist += distances[i]
	for j in range(0, len(x)):
		if ( (accm_dist >= x[j]) ):
			top = y[j]
	plt.vlines(accm_dist, 0, top, color = 'darkgreen')

plt.axis([0, 10, 0, 450])

ttext = plt.title(options.title)
ytext = plt.ylabel('Altitude (m)')
xtext = plt.xlabel('Distance (km)')

plt.grid(True)
plt.setp(xtext, size='medium', name='courier', color='black')
plt.show()

