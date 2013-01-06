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
    screen = pygame.display.set_mode((350, 400))
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
    backgroundColor = (250, 250, 250)
    # Text stuff
    textX = 210
    scoreY = 150
    levelY = 220
    scoreHeight = 15
    headerHeight = 25
    fontFile = 'resources/interstate-black.ttf'
    
    # Score
    scoreFont = pygame.font.Font(fontFile, scoreHeight)
    scoreSurface = scoreFont.render(str(board.score), 1, (25, 25, 25))
    scorePosition = (textX, scoreY)
    
    # Level
    levelSurface = scoreFont.render(str(board.blockSpeed), 1, (25, 25, 25))
    levelPosition = (textX, levelY)
    
    # Score label
    headerFont = pygame.font.Font(fontFile, headerHeight)
    scoreHeader = headerFont.render('Score:', 1, (50, 120, 80))
    
    # Level label
    levelHeader = headerFont.render('Level:', 1, (200, 0, 35))
    
    # We need to whiteout the score and level text region before each new rendering of it
    scoreEraser = pygame.Surface((140, scoreHeight))
    scoreEraser = scoreEraser.convert()
    scoreEraser.fill(backgroundColor)
    levelEraser = pygame.Surface((140, scoreHeight))
    levelEraser = levelEraser.convert()
    levelEraser.fill(backgroundColor)
    # Divides the board space from the information space
    divider = pygame.Surface((5, 400))
    divider = divider.convert()
    divider.fill((125, 125, 125))
    
    # Blit All the Things!
    background.blit(divider, (200, 0))
    background.blit(scoreHeader, (textX, scoreY - 30))
    background.blit(scoreEraser, scorePosition)
    background.blit(levelHeader, (textX, levelY - 30))
    background.blit(levelEraser, levelPosition)
    background.blit(scoreSurface, scorePosition)
    background.blit(levelSurface, levelPosition)
    pygame.display.flip()
    
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
        
        # Quick exit for ESC key
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
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
        
        # Draw everythings
        scoreSurface = scoreFont.render(str(board.score), 1, (25, 25, 25))
        levelSurface = scoreFont.render(str(board.blockSpeed), 1, (25, 25, 25))
        background.blit(scoreEraser, scorePosition)
        background.blit(scoreSurface, scorePosition)
        background.blit(levelEraser, levelPosition)
        background.blit(levelSurface, levelPosition)
        screen.blit(background, (0, 0))
        board.draw(screen)
        pygame.display.flip()
    
    pygame.quit()

# this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
