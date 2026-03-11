import pygame
import os
from constants import ANCHO_PANTALLA, ALTO_PANTALLA, VELOCIDAD_JUGADOR, VELOCIDAD_BALA, VIDA_JUGADOR_MAXIMA

# Esta clase define cómo se comporta el Jugador (la nave que controlas)
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        # Inicializamos la clase Sprite de Pygame
        super().__init__()
        
        # Atributos de salud (privado como en tu ejemplo) y velocidad
        self.__vida = VIDA_JUGADOR_MAXIMA
        self.velocidad = VELOCIDAD_JUGADOR
        
        # Ruta de la imagen del jugador
        ruta_jugador = os.path.join("assets", "images", "jugador.png")
        
        try:
            # ¡PERFECTO! Como has puesto transparencia real en el PNG, 
            # usamos convert_alpha() para que se vea impecable sin hacer nada más.
            self.image = pygame.image.load(ruta_jugador).convert_alpha()
        except Exception as error:
            print(f"No se pudo cargar la imagen: {error}")
            # Cuadrado por si falla la carga
            self.image = pygame.Surface((50, 50))
            self.image.fill((0, 255, 0)) # Verde
            
        # Ajustamos el tamaño a 64x64 píxeles
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        
        # Máscara para que los choques solo ocurran si se tocan los dibujos
        self.mask = pygame.mask.from_surface(self.image)
        
        # Colocamos la nave abajo en el centro
        self.rect.centerx = ANCHO_PANTALLA // 2
        self.rect.bottom = ALTO_PANTALLA - 20

    def update(self):
        """Mueve la nave según las flechas del teclado"""
        teclas = pygame.key.get_pressed()
        
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT] and self.rect.right < ANCHO_PANTALLA:
            self.rect.x += self.velocidad
        if teclas[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.velocidad
        if teclas[pygame.K_DOWN] and self.rect.bottom < ALTO_PANTALLA:
            self.rect.y += self.velocidad

    def disparar(self):
        """Crea una bala en la punta de la nave"""
        return Bala(self.rect.centerx, self.rect.top)

    def recibir_danio(self, cantidad):
        """Resta salud al jugador"""
        self.__vida -= cantidad
        if self.__vida < 0: self.__vida = 0

    def get_vida(self):
        """Devuelve la salud actual"""
        return self.__vida

# Clase para los disparos del jugador
class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Pequeño disparo amarillo
        self.image = pygame.Surface((4, 15), pygame.SRCALPHA)
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.velocidad_bala = VELOCIDAD_BALA
        # Máscara para choques precisos de la bala
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        """La bala sube y desaparece al salir de la pantalla"""
        self.rect.y += self.velocidad_bala
        if self.rect.bottom < 0:
            self.kill()