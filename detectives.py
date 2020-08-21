import sys
import random
sys.path.append('.')
sys.path.append('../')
# sys.path.append('src/')
import utils
from scotlandyard import Agent

class Detectives(Agent) :
    def __init__(self, index, evalFn = None):
        super().__init__(index)
        # self.index = index
        if evalFn:
            self.evaluationFunction = evalFn


    def evaluationFunction(self, game_state, board, action):
        # for evaluation function the current action has to be evaluated using only the state of the board after taking
        # this particular action and nothing else. Using depth and other optimization is the job of algorithm and should not be done here
        det_node = action[0]
        # Level 1 eval function. Use only distance between new node and possible thief positions as a measure of goodness.
        #TODO for move number less than 5 this won't work as no knowledge of thief yet.
        max_dist = float('-inf')
        min_dist = float('inf')
        for thief_node in list(game_state.possible_thief_nodes):
            temp_dist = board.pairwise_distances((det_node, thief_node))
            max_dist = max(max_dist, temp_dist)
            min_dist = min(min_dist, temp_dist)

        return (max_dist + min_dist)/2


    def GetLegalMoves(self, game_state, moves):
        legal_moves = []
        detective_state = getattr(game_state,'detective%d' % self.index)
        for move in moves:
            if move[1] == 'F' :
                continue
            elif detective_state.resources[move[1]] <= 0:
                continue

            if move[0] in game_state.occupied_positions[1:]:
                continue

            legal_moves.append(move)

        return legal_moves

    def UpdatePossibleThiefNodes(self, game_state, board, thief_mode):
        '''
        Calculates all the posible nodes where the thief could be, given previous possible locations for thief and the current move
        made by thief
        :param game_state:
        :param board:
        :param thief_mode: last mode of transport used by the thief
        :return: None. Updates the possible thief locations in GameState object
        '''
        new_thief_nodes = set()
        if game_state.move_number < 5: return []

        if game_state.move_number in [5, 8, 13, 18]:
            new_thief_nodes = set([game_state.last_thief_location])

        else:
            for node in game_state.possible_thief_nodes:
                moves = board.GetPossibleMoves(node) # (node, mode)
                for move in moves:
                    if thief_mode == 'black':
                        new_thief_nodes.add(move[0])
                    elif move[1] == thief_mode:
                        new_thief_nodes.add(move[0])

        game_state.possible_thief_nodes = new_thief_nodes

        return

class RandomAgent(Detectives):

    def getAction(self, game_state, board):
        # detective_state = getattr(game_state, 'detective%d' % self.index)
        current_pos = game_state.occupied_positions[self.index]
        moves = board.GetPossibleMoves(current_pos)
        legal_moves = self.GetLegalMoves(game_state,moves)
        return random.choice(legal_moves)


class GreedyBFSAgent(Detectives):

    def getAction(self, game_state, board, depth=2):
        current_pos = game_state.occupied_positions[self.index]
        moves = board.GetPossibleMoves(current_pos)
        legal_moves = self.GetLegalMoves(game_state,moves)
        min_cost = float('inf')
        for move in legal_moves:
            curr_cost = self.evaluationFunction(game_state, board, move)
            if curr_cost < min_cost:
                min_cost, optimal_move = curr_cost, move

        return optimal_move


class UCSAgent(Detectives):
    def getAction(self, game_state, board, depth = 2):
        current_pos = game_state.occupied_positions[self.index]
        moves = board.GetPossibleMoves(current_pos)
        legal_moves = self.GetLegalMoves(game_state, moves)
        priority_queue = utils.PriorityQueue()
        for move in legal_moves:
            priority_queue.push(move, self.evaluationFunction(game_state, board, move))

class MinimaxAgent(Detectives):
  """
    Your minimax agent (problem 1)
  """

  def getAction(self, game_state):
      pass


class AlphaBetaAgent(Detectives) :

    def getAction(self, game_state):
        pass

class BasicColabAgent(Detectives):

    def __init__(self, detective_objects):
        self.detective_objects = detective_objects

    def getAction(self, game_state):
        all_actions = []
        for i, detective in enumerate(self.detective_objects):
            all_actions.append(detective.getAction(game_state))

        return all_actions

def betterEvaluationFunction(game_state, action):
    pass



# Unit Tests for different functions
#TODO combine all the different LegalMoves test functions into a single generalized function

def LegalMovesTrainTest(board):
    game_state = GameState([10, 56, 23, 1, 76, 88])
    game_state.current_player = 3
    game_state.detective3.resources['U'] = 0
    agent = GreedyBFSAgent(3)
    moves = board.GetPossibleMoves(1)
    legal_moves = agent.GetLegalMoves(game_state, moves)
    unallowed_moves = [(46, 'U')]
    print(f'testing train, agent: {game_state.detective3.resources}, moves: {moves}, legal_moves : {legal_moves}')
    for move in legal_moves:
        if move in unallowed_moves:
            return False

    return True

def LegalMovesBusTest(board):
    game_state = GameState([10, 56, 23, 1, 76, 88])
    game_state.current_player = 3
    game_state.detective3.resources['B'] = 0
    agent = GreedyBFSAgent(3)
    moves = board.GetPossibleMoves(1)
    legal_moves = agent.GetLegalMoves(game_state, moves)
    unallowed_moves = [(46, 'B'), (58, 'B')]
    print(f'testing bus, agent: {game_state.detective3.resources}, moves: {moves}, legal_moves : {legal_moves}')
    for move in legal_moves:
        if move in unallowed_moves:
            return False

    return True


def LegalMovesTaxiTest(board):
    game_state = GameState([10, 56, 23, 1, 76, 88])
    game_state.current_player = 3
    game_state.detective3.resources['T'] = 0
    agent = GreedyBFSAgent(3)
    moves = board.GetPossibleMoves(1)
    legal_moves = agent.GetLegalMoves(game_state, moves)
    unallowed_moves = [(8, 'T'), (9, 'T')]
    print(f'testing taxi, agent: {game_state.detective3.resources}, moves: {moves}, legal_moves : {legal_moves}')
    for move in legal_moves:
        if move in unallowed_moves:
            return False

    return True

def LegalMovesFerryTest(board):
    game_state = GameState([10, 56, 23, 194, 76, 88])
    game_state.current_player = 3
    agent = GreedyBFSAgent(3)
    moves = board.GetPossibleMoves(194)
    legal_moves = agent.GetLegalMoves(game_state, moves)
    unallowed_moves = [(157, 'F')]
    print(f'testing ferry move, agent: {game_state.detective3.resources}, moves: {moves}, legal_moves : {legal_moves}')
    for move in legal_moves:
        if move in unallowed_moves:
            return False

    return True

def LegalPositions(board):
    game_state = GameState([10, 56, 23, 1, 46, 9])
    game_state.current_player = 3
    agent = GreedyBFSAgent(3)
    moves = board.GetPossibleMoves(1)
    legal_moves = agent.GetLegalMoves(game_state, moves)
    unallowed_pos = [46, 9]
    print(f'testing occupied positions, moves: {moves}, legal_moves : {legal_moves}')
    for move in legal_moves:
        if move[0] in unallowed_pos:
            return False

    return True

def testLegalMoves():
    # Following tests are needed
    # 1. if no ug tickets, should not return moves corresponding to train
    # 2. if no bus tickets, should not return moves corresponding to bus
    # 3. if no taxi tickets, should not return moves corresponding to taxi
    # 4. Should not consider moves corresponding to ferry
    # 5. if position is already occupied remove it from possible moves.
    from src.scotlandyard import GameState
    from Board import Board
    game_file = "./data/SCOTMAP.TXT"  # assuming the current working directory is the location of this file
    board =  Board(game_file)
    total_passed = 0
    total_tests = 5
    if LegalMovesTrainTest(board):
        print('Successfully passed Legal moves unit test for trains')
        total_passed += 1
    else: print('Failed Legal moves unit test for trains')
    if LegalMovesBusTest(board):
        print('Successfully passed Legal moves unit test for bus')
        total_passed += 1
    else: print('Failed Legal moves unit test for bus')
    if LegalMovesTaxiTest(board):
        print('Successfully passed Legal moves unit test for taxi')
        total_passed += 1
    else: print('Failed Legal moves unit test for taxi')
    if LegalMovesFerryTest(board):
        print('Successfully passed Legal moves unit test for Ferry')
        total_passed += 1
    else: print('Failed Legal moves unit test for Ferry')
    if LegalPositions(board):
        print('Successfully passed Legal moves unit test for pre-occupied positions')
        total_passed += 1
    else:
        print('Failed Legal moves unit test for pre-occupied positions')

    print(f'Successfully passed {total_passed} of the 5 test cases')

    assert total_tests == total_passed
    return

def testEvalFunc():
    node1, node2 = 10, 15
    # Test Cases
    # 1. The first 5 turns, when no knowledge of thief nodes.
    # 2.
    game_file = "./data/SCOTMAP.TXT"  # assuming the current working directory is the location of this file
    board =  Board(game_file)
    assert True


def test_UpdateThiefNodes():

    game_file = "./data/SCOTMAP.TXT"  # assuming the current working directory is the location of this file
    board = Board(game_file)
    # Required setup - move number, thief previous possible nodes, mode of transportation chosen
    test_cases = {'U' : [46, 67, 89], 'B' : [23, 14, 52], 'T' : [4, 14, 24, 23, 36, 50], 'black' : [4, 14, 24, 23, 36, 50, 52, 46, 67, 89]}
    # Different test cases
    # 1. move number in [5,8,13,18]. irrespective of previous possibilities, the output should be one single node as revealed by the thief.
    # 2. possible locations when previous possibility was a single location
    # 3. When previous history was more than 1 node.
    # Check for taxi, bus and train and black ticket as mode of transport.

    # test 1
    no_tests = 0
    passed_tests = 0
    for mode, answer in test_cases.items():
        no_tests += 1
        game_state = GameState([13, 55, 6, 88, 10, 73])
        game_state.move_number = 5
        game_state.last_thief_location = 13
        agent = GreedyBFSAgent(1)
        agent.UpdatePossibleThiefNodes(game_state, board, mode)
        if len(game_state.possible_thief_nodes) == 1 and game_state.possible_thief_nodes.pop() == game_state.last_thief_location:
            print(f'Test successful for reveal move of thief for mode : {mode}')
            passed_tests += 1
        else: print(f'Test failed for reveal move of thief for mode : {mode}')

    # test 2
    for mode, answer in test_cases.items():
        no_tests += 1
        game_state = GameState([13, 55, 6, 88, 10, 73])
        game_state.move_number = 6
        game_state.last_thief_location = 13
        game_state.possible_thief_nodes = set([13, 37])
        agent = GreedyBFSAgent(1)
        agent.UpdatePossibleThiefNodes(game_state, board, mode)
        if game_state.possible_thief_nodes == set(answer):
            print(f'Test successful for singleton history of thief for mode : {mode}')
            passed_tests += 1
        else:
            print(f'Test failed for singleton history of thief for mode : {mode}')
            print(f'Expected possible nodes : {answer}'
                  f'\nObtained possible nodes : {game_state.possible_thief_nodes}')

    print(f'Successfully passed {passed_tests} of the {no_tests} test cases')
    assert no_tests == passed_tests

    # Test 3

    return




# Archive Codes or junk code for future use
# Below code to be used someplace else
        # possible_detective_locations = set()
        # explored_nodes = set()
        # unexplored_nodes = [action]
        # for i in range(depth):
        #     legal_moves = []
        #     while unexplored_nodes:
        #         option = unexplored_nodes.pop()
        #         explored_nodes.add(option)
        #         pseudo_game_state = pseudoUpdate(copy.deepcopy(game_state), self.index, option)
        #         moves = board.GetPossibleMoves(option[0])
        #         legal_moves = legal_moves + (self.GetLegalMoves(pseudo_game_state, moves))
        #
        #     for move in legal_moves:
        #         if move not in explored_nodes:
        #             unexplored_nodes.append(move)
        #
        # for move in legal_moves:
        #     possible_detective_locations.add(move[0])
        #
        # for node in self.possible_thief_nodes:
        #     thief_current_possible_nodes = board.GetPossibleMoves(node)