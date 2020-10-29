#! /usr/bin/python

""""""""""""""""""""""
	Stephanie Michalowicz
	Digital Forensics
	Final Project

	iFind: A python command line reverse geocoding location request and response tool 
	based on the coordinates of cell phone towers pinged by a user's mobile device and 
	obtained through records provided by their wireless carrier

	Can be used to track the movement of wanted criminals, kidnappers, 
	drug / sex trafficking circles, or mobile phone thieves in real time 
	by pinging their phone when its on.

	Current tools only parse a phone's memory when obtained by warrent or at the scene of a crime.

	Processes Google Maps Javascript API responses through python.

"""""""""""""""""""""""

import fileinput
import argparse
import string
import gmplot							# pip install gmaps
from datetime import datetime

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


def getMap(towerFile, dataFile, directory, showHeatMap, showPolygon, showOutline, showMarkers, showOrder, showActivity, showDate, showTime):
	#API Demo Key 
	key="AIzaSyBi93kmM1pdFNFtMlqZdbG7bzRYY9fon0k"

	#store URL in variable URL
	url = "https://maps.googleapis.com/maps/api/staticmap?"

	#create a list of towers and corresponding coordinates
	tower = towerFile.readline()
	latitudes = []
	longitudes = []
	towerNames = []

	while(tower):
		try:
			tower = getTower(towerFile).split()
			towerNames.append(tower[0])
			latitudes.append(float(tower[1]))
			longitudes.append(float(tower[2]))
		except:
			print(" ")

	#create lists for phone record (date, time, and record type)
	data = dataFile.readline()
	dateList = []
	timeList = []
	recordList = []
	towerList = []

	while(data):
		try:
			data = getRecord(dataFile).split()
			dateList.append(data[0])
			timeList.append(data[1])
			recordList.append(data[2])
			towerList.append(data[3])
		except:
			print(" " )
	
	#match tower ID from data file to it's geographical location in the tower location file
	matchedLat = []
	matchedLong = []
															## TO DO:
	for index1, tower1  in enumerate(towerList):			## if tower IDs are already sorted and  
		for index2, tower2 in enumerate(towerNames):		## tower list is larger than data file,
			if tower1 == tower2:							## convert to binary sort to decrease  
				matchedLat.append(latitudes[index2])		## run time from O(n log n) to: best case O(1)
				matchedLong.append(longitudes[index2])      ## average/ worst case O(log n)
	
	#instantiate map with the first location and zoom size 
	gmap = gmplot.GoogleMapPlotter(matchedLat[0], matchedLong[0], 10)

	color = " "
	count = 0
	string = " "
	
	for index3, record in enumerate(recordList):    #TO DO: is there a switch case method in python besides using functions or lambdas??
		if "SMS" in record:
			color = "blue"

		if "Ping" in record:
			color = "green"

		if "Email" in record:
			color = "red"

		if "Call" in record:
    			color = "yellow"

		if (color != " "):
			lat = [latitudes[count]]
			longit = [longitudes[count]]

			if showMarkers:
				gmap.scatter(lat, longit, color)

			if showOrder:
    				string += str(count) + " "
			
			if showActivity:
    				string += record + " "
			
			if showTime:
    				string += timeList[index3] + " "    #TO DO: give option to show times/dates in a range

			if showDate:
    				string += dateList[index3] + " "

			#add selected text to the map
			gmap.text(latitudes[count], longitudes[count], string, color = color)
			count += 1
			string = " "

	if showPolygon:
		gmap.polygon(latitudes, longitudes, color = 'blue')

	if showOutline:
		gmap.plot(latitudes,longitudes, 'red', edge_width = 3.0)

	if showHeatMap:
		gmap.heatmap(latitudes, longitudes)
	
	#TO DO: figure out how to scale the legend on map.html and make it float

	#insert map legend 
	url = '/Users/stephaniemichalowicz/Desktop/iFind_Updated_2020/legend.png'
	bounds = {'north': 35.587376, 'south': 32.587376, 'east': -64.515560, 'west': -68.515560 }
	gmap.ground_overlay(url, bounds, opacity=0.5)

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
	print(" | Yellow  | Call       |")
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
	parser.add_argument('-towers', help='cell tower data', required=True)
	parser.add_argument('-record', help='phone record', required=True)
	parser.add_argument('-directory', help='output directory', required=True)
	parser.add_argument('-heatmap', action='store_true', help='show a heat map', required=False)
	parser.add_argument('-polygon', action='store_true', help='create a polygon to triangulate area between towers', required=False)
	parser.add_argument('-lines', action='store_true', help='show an outline / line', required=False)
	parser.add_argument('-markers', action='store_true', help='show markers colored by record type', required=False)
	parser.add_argument('-order', action='store_true', help='show order of activity', required=False)
	parser.add_argument('-activity', action='store_true', help='show phone record activity type (i.e., ping, call, SMS, email', required=False)
	parser.add_argument('-day', action='store_true', help='show the date', required=False)
	parser.add_argument('-time', action='store_true', help='show the time', required=False)

	args = parser.parse_args()
	cellTowers = args.towers
	records = args.record
	dirPath = args.directory
	heatMap = args.heatmap
	polygon = args.polygon
	outline = args.lines
	markers = args.markers
	order = args.order
	activity = args.activity
	date = args.day
	clock_time = args.time

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
		getMap(towerFile, dataFile, dirPath, heatMap, polygon, outline, markers, order, activity, date, clock_time)
		towerFile.close()
		dataFile.close()

if __name__ == '__main__':
	main()