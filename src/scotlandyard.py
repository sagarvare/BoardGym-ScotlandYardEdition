import os
import sys
import utils
from collections import defaultdict
import copy
sys.path.append('.')
sys.path.append('../')
import Board
# from keyboardAgents import KeyboardAgent

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
        The Agent will receive a GameState (scotlandyard.py) and
        must return an action from one of the valid actions
        """
        utils.raiseNotDefined()

    def GetLegalMoves(self, state, moves):
        utils.raiseNotDefined()


class Constants:
    input_file_name = 'SCOTMAP.TXT'
    data_directory = '/Users/saahil/Documents/random/BoardGym-ScotlandYardEdition/data'
    max_turns = 22
    max_tries = 5
    number_of_players = 6


class Game:
    def __init__(self, role, thief, detectives, no_of_human_players = 1, level = 1):
        '''

        :param role: Whether the human player is playing as a thief or a detective
        :param thief: an object of class thief
        :param detectives: a list of 5 independent objects of class detective corresponding to each detective
        :param no_of_human_players: for future for multiple human players
        :param level: for different types of adverserial agents where higher level indicates more adavnced agent
        '''

        self.board = Board.Board(os.path.join(Constants.data_directory,Constants.input_file_name))
        self.human_player = role # either 'thief' or 'detective'. if multiple players then it has to be designed differently
        print(self.board.GetPossibleMoves(1))
        if isinstance(level, int) and level <= 5 and level >= 1:
            self.level = level
        else :
            raise ValueError('The level should be of INTEGER type and should have values between 1-5')

        self.thief = thief
        self.detectives = detectives
        start_positions = self.board.GetNRandomPositions()
        self.state = GameState(start_positions)
        self.log = defaultdict(list)
        self.log[0] = start_positions
        return

    def play(self):
        '''
        :return:
        '''

        print('The starting positions of all the player is {}'.format(self.state.occupied_positions))
        for turn in range(1,Constants.max_turns+1):
            actions = []
            print('Playing turn {}'.format(turn))
            for player_idx in range(6):
                action = self.PlayTurn(player_idx)
                max_try = Constants.max_tries
                while max_try and not self.ValidateAction(player_idx, action):
                    print(f'Invalid action : {action}. You have {max_try} try remaining.')
                    action = self.PlayTurn(player_idx)
                    max_try -= 1

                if not max_try:
                    print(f'Exceeded maximum number of attempts to choose a valid action for player : {player_idx}.'
                          f'Exiting run.')
                    sys.exit(1)

                print(f'Action chosen by the player {player_idx} is - node : {action[0]} and mode : {action[1]}')
                if player_idx == 0:
                    # update the possible locations for thief as per the new move. Update is needed only once using the
                    self.state.UpdatePossibleThiefNodes(self.board, action[1])

                actions.append(action)
                # self.state.last_moves.push(action[1])
                # update state
                self.UpdateState(player_idx, action)
                if self.CheckGameOver():
                    print('game over')
                    sys.exit(0)
                    # TODO Call another function, that displays game history and other stats and details of the current game.

            self.UpdateLog(turn, actions) #TODO(saahil) Write a test case for checking the UpdateLog code

            self.state.move_number += 1
            print('The new occupied positions by the players are {}'.format(self.state.occupied_positions))
        return

    def PlayTurn(self, ind):
        '''

        :param ind:
        :return:
        '''
        game_state_copy = copy.deepcopy(self.state)
        if ind == 0:
            player = self.thief
        else :
            game_state_copy.occupied_positions[0] = 'null'
            game_state_copy.thief.position = 'null'
            player = self.detectives[ind-1] #since the detectives list start with 0 indexing but the detectives player index starts from 1
        return player.getAction(game_state_copy, self.board)


    def ValidateAction(self, player_idx, action):
        if player_idx == 0:
            if self.state.thief.resources[action[1]] <= 0: return False

        else:
            player = getattr(self.state, 'detective%d' % player_idx)
            if action[1] == 'F' : return False
            if player.resources[action[1]] <= 0: return False
            if action[0] in self.state.occupied_positions[1:]: return False

        return True

    def UpdateState(self, player, action):
        """

        :param player: Index of the current player
        :param action: The action taken by the current
        :return: Updates the gamestate a per the player action.
        """
        if player == 0:
            if self.state.move_number in [5, 8, 13, 18]:
                self.state.last_thief_location = action[0]
            self.state.thief.position = action[0]
            self.state.thief.resources[action[1]] -= 1
        else:
            self.state.occupied_positions[player] = action[0]
            detective = getattr(self.state, 'detective%d' % player)
            detective.position = action[0]
            detective.resources[action[1]] -= 1
        self.state.current_player = (player+1) % Constants.number_of_players

        return

    def UpdateLog(self, turn, actions):
        '''
        Updates the log of the game with the actions take by each player during every turn. For thief it only updates
        the mode of transportation used.
        '''
        self.log[turn] = actions

    def Undo(self, no_steps = 1):
        # Allow users to undo an action.
        #TODO (svare) Write the undo function to revert the game by specified number of steps
        pass

    def CheckGameOver(self):
        '''

        :return:
        '''
        thief_location = self.state.thief.position # self.log[turn][0][0]
        if thief_location in self.state.occupied_positions[1:]:
            print("One of the detectives caught the thief.")
            print(f"Thief's location : {thief_location}")
            for idx in range(1,6):
                if (self.state.occupied_positions[idx] == thief_location):
                    print(f"The detective #{idx} caught the thief.")
            self.state.outcome = 2 # detectives wins
            return True
        elif self.state.move_number == Constants.max_turns - 1:
            self.state.outcome = 1 # thief wins
            print('Thief wins the game')
            return True

        return False


class Player:
    def __init__(self, position, taxi_tickets, bus_tickets, ug_tickets, ferry_tickets):
        self.resources = {'B': bus_tickets, 'T': taxi_tickets, 'U' : ug_tickets, 'F': ferry_tickets}
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
        self.occupied_positions = positions
        self.last_thief_location = None
        self.outcome = 0
        self.last_moves = utils.Stack() # a list containing the last mode of transportation used by the players
        self.possible_thief_nodes = None

    def UpdatePossibleThiefNodes(self, board, thief_mode):
        '''
        Calculates all the posible nodes where the thief could be, given previous possible locations for thief and the current move
        made by thief
        :param gameState:
        :param board:
        :param thief_mode: last mode of transport used by the thief
        :return: None. Updates the possible thief locations in GameState object
        '''
        new_thief_nodes = set()
        if self.move_number < 5: return []

        if self.move_number in [5, 8, 13, 18]:
            new_thief_nodes = set([self.last_thief_location])

        else:
            for node in self.possible_thief_nodes:
                moves = board.GetPossibleMoves(node) # (node, mode)
                for move in moves:
                    if thief_mode == 'black':
                        new_thief_nodes.add(move[0])
                    elif move[1] == thief_mode:
                        new_thief_nodes.add(move[0])

        self.possible_thief_nodes = new_thief_nodes

        return


# Unit tests for different functions

def test_UpdateState():
    import thief, detectives
    args = {}
    args['role'] = 'auto'
    args['thief'] = thief.RandomAgent()
    args['detectives'] = [detectives.RandomAgent(i + 1) for i in range(5)]
    game = Game(**args)
    player_idx = 1
    no_tests = 0
    passed_tests = 0

    print(game.state.occupied_positions)

    # To test - tickets and location of the corresponding playershould be updated,
    # for detectives
    tests = {(92, 'T') : [92, 11, 2, ['null', 92, 20, 30, 40, 50]], # answer - [new_pos, tickets left, next player, new positions of all]
             (94, 'B'): [94, 7, 2, ['null', 94, 20, 30, 40, 50]],
             (79, 'U'): [79, 3, 2, ['null', 79, 20, 30, 40, 50]]}

    for test, answer in tests.items():
        no_tests += 1
        game.state.detective1 = Player(93, 12, 8, 4, 0)
        # game.state.occupied_positions = ['null', 93, 20, 30, 40, 50]
        game.UpdateState(player=player_idx, action=test)
        print(game.state.occupied_positions, game.state.detective1.resources)
        if game.state.detective1.position == answer[0] and game.state.detective1.resources[test[1]] == answer[1] and \
            game.state.current_player == answer[2] and game.state.occupied_positions == answer[3]:
            print(f'Test successful ')
            passed_tests += 1

    # for thief
    tests = {(9, 'T') : [9, 11, 1, ['null', 10, 20, 30, 40, 50]], # answer - [new_pos, tickets left, next player, new positions of all]
             (58, 'B'): [58, 7, 1, ['null', 10, 20, 30, 40, 50]],
             (46, 'U'): [46, 3, 1, ['null', 10, 20, 30, 40, 50]],
             (194,'F'): [194, 2, 1, ['null', 10, 20, 30, 40, 50]]}
    player_idx = 0
    game.state.move_number = 5
    for test, answer in tests.items():
        no_tests += 1
        game.state.thief = Player(1, 12, 8, 4, 3)
        if test[1] == 'F': game.state.thief = Player(157, 12, 8, 4, 3)
        game.UpdateState(player=player_idx, action=test)
        print(game.state.occupied_positions, game.state.thief.resources)
        if game.state.last_thief_location == answer[0] and game.state.thief.resources[test[1]] == answer[1] and \
            game.state.current_player == answer[2]:
            print(f'Test successful ')
            passed_tests += 1

    assert no_tests == passed_tests
    return

