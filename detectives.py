
import collections
from utils import raiseNotDefined
from src.scotlandyard import Agent

class Detectives(Agent) :
    def __init__(self, index, evalFn = None):
        #super(Detectives, self).__init__()
        self.index = index
        if evalFn is not None:
            self.evaluationFunction = evalFn

    def evaluationFunction(self, gameState, action):
        pass


class RandomAgent(Detectives):

    def getAction(self, gameState):
        pass


class MinimaxAgent(Detectives):
  """
    Your minimax agent (problem 1)
  """

  def getAction(self, gameState):
      pass


class AlphaBetaAgent(Detectives) :

    def getAction(self, gameState):
        pass




def betterEvaluationFunction(gameState, action):
    pass