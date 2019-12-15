from collections import defaultdict

class Node():
	def __init__(self, pos):
		self.pos = pos
		self.adjacent_bus_nodes = []
		self.adjacent_ug_nodes = []
		self.adjacent_taxi_nodes = []
		self.adjacent_ferry_nodes = []

class Board():
	def __init__(self, total_nodes, total_edges):
		self.total_nodes = total_nodes
		self.total_edges = total_edges
		self.node_dict = {}

	def AddNode(self, node_number):
		if node_number not in self.node_dict:
			self.node_dict[node_number] = Node(node_number)


	def Get(self, node_number):
		'''
		Clients duty to make sure that the node_number is correct.
		Gets the specified by node_number.
		Assumes that the number specified is present in the dictionary.
		'''
		return self.node_dict[node_number]

	def AddEdge(self, node_number1, node_number2, edge_type):
		AddNode(node_number1)
		AddNode(node_number2)
		if edge_type == "B":
			node_number1.adjacent_bus_nodes.append(node_number2)
			node_number2.adjacent_bus_nodes.append(node_number1)
		elif edge_type == "UG":
			node_number1.adjacent_ug_nodes.append(node_number2)
			node_number2.adjacent_ug_nodes.append(node_number1)
		elif edge_type == "T":
			node_number1.adjacent_taxi_nodes.append(node_number2)
			node_number2.adjacent_bus_nodes.append(node_number1)
		elif edge_type == "F":
			node_number1.adjacent_ferry_nodes.append(node_number2)
			node_number2.adjacent_ferry_nodes.append(node_number1)
		else:
			print "Incorrect transportation format specified."

	def GetPossibleMoves(node_number):
		'''
		returns a bunch of possible moves.
		'''
		for mode






def  (filename):
	return
