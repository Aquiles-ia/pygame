import pygame

class Aliado:
    def __init__(self, x, y, width=50, height=50):
        # El aliado será de color verde por defecto
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (0, 255, 0) # Verde

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, self.color, self.rect)
