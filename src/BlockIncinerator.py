'''
Incinerate the blocks!

The basic structure is stolen from chimp.py in the examples folder for pygame
@author: Bobbertface
'''
from Board import Board
from KeyHandler import KeyHandler
from pygame.locals import QUIT
import pygame
from Tetramino import Tetramino
import Pieces

def main():
    '''
    The block size is 20 x 20 pixels
    There are magic numbers everywhere, which means this is not very maintainable at the moment
    Also... wall-o-text
    '''
    # Initialize
    pygame.init()
    screenSize = (350, 400)
    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption('Destroy all blocks! DO EEET!')
    pygame.mouse.set_visible(False)

    # Create the background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    backgroundColor = (250, 250, 250)
    background.fill(backgroundColor)

    # Display the background
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Prepare game objects
    clock = pygame.time.Clock()
    keyHandler = KeyHandler()
    board = Board((10, 21))
    board.addTetramino(Pieces.getRandomName())

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
    scoreHeader = headerFont.render('Score:', 1, (50, 120, 200))

    # Level label
    levelHeader = headerFont.render('Level:', 1, (200, 50, 0))

    # Piece preview
    piecePreview = pygame.Surface((80, 40))
    piecePreview = piecePreview.convert()
    piecePreview.fill(backgroundColor)
    previewPositionLocal = (0, 0)
    previewPositionGlobal = (textX, 40)
    tetramino = Tetramino(Pieces.getRandomName(), previewPositionLocal, 20)
    tetramino.draw(piecePreview)

    # We need to whiteout the score and level text regions before each new rendering of it
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
    background.blit(piecePreview, (textX, 40))
    pygame.display.flip()

    cooldownCounter = 0
    cooldownMax = 30
    lineClearCounter = 0
    lineClearDelay = 10
    collision = False
    gameOver = False
    mainLoopRun = True
    exitProgram = False

    # Main Loop
    while mainLoopRun:
        clock.tick(60)

        # Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                mainLoopRun = False
                exitProgram = True

        # Quick exit for ESC key
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            mainLoopRun = False
            exitProgram = True

        # Delay between collisions (and line clears) and the next piece getting loaded
        if collision:
            if lineClearCounter >= lineClearDelay:
                lineClearCounter = 0
                collision = False
                gameOver = board.addTetramino(tetramino.name)
                tetramino = Tetramino(Pieces.getRandomName(), previewPositionLocal, 20)
                piecePreview.fill(backgroundColor)  # erase it before getting the next one
                tetramino.draw(piecePreview)
            else:
                lineClearCounter += 1

        # Move things based on current state
        if not gameOver and not collision:
            # Hard Drop
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                board.hardDrop()
                collision = True
            else:
                keyHandler.handleKeys(pygame.key.get_pressed(), board)
                collision = board.drop()

        # Close game if it ended after a period of time
        if cooldownCounter >= cooldownMax:
            mainLoopRun = False

        if gameOver:
            cooldownCounter += 1

        # Draw everything
        scoreSurface = scoreFont.render(str(board.score), 1, (25, 25, 25))
        levelSurface = scoreFont.render(str(board.blockSpeed), 1, (25, 25, 25))
        background.blit(scoreEraser, scorePosition)
        background.blit(scoreSurface, scorePosition)
        background.blit(levelEraser, levelPosition)
        background.blit(levelSurface, levelPosition)
        background.blit(piecePreview, previewPositionGlobal)
        screen.blit(background, (0, 0))
        board.draw(screen)
        pygame.display.flip()

    # Game over
    endGameSurface = pygame.Surface(screenSize, pygame.SRCALPHA)
    endGameSurface.fill((125, 125, 125, 100))
    gameOverText = headerFont.render('GAME OVER', 1, (0, 0, 0))
    endGameSurface.blit(gameOverText, (100, 175))
    screen.blit(endGameSurface, (0, 0))
    pygame.display.flip()

    # Wait for user to exit the program
    while not exitProgram:
        for event in pygame.event.get():
            if event.type == QUIT:
                exitProgram = True
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            exitProgram = True
    pygame.quit()

# this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
