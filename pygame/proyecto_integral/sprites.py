import pygame
import os
import random
from constants import ANCHO, ALTO, VEL_JUGADOR, VEL_ENEMIGO

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Ponemos la ruta de la imagen directamente entre comillas
        ruta_imagen = "assets/images/jugador.png"
        
        # Cargamos el dibujo
        self.image = pygame.image.load(ruta_imagen)
        self.image = pygame.transform.scale(self.image, (64, 64)) # Redimensionamos la imagen
        
        # Rect es un rectángulo invisible que rodea la imagen. Se usa para moverla y para las colisiones.
        self.rect = self.image.get_rect()
        # Colocamos al jugador en el centro y abajo de la pantalla
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = ALTO - 20
        
        # Sonido de movimiento (usaremos uno sintético si no hay archivo)
        self.move_sound = None 

    def update(self):
        teclas = pygame.key.get_pressed()
        moved = False
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= VEL_JUGADOR
            moved = True
        if teclas[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += VEL_JUGADOR
            moved = True
        if teclas[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= VEL_JUGADOR
            moved = True
        if teclas[pygame.K_DOWN] and self.rect.bottom < ALTO:
            self.rect.y += VEL_JUGADOR
            moved = True
            
        return moved

    def disparar(self):
        # Crear una bala en la posición actual del jugador
        return Bala(self.rect.centerx, self.rect.top)

class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 0), (5, 5), 5) # Bolita amarilla
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10 # Velocidad hacia arriba

    def update(self):
        # La bala se mueve hacia arriba (restando en el eje Y)
        self.rect.y += self.speedy
        # Si la bala sale por arriba (Y < 0), la borramos para no gastar memoria
        if self.rect.bottom < 0:
            self.kill()

class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        ruta_imagen = "assets/images/enemigo.png"
        
        # Dibujo del enemigo
        self.image = pygame.image.load(ruta_imagen)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.reset_position()

    def reset_position(self):
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, VEL_ENEMIGO + 2)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > ALTO + 10:
            self.reset_position()
