import pygame
import sys
from constants import ANCHO, ALTO, FPS, MENU, JUEGO, PAUSA, GAMEOVER, CREAR_ENEMIGO
from game_states import EstadosJuego

def main():
    # Inicializamos todas las funciones de Pygame y el mezclador de sonido
    pygame.init()
    pygame.mixer.init()
    
    # Configuramos el tamaño de la ventana y el título que aparece arriba
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Mi Gran Videojuego")
    clock = pygame.time.Clock()
    
    # Creamos el objeto principal gestiona los estados (Menú, Juego, etc.)
    game = EstadosJuego(pantalla)
    
    # Creamos un temporizador para que aparezca un enemigo cada 5000 milisegundos (5 seg)
    pygame.time.set_timer(CREAR_ENEMIGO, 5000)
    
    # Bucle infinito del juego
    while True:
        # Según en qué estado estemos, ejecutamos una función u otra
        if game.estado == MENU:
            game.run_menu()
        elif game.estado == JUEGO:
            game.run_game()
        elif game.estado == PAUSA:
            game.run_pause()
        elif game.estado == GAMEOVER:
            game.run_gameover()
            
        # Actualizamos la pantalla para ver los cambios
        pygame.display.flip()
        # Controlamos que el juego no vaya demasiado rápido (60 veces por segundo)
        clock.tick(FPS)

if __name__ == "__main__":
    main()
