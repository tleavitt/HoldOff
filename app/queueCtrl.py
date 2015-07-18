from queueBuffer import QueueBuffer

class QueueCtrl(object):
	def __init__(self):
		self.bufferList = {}
		return

	def createChannel(self, id):
		if id in self.bufferList:
			return
		else:
			self.bufferList[id] = QueueBuffer()

	def getNextFrom(self, id):
		if id in self.bufferList:
			return self.bufferList[id].get()
		else:
			return None

	def putNext(self, id, priority, QAlist):
		if id in self.bufferList:
			self.bufferList[id].put(priority, QAlist)
		else:
			return

	def empty(self, id):
		if id in self.bufferList:
			return self.bufferList[id].empty()
		else:
			False

# if __name__=="__main__":
# 	ctrl = QueueCtrl()
# 	ctrl.createChannel('VISA')
# 	ctrl.createChannel('Sales')
# 	ctrl.putNext('VISA',2.5,[('What is the meal','burger'),("Name","Tom")])
# 	ctrl.putNext('VISA',3.5,[('What is the meal','Sandwich'),("Name","James")])
# 	ctrl.putNext('VISA',1.5,[('What is the meal','burger'),("Name","Rebecca")])
# 	ctrl.putNext('Sales',1.4,[('What is the meal','food'),("Name","Will")])

# 	print ctrl.empty('Sales')
# 	ctrl.getNextFrom('Sales')
# 	ctrl.getNextFrom('VISA')
# 	print ctrl.empty('Sales')
# 	ctrl.getNextFrom('VISA')
# 	ctrl.getNextFrom('VISA')
# 	print ctrl.empty('VISA')
