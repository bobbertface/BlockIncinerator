'''
@author: Bobbertface
'''
import Pieces

class Tetramino():
    def __init__(self, name, initialPosition, blockSize):
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
        self.incrementOrientation()
        self.blocks = self.blockArrangements[self.position]
    
    def incrementOrientation(self):
        self.orientation += 1
        if (self.orientation >= self.blockArrangements.size):
            self.orientation = 0
        elif (self.orientation < 0):
            self.orientation = self.blockArrangements.size - 1
