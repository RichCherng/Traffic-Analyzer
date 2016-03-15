
class Street(object):
	intersection_1 = ""
	intersection_2 = ""
	speeds = {}

	def __init__(self, inte_1, inte_2):

		intersection_1 = inte_1
		intersection_2 = inte_2
		for x in range(0,24):
			tempList = []
			speeds[x] = tempList
