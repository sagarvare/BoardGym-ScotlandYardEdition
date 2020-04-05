from collections import defaultdict
import pandas as pd
import csv

class Node():
	def __init__(self, pos):
		self.pos = pos
		self.adjacent_bus_nodes = []
		self.adjacent_ug_nodes = []
		self.adjacent_taxi_nodes = []
		self.adjacent_ferry_nodes = []

class Board():
	def __init__(self, game_txt_file):
		self.total_nodes = -1
		self.total_edges = -1
		self.node_dict = {}
		self.ReadBoard(game_txt_file)

	def AddNode(self, node_number):
		'''
		Adds node to the board, if not present.
		'''
		if node_number not in self.node_dict:
			self.node_dict[node_number] = Node(node_number)


	def GetNode(self, node_number):
		'''
		Clients duty to make sure that the node_number is correct.
		Gets the specified by node_number.
		Assumes that the number specified is present in the dictionary.
		'''
		return self.node_dict[node_number]

	def AddEdge(self, node_number1, node_number2, edge_type):
		self.AddNode(node_number1)
		self.AddNode(node_number2)
		node_1 = self.GetNode(node_number1)
		node_2 = self.GetNode(node_number2)
		if edge_type == "B":
			node_1.adjacent_bus_nodes.append(node_number2)
			node_2.adjacent_bus_nodes.append(node_number1)
		elif edge_type == "U":
			node_1.adjacent_ug_nodes.append(node_number2)
			node_2.adjacent_ug_nodes.append(node_number1)
		elif edge_type == "T":
			node_1.adjacent_taxi_nodes.append(node_number2)
			node_2.adjacent_taxi_nodes.append(node_number1)
		elif edge_type == "F":
			node_1.adjacent_ferry_nodes.append(node_number2)
			node_2.adjacent_ferry_nodes.append(node_number1)
		else:
			print("Incorrect transportation format specified.")

	def GetPossibleMoves(self, node_number):
		"""
		returns a bunch of possible moves from the given node.
		"""
		node = self.GetNode(node_number)
		possible_moves = []

		for node_number in node.adjacent_ferry_nodes:
			possible_moves.append((node_number , "F"))

		for node_number in node.adjacent_taxi_nodes:
			possible_moves.append((node_number, "T"))

		for node_number in node.adjacent_bus_nodes:
			possible_moves.append((node_number, "B"))

		for node_number in node.adjacent_ug_nodes:
			possible_moves.append((node_number, "U"))

		return possible_moves   

	def ReadBoard(self, game_file):
		"""
		Reads the board in.
		"""
		with open(game_file) as f:
			row_count = 0
			file_reader = csv.reader(f, delimiter = ' ')
			for row in file_reader:
				if row_count == 0:
					## First row should contain total_nodes and total_edges
					try:
						row_count += 1
						self.total_nodes = int(row[0])
						self.total_edges = int(row[1])
						continue

					except:
						print("First row of file should contain total_nodes and total_edges.")
						return False
				## Next rows should have size three.
				if len(row) != 3:
					print("Each row in file after the first, should have length 3.")
					print("blacklisted row:", row)
					return False
				self.AddEdge(int(row[0]), int(row[1]), row[2])

	def GetNRandomPositions(self, N=6):
		'''
		Returns N random unique positions within the board.
		'''
		return [1, 10, 20, 30, 40, 50]

def RunTest():
	## TODO(svare) : Machine Independent test.
	game_file = "/Users/sagarvare/Documents/BoardGym-ScotlandYardEdition/data/SCOTMAP.TXT"
	board = Board(game_file)

	## Check for a basic test case.
	possible_moves = board.GetPossibleMoves(89)
	expected_possible_moves = set([(71, "T"), (88, "T"), (105, "T"), (55, "B"), (105, "B"), (13, "U"), (67, "U"), (140, "U"), (128, "U")])
	
	for move in possible_moves:
		if move in expected_possible_moves:
			continue
		else:
			print("not found move:", move,  " in expected_possible_moves")
			return False


	for move in expected_possible_moves:
		if move in possible_moves:
			continue
		else:
			print("not found move:", move,  " in possible_moves")
			return False
	return True




if __name__ == '__main__':
	if RunTest():
		print("Test Successful.")











		






