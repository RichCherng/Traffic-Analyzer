
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
		#print (time)
		#print (self.speeds)
		speeds_list = self.speeds[time]
		speeds_list.append(velocity)
		#print (self.speeds)
		#print (len(speeds_list))