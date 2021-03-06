'''
@author: Bobbertface
'''
from Tetramino import Tetramino
from numpy import zeros

class Board():
    def __init__(self, size):
        self.initialPosition = 3, 0  # Initial position for tetraminos
        self.blockSize = 20  # used to translate between block coordinates and pixels
        self.x_size, self.y_size = size
        self.board = zeros(size)
        self.frameCounter = 0
        self.blockSpeed = 1
        self.frameCounterCeilingCoefficient = 60
        self.isAccelerated = False
        self.frameCounterCeiling = self.calculateFrameCounterCeiling()
        self.blocks = []
        self.baseScore = 50
        self.scoreModifierForLine = [1, 3, 7, 12]
        self.score = 0
        self.lines = 0
        self.currentLines = 0
        self.linesForNextLevel = 9
        self.maxBlockSpeed = 15

    '''Returns True when the game is not over based on this tetramino, False otherwise'''
    def addTetramino(self, name):
        tetramino = Tetramino(name, self.initialPosition, self.blockSize)
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
                self.dropTetramino(1)
            else:
                self.clearLines()
                return True
            self.frameCounter = 0
        else:
            self.frameCounter += 1
        return False

    def clearLines(self):
        # find any lines that we need to clear
        clearedLineYValues = []
        for i in range(self.y_size):
            if sum(self.board[:, i]) == self.x_size:
                clearedLineYValues.append(i)

        if len(clearedLineYValues) > 0:
            ''' In-alteration combined with the speed of list comprehensions according to Alex Martelli's answer in
                http://stackoverflow.com/questions/1207406/remove-items-from-a-list-while-iterating-in-python'''
            self.updateScore(len(clearedLineYValues))
            # remove old positions in board for all the blocks
            self.board = zeros((self.x_size, self.y_size))
            # delete the blocks for each removed line
            self.blocks[:] = [block for block in self.blocks if block.position[1] not in clearedLineYValues]

            # move everything down by the number of lines that got removed below it
            for block in self.blocks:
                dropMovement = 0
                for i in range(len(clearedLineYValues)):
                    if block.position[1] < clearedLineYValues[i]:
                        dropMovement = len(clearedLineYValues) - i
                        break
                if dropMovement > 0:
                    x, y = block.position
                    newY = y + dropMovement
                    block.changePosition((x, newY))
            # add the board positions back
            for block in self.blocks:
                x, y = block.position
                self.board[x, y] = 1

    def hardDrop(self):
        numLines = self.getHardDropLength()
        self.dropTetramino(numLines)
        self.clearLines()

    def getHardDropLength(self):
        # find lowest block per x coordinate
        checkBlocks = self.getLowestBlocksPerXCoordinate()
        # compare the lowest blocks with the board position 1 lower iteratively until we figure out how many lines we can drop the piece
        candidateYValues = []
        for block in checkBlocks.values():
            x, y = block.position
            numLines = 0
            for checkY in range(y + 1, self.y_size):
                hitBottom = checkY >= self.y_size
                if not hitBottom and not self.board[x, checkY]:
                    numLines = checkY - y
                else:
                    break;
            candidateYValues.append(numLines)
        return min(candidateYValues)

    def dropTetramino(self, numLines):
        # update tetramino position
        tx, ty = self.tetramino.position
        self.tetramino.position = (tx, ty + numLines)
        # remove old positions in board
        self._clearBlockPositions(self.tetramino.blocks)
        # update position in board and on blocks
        for block in self.tetramino.blocks:
            x, oldY = block.position
            newY = oldY + numLines
            self.board[x, newY] = 1
            block.changePosition((x, newY))

    def updateScore(self, linesCleared):
        self.lines += linesCleared
        self.currentLines += linesCleared
        if self.currentLines >= self.linesForNextLevel:
            self.blockSpeed += 1
            self.currentLines = self.currentLines - self.linesForNextLevel
            self.linesForNextLevel += 1
        lineBasedScore = (self.baseScore + (self.blockSpeed - 1) * 5) * self.scoreModifierForLine[linesCleared - 1]
        self.score += lineBasedScore

    def rotateTetramino(self):
        if self.passRotateTest():
            # remove old positions in board
            self._clearBlockPositions(self.tetramino.blocks)
            # rotate tetramino
            self.tetramino.rotate()
            # update position in board
            for block in self.tetramino.blocks:
                x, y = block.position
                self.board[x, y] = 1

    def moveTetramino(self, left):
        if self.passMoveTest(left):
            # update tetramino position
            tx, ty = self.tetramino.position
            self.tetramino.position = (tx - 1 if left else tx + 1, ty)
            # remove old positions on board
            self._clearBlockPositions(self.tetramino.blocks)
            # update position in board an on blocks
            for block in self.tetramino.blocks:
                oldX, y = block.position
                newX = oldX - 1 if left else oldX + 1
                self.board[newX, y] = 1
                block.changePosition((newX, y))

    def _clearBlockPositions(self, blocks):
        for block in self.tetramino.blocks:
            x, oldY = block.position
            self.board[x, oldY] = 0

    '''Returns True if the piece can move down, False otherwise'''
    def passDropTest(self):
        # find lowest block per x coordinate
        checkBlocks = self.getLowestBlocksPerXCoordinate()
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

    def getLowestBlocksPerXCoordinate(self):
        checkBlocks = {}
        for block in self.tetramino.blocks:
            x, y = block.position
            if x in checkBlocks:
                if y > checkBlocks[x].position[1]:
                    checkBlocks[x] = block
            if x not in checkBlocks:
                checkBlocks[x] = block
        return checkBlocks

    '''Returns True if the active tetramino can rotate, False otherwise'''
    def passRotateTest(self):
        currentPositions = []
        for block in self.tetramino.blocks:
            x, y = block.position
            if not self.board[x, y]:
                # This tetramino got rotated when some of its blocks have been removed
                return False
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
            xInBounds = x < self.x_size and x >= 0
            yInBounds = y < self.y_size and y >= 0
            inBounds = xInBounds and yInBounds
            if not inBounds or (self.board[x, y] and newPosition not in currentPositions):
                return False
        return True

    def passMoveTest(self, left):
        # find left or right most block per y coordinate
        checkBlocks = {}
        for block in self.tetramino.blocks:
            x, y = block.position
            if not self.board[x, y]:
                # This tetramino got moved when some of its blocks have been removed
                return False
            if y in checkBlocks:
                if x < checkBlocks[y].position[0] if left else x > checkBlocks[y].position[0]:
                    checkBlocks[y] = block
            if y not in checkBlocks:
                checkBlocks[y] = block
        # compare the left or right most blocks with the wall or other blocks on the board
        for block in checkBlocks.values():
            x, y = block.position
            newX = x - 1 if left else x + 1
            hitWall = newX < 0 if left else newX >= self.x_size
            if hitWall or self.board[newX, y]:
                return False
            else:
                continue
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
        return 1 if self.isAccelerated else self.frameCounterCeilingCoefficient / self.blockSpeed

    def draw(self, surface):
        for block in self.blocks:
            block.draw(surface)
