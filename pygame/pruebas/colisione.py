import pygame
from aliado import Aliado
from enemigo import Enemigo
import sys

pygame.init()
pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Colisiones")
reloj = pygame.time.Clock()

# Inicializamos el jugador (usaremos Aliado como base o una clase Jugador)
jugador = Aliado(100, 100)
# Inicializamos el enemigo
enemigo = Enemigo(200, 200)

blanco = (255, 255, 255)
velocidad = 7
ejecutando = True

def display_message(texto, color):
    fuente = pygame.font.SysFont("Arial", 48)
    img = fuente.render(texto, True, color)
    pantalla.blit(img, (250, 250))
    pygame.display.update()
    pygame.time.wait(2000)

while ejecutando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecutando = False
            
    pantalla.fill(blanco)
    
    teclas = pygame.key.get_pressed()
    # Movimiento del jugador
    if teclas[pygame.K_LEFT]:
        jugador.rect.x -= velocidad
    if teclas[pygame.K_RIGHT]:
        jugador.rect.x += velocidad
    if teclas[pygame.K_UP]:
        jugador.rect.y -= velocidad
    if teclas[pygame.K_DOWN]:
        jugador.rect.y += velocidad
        
    # Movimiento del enemigo (con WASD según el código original)
    if teclas[pygame.K_a]:
        enemigo.mover(-velocidad, 0)
    if teclas[pygame.K_d]:
        enemigo.mover(velocidad, 0)
    if teclas[pygame.K_w]:
        enemigo.mover(0, -velocidad)
    if teclas[pygame.K_s]:
        enemigo.mover(0, velocidad)
        
    # Dibujar objetos
    jugador.dibujar(pantalla)
    enemigo.dibujar(pantalla)
    
    # Detección de colisiones
    if jugador.rect.colliderect(enemigo.rect):
        display_message("¡COLISIÓN!", (255, 0, 0))
        ejecutando = False
        
    pygame.display.update()
    reloj.tick(60)

pygame.quit()