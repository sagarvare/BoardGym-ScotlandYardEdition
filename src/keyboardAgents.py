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

    def getAction(self, state, board):
        current_pos = state.occupied_positions[self.index]
        moves = board.GetPossibleMoves(current_pos)
        print('Possible moves for keyboard agent are {}'.format(moves))
        count = 5
        while count > 0 :
            move_input = input('Enter the node number (integer) and the mode of transportation (T | B | UG) by separating '
                           'them with comma. For ex. 33,B: ').split(',')
            if self.getvalidInput(move_input):
                node, transport = int(move_input[0].strip()), move_input[1].strip()
                move = (node, transport)
                # if move is legal :
                    # return move
                return move
            else:
                count -= 1
                print("Invalid input, please enter the input in appropriate format as instructed. You have {} attempts "
                      "left".format(count))
        raise TimeoutError('Exceeded the maximum number of attempts')

    def getvalidInput(self,turn):
        if turn == '':
            return False

        try:
            _ = int(turn[0].strip())
        except ValueError:
            print('not an integer {}'.format(turn[0]))
            return False

        if turn[1].strip() not in ['T', 'B', 'UG']:
            print('not a valid choice ' + turn[1])
            return False

        return True