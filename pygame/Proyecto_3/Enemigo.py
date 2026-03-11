import pygame
import os
import random
from constants import ANCHO, ALTO, VEL_ENEMIGO

# Clase para los enemigos que caen desde arriba
class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Buscamos la imagen del enemigo
        ruta_imagen = os.path.join("assets", "images", "enemigo.png")
        
        try:
            # Cargamos la imagen y activamos la transparencia del color negro
            self.image = pygame.image.load(ruta_imagen).convert()
            self.image.set_colorkey((0, 0, 0))
        except:
            # Si falla la carga, dibujamos un cuadrado rojo
            self.image = pygame.Surface((50, 50))
            self.image.fill((255, 0, 0))
            
        # Redimensionamos al enemigo
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        
        # Llamamos a esta función para darle una posición inicial aleatoria
        self.reiniciar_posicion()

    def reiniciar_posicion(self):
        """Coloca al enemigo en la parte superior en una X aleatoria"""
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        # Aparece un poco fuera de pantalla por arriba (-150 a -50)
        self.rect.y = random.randrange(-150, -50)
        # Le damos una velocidad aleatoria para que no bajen todos igual
        self.velocidad_y = random.randint(VEL_ENEMIGO, VEL_ENEMIGO + 2)

    def update(self):
        """Mueve al enemigo hacia abajo en cada fotograma"""
        self.rect.y += self.velocidad_y
        
        # Si el enemigo llega al fondo de la pantalla, vuelve a aparecer arriba
        if self.rect.top > ALTO + 10:
            self.reiniciar_posicion()