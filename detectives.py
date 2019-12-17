
import collections
from utils import raiseNotDefined

class Detectives :
    def __init__(self, depth = '2', evalFn = None):
        #super(Detectives, self).__init__()
        self.numAgents = 5
        self.depth = int(depth)
        if evalFn is not None:
            self.evaluationFunction = evalFn

    def evaluationFunction(self, gameState, action):
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