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

    def evaluationFunction(self, gameState, action):
        # Ideas on evaluation function :
        # 1 :
        #
        #
        #
        pass

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