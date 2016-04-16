
from street import Street
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg

Streets = {} 

#	Take in 2 intersections and return the distance between the Them
def getDistance(intersection_1, intersection_2):
	
	st = None
	if intersection_1 == intersection_2:
		return 0
	if intersection_1 < intersection_2:
		st = Streets.get(intersection_1+"-"+intersection_2)
	else:
		st = Streets.get(intersection_2+"-"+intersection_1)

	#if no such street exists, return None
	return None if st is None else st.length


#Convert time of the day to second starting from midnight
def convertToSec(time, period):


	t = time.split(':')
	#if t[0] == 0:
	#	print (t)
	if(period == 'PM'):
		return (int(t[0])%12 * 3600) + (int(t[1]) * 60) + int(t[2]) + 43200
	else:
		return (int(t[0])%12 * 3600) + (int(t[1]) * 60) + int(t[2])


#add the speed of that street
def updateSpeed(intersection_1, intersection_2, velocity, time, timeStamp):
	#find that specific street between two intersections
	st = None
	if intersection_1 < intersection_2:
		st = Streets.get(intersection_1+"-"+intersection_2)
	else:
		st = Streets.get(intersection_2+"-"+intersection_1)
	if st == None:
		print("Error: No Street Found")


	### update the street object ###

	t = time[1].split(':')
	hour = int(t[0])
	#if hour == 0:
	#	print (time[1])
	if time[2] == "PM" :
		hour = (hour % 12) + 12

	else:
		hour %= 12

#	print (intersection_1)
#	print (intersection_2)
#	print (velocity)
#	print (st.getName())
#	inp = input("check")
	st.addSpeed(hour, velocity)
	st.logged(timeStamp / 3600, velocity)



def updateTravelTime(intersection_1, intersection_2, travelTime, time):

	#travelTime in term of seconds


	#find that specific street between two intersections
	st = None
	if intersection_1 < intersection_2:
		st = Streets.get(intersection_1+"-"+intersection_2)
	else:
		st = Streets.get(intersection_2+"-"+intersection_1)

	if st == None:
		print("Error: No Street Found")


	### update the street object ###

	t = time[1].split(':')
	hour = int(t[0])
	#if hour == 0:
	#	print (time[1])
	if time[2] == "PM" :
		hour = (hour % 12) + 12
	else:
		hour = hour % 12

	st.addTravelTime(hour, travelTime)


# Check if the car has been registered
def checkKey(key, dict):
	keys = dict.keys()
	if key in keys:
		return True
	else :
		return False

# create a logs of all speed between 2 intersection
def getSpeed(speeds , carID, cars):
	#speedList is [time_1, time_2, velocty, street_1, street_2, carID]
	speedList = []
	logs = []
	#get all the log and sort it
	for log in cars.get(carID):
		logs.append(log)
	logs.sort()

	for i in range(len(logs)):
		dist = 0
		if (i+1) < len(logs):

			# return zero or None = not in straight path
			# Get distance between two intersection
			intersection_1 = logs[i+1][3]
			intersection_2 = logs[i][3]
			dist = getDistance(intersection_1, intersection_2)
			if dist is None:
				continue

			# Get time : ['mm/dd/yyyy', 'hh:mm:ss', 'AM']
			time1 = logs[i][0].split()
			time2 = logs[i+1][0].split()

			# check if it's on the same day
			if( time1[0] == time2[0]):
				# convert to second
				t1 = convertToSec(time1[1], time1[2])
				t2 = convertToSec(time2[1], time2[2])
				delTime = abs(t1 - t2)
				
				#convert to mile/hr
				if delTime == 0:
					print (t1)
					print (time1)
					print (t2)
					print (time2)
					inp = input("hi")
				velocity = float(dist/delTime) * 3600
				if(velocity < 20): #threshold velocity
					continue

				# add speed to the list of speed in object street
				#print (intersection_1)
				#print (intersection_2)
				#print (velocity)
				#inp = input("Check")
				updateSpeed(intersection_1, intersection_2, velocity, time1, (t1+t2)/2)
				updateTravelTime(intersection_1, intersection_2, delTime, time1)


				#"{} and {}".format("string", 1)
				#print ("{}, {}, {}m/h, {}-{}, {}".format(logs[i][0],logs[i+1][0], '%.2f' % (velocity), logs[i][3], logs[i+1][3], logs[i][4]))
				#print (velocity)

				speed = [logs[i][0],logs[i+1][0], velocity, logs[i][3], logs[i+1][3], logs[i][4]]
				speedList.append(speeds)
	
	if len(speedList) > 0:
		speeds[carID] = speedList	


# Read in file
def readFile(fileName, cars, car_speeds):
	f = open(fileName, 'r');
	 

	for line in f:

		if line == "\n":
			break

		capture = line.split(',')
		macID = capture[4]

		if not checkKey(macID, cars):
			logs = [capture]
			cars[macID] = logs
			car_speeds[macID] = {}

		else :
			logs = cars[macID]
			logs.append(capture)
			cars[macID] = logs

# add more streets
def addStreet(str_lists, intersection_1, intersection_2, distance):

	if(intersection_1 < intersection_2):
		str_lists[intersection_1 + "-" + intersection_2] = Street(intersection_1,
		 intersection_2, distance)
		#return Street(intersection_1, intersection_2, distance)
	else:
		str_lists[intersection_2 + "-" + intersection_1] = Street(intersection_2,
		 intersection_1, distance)
		#return Street(intersection_2, intersection_1, distance)


def cal():
	cars = {}
	car_speeds = {}
	#street_avg_speed = {x for x in distances.keys()}

	readFile('Iteris_bt_05-18-2014.txt', cars, car_speeds)

	for key in cars.keys():
		getSpeed(car_speeds, key, cars)
		if not len(car_speeds[key]) > 0:
			del car_speeds[key]


###### Create Streets ######
addStreet(Streets, "Lincoln_Statecollege", "Lincoln_East", 0.8)
addStreet(Streets, "Lincoln_East", "Lincoln_Harbor", 1.0)
addStreet(Streets, "Lincoln_Euclid", "Lincoln_Harbor", 1.3)


cal()


if __name__ == '__main__':
	import sys
	for key, value in Streets.items():
		#print (value.getAvgSpeed())
		#value.getAvgSpeed()
		#print (value.getAvgTime())

		#print (value.getTimeLog())
		#print (len(value.getSpeedLog()))
		print (value.getName())

	s = input("Select Street: ")


	app = QtGui.QApplication([])

	win = pg.GraphicsWindow(title="Traffic Graph")
	#win = pg.GraphicsLayoutWidget(title="Traffic Graph")
	win.resize(1000,600)
	win.setWindowTitle("Traffic Graph")

	p1 = win.addPlot(title="Average Speed per Hour", x = np.arange(24), y = Streets.get(s).getAvgSpeed())
	x = Streets.get(s).getTimeLog()
	y = Streets.get(s).getSpeedLog()
	p1.plot(x, y, pen=None, symbol='t', symbolPen=None, symbolSize=10, symbolBrush=(100, 100, 255, 50))
	p1.setLabel('bottom', 'Hour', 's')
	p1.setLabel('left', 'Average Speed', 'mile/hr')

	p2 = win.addPlot(title="Car Count per Hour", x = np.arange(24), y = Streets.get(s).getCarCount())
	p2.setLabel('bottom', 'Hour', 's')
	p2.setLabel('left', 'Car Count', 's')

	win.nextRow()

	
	p3 = win.addPlot(title="Average Travel Time per Hour", x = np.arange(24), y = Streets.get(s).getAvgTime())
	p3.setLabel('bottom', 'Hour', 's')
	p3.setLabel('left', 'Average Travel time', 'm')


	if(sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
		QtGui.QApplication.instance().exec_()
