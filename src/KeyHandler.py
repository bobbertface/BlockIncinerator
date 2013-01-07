'''
@author: Bobbertface
'''
import pygame

class KeyHandler:

    def __init__(self):
        self.rotating = False
        self.movingLeft = False
        self.movingRight = False

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
        if isLeft and not self.movingLeft:
            self.movingLeft = True
            board.moveTetramino(True)
        if not isLeft:
            self.movingLeft = False

        # Move right
        if isRight and not self.movingRight:
            self.movingRight = True
            board.moveTetramino(False)
        if not isRight:
            self.movingRight = False
