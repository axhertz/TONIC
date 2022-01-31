
class Node:
	def __init__(self,key):
		self.gamma = 1
		self.key = key
		self.child_nodes = {}
		self.hashCost = 0
		self.nestCost = 0

	def addHashCost(self, cost):
		self.hashCost = self.hashCost*self.gamma + cost
	def addNestCost(self,cost):
		self.nestCost = self.nestCost*self.gamma + cost


	def getRecommended(self):
		if self.hashCost <= self.nestCost:
			return "HashJoin"
		else:
			return "NestLoop"

	def getNext(self,key, selectivity):
		if not key in self.child_nodes.keys():
			return Node(key)

		closestNode = None
		proximity = 1
		for interval in self.child_nodes[key].keys():
			if min(abs(selectivity-interval[1]), abs(selectivity-interval[0])) < proximity:
				proximity = min(abs(selectivity-interval[1]), abs(selectivity-interval[0]))
				closestNode = self.child_nodes[key][interval]
		if closestNode is not None:
			return closestNode
		return Node(key)


	def updateKey(self, key,costList, selectivity, immutable = False):
		if not key in self.child_nodes:
			newNode = Node(key)
			newNode.addHashCost(costList[0])
			newNode.addNestCost(costList[1])
			self.child_nodes[key]= {}
			if immutable:
				self.child_nodes[key][(0,1)] = newNode
			else:
				self.child_nodes[key][(selectivity,selectivity)] = newNode
			return
		closestNode = None
		proximity = 1

		for interval in self.child_nodes[key].keys():
			if interval[0] <= selectivity and interval[1] >= selectivity:
				self.child_nodes[key][interval].addHashCost(costList[0])
				self.child_nodes[key][interval].addNestCost(costList[1])
				return
			if min(abs(selectivity-interval[1]), abs(selectivity-interval[0])) < proximity:
				proximity = min(abs(selectivity-interval[1]), abs(selectivity-interval[0]))
				closestNode = interval
		if closestNode is not None:

			if self.child_nodes[key][closestNode].getRecommended() == "HashJoin" and (costList[0] < costList[1] or  abs(costList[0] - costList[1])< 0.01):
				self.child_nodes[key][closestNode].addHashCost(costList[0])
				self.child_nodes[key][closestNode].addNestCost(costList[1])
				self.child_nodes[key][(min(selectivity, closestNode[0]), max(selectivity, closestNode[1]))] = self.child_nodes[key].pop(closestNode)
				return
			if self.child_nodes[key][closestNode].getRecommended() == "NestLoop" and (costList[1] < costList[0] or  abs(costList[0] - costList[1])< 0.01):
				self.child_nodes[key][closestNode].addHashCost(costList[0])
				self.child_nodes[key][closestNode].addNestCost(costList[1])
				self.child_nodes[key][(min(selectivity, closestNode[0]), max(selectivity, closestNode[1]))] = self.child_nodes[key].pop(closestNode)
				return

		newNode = Node(key)
		newNode.addHashCost(costList[0])
		newNode.addNestCost(costList[1])
		self.child_nodes[key][(selectivity,selectivity)] = newNode


