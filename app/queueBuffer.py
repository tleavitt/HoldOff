try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q

#private
class _Person(object):
    def __init__(self, priority, QAlist):
        self.priority = priority
        self.QAlist = QAlist
        return

    def getQA(self):
        return self.QAlist

    def __cmp__(self, other):
        return cmp(self.priority, other.priority)

#public
class QueueBuffer(object):
    def __init__(self):
        self.q = Q.PriorityQueue()
        return

    #return next QAlist
    def get(self):
        person = self.q.get()
        #for p in person.getQA(): print p
        return person.getQA()

    def put(self, priority, QAlist):
        person = _Person(priority, QAlist)
        self.q.put(person)

    def empty(self):
        return self.q.empty()

    def getLen():
        return self.q.qsize()

# if __name__ == "__main__":
#     qb = QueueBuffer()
#     qb.put(2.5,[('What is the meal','burger'),("Name","Tom")])
#     qb.put(3.5,[('What is the meal','Sandwich'),("Name","James")])
#     qb.put(1.5,[('What is the meal','burger'),("Name","Rebecca")])
#     qb.put(1.4,[('What is the meal','food'),("Name","Will")])
#     print qb.empty()
#     qb.get()
#     qb.get()
#     print qb.empty()
#     qb.get()
#     qb.get()
#     print qb.empty()
