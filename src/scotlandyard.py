import Board
import random
# import utils
import os

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

    def GetLegalMoves(self):
        utils.raiseNotDefined()


class Constants:
    input_file_name = ''
    current_directory = ''


class Game:
    def __init__(self, role, thief, detectives, no_of_human_players = 1, level = 1):
        '''

        :param role: Whether the human player is playing as a thief or a detective
        :param thief: an object of class thief
        :param detectives: a list of 5 independent objects of class detective corresponding to each detective
        :param no_of_human_players: for future for multiple human players
        :param level: for different types of adverserial agents
        '''

        self.board = Board.Board(os.path.join(Constants.current_directory,Constants.input_file_name))
        self.human_player = role # either 'thief' or 'detective'. if multiple players then it has to be designed differently

        if isinstance(level, int) and level <= 5 and level >= 1:
            self.level = level
        else :
            raise ValueError('The level should be of INTEGER type and should have values between 1-5')

        self.thief = thief
        self.detectives = detectives
        self.state = GameState(self.board.GetNRandomPositions())
        return

    def play(self):
        for turn in range(1,22):
            for player in range(6):
                action = self.PlayTurn(player)

                # update state
                self.update(player, action)
            self.state.move_number += 1

                # Check if game over
        return

    def PlayTurn(self, ind):
        player = self.detectives[ind]
        return player.getAction(self.state)


    def update(self, player, action):
        self.state.current_player = player
        if player == 0:
            if self.state.move_number in [5, 8, 13, 18]:
                self.state.last_thief_location = action[1]
            self.state.occupied_positions[player] = action[1]
            self.state.thief[0] = action [1]
            if action[0] == 'T' :
                self.state.thief.taxi_tickets -= 1
            elif action[0] == 'B' :
                self.state.thief.bus_tickets -= 1
            elif action[0] == 'U' :
                self.state.thief.ug_ticket -= 1
            elif action[0] == 'F' :
                self.state.thief.ferry_tickets -= 1
        else:
            detective = getattr(self.state, 'detective%d' % player)
            detective.position = action[1]
            self.state.occupied_positions[action[1]]
            if action[0] == 'T' :
                detective.taxi_tickets -= 1
            elif action[0] == 'B' :
                detective.bus_tickets -= 1
            elif action[0] == 'U' :
                detective.ug_ticket -= 1
        return

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
        self.current_player = 0
        self.occupied_positions = positions.copy()
        self.last_thief_location = None

