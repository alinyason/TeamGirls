import pygame

class Character:
    def init(self, x, y, color=(255, 0, 0), size=2):
        self.x = x
        self.y = y
        self.color = color
        self.size = size

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))