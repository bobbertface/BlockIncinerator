'''
@author: Bobbertface
'''
import Pieces

class Tetramino():
    def __init__(self, name, initialPosition, blockSize):
        self.position = initialPosition
        self.positionModifier = 20
        self.orientation = 0  # Initial piece orientation in the piece dictionary
        self.name = Pieces.nameCheck(name)
        self.blocks = Pieces.getBlocks(self.name, initialPosition, self.positionModifier)
        self.blockArrangements = Pieces.positionDictionary.get(self.name)

    '''pass the surface down to the blocks'''
    def draw(self, surface):
        for block in self.blocks:
            block.draw(surface)

    def rotate(self):
        self.orientation = self.incrementOrientation()
        tx, ty = self.position
        for i in range(len(self.blockArrangements[self.orientation])):
            x, y = self.blockArrangements[self.orientation][i]
            self.blocks[i].changePosition((tx + x, ty + y))

    def incrementOrientation(self):
        orientation = self.orientation + 1
        if (orientation >= len(self.blockArrangements)):
            orientation = 0
        return orientation
