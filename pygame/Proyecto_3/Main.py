import pygame
import sys
import os

# --- PREPARACIÓN DEL ENTORNO ---
# Esta línea asegura que Python busque los archivos (imágenes, sonidos) siempre en la carpeta del juego
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Importamos nuestras propias configuraciones y clases
from constants import *
from Jugador import Jugador
from Enemigo import Enemigo

# Esta clase es el "cerebro" del juego. Controla los puntos, las pantallas y los sprites.
class GerenteJuego:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.estado = MENU  # Empezamos en el menú principal
        self.puntos = 0
        
        # --- CARGA DE FUENTES (LETRAS) ---
        ruta_letra = os.path.join("assets", "fonts", "letra.ttf")
        if os.path.exists(ruta_letra):
            self.fuente_titulo = pygame.font.Font(ruta_letra, 64)
            self.fuente_texto = pygame.font.Font(ruta_letra, 32)
        else:
            # Si no hay archivo de letra, usamos la genérica del sistema (Arial)
            self.fuente_titulo = pygame.font.SysFont("Arial", 64, bold=True)
            self.fuente_texto = pygame.font.SysFont("Arial", 32)
            
        # --- CARGA DE FONDOS ---
        try:
            self.fondo_menu = pygame.image.load(os.path.join("assets", "images", "menu_fondo.png")).convert()
            self.fondo_menu = pygame.transform.scale(self.fondo_menu, (ANCHO, ALTO))
            self.fondo_juego = pygame.image.load(os.path.join("assets", "images", "juego_fondo.png")).convert()
            self.fondo_juego = pygame.transform.scale(self.fondo_juego, (ANCHO, ALTO))
        except:
            # Fondos de emergencia si las imágenes no cargan
            self.fondo_menu = pygame.Surface((ANCHO, ALTO))
            self.fondo_menu.fill(NEGRO)
            self.fondo_juego = pygame.Surface((ANCHO, ALTO))
            self.fondo_juego.fill((0, 0, 50))
            
        # Preparamos las listas de objetos
        self.reiniciar_partida()
        
        # Iniciamos la música del menú
        self.reproducir_musica("menu_music.mp3")

    def reproducir_musica(self, nombre_archivo):
        """Carga y reproduce música de fondo en bucle"""
        ruta = os.path.join("assets", "sounds", nombre_archivo)
        if os.path.exists(ruta):
            pygame.mixer.music.load(ruta)
            pygame.mixer.music.play(-1) # El -1 significa que se repite infinito

    def reiniciar_partida(self):
        """Pone todo a cero para empezar una partida nueva"""
        self.puntos = 0
        # Los grupos de sprites son listas inteligentes de Pygame
        self.todos_los_sprites = pygame.sprite.Group() # Para dibujar y actualizar todo a la vez
        self.enemigos = pygame.sprite.Group()          # Solo para detectar choques con enemigos
        self.balas = pygame.sprite.Group()             # Solo para los disparos
        
        # Creamos al jugador
        self.jugador = Jugador()
        self.todos_los_sprites.add(self.jugador)
        
        # Creamos los primeros enemigos del juego
        for _ in range(ENEMIGOS_INICIALES):
            nuevo_enemigo = Enemigo()
            self.enemigos.add(nuevo_enemigo)
            self.todos_los_sprites.add(nuevo_enemigo)

    def dibujar_texto(self, texto, fuente, color, x, y):
        """Función auxiliar para escribir texto centrado fácilmente"""
        imagen_texto = fuente.render(texto, True, color)
        rectangulo = imagen_texto.get_rect()
        rectangulo.center = (x, y)
        self.pantalla.blit(imagen_texto, rectangulo)

    def ejecutar_menu(self):
        """Dibuja el menú y espera a que el usuario pulse ESPACIO"""
        self.pantalla.blit(self.fondo_menu, (0, 0))
        self.dibujar_texto("SPACE ADVENTURE", self.fuente_titulo, BLANCO, ANCHO//2, 150)
        self.dibujar_texto("Presiona ESPACIO para comenzar", self.fuente_texto, VERDE, ANCHO//2, 450)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    self.reiniciar_partida()
                    self.estado = JUEGO
                    self.reproducir_musica("game_music.mp3") # Cambiamos a música de acción
        return True

    def ejecutar_juego(self):
        """La lógica principal mientras estás jugando"""
        self.pantalla.blit(self.fondo_juego, (0, 0))
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: return False
            
            # Crear un enemigo nuevo cuando el temporizador lo indique
            if evento.type == CREAR_ENEMIGO:
                nuevo_enemigo = Enemigo()
                self.enemigos.add(nuevo_enemigo)
                self.todos_los_sprites.add(nuevo_enemigo)
                
            # Disparar al pulsar ESPACIO
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    nueva_bala = self.jugador.disparar()
                    self.balas.add(nueva_bala)
                    self.todos_los_sprites.add(nueva_bala)
                # Pausar el juego con la letra P
                if evento.key == pygame.K_p: self.estado = PAUSA
        
        # Actualizamos la posición de todos los objetos
        self.todos_los_sprites.update()
        
        # --- DETECCIÓN DE COLISIONES ---
        # ¿Han chocado las balas con los enemigos?
        # groupcollide(grupo1, grupo2, borrar1, borrar2)
        impactos = pygame.sprite.groupcollide(self.enemigos, self.balas, True, True)
        for _ in impactos:
            self.puntos += 10 # 10 puntos por cada nave destruida
            # Creamos un nuevo enemigo para que la pantalla no se quede vacía
            nuevo_enemigo = Enemigo()
            self.enemigos.add(nuevo_enemigo)
            self.todos_los_sprites.add(nuevo_enemigo)
            
        # ¿Ha chocado el jugador contra algún enemigo?
        if pygame.sprite.spritecollide(self.jugador, self.enemigos, False):
            self.estado = GAMEOVER # Si chocamos, se acaba la partida
            
        # Dibujamos todo en la pantalla
        self.todos_los_sprites.draw(self.pantalla)
        # Mostramos los puntos arriba a la izquierda
        self.dibujar_texto(f"Puntos: {self.puntos}", self.fuente_texto, BLANCO, 100, 30)
        
        return True

    def ejecutar_pausa(self):
        """Mantiene el juego detenido hasta pulsar P de nuevo"""
        # Dibujamos el estado actual del juego de fondo
        self.pantalla.blit(self.fondo_juego, (0, 0))
        self.todos_los_sprites.draw(self.pantalla)
        
        # Ponemos el cartel de PAUSA encima
        self.dibujar_texto("PAUSA", self.fuente_titulo, ROJO, ANCHO//2, ALTO//2)
        self.dibujar_texto("Presiona P para continuar", self.fuente_texto, BLANCO, ANCHO//2, ALTO//2 + 80)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p: self.estado = JUEGO
        return True

    def ejecutar_gameover(self):
        """Muestra la puntuación final y permite reiniciar"""
        self.pantalla.fill(NEGRO)
        self.dibujar_texto("GAME OVER", self.fuente_titulo, ROJO, ANCHO//2, 150)
        self.dibujar_texto(f"Puntos Finales: {self.puntos}", self.fuente_texto, BLANCO, ANCHO//2, 250)
        self.dibujar_texto("R para Reintentar - M para Menú", self.fuente_texto, VERDE, ANCHO//2, 450)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: return False
            if evento.type == pygame.KEYDOWN:
                # 'R' reinicia la partida directamente
                if evento.key == pygame.K_r:
                    self.reiniciar_partida()
                    self.estado = JUEGO
                    self.reproducir_musica("game_music.mp3")
                # 'M' te lleva al menú inicial
                if evento.key == evento.key == pygame.K_m:
                    self.estado = MENU
                    self.reproducir_musica("menu_music.mp3")
        return True

def main():
    # Inicialización básica de Pygame
    pygame.init()
    pygame.mixer.init() # Para el sonido
    
    # Creamos la ventana con el tamaño de constants.py
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("SPACE ADVENTURE - PROYECTO 3")
    reloj = pygame.time.Clock() # Para controlar los FPS
    
    # Creamos el objeto principal que gestiona todo
    juego = GerenteJuego(pantalla)
    
    # Ponemos en marcha el reloj para que aparezcan enemigos cada X tiempo
    pygame.time.set_timer(CREAR_ENEMIGO, TIEMPO_APARICION)
    
    # BUCLE PRINCIPAL (El corazón del programa)
    ejecutando = True
    while ejecutando:
        # Llamamos a la función correspondiente según el estado del juego
        if juego.estado == MENU: ejecutando = juego.ejecutar_menu()
        elif juego.estado == JUEGO: ejecutando = juego.ejecutar_juego()
        elif juego.estado == PAUSA: ejecutando = juego.ejecutar_pausa()
        elif juego.estado == GAMEOVER: ejecutando = juego.ejecutar_gameover()
        
        if ejecutando:
            # Actualizamos la visualización de la pantalla
            pygame.display.flip()
            # Mantenemos la velocidad constante (60 FPS)
            reloj.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()