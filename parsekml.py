from lxml import etree
import math 
import cmath

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
	coords= []
	for child in root.iter():
		if child.tag == "{http://earth.google.com/kml/2.2}coordinates":
			coords.append(child.text)
	#if (len(coords)):
	#	coord_list = nestedSplit(coords[0], "\n", ",")
	coord_list = nestedSplit(coords[1], "\n", ",")
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
			track[i].append(getDist(prev[0], prev[1], track[i][0], track[i][1]))	
	return track

track = getTrackFromKML('/home/mike/Desktop/maps/kml/1_1_1_1.kml')
track = addDistToTrack(track)
print track

max_ele = 0
min_ele = 0
tot_dist = 0
for i in track:
	tot_dist += i[3]
	if i[2] > max_ele:
		max_ele = i[2]
	if  i[2] < min_ele:	
		mix_ele = i[2]
print tot_dist
print max_ele
print min_ele

import matplotlib.pyplot as plt
x =[]
y = []
for i in track:
	x.append(i[3])
	y.append(i[2])
plt.plot(x, y)
plt.show()


"""
triple1 = track[0]
triple2 = track[1]
print triple1
print triple2
print getDist(triple1[0], triple1[1], triple2[0], triple2[1])
"""
