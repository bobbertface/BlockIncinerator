'''
Incinerate the blocks!

The basic structure is stolen from chimp.py in the examples folder for pygame
@author: Bobbertface
'''
from Board import Board
from KeyHandler import KeyHandler
from pygame.locals import QUIT
import pygame

def main():
# Initialize
    pygame.init()
    '''block size = 20 x 20 pixels'''
    screen = pygame.display.set_mode((200, 400))
    pygame.display.set_caption('Destroy all blocks! DO EEET!')
    pygame.mouse.set_visible(False)

# Create the background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

# Display the background
    screen.blit(background, (0, 0))
    pygame.display.flip()
    
# Prepare game objects
    clock = pygame.time.Clock()
    keyHandler = KeyHandler()
    board = Board((10, 20))
    board.addTetramino()
    cooldownCounter = 0
    cooldownMax = 30
    gameOver = False
    mainLoopRun = True

# Main Loop
    while mainLoopRun:
        clock.tick(60)
        
        # Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                mainLoopRun = False
        
        # Move things based on current state
        if not gameOver:
            keyHandler.handleKeys(pygame.key.get_pressed(), board)
            gameOver = board.drop()
        
        # Close game if it ended after a period of time
        if cooldownCounter >= cooldownMax:
            mainLoopRun = False        
        
        if gameOver:
            cooldownCounter += 1
            
        # Draw everything
        screen.blit(background, (0, 0))
        board.draw(screen)
        pygame.display.flip()
    
    pygame.quit()

# this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
