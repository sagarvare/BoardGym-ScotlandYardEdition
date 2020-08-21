
def DummyActions():
    '''

    :return: list of actions, where each action is a tuple whose first element is the new node and the second element is
    the mode of transportation to be used to reach the node
    '''
    import random
    coin_flip = random.random()
    if coin_flip >= 0.5:
        return [(38, 'B'), (78, 'T'), (108, 'U')]
    else:
        return [(48, 'B'), (58, 'T'), (68, 'U')]

if __name__ == '__main__' :

    print('Running assignment dummy APIs')

    for action in DummyActions():
        print(action)