import os
import sys
sys.path.append('.')
sys.path.append('../')
import Board
import utils

class Agent:
    """
    An agent must define a getAction method, but may also define the
    following methods which will be called if they exist:

    def registerInitialState(self, state): # inspects the starting state
    """
    def __init__(self, index=0):
        self.index = index

    def getAction(self, state, board):
        """
        The Agent will receive a GameState (from either {pacman, capture, sonar}.py) and
        must return an action from Directions.{North, South, East, West, Stop}
        """
        utils.raiseNotDefined()

    def GetLegalMoves(self):
        utils.raiseNotDefined()


class Constants:
    input_file_name = 'SCOTMAP.TXT'
    current_directory = '../data'


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
        print('The starting positions of all the player is {}'.format(self.state.occupied_positions))
        for turn in range(1,22):
            print('Playing turn {}'.format(turn))
            for player_idx in range(6):
                action = self.PlayTurn(player_idx)
                print('Action chosen by the player {} is {} and {}'.format(player_idx, action[0], action[1]))
                if player_idx == 0:
                    if self.CheckGameOver():
                        print('game over')
                        sys.exit(0)
                # update state
                self.update(player_idx, action)
            if self.CheckGameOver() :
                print('game over')
                sys.exit(0)
                #TODO Call another function, that displays the outcome, game history and other stats and details of the current game.
                #TODO Exit from the script.

            self.state.move_number += 1
            print('The new occupied positions by the players are {}'.format(self.state.occupied_positions))
                # Check if game over
        return

    def PlayTurn(self, ind):
        if ind == 0:
            player = self.thief
        else :
            player = self.detectives[ind-1] #since the detectives list start with 0 indexing but the detectives player index starts from 1
        return player.getAction(self.state, self.board)


    def update(self, player, action):
        """

        :param player: Index of the current player
        :param action: The action taken by the current
        :return: Updates the gamestate a per the player action.
        """
        self.state.current_player = player
        self.state.occupied_positions[player] = action[0]

        if player == 0:
            if self.state.move_number in [5, 8, 13, 18]:
                self.state.last_thief_location = action[1]
            self.state.thief.position = action[1]
            if action[1] == 'T' :
                self.state.thief.taxi_tickets -= 1
            elif action[1] == 'B' :
                self.state.thief.bus_tickets -= 1
            elif action[1] == 'U' :
                self.state.thief.ug_ticket -= 1
            elif action[1] == 'F' :
                self.state.thief.ferry_tickets -= 1
        else:
            detective = getattr(self.state, 'detective%d' % player)
            detective.position = action[1]
            if action[1] == 'T' :
                detective.taxi_tickets -= 1
            elif action[1] == 'B' :
                detective.bus_tickets -= 1
            elif action[1] == 'U' :
                detective.ug_ticket -= 1

        return

    def CheckGameOver(self):
        if self.state.occupied_positions[0] in self.state.occupied_positions[1:]:
            self.state.outcome = 2 # detectives wins
            return True
        elif self.state.move_number == 21:
            self.state.outcome = 1 # thief wins
            return True

        return False

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
        self.outcome = 0