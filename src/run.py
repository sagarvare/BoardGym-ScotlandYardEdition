from src import Board
import random

class Game():
    def __init__(self, file1, level, role, no_of_human_players = 1):
        # levels will have options - every number corresponding to a default pre-defined
        # agents or a custom in which case it will take a string defining the agent type for thief and all detectives

        self.board = Board(file1)
        self.human_player = role # either 'thief' or 'detective'. if multiple players then it has to be designed differently
        self.players = ['theif', 'D1', 'D2', 'D3', 'D4', 'D5']

        if isinstance(level, int) and level <= 5 and level >= 1:
            self.level = level
        else :
            raise ValueError('The level should be of INTEGER type and should have values between 1-5')

        self.state = GameState(self.board.GetNRandomPositions())



        return

class Player():
    def __init__(self, position, bus_tickets, taxi_tickets, ug_tickets, ferry_tickets):
        self.bus_tickets = bus_tickets
        self.taxi_tickets = taxi_tickets
        self.ug_ticket = ug_tickets
        self.ferry_tickets = ferry_tickets
        self.position = position

class GameState():
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



# ---------------------------------------------------------------------------------------------------------
#
#     Code Archive
#
# ---------------------------------------------------------------------------------------------------------
# def InitializeGame(self):
#     '''
#     Initialize the starting state of the game. Update the game state with start positions of each player and resources of each player
#     :return:
#     '''
#     start_positions = self.board.GetNRandomPositions()
#     self.state['thief']['start_pos'] = start_positions.pop(0)
#     for i, player in enumerate(self.players) :
#         self.state[player]['start_pos'] = start_positions[i]
#         self.
#         if player == 'thief':
#             self.state[player]['tickets'] = [1000,1000,1000]
#         else:
#             self.state[player]['tickets'] = [4,8,12]


