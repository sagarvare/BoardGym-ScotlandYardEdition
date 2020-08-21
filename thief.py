import copy
import random
import os
import sys
# sys.path.append('.')
sys.path.append('src/')
from scotlandyard import Agent

class Thief(Agent):
    def __init__(self, depth = '2', evalFn = None):
        self.index = 0
        self.depth = int(depth)
        if evalFn is not None:
            self.evaluationFunction = evalFn

    def evaluationFunction(self, gameState, action):
        pass

    def GetLegalMoves(self, gameState, moves):
        legal_moves = copy.deepcopy(moves)
        for move in moves:
            if move[1] == 'F' and gameState.thief.ferry_tickets <= 0:
                legal_moves.remove(move)

        return legal_moves

class RandomAgent(Thief):

    def getAction(self, gameState, board, current_pos):
        # current_pos = gameState.occupied_positions[self.index]
        moves = board.GetPossibleMoves(current_pos)
        legal_moves = self.GetLegalMoves(gameState,moves)

        return random.choice(legal_moves)


class MinimaxAgent(Thief):
  """
    Your minimax agent (problem 1)
  """

  def getAction(self, gameState):
      pass


class AlphaBetaAgent(Thief) :

    def getAction(self, gameState):
        pass