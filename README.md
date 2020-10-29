Stephanie Michalowicz
Digital Forensics
Final Project
NYU

iFind: A python command line reverse geocoding location request and response tool based on the coordinates of cell phone towers pinged by a user's mobile device and obtained through records provided by their wireless carrier. 

To run, you must first install gmaps by running the following command:

pip install gmaps

'-tower' cell tower data <br/>
'-record' phone record<br/>
'-directory' output directory<br/>
'-heatmap' show a heat map<br/>
'-polygon' create a polygon to triangulate area between towers<br/>
'-lines' show an outline / line<br/>
'-markers'show markers colored by record type<br/>
'-order' show order of activity<br/>
'-activity' show phone record activity type (i.e., ping, call, SMS, email<br/>
'-day' show the date<br/>
'-time'show the time<br/>
<br/>

 ______________________ <br/>
|     Map Legend       | <br/>
|______________________|<br/>
|______________________|<br/>
| Color   Record Type  |<br/>
|~~~~~~~~~~~~~~~~~~~~~~|<br/>
| Blue    | SMS        |<br/>
| Red     | Email      |<br/>
| Green   | Ping       |<br/>
| Yellow  | Call       |<br/>
|______________________|<br/>
| Black   | First Tower|<br/>
|______________________|<br/>
|______________________|<br/>
| Line    | Tower Path |<br/>
|______________________|<br/>
|______________________|<br/>
| Blue    | Potential  |<br/>
| Area    | Location   |<br/>
|______________________|<br/>

 ______________________
 
<br/>

TO DO:
1)  If tower IDs are already sorted and tower list is larger than data file, convert to binary sort to decrease run time from O(n log n) to: best case O(1) average/ worst case O(log n)

2)  Convert if/else to switch case method - is there a way in python besides using functions or lambdas?

3)  Give option to show times/dates in a range

4)  Figure out how to scale the legend and make it float 
