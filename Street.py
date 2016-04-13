
class Street(object):
	intersection_1 = ""
	intersection_2 = ""
	length = 0;
	speeds = {}

	def __init__(self, inte_1, inte_2, l):

		self.intersection_1 = inte_1
		self.intersection_2 = inte_2
		self.length = l
		for x in range(0,24):
			tempList = []
			#speeds["abc"] = tempList
			self.speeds[x] = tempList

	def addSpeed(self, time, velocity):
		#print (self.intersection_1+"-"+self.intersection_2)
		#print (velocity)
		#print (time)
		#print (self.speeds)
		speeds_list = self.speeds[time]
		speeds_list.append(velocity)
		#print (len(self.speeds))
		#print (speeds_list)
		#print (self.speeds)
		#print (len(speeds_list))

	def getSpeed(self):
		return len(self.speeds)

	def getName(self):
		return self.intersection_1+"-"+self.intersection_2

	def getAvgSpeed(self):
		avgSpeed = []
		#print (self.speeds.get(2))
		for i in range(1,24):
			speeds = self.speeds.get(i)
			sumSpeed = 0
			for s in speeds:
				sumSpeed += s
			avgSpeed.append(sumSpeed/len(speeds))

		return avgSpeed

	def getCarCount(self):
		hrs = []

		for i in range(1,24):
			speeds = self.speeds.get(i)
			count = 0
			for s in speeds:
				count += 1
			hrs.append(count)

		return hrs