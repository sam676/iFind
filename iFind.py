#! /usr/bin/python

#Stephanie Michalowicz
#Digital Forensics
#Final Project
#iFind: A python command line reverse geocoding location request and response tool 
#based on the coordinates of cell phone towers pinged by a user's mobile device and 
#obtained through records provided by their wireless carrier

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
	#API Key
	key="AIzaSyBi93kmM1pdFNFtMlqZdbG7bzRYY9fon0k"

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
			towerNames.append(towerName)
			latitudes.append(float(tower[1]))
			longitudes.append(float(tower[2]))
		except:
			print(" ")

	#create lists for date, time, and record type
	data = dataFile.readline()
	dateList = []
	timeList = []
	recordList = []
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
		except:
			print(" " )

	gmap = gmplot.GoogleMapPlotter(latitudes[0], longitudes[0], 10)

	color = ""
	count = 0
	for record in recordList:
		if "SMS" in record:
			color = "blue"
		if "Ping" in record:
			color = "green"
		if "Email" in record:
			color = "red"
		lat = [latitudes[count]]
		longit = [longitudes[count]]
		gmap.scatter(lat, longit, color)
		count += 1
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

	gmap.polygon(latitudes, longitudes, color = 'blue')
	gmap.plot(latitudes,longitudes, 'red', edge_width = 3.0)

	print("\nCreating report.txt file.\n")
	f = open('{0}/report.csv'.format(directory), 'w')
	f.write("Tower ID, Latitudes, Longitudes, Time, Date, Record Type\n")
	counting = 0
	for record in recordList:
		f.write(towerNames[counting] + "," + str(latitudes[counting])+ "," + str(longitudes[counting])+ "," +  timeList[counting]  + "," + dateList[counting] + "," + recordList[counting]+ "\n")
		counting += 1

	gmap.apikey = key
	gmap.draw('{0}/Map.html'.format(directory))

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