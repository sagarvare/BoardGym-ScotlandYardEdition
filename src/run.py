"""
The main script to run the scotlandyard game.
"""
import utils
import sys
from src import keyboardAgents
import detectives
import thief
from src.scotlandyard import Game

def default(str):
  return str + ' [Default: %default]'

def readCommand( argv ):
    """
    Processes the command used to run pacman from the command line.
    """
    from optparse import OptionParser
    usageStr = """
    USAGE:      python run.py <options>
    EXAMPLES:   (1) python run.py
                  - starts an interactive game
              (2) python run.py 
              #TODO to be completed
    """
    parser = OptionParser(usageStr)

    # parser.add_option('-n', '--numGames', dest='numGames', type='int',
    #                 help=default('the number of GAMES to play'), metavar='GAMES', default=1)
    #TODO we can have a default auto mode. In this case the game will auto run and generate some stats.
    parser.add_option('-r', '--role', dest='role',
                    help=default('Chose either one of the three roles - thief, detective or auto'),
                    metavar='ROLE', default='thief')
    parser.add_option('-t', '--thief', dest='thief',
                    help=default('the agent TYPE in the thief module to use'),
                    metavar='THIEF_TYPE', default='KeyboardAgent')
    parser.add_option('-d', '--detectives', dest='detectives',
                    help=default('the agent TYPE in the detectives module to use'),
                    metavar = 'TYPE', default='RandomDetective')
    parser.add_option('-k', '--numDetectives', type='int', dest='numDetectives',
                    help=default('The maximum number of detectives to use'), default=5)
    parser.add_option('-d1', '--detective1', dest='D1',
                    help=default('The agent TYPE in the detectives module to use for detective 1'), default='KeyboardAgent')
    parser.add_option('--timeout', dest='timeout', type='int',
                    help=default('Maximum length of time an agent can spend computing in a single game'), default=30)

    options, otherjunk = parser.parse_args(argv)
    if len(otherjunk) != 0:
        raise Exception('Command line input not understood: ' + str(otherjunk))
    args = dict()

    #TODO There is a fancy of loading the pacman and ghost agents here bu using the script similar to pacman but right
    # now we will implement implement by string matching method
    #TODO currently assume all the detectives have the same agent type. We can later also built in arguments for defining
    # agent type for each detective

    if options.role == 'thief' :
        args['role'] = 'thief'
        if options.thief == 'KeyboardAgent':
            args['thief'] = keyboardAgents.KeyboardAgent()
        elif options.thief == 'minimax':
            args['thief'] = thief.MinimaxAgent()
        # multiple elif conditions or use the load agent module from the pacman script.
        elif options.thief == 'random':
            args['thief'] = thief.RandomAgent()
        else:
            raise Exception('The agent ' + options.thief + ' is not specified in any *Agents.py.')

        args['detectives'] = [detectives.RandomAgent(i+1) for i in range(options.numDetectives)]

    elif options.role == 'detective' :
        args['role'] = 'detective1'
        if options.D1 == 'KeyboardAgent':
            args['detectives'] = [keyboardAgents.KeyboardAgent()] + [detectives.RandomAgent(i+1) for i in range(1,options.numDetectives)]
        elif options.D1 == 'minimax':
            args['detectives'] = [detectives.MinimaxAgent()] + [detectives.RandomAgent(i+1) for i in range(1,options.numDetectives)]
        # multiple elif conditions or use the load agent module from the pacman script.
        elif options.D1 == 'random':
            args['thief'] = thief.RandomAgent()
        else:
            raise Exception('The agent ' + options.D1 + ' is not specified in any *Agents.py.')

        # check for the first agent type for detective, if not specified assign keyboard.

    else :
        # Check for the specification for agents for thief and detectives. If not specified for thief, then assign random.
        args['role'] = 'auto'
        args['thief'] = thief.RandomAgent()
        args['detectives'] = [detectives.RandomAgent(i+1) for i in range(options.numDetectives)]


    return args


def runGames(role, thief, detectives, timeout):
    # game = Game()
    # game.play()
    pass

if __name__ == '__main__':
  """
  The main function called when run.py is run
  from the command line:

  > python run.py

  See the usage string for more details.

  > python run.py --help
  """
  args = readCommand( sys.argv[1:] ) # Get game components based on input
  # runGames( **args )
  game = Game(**args)
  game.play()
# ---------------------------------------------------------------------------------------------------------
#
#     To Do's
#
# ---------------------------------------------------------------------------------------------------------
#
# Step 1 : An input args parser to read all the input arguments. Define the destination, and the default value for each of the arguments
#
# Step 2 : An intermediate run function, that takes in these arguments and instantiates the game with the appropriate theif and detective agents as specified in the input arguments
#
# Step 3 : Defaults : a) If no algorithm name specified then by deaulf it is a keyboard human player.
#                     b) human player is thief if not specified and thief is a keyboard agent
#                     b) If human player is detective then by default it is always D1

# Every player should have a function called get action. so basically while initializing players we need to also initialize the type of agent for them.





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


