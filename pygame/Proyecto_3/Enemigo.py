import pygame
import os
import random
from constants import ANCHO_PANTALLA, ALTO_PANTALLA, VELOCIDAD_ENEMIGO

# Clase para los enemigos que caen desde arriba
class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        # Inicializamos el Sprite
        super().__init__()
        
        # Ruta de la imagen del enemigo
        ruta_enemigo = os.path.join("assets", "images", "enemigo.png")
        
        try:
            # ¡GENIAL! Tu imagen ya tiene transparencia real. 
            # Usamos convert_alpha() para un resultado perfecto.
            imagen_base = pygame.image.load(ruta_enemigo).convert_alpha()
            
            # Giramos la nave 180 grados para que mire hacia abajo al jugador
            self.image = pygame.transform.rotate(imagen_base, 180)
        except Exception as error:
            print(f"Error al cargar imagen del enemigo: {error}")
            # Si falla, usamos un cuadrado rojo
            self.image = pygame.Surface((40, 40))
            self.image.fill((255, 0, 0))
            
        # La escalamos a 50x50 píxeles
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        
        # Máscara para colisiones precisas píxel por píxel
        self.mask = pygame.mask.from_surface(self.image)
        
        # Lo mandamos a su posición inicial
        self.reiniciar_posicion()

    def reiniciar_posicion(self):
        """Manda al enemigo arriba en un sitio aleatorio"""
        self.rect.x = random.randrange(ANCHO_PANTALLA - self.rect.width)
        self.rect.y = random.randrange(-150, -50)
        # Velocidad de caída proporcional a la constante
        self.velocidad_caida = VELOCIDAD_ENEMIGO + random.randint(0, 2)

    def update(self):
        """Mueve al enemigo hacia abajo"""
        self.rect.y += self.velocidad_caida
        
        # Si el enemigo se sale por abajo, vuelve a aparecer arriba
        if self.rect.top > ALTO_PANTALLA:
            self.reiniciar_posicion()