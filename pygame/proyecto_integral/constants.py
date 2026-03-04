import pygame

# Dimensiones de la pantalla
ANCHO = 800
ALTO = 600
FPS = 60

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)

# Estados del juego
MENU = "MENU"
JUEGO = "JUEGO"
PAUSA = "PAUSA"
GAMEOVER = "GAMEOVER"

# Velocidades
VEL_JUGADOR = 5
VEL_ENEMIGO = 3

# Eventos personalizados
CREAR_ENEMIGO = pygame.USEREVENT + 1
