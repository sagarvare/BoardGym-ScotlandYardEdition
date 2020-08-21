import sys
sys.path.append('.')
sys.path.append('../')
from scotlandyard import Agent


class KeyboardAgent(Agent):
    """
    An agent controlled by the keyboard.
    """

    def __init__(self,index):
        self.index = index

    def getvalidInput(self,turn):
        if turn == '':
            return False

        try:
            _ = int(turn[0].strip())
        except ValueError:
            print('not an integer {}'.format(turn[0]))
            return False

        if turn[1].strip() not in ['T', 'B', 'UG']:
            print(f'{turn[1]} not a valid mode of transportation.' )
            return False

        return True

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

    def getAction(self, state, board):
        current_pos = state.occupied_positions[self.index]
        moves = board.GetPossibleMoves(current_pos)
        legal_moves = self.GetLegalMoves(state, moves)
        print('Possible moves for keyboard agent are {}'.format(legal_moves))
        count = 5
        while count > 0 :
            move_input = input('Enter the node number (integer) and the mode of transportation (T | B | UG) by separating '
                           'them with comma. For ex. 33,B: ').split(',')
            if self.getvalidInput(move_input):
                node, transport = int(move_input[0].strip()), move_input[1].strip()
                move = (node, transport)
                if move in legal_moves :
                    return move
                else:
                    count -= 1
                    input(f'The chosen move: {(node, transport)} is invalid. Please try again and choose a move from {legal_moves}')
                return move

            else:
                count -= 1
                print("Invalid input, please enter the input in appropriate format as instructed. You have {} attempts "
                      "left".format(count))
        raise TimeoutError('Exceeded the maximum number of attempts')