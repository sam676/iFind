Stephanie Michalowicz
Digital Forensics
Final Project
NYU

iFind: A python command line reverse geocoding location request and response tool based on the coordinates of cell phone towers pinged by a user's mobile device and obtained through records provided by their wireless carrier. 

To run, you must first install gmaps by running the following command:

pip install gmaps

'-tower' cell tower data
'-record' phone record
'-directory' output directory
'-heatmap' show a heat map
'-polygon' create a polygon to triangulate area between towers
'-lines' show an outline / line
'-markers'show markers colored by record type
'-order' show order of activity
'-activity' show phone record activity type (i.e., ping, call, SMS, email
'-day' show the date
'-time'show the time

 ______________________


TO DO:
1)  if tower IDs are already sorted and tower list is larger than data file, convert to binary sort to decrease run time from O(n log n) to: best case O(1) average/ worst case O(log n)

2)  Convert if/else to switch case method - is there a way in python besides using functions or lambdas?

3)  Give option to show times/dates in a range

4)  Figure out how to scale the legend and make it float 