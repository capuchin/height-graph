#!/usr/bin/env python

from lxml import etree
import math 
import cmath
import matplotlib.pyplot as plt
from optparse import OptionParser
import re


def nestedSplit(astring, sep=None, *subsep):
    """
	nestedSplit(astring, sep=None, *subsep): given astring, and one or more split
    strings, it splits astring hierarchically. The first split key is the higher level one.
    Ex.: nestedSplit("a b\nc d", "\n", " ") => [['a', 'b'], ['c', 'd']] 
	"""
    if subsep:
        return [nestedSplit(fragment, *subsep) for fragment in astring.split(sep)]
    return astring.split(sep)

def getTrackFromKML(filepath):
	""" 
	Takes a path to kml file 
	returns a list containing [lat, long, elevation] triples
	"""
	f = open(filepath, 'r')
	str = f.read()
	root = etree.fromstring(str)

	regex = re.compile('{\S+}coordinates')

	coords= []
	for child in root.iter():
		if regex.match(child.tag):
			coords.append(child.text)

	print "found %d lines in file" % len(coords)

	# split each coord triple on whitespace
	# then append each triple as a list to coord_list
	regex2 = re.compile('\s+')
	s = regex2.split(coords[0])
	coord_list = []
	for i in s:
		coord_list.append(i.split(','))

	new_coord_list = []
	for item in coord_list:
		triple = []
		for n in item:
			s = n.strip()
			try:
				triple.append( float(s))
			except ValueError:
				pass
		if (len(triple)!=0):
			new_coord_list.append(triple)
	return new_coord_list
		
def getDist(lat1,long1,lat2,long2):
	"""
	Calc the distance between 2 points using Vincenty
	"""
	lat1 = math.radians(lat1)
	long1 = math.radians(long1)
	lat2 = math.radians(lat2)
	long2 = math.radians(long2)
	R = 6371 # km
	d = cmath.acos(cmath.sin(lat1) * cmath.sin(lat2) + \
	cmath.cos(lat1) * cmath.cos(lat2) *
	cmath.cos(long2 - long1)) * R
	return abs(d) # cast to float
	
def addDistToTrack(track):
	"""
	Add distance from last point to track
	"""
	for i in range(0, len(track)):		
		if (i == 0):
			prev = track[i]			
			track[i].append(0)
		else:
			prev = track[i-1]
			track[i].append(getDist(prev[0], prev[1], track[i][0], track[i][1]))	
	return track

def addCumDistToTrack(track):
	"""
	Add total
	"""
	tot = 0
	for i in range(0, len(track)):		
		tot += track[i][3]
		track[i].append(tot)
	return track


parser = OptionParser()
parser.add_option("-i", "--input-file", dest="input_file",
                  help="kml file to read from", metavar="FILE")
parser.add_option("-t", "--title", dest="title",
                  help="title text used on graphic", metavar="TITLE")

(options, args) = parser.parse_args()

track = getTrackFromKML(options.input_file)
track = addDistToTrack(track)
track = addCumDistToTrack(track)

max_ele = 0
min_ele = 0
tot_dist = 0
for i in track:
	tot_dist += i[3]
	if i[2] > max_ele:
		max_ele = i[2]
	if  i[2] < min_ele:	
		mix_ele = i[2]

print "tot dist: " + str(tot_dist)
print "max ele: " + str(max_ele)
print "min ele :" + str(min_ele)


x =[]
y = []
for i in track:
#for i in range(len(track), 0):
	x.append(i[4])
	y.append(i[2])




plt.plot(x, y)
ttext = plt.title(options.title)
ytext = plt.ylabel('Elevation (m)')
xtext = plt.xlabel('Distance (km)')
plt.setp(xtext, size='medium', name='courier', weight='bold', color='black')

plt.show()


"""
triple1 = track[0]
triple2 = track[1]
print triple1
print triple2
print getDist(triple1[0], triple1[1], triple2[0], triple2[1])
"""
