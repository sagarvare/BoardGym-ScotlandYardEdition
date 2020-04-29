import collections
import sys
sys.path.append('.')
sys.path.append('../')
from scotlandyard import Agent
import random
import copy
import pdb

class Detectives(Agent) :
    def __init__(self, index, evalFn = None):
        #super(Detectives, self).__init__()
        self.index = index
        if evalFn is not None:
            self.evaluationFunction = evalFn

        self.possible_thief_nodes = None

    def evaluationFunction(self, gameState, board, action, depth = 1):
        possible_detective_locations = set()
        explored_nodes = set()
        unexplored_nodes = [action]
        for i in range(depth):
            legal_moves = []
            while unexplored_nodes:
                option = unexplored_nodes.pop()
                explored_nodes.add(option)
                pseudo_gameState = pseudoUpdate(copy.deepcopy(gameState), self.index, option)
                moves = board.GetPossibleMoves(option[0])
                legal_moves = legal_moves + (self.GetLegalMoves(pseudo_gameState, moves))

            for move in legal_moves:
                if move not in explored_nodes:
                    unexplored_nodes.append(move)

        for move in legal_moves:
            possible_detective_locations.add(move[0])

        for node in self.possible_thief_nodes:
            thief_current_possible_nodes = board.GetPossibleMoves(node)
            #TODO(Saahil) to be completed


    def GetLegalMoves(self, gameState, moves):
        legal_moves = copy.deepcopy(moves)
        detective_state = getattr(gameState,'detective%d' % self.index)
        for move in moves:
            if moves[1] == 'F' :
                legal_moves.remove(move)
            elif moves[1] == 'T' and detective_state.taxi_tickets <= 0:
                legal_moves.remove(move)
            elif moves[1] == 'B' and detective_state.bus_tickets <= 0:
                legal_moves.remove(move)
            elif moves[1] == 'U' and detective_state.ug_tickets <= 0:
                legal_moves.remove(move)

            if move[0] in gameState.occupied_positions[1:]:
                legal_moves.remove(move)

        return legal_moves

    def UpdatePossibleThiefNodes(self, gameState, board, thief_mode, possible_thief_nodes):
        '''
        Calculates all the posible nodes
        :param gameState:
        :return:
        '''
        #TODO(Saahil) Write a test for testing this function
        new_thief_nodes = set()
        if self.index != 1: # if other than first detective, then just use what first detective has computed
            self.possible_thief_nodes = possible_thief_nodes.copy()
            return possible_thief_nodes
        if gameState.move_number < 5: return None

        if gameState.move_number in [5, 8, 13, 18]:
            new_thief_nodes = set(gameState.last_thief_location)

        else:
            for node in possible_thief_nodes:
                moves = board.GetPossibleMoves(node)
                for move in moves:
                    if move[1] == thief_mode:
                        new_thief_nodes.add(move[0])

        self.possible_thief_nodes = new_thief_nodes.copy()

        return new_thief_nodes

class RandomAgent(Detectives):

    def getAction(self, gameState, board):
        # detective_state = getattr(gameState, 'detective%d' % self.index)
        current_pos = gameState.occupied_positions[self.index]
        moves = board.GetPossibleMoves(current_pos)
        legal_moves = self.GetLegalMoves(gameState,moves)
        return random.choice(legal_moves)


class GreedyBFSAgent(Detectives):

    def getAction(self, gameState, board, depth=2):
        current_pos = gameState.occupied_positions[self.index]
        moves = board.GetPossibleMoves(current_pos)
        legal_moves = self.GetLegalMoves(gameState,moves)

class MinimaxAgent(Detectives):
  """
    Your minimax agent (problem 1)
  """

  def getAction(self, gameState):
      pass


class AlphaBetaAgent(Detectives) :

    def getAction(self, gameState):
        pass

class BasicColabAgent(Detectives):

    def __init__(self, detective_objects):
        self.detective_objects = detective_objects

    def getAction(self, gameState):
        all_actions = []
        for i, detective in enumerate(self.detective_objects):
            all_actions.append(detective.getAction(gameState))

        return all_actions

def betterEvaluationFunction(gameState, action):
    pass