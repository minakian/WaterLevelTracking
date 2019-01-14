# WaterLevelTracking

Requires PySerial to be installed

Arguments:
* -p, --print option to print the read data to the commandline
* -s, --sleep	time in seconds to sleep between readings, default=60

Operatiom:
1. Detects the correct port for connecting
2. Opens the appropriate port
3. Reads the "WATER" data
4. Closes the port
5. Opens/Creates test.csv
6. Appends/Writes the data to said file
7. Repeats every 60 seconds from step 2

Use:
  From the commandline, navigate to the folder containing WaterCalTracking.py and give the following command:
  `python WaterCalTracking.py` or `python3 WaterCalTracking.py` depending on your installation