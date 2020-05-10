import pygame, thorpy
import os

# Inputs required from main game running loop
# player turn
# turn number
# current position of all players excluding thief
# possible actions for the current player

## Constants
DISPLAY_SIZE = (1024,800) #widht, height
ORIGIN = (0,0) # upper left corner of the window
#COLORS # RGB
BLACK = (0,0,0)
NUM_KEYS = {pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8,
            pygame.K_9}
MAX_NODE_POS = 200
MIN_NODE_POS = 1

node_pixel_file = os.path.join('../data', 'SCOTPOS.TXT')
NODE_PIXEL_DICT = {}

class NodePixel():
    def __init__(self, pos, x, y):
        self.position = pos
        self.x = x
        self.y = y

def AddNodeToDict(node_number, x, y):
    NODE_PIXEL_DICT[node_number] = NodePixel(int(node_number), int(x), int(y))


with open(node_pixel_file, 'r') as f:
    node_count = 0
    for i, line in enumerate(f):
        line = line.rstrip('\n').split(' ')
        if i== 0:
            try :
                node_count = int(line[0])
                print(node_count)
                continue
            except Exception as e:
                print('Firt row should contain the total number of nodes in the file')

        if len(line) != 3:
            print('All lines except first line should contain the node and the x and y pixels for the node')
            print('Bad behaving line number is {} and line is : {}'.format(i, line))

        AddNodeToDict(line[0], line[1], line[2])

# Game GUI related functions
pygame.init()
screen = pygame.display.set_mode(DISPLAY_SIZE)

pygame.display.set_caption('SCOTLANDYARD')
clock = pygame.time.Clock()

## Loading all images
def LoadInput(img_path='../graphics', backgroundfile_name='map.jpg', player_icons=None ):
    '''

    :param img_path: path to the directory containing all image files
    :param backgroundfile_name: name of the background image file
    :param player_icons: list containing the file names of icons for each player
    :return: pyimage objects for background and all the players
    '''

    image_path = img_path
    background_img = os.path.join(image_path, backgroundfile_name)
    # print(os.getcwd())
    # print(os.listdir(os.getcwd()))
    #Background
    background = pygame.image.load(background_img)
    #Icons for each player
    thief = pygame.image.load(os.path.join(image_path,'FLAG0.gif'))
    d1 = pygame.image.load(os.path.join(image_path,'FLAG1.gif'))
    d2 = pygame.image.load(os.path.join(image_path,'FLAG2.gif'))
    d3 = pygame.image.load(os.path.join(image_path,'FLAG3.gif'))
    d4 = pygame.image.load(os.path.join(image_path,'FLAG4.gif'))
    d5 = pygame.image.load(os.path.join(image_path,'FLAG5.gif'))

    return background, thief, d1, d2, d3, d4, d5

def DisplayAgent(pos, agent_icon):
    screen.blit(agent_icon, pos)

def DisplayAllAgents(agent_icons, agents_pos, skip_agent):
    for agent in range(1,6):
        if agent != skip_agent:
            DisplayAgent(agents_pos[agent], agent_icons[agent])


def NodeToPixel(node):
    '''
    returns the pixel location for the given node
    :param node:
    :return: a tuple containing x and y values of the pixel
    '''
    try :
        return (NODE_PIXEL_DICT[node].x, NODE_PIXEL_DICT[node].y)
    except KeyError as e:
        print(f'{node} not in the node dict dictionary. The node number should be of type string and between 1-200')
        raise e

background, thief, d1, d2, d3, d4, d5 = LoadInput()
agent_icons = [thief, d1, d2, d3, d4, d5]
curr_num = ''
running = True
x,y = 500,500
player_turn = 0
blink = 1
# for testing only. ideally initialize using the node to pixel function and the positions obtained from the game code
agents_pos = {0:(2,2), 1: (10,10), 2: (20,20), 3: (30,30), 4: (40,40), 5: (50,50)}

while running:
    clock.tick(5)
    screen.fill((255,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # left button pressed
            print(event.pos)
        if event.type == pygame.KEYDOWN:
            if event.key in NUM_KEYS and len(curr_num) < 3:
                curr_num += event.unicode

            if event.key == pygame.K_BACKSPACE:
                curr_num = curr_num[:len(curr_num) - 1]

            if event.key == pygame.K_RETURN:
                x,y = NodeToPixel(curr_num)
                agents_pos[player_turn] = (x,y)
                print(curr_num, x,y)
                curr_num = ''
                if player_turn == 5:
                    player_turn = 0
                else:
                    player_turn += 1

    screen.blit(background, (0, 0))
    if blink:
        DisplayAllAgents(agent_icons, agents_pos, -1)
        blink = 0
    else:
        DisplayAllAgents(agent_icons, agents_pos, player_turn)
        blink = 1

    pygame.display.update()


quit()

#
# def RunUnitTest():
