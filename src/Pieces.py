'''
@author: Bobbertface
'''
from Block import Block
import random

s_blockPositions = [[(1, 1), (2, 1), (2, 2), (3, 2)],
                    [(3, 0), (3, 1), (2, 1), (2, 2)]]
z_blockPositions = [[(2, 1), (3, 1), (1, 2), (2, 2)],
                    [(1, 0), (1, 1), (2, 1), (2, 2)]]
t_blockPositions = [[(1, 1), (2, 1), (3, 1), (2, 2)],
                    [(2, 0), (1, 1), (2, 1), (2, 2)],
                    [(2, 0), (1, 1), (2, 1), (3, 1)],
                    [(2, 0), (2, 1), (3, 1), (2, 2)]]
l_blockPositions = [[(1, 1), (2, 1), (3, 1), (1, 2)],
                    [(2, 0), (2, 1), (2, 2), (3, 2)],
                    [(1, 1), (2, 1), (3, 1), (3, 0)],
                    [(1, 0), (2, 0), (2, 1), (2, 2)]]
j_blockPositions = [[(1, 1), (2, 1), (3, 1), (3, 2)],
                    [(2, 0), (3, 0), (2, 1), (2, 2)],
                    [(1, 0), (1, 1), (2, 1), (3, 1)],
                    [(2, 0), (2, 1), (1, 2), (2, 2)]]
i_blockPositions = [[(0, 1), (1, 1), (2, 1), (3, 1)],
                    [(1, 0), (1, 1), (1, 2), (1, 3)]]
o_blockPositions = [[(1, 1), (2, 1), (1, 2), (2, 2)]]
positionDictionary = {'s':s_blockPositions,
                      'z':z_blockPositions,
                      't':t_blockPositions,
                      'l':l_blockPositions,
                      'j':j_blockPositions,
                      'i':i_blockPositions,
                      'o':o_blockPositions}
colorDictionary = {'s':'red', 'z':'green', 't':'yellow', 'l':'blue', 'j':'orange', 'i':'purple', 'o':'black'}
possibleNames = list(positionDictionary.keys())

def getBlocks(name, position, positionModifier):
    lookupName = nameCheck(name)
    blockColor = colorDictionary[lookupName]
    blockArrangement = positionDictionary[lookupName]
    baseX, baseY = position
    blocks = []
    for i in range(len(blockArrangement[0])):
        blocks.append(Block(blockColor, (baseX + blockArrangement[0][i][0], baseY + blockArrangement[0][i][1]), positionModifier))
    return blocks

def nameCheck(name):
    return name if name in possibleNames else getRandomName()

def getRandomName():
    return possibleNames[random.randint(0, len(possibleNames) - 1)]
