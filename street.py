
class Street(object):
	intersection_1 = ""
	intersection_2 = ""
	length = 0; #distance between two intersections
	speeds = {} #list of speeds by the hour
	travelTime = {} #list of travel time by the hour
	timeLog = []
	speedLog = []

	def __init__(self, inte_1, inte_2, l):

		self.intersection_1 = inte_1
		self.intersection_2 = inte_2
		self.length = l
		self.speeds = {}
		self.travelTime = {}
		self.timeLog = []
		self.speedLog = []
		for x in range(0,24):
			newSpeedList = []
			newTravelTimeList = []
			#speeds["abc"] = tempList
			self.speeds[x] = newSpeedList
			self.travelTime[x] = newTravelTimeList



	def logged(self, timeStamp, velocity):
		self.timeLog.append(timeStamp)
		self.speedLog.append(velocity)

	def getTimeLog(self):
		return self.timeLog

	def getSpeedLog(self):
		return self.speedLog


	def addSpeed(self, time, velocity):
		#print (self.intersection_1+"-"+self.intersection_2)
		#print (velocity)
		#print (time)
		#print (self.speeds)

		speeds_list = self.speeds[time]
		speeds_list.append(velocity)
		#self.speeds[time] = speeds_list

		#print (len(self.speeds))
		#print (speeds_list)
		#print (self.speeds)
		#print (len(speeds_list))

	def addTravelTime(self, time, travelTime):

		travelTime_list = self.travelTime[time]
		travelTime_list.append(travelTime)



	def getSpeed(self):
		return len(self.speeds)

	def getName(self):
		return self.intersection_1+"-"+self.intersection_2

	def getAvgSpeed(self):
		avgSpeed = []
		#print (self.speeds)

		for i in range(0,24):
			speeds = self.speeds.get(i)
			if len(speeds) < 1:
				avgSpeed.append(0)
				continue
			sumSpeed = 0
			for s in speeds:
				sumSpeed += s
			avgSpeed.append(sumSpeed/len(speeds))

		return avgSpeed


	def getAvgTime(self):
		avgTravelTime = []
		for i in range(0,24):
			travelTime = self.travelTime.get(i)
			if len(travelTime) < 1:
				avgTravelTime.append(0)
				continue
			sumTime = 0
			for s in travelTime:
				sumTime += s
			#print (sumTime)
			#print (len(travelTime)
			#print (sumTime/len(travelTime) / 60)
			#
			#print (sumTime)
			#print (len(travelTime))
			#print (sumTime/len(travelTime))
			#print (sumTime/len(travelTime)/60)
			#inp = input("check")

			avgTravelTime.append( (sumTime/len(travelTime))/60 )

		return avgTravelTime

	def getCarCount(self):
		hrs = []

		for i in range(0,24):
			speeds = self.speeds.get(i)
			count = 0
			for s in speeds:
				count += 1
			hrs.append(count)

		return hrs