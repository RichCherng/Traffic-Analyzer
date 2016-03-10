

distances = { 'Euclid-Harbor' :	1.3, 'East-Harbor': 1.0, 'East-Statecollege': 0.8}


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
	#intersections = ""
	if street1 < street2:
		#intersections += street1 + '-' + street2
		return distances.get(street1+'-'+street2)
	else :
		#intersections += street2 + '-' + street1
		return distances.get(street2+'-'+street1)
	'''


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
				'''
				print (delTime)
				print (dist)
				print (logs[i][3])
				print (logs[i+1][3])
				'''
				
				velocity = float(dist/delTime) * 3600
				if(velocity < 5): #threshold velocity
					continue

				#"{} and {}".format("string", 1)
				#print ("{}, {}, {}m/h, {}-{}, {}".format(logs[i][0],logs[i+1][0], '%.2f' % (velocity), logs[i][3], logs[i+1][3], logs[i][4]),end="")
				#print (velocity)

				speed = [logs[i][0],logs[i+1][0], velocity, logs[i][3], logs[i+1][3], logs[i][4]]

				speedList.append(speeds)
				
				#speeds.append(speedList)
	
	#print (speed)
	#print (len(speedList))
	if len(speedList) > 0:
		speeds[carID] = speedList	



cars = {}
speeds = {}
### Read in file ###
f = open('Iteris_bt_05-18-2014.txt', 'r');
#f = open('test.txt', 'r')
count = 0;
for line in f:
	count += 1
	if line == "\n":
		#print (line)
		break 
	capture = line.split(',')
	#date = capture[0]
	#intersection = capture[3]
	macID = capture[4]

	if not checkKey(macID, cars):
		logs = [capture]
		cars[macID] = logs
		speeds[macID] = {}
		#print ('added')
	else :
		logs = cars[macID]
		logs.append(capture)
		cars[macID] = logs

print (count)

### End of read file ###


### find speed of the car ###
for key in cars.keys():
	getSpeed(speeds, key, cars)
	#print (speeds.get(key))


#############################
#for key in cars.keys():
	#for log in cars.get(key):
		#print (log)


#print (getDistance('Lincoln_East', 'Lincoln_Harbor'))




#for index, item in enumerate(my_list):
#    print index, item

#for i in range(len(my_list)):
 #   print i