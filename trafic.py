
from Street import Street


distances = { 'Euclid-Harbor' :	1.3, 'East-Harbor': 1.0, 'East-Statecollege': 0.8}
Streets = {} 
'''
# distance between two intersections
def getDistance(street1, street2):

	s1 = street1.split('_')
	s2 = street2.split('_')
	streets = [s1[0], s1[1], s2[0], s2[1]]
	#streets = set(s1[0],s1[1],s2[0],s2[1])
	streets = sorted(set(streets))	
	#l3 = [x for x in l1 if x not in l2]
	streets = [x for x in streets if not (x in s1 and x in s2)]

	if len(streets) != 2:
		#print ("Error")
		return 0	

	streets.sort()
	return distances.get(streets[0]+'-'+streets[1])
'''

def getDistance(intersection_1, intersection_2):
	
	if intersection_1 == intersection_2:
		return 0
	if intersection_1 < intersection_2:
		st = Streets.get(intersection_1+"-"+intersection_2)
		if st is None:
			return None
		else:
			return st.length
		#return Streets[intersection_1+"-"+intersection_2].length
	else:
		st = Streets.get(intersection_2+"-"+intersection_1)
		if st is None:
			return None
		else:
			return st.length
		#return Streets[intersection_2+"-"+intersection_1].length



def convertToSec(time, period):

	#convert to second, add time period if pm
	# 12 hrs = 43200s
	ti = time.split()
	
	t = ti[0].split(':')
	if(period == 'PM'):
		return (int(t[0]) * 3600) + (int(t[1]) * 60) + int(t[2]) + 43200
	else:
		return (int(t[0]) * 3600) + (int(t[1]) * 60) + int(t[2])
	


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
#	for i in logs:
#		print (i)

	for i in range(len(logs)):
		dist = 0
		if (i+1) < len(logs):

			# return zero or None = not in straight path
			# Get distance between two intersection
			dist = getDistance(logs[i+1][3], logs[i][3])
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
				
				velocity = float(dist/delTime) * 3600
				if(velocity < 20): #threshold velocity
					continue

				#"{} and {}".format("string", 1)
				print ("{}, {}, {}m/h, {}-{}, {}".format(logs[i][0],logs[i+1][0], '%.2f' % (velocity), logs[i][3], logs[i+1][3], logs[i][4]))
				#print (velocity)

				speed = [logs[i][0],logs[i+1][0], velocity, logs[i][3], logs[i+1][3], logs[i][4]]

				speedList.append(speeds)
				
				#speeds.append(speedList)
	

	if len(speedList) > 0:
		speeds[carID] = speedList	

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

def addStreet(str_lists, intersection_1, intersection_2, distance):

	if(intersection_1 < intersection_2):
		str_lists[intersection_1 + "-" + intersection_2] = Street(intersection_1,
		 intersection_2, distance)
		#return Street(intersection_1, intersection_2, distance)
	else:
		str_lists[intersection_2 + "-" + intersection_1] = Street(intersection_2,
		 intersection_1, distance)
		#return Street(intersection_2, intersection_1, distance)


def main():
	cars = {}
	car_speeds = {}
	street_avg_speed = {x for x in distances.keys()}

	readFile('Iteris_bt_05-18-2014.txt', cars, car_speeds)

	for key in cars.keys():
		getSpeed(car_speeds, key, cars)
		if not len(car_speeds[key]) > 0:
			del car_speeds[key]

	print (street_avg_speed)

	#print (len(car_speeds))
	#print (car_speeds)
	#############################


	### Find Average Travel Time for each edge ###
	#calculateAvergeSpeed(car_speeds, street_avg_speed)


##############################################

####Temporary Interface #######





#for key in cars.keys():
	#for log in cars.get(key):
		#print (log)


#print (getDistance('Lincoln_East', 'Lincoln_Harbor'))
addStreet(Streets, "Lincoln_Statecollege", "Lincoln_East", 0.8)
addStreet(Streets, "Lincoln_East", "Lincoln_Harbor", 1.0)
addStreet(Streets, "Lincoln_Euclid", "Lincoln_Harbor", 1.3)
print (Streets)
main()
