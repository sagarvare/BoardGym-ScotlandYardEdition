
class thief:
    def __init__(self, depth = '2', evalFn = None):
        self.index = 0
        self.depth = int(depth)
        if evalFn is not None:
            self.evaluationFunction = evalFn

    def evaluationFunction(self, gameState, action):
        pass


class MinimaxAgent(thief):
  """
    Your minimax agent (problem 1)
  """

  def getAction(self, gameState):
      pass


class AlphaBetaAgent(thief) :

    def getAction(self, gameState):
        pass