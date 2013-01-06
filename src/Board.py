'''
@author: Bobbertface
'''
from numpy import zeros
import Pieces
from Tetramino import Tetramino

class Board():
    def __init__(self, size):
        self.initialPosition = 3, -1  # Initial position for tetraminos
        self.blockSize = 20  # used to translate between block coordinates and pixels
        self.x_size, self.y_size = size  # currently not used anywhere, consider removing
        self.board = zeros(size)
        self.frameCounter = 0
        self.blockSpeed = 1
        self.frameCounterCeilingCoefficient = 15
        self.frameCounterCeiling = self.calculateFrameCounterCeiling()
        self.blocks = []
    
    '''Returns True when the game is not over based on this tetramino, False otherwise'''
    def addTetramino(self):
        tetramino = Tetramino(Pieces.getRandomName(), self.initialPosition, self.blockSize)
        collide = False
        for block in tetramino.blocks:
            if self.addBlock(block):
                collide = True
        self.tetramino = tetramino
        return collide

    '''Returns True if there was a collision'''
    def drop(self):
        self.frameCounterCeiling = self.calculateFrameCounterCeiling()
        if self.frameCounter >= self.frameCounterCeiling:
            if self.passDropTest():
                #update tetramino position
                tx, ty = self.tetramino.position
                self.tetramino.position = (tx, ty+1)
                #remove old positions in board
                self._clearBlockPositions()
                #update position in board and on block
                for block in self.tetramino.blocks:
                    x, oldY = block.position
                    newY = oldY + 1
                    self.board[x, newY] = 1
                    block.changePosition((x, newY))
            else:
                return self.addTetramino()
            self.frameCounter = 0
        else:
            self.frameCounter += 1
        return False

    def rotateTetramino(self):
        if self.passRotateTest():
            #remove old positions in board
            self._clearBlockPositions()
            #rotate tetramino
            self.tetramino.rotate()
            # update position in board
            for block in self.tetramino.blocks:
                x, y = block.position
                self.board[x, y] = 1

    def _clearBlockPositions(self):
        for block in self.tetramino.blocks:
            x, oldY = block.position
            self.board[x, oldY] = 0

    '''Returns True if the piece can move down, False otherwise'''
    def passDropTest(self):
        # find lowest block per x coordinate
        checkBlocks = {}
        for block in self.tetramino.blocks:
            x, y = block.position
            if x in checkBlocks:
                if y > checkBlocks[x].position[1]:
                    checkBlocks[x] = block
            if x not in checkBlocks:
                checkBlocks[x] = block
        # compare the lowest blocks with the board position 1 lower
        for block in checkBlocks.values():
            x, y = block.position
            newY = y + 1
            hitBottom = newY >= len(self.board[x])
            if hitBottom or self.board[x, newY]:
                return False
            else:
                continue
        return True

    '''Returns True if the active tetramino can rotate, False otherwise'''
    def passRotateTest(self):
        currentPositions = []
        for block in self.tetramino.blocks:
            currentPositions.append(block.position)
        
        newOrientation = self.tetramino.incrementOrientation()
        newBlockArrangement = self.tetramino.blockArrangements[newOrientation]
        newPositions = []
        for unOffsetPosition in newBlockArrangement:
            tx, ty = self.tetramino.position
            x, y = unOffsetPosition
            newPositions.append((tx + x, ty + y))
        for newPosition in newPositions:
            x, y = newPosition
            if (self.board[x, y] and newPosition not in currentPositions):
                return False
        return True
        
    '''Returns True if we couldn't add the block, False otherwise'''
    def addBlock(self, block):
        collide = False
        if self.board[block.position[0], block.position[1]]:
            collide = True
        else:
            self.board[block.position[0], block.position[1]] = 1
            self.blocks.append(block)
        return collide

    '''drop speed formula'''
    def calculateFrameCounterCeiling(self):
        return self.frameCounterCeilingCoefficient / self.blockSpeed       

    def draw(self, surface):
        for block in self.blocks:
            block.draw(surface)
