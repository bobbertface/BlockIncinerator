'''
@author: Bobbertface
'''
import ResourceLoader
import pygame

class Block(pygame.sprite.Sprite):
    def __init__(self, color, position, positionModifier):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = ResourceLoader.load_image(ResourceLoader.getImagePathForColor(color), -1)
        self.position = position
        self.positionModifier = positionModifier
        self.changePosition(position)

    def draw(self, surface):
        surface_blit = surface.blit
        surface_blit(self.image, self.rect)

    def changePosition(self, positionTuple):
        self.position = positionTuple
        x, y = positionTuple
        self.rect.topleft = x * self.positionModifier, (y-1) * self.positionModifier
