from src import Board
import random
import utils

class Agent:
  """
  An agent must define a getAction method, but may also define the
  following methods which will be called if they exist:

  def registerInitialState(self, state): # inspects the starting state
  """
  def __init__(self, index=0):
    self.index = index

  def getAction(self, state):
    """
    The Agent will receive a GameState (from either {pacman, capture, sonar}.py) and
    must return an action from Directions.{North, South, East, West, Stop}
    """
    utils.raiseNotDefined()


class Game:
    def __init__(self, file1, level, role, player_type = ['random'], no_of_human_players = 1):
        # levels will have options - every number corresponding to a default pre-defined
        # agents or a custom in which case it will take a string defining the agent type for thief and all detectives

        self.board = Board(file1)
        self.human_player = role # either 'thief' or 'detective'. if multiple players then it has to be designed differently
        self.players = ['theif', 'D1', 'D2', 'D3', 'D4', 'D5']
        self.agents = player_type

        if isinstance(level, int) and level <= 5 and level >= 1:
            self.level = level
        else :
            raise ValueError('The level should be of INTEGER type and should have values between 1-5')

        self.state = GameState(self.board.GetNRandomPositions())
        self.state.InitializeAgents(player_type, no_of_human_players)

        return

    def play(self):
        for player in self.players():
            self.PlayTurn(player)


    def PlayTurn(self, player):
        pass

    def update(self):
        pass

class Player:
    def __init__(self, position, bus_tickets, taxi_tickets, ug_tickets, ferry_tickets):
        self.bus_tickets = bus_tickets
        self.taxi_tickets = taxi_tickets
        self.ug_ticket = ug_tickets
        self.ferry_tickets = ferry_tickets
        self.position = position

    def PlayerStrategy(self):
        # initialize the agent with the specified strategy
        pass


class GameState:
    def __init__(self, positions):
        '''
        :param positions: a list of 6 integers that determine the starting position of each player
        '''
        self.thief = Player(positions[0], 1000, 1000, 1000, 3)
        self.detective1 = Player(positions[1], 12, 8, 4, 0)
        self.detective2 = Player(positions[2], 12, 8, 4, 0)
        self.detective3 = Player(positions[3], 12, 8, 4, 0)
        self.detective4 = Player(positions[4], 12, 8, 4, 0)
        self.detective5 = Player(positions[5], 12, 8, 4, 0)
        self.move_number = 1

    def InitializeAgents(self, p_type, no_of_human_players):

        if len(p_type) != no_of_human_players:
            raise RuntimeError("The strategies defined {} are not enough strategies defined for the provided number of "
                               "human players {}".format(p_type,no_of_human_players))
