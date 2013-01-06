'''
@author: whoever wrote chimp.py in the examples folder for pygame, I only barely changed the code from there (Bobbertface)
'''
from pygame.compat import geterror
import os
import pygame

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'resources')

def getImagePathForColor(color):
    return '{0}{1}'.format(color, '_block.png')

# Copied directly from chimp.py in the examples folder for pygame
def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print ('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    return image, image.get_rect()

# Copied directly from chimp.py in the examples folder for pygame
def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(data_dir, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print ('Cannot load sound: %s' % fullname)
        raise SystemExit(str(geterror()))
    return sound
