import pygame

class Enemigo:
    def __init__(self, x, y, width=50, height=50):
        # El enemigo será de color rojo por defecto
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 0, 0) # Rojo

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, self.color, self.rect)

    def mover(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
