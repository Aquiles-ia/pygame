import pygame
import sys
import os

# Aseguramos que el programa use su propia carpeta como referencia para los archivos
# Esto evita errores cuando se abre el juego desde fuera de su carpeta
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from constants import ANCHO, ALTO, FPS, MENU, JUEGO, PAUSA, GAMEOVER, CREAR_ENEMIGO
from game_states import EstadosJuego

def main():
    try:
        # Inicializamos todas las funciones de Pygame y el mezclador de sonido
        pygame.init()
        pygame.mixer.init()
        
        # Configuramos el tamaño de la ventana y el título que aparece arriba
        pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Mi Gran Videojuego")
        reloj = pygame.time.Clock()
        
        # Creamos el objeto principal gestiona los estados (Menú, Juego, etc.)
        juego = EstadosJuego(pantalla)
        
        # Creamos un temporizador para que aparezca un enemigo nuevo cada X milisegundos
        # Este tiempo ahora lo puedes cambiar fácilmente desde el archivo constants.py
        from constants import TIEMPO_APARICION
        pygame.time.set_timer(CREAR_ENEMIGO, TIEMPO_APARICION)
        
        ejecutando = True
        # Bucle infinito del juego
        while ejecutando:
            # Según en qué estado estemos, ejecutamos una función u otra
            if juego.estado == MENU:
                ejecutando = juego.ejecutar_menu()
            elif juego.estado == JUEGO:
                ejecutando = juego.ejecutar_juego()
            elif juego.estado == PAUSA:
                ejecutando = juego.ejecutar_pausa()
            elif juego.estado == GAMEOVER:
                ejecutando = juego.ejecutar_gameover()
            
            if ejecutando:
                # Actualizamos la pantalla para ver los cambios
                pygame.display.flip()
                # Controlamos que el juego no vaya demasiado rápido (60 veces por segundo)
                reloj.tick(FPS)
            
    except BaseException as e:
        # Si algo falla, lo guardamos en un archivo de texto para poder leerlo
        import traceback
        error_info = traceback.format_exc()
        with open("error_log.txt", "w") as f:
            f.write(error_info)
        
        # Si no es un cierre normal, mostramos el error y esperamos
        if not isinstance(e, SystemExit):
            print("\n--- ERROR DETECTADO ---")
            print(error_info)
            print("-----------------------")
            input("El juego ha fallado. Presiona ENTER para salir y ver el archivo error_log.txt...")
            
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
