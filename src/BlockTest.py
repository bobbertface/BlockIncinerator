'''
@author: Bobbertface
'''
from pygame.locals import QUIT
from Block import Block
import pygame

def main():
# Initialize
    pygame.init()
    '''block size = 20 x 20 pixels'''
    screen = pygame.display.set_mode((200, 400))
    area = screen.get_rect()
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
    block = Block('red', (4,0), 20)
    count = 0
    maxCount = 30
# Main Loop
    gameNotOver = True
    while gameNotOver:
        clock.tick(60)
        
        # Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                gameNotOver = False
        
        # Move things based on current state
        if count >= maxCount:
            count = 0
            x, y = block.position
            block.changePosition((x, y+1))
        else:
            count += 1
        
        if block.rect.bottom >= area.bottom:
            gameNotOver = False
        
        # Draw everything
        screen.blit(background, (0, 0))
        block.draw(screen)
        pygame.display.flip()
    
    pygame.quit()

# this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
