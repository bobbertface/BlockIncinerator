'''
@author: Bobbertface
'''
import pygame

class KeyHandler:
    
    def __init__(self):
        self.rotating = False
        self.softDropping = False
        self.movingLeft = False
        self.movingRight = False
    
    def handleKeys(self, keys, board):
        isUp = keys[pygame.K_UP]
        isDown = keys[pygame.K_DOWN]
        isLeft = keys[pygame.K_LEFT]
        isRight = keys[pygame.K_RIGHT]
        isSpace = keys[pygame.K_SPACE]
        
        # Rotation
        if isUp and not self.rotating:
            self.rotating = True
            board.rotateTetramino()
        if not isUp:
            self.rotating = False
        
        # Soft Drop
        # Move left
        # Move right
        # Hard Drop
