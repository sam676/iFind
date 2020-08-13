#! /usr/bin/python

"""

Stephanie Michalowicz
Digital Forensics
Final Project

iFind: A python command line reverse geocoding location request and response tool 
based on the coordinates of cell phone towers pinged by a user's mobile device and 
obtained through records provided by their wireless carrier.
iFind matches tower_id in ISP record to local tower records, returns csv report, 
and draws a polygon over the estimated location of the user on Google Maps web page.
The scatter plot color refers to record type.

"""


import fileinput
import argparse
import string
import gmplot

def getTower(towerFile):
	#try opening cell tower data
	try:
		contents = towerFile.readline()
		return (contents)	
	except:
		print("Can't open cell tower file!")

def getRecord(dataFile):
	#try opening phone record
	try:
		dataContents = dataFile.readline()
		return(dataContents)
	except:
		print("Can't open data file!")

def getMap(towerFile, dataFile, directory):
	##API Key
	##REMOVED FOR SAFTEY REASONS##
	key="xxxxxxxxxxxxxxx"

	#store URL in variable URL
	url = "https://maps.googleapis.com/maps/api/staticmap?"

	#create a list of locations
	tower = towerFile.readline()
	latitudes = []
	longitudes = []
	towerNames = []

	while(tower):
		try:
			tower = getTower(towerFile)
			tower = tower.split()
			towerName = tower[0]
			towerNames.append(int(towerName))
			latitudes.append(float(tower[1]))
			longitudes.append(float(tower[2]))
		except:
			print(" ")

	#create lists for date, time, and record type
	data = dataFile.readline()
	dateList = []
	timeList = []
	recordList = []
	tower_id = []
	while(data):
		try:
			data = getRecord(dataFile)
			data = data.split()
			date = data[0]
			dateList.append(date)
			time = data[1]
			timeList.append(time)
			recordType = data[2]
			recordList.append(recordType)
			data_tower_name = int(data[3])
			tower_id.append(data_tower_name)
		except:
			print(" " )

	gmap = gmplot.GoogleMapPlotter(latitudes[0], longitudes[0], 10)

	print("Plotting data on map.html file.")
	print("  ______________________")
	print(" |     Map Legend       |")
	print(" |______________________|")
	print(" |______________________|")
	print(" | Color   Record Type  |")
	print(" |~~~~~~~~~~~~~~~~~~~~~~|")
	print(" | Blue    | SMS        |")
	print(" | Red     | Email      |")
	print(" | Green   | Ping       |")
	print(" |______________________|")
	print(" | Black   | First Tower|")
	print(" |______________________|")
	print(" |______________________|")
	print(" | Line    | Tower Path |")
	print(" |______________________|")
	print(" |______________________|")
	print(" | Blue    | Potential  |")
	print(" | Area    | Location   |")
	print(" |______________________|")

	color = ""
	latList = []
	longitList= []

	print("\nCreating report.txt file.\n")
	f = open('{0}/report.csv'.format(directory), 'w')
	f.write("Tower ID, Latitudes, Longitudes, Time, Date, Record Type\n")


	for index, record in enumerate(recordList):
		if "SMS" in record:
			color = "blue"
		if "Ping" in record:
			color = "green"
		if "Email" in record:
			color = "red"
		identifier = tower_id[index]

		if identifier in towerNames:
			towerNameIndex = towerNames.index(identifier)
			lat = latitudes[towerNameIndex]
			latList.append(lat)
			longit = longitudes[towerNameIndex]
			longitList.append(longit)
			gmap.scatter(latList, longitList, color)
			gmap.polygon(latList, longitList, "blue")
			gmap.plot(latList,longitList,"red", edge_width = 3.0)	
			gmap.apikey = key
			gmap.draw('{0}/Map.html'.format(directory))
			f.write('{0}, {1}, {2}, {3}, {4}, {5} \n'.format(towerNames[towerNameIndex],lat, longit, timeList[index], dateList[index], recordList[index]))
		else:
			print("No tower record for specified tower id.")

		
	# save and close the file 
	f.close() 

	print("done\n")


def main():
	#parse command line arguments 
	parser = argparse.ArgumentParser(description='Mobile tracking based on pinged cell tower location')
	parser.add_argument('-t', help='cell tower data', required=True)
	parser.add_argument('-r', help='phone record', required=True)
	parser.add_argument('-d', help='output directory', required=True)
	args = parser.parse_args()
	cellTowers = args.t
	records = args.r
	dirPath = args.d

	#confirm files exist, open it, and read column header 
	if not cellTowers:
	    print('No cell tower information was provided.')
	    exit(0)
	elif not records:
		print('No record data was provided.')
		exit(0)
	else:
		towerFile = open(cellTowers, 'r')
		dataFile = open(records, 'r')
		getMap(towerFile, dataFile, dirPath)
		towerFile.close()
		dataFile.close()


if __name__ == '__main__':
	main()
