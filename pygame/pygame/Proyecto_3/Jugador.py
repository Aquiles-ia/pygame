import pygame
import os
from constants import ANCHO, ALTO, VEL_JUGADOR, VEL_BALA

# Clase que representa al jugador (el personaje que controlas)
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Ruta para encontrar la imagen del jugador
        ruta_imagen = os.path.join("assets", "images", "jugador.png")
        
        try:
            # Cargamos la imagen y la optimizamos
            self.image = pygame.image.load(ruta_imagen).convert()
            # Hacemos que el color negro sea transparente (el "cuadrado raro")
            self.image.set_colorkey((0, 0, 0)) 
        except:
            # Si no encuentra la imagen, dibuja un cuadrado azul para que el juego no falle
            self.image = pygame.Surface((64, 64))
            self.image.fill((0, 0, 255))
            
        # Ajustamos el tamaño de la imagen a 64x64 píxeles
        self.image = pygame.transform.scale(self.image, (64, 64))
        
        # El "rect" es el rectángulo que envuelve a la imagen, usado para posición y colisiones
        self.rect = self.image.get_rect()
        
        # Colocamos al jugador en el centro horizontal y cerca del borde inferior
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = ALTO - 20

    def update(self):
        """Esta función se ejecuta en cada fotograma para mover al jugador"""
        teclas = pygame.key.get_pressed() # Detecta qué teclas están pulsadas
        
        # Movimiento con las flechas del teclado, con límites para no salir de la pantalla
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= VEL_JUGADOR
        if teclas[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += VEL_JUGADOR
        if teclas[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= VEL_JUGADOR
        if teclas[pygame.K_DOWN] and self.rect.bottom < ALTO:
            self.rect.y += VEL_JUGADOR

    def disparar(self):
        """Crea un objeto Bala en la posición actual del jugador"""
        return Bala(self.rect.centerx, self.rect.top)

# Clase que representa los disparos del jugador
class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # La bala es un pequeño rectángulo amarillo
        self.image = pygame.Surface((5, 12))
        self.image.fill((255, 255, 0))
        
        # Posicionamos la bala donde esté el jugador al disparar
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.velocidad_y = VEL_BALA # La velocidad viene de constants.py

    def update(self):
        """Mueve el disparo hacia arriba"""
        self.rect.y += self.velocidad_y
        
        # Si la bala sale de la pantalla por arriba, la eliminamos para ahorrar memoria
        if self.rect.bottom < 0:
            self.kill()