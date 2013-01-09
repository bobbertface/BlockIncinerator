'''
@author: Bobbertface
'''
import pygame

class KeyHandler:

    def __init__(self):
        self.rotating = False
        self.movingLeft = False
        self.movingRight = False
        self.moveLeftCounter = 0
        self.moveLeftCounterMax = 1
        self.moveRightCounter = 0
        self.moveRightCounterMax = 1
        self.moveLeftDelayCounter = 0
        self.moveRightDelayCounter = 0
        self.continuousMovementDelay = 15


    def handleKeys(self, keys, board):
        isUp = keys[pygame.K_UP]  # rotate
        isDown = keys[pygame.K_DOWN]  # soft drop
        isLeft = keys[pygame.K_LEFT]
        isRight = keys[pygame.K_RIGHT]

        # Rotation
        if isUp and not self.rotating:
            self.rotating = True
            board.rotateTetramino()
        if not isUp:
            self.rotating = False

        # Soft Drop
        if isDown:
            board.isAccelerated = True
        if not isDown:
            board.isAccelerated = False

        # Move left
        if isLeft:
            if self.movingLeft:
                if self.moveLeftDelayCounter >= self.continuousMovementDelay:
                    if self.moveLeftCounter >= self.moveLeftCounterMax:
                        board.moveTetramino(True)
                        self.moveLeftCounter = 0
                    else:
                        self.moveLeftCounter += 1
                else:
                    self.moveLeftDelayCounter += 1
            else:
                self.movingLeft = True
                board.moveTetramino(True)
        if not isLeft:
            self.movingLeft = False
            self.moveLeftDelayCounter = 0

        # Move right
        if isRight:
            if self.movingRight:
                if self.moveRightDelayCounter >= self.continuousMovementDelay:
                    if self.moveRightCounter >= self.moveLeftCounterMax:
                        board.moveTetramino(False)
                        self.moveRightCounter = 0
                    else:
                        self.moveRightCounter += 1
                else:
                    self.moveRightDelayCounter += 1
            else:
                self.movingRight = True
                board.moveTetramino(False)
        if not isRight:
            self.movingRight = False
            self.moveRightDelayCounter = 0
