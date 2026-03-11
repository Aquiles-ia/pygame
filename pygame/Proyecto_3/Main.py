import pygame
import sys
import os

# --- PREPARACIÓN DEL DIRECTORIO ---
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Importamos constantes y clases
from constants import *
from Jugador import Jugador
from Enemigo import Enemigo

# Clase que gestiona el funcionamiento global del juego
class GerenteJuego:
    def __init__(self, ventana_juego):
        self.ventana = ventana_juego
        self.estado_actual = MENU
        self.puntuacion_total = 0
        
        # --- CARGA DE RECURSOS (Letras y Fondos) ---
        ruta_fuente = os.path.join("assets", "fonts", "letra.ttf")
        if os.path.exists(ruta_fuente):
            self.fuente_grande = pygame.font.Font(ruta_fuente, 64)
            self.fuente_pequeña = pygame.font.Font(ruta_fuente, 32)
        else:
            self.fuente_grande = pygame.font.SysFont("Arial", 64, bold=True)
            self.fuente_pequeña = pygame.font.SysFont("Arial", 32)
            
        try:
            self.fondo_menu = pygame.image.load(os.path.join("assets", "images", "menu_fondo.png")).convert()
            self.fondo_menu = pygame.transform.scale(self.fondo_menu, (ANCHO_PANTALLA, ALTO_PANTALLA))
            self.fondo_juego = pygame.image.load(os.path.join("assets", "images", "juego_fondo.png")).convert()
            self.fondo_juego = pygame.transform.scale(self.fondo_juego, (ANCHO_PANTALLA, ALTO_PANTALLA))
        except:
            self.fondo_menu = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA))
            self.fondo_menu.fill(NEGRO)
            self.fondo_juego = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA))
            self.fondo_juego.fill((0, 0, 50))
            
        self.iniciar_partida_nueva()
        self.gestionar_musica("menu_music.mp3")

    def gestionar_musica(self, nombre_archivo_musica):
        """Reproduce música de fondo"""
        ruta_audio = os.path.join("assets", "sounds", nombre_archivo_musica)
        if os.path.exists(ruta_audio):
            pygame.mixer.music.load(ruta_audio)
            pygame.mixer.music.play(-1)

    def iniciar_partida_nueva(self):
        """Limpia los datos para comenzar de cero"""
        self.puntuacion_total = 0
        self.grupo_todos_los_elementos = pygame.sprite.Group()
        self.grupo_enemigos = pygame.sprite.Group()
        self.grupo_balas = pygame.sprite.Group()
        
        self.nave_jugador = Jugador()
        self.grupo_todos_los_elementos.add(self.nave_jugador)
        
        for i in range(ENEMIGOS_INICIALES):
            enemigo_nuevo = Enemigo()
            self.grupo_enemigos.add(enemigo_nuevo)
            self.grupo_todos_los_elementos.add(enemigo_nuevo)

    def escribir_texto(self, mensaje, fuente, color, coord_x, coord_y):
        """Dibuja texto en la pantalla"""
        dibujo_texto = fuente.render(mensaje, True, color)
        rect_texto = dibujo_texto.get_rect()
        rect_texto.center = (coord_x, coord_y)
        self.ventana.blit(dibujo_texto, rect_texto)

    def dibujar_salud_jugador(self, x, y, salud):
        """Dibuja una barra de vida roja muy simple"""
        if salud < 0: salud = 0
        ANCHO_MAXIMO = 200
        ALTO_BARRA = 20
        relleno = (salud / VIDA_JUGADOR_MAXIMA) * ANCHO_MAXIMO
        
        rectangulo_fondo = pygame.Rect(x, y, ANCHO_MAXIMO, ALTO_BARRA)
        rectangulo_salud = pygame.Rect(x, y, relleno, ALTO_BARRA)
        
        # Barra roja de salud
        pygame.draw.rect(self.ventana, ROJO, rectangulo_salud)
        # Borde blanco
        pygame.draw.rect(self.ventana, BLANCO, rectangulo_fondo, 2)

    def controlar_menu(self):
        """Dibuja el menú principal"""
        self.ventana.blit(self.fondo_menu, (0, 0))
        self.escribir_texto("SPACE ADVENTURE", self.fuente_grande, BLANCO, ANCHO_PANTALLA//2, 150)
        self.escribir_texto("Presiona ESPACIO para empezar", self.fuente_pequeña, VERDE, ANCHO_PANTALLA//2, 450)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    self.iniciar_partida_nueva()
                    self.estado_actual = JUEGO
                    self.gestionar_musica("game_music.mp3")
        return True

    def controlar_juego(self):
        """Dibuja y actualiza la acción del juego"""
        self.ventana.blit(self.fondo_juego, (0, 0))
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: return False
            if evento.type == EVENTO_CREAR_ENEMIGO:
                nuevo = Enemigo()
                self.grupo_enemigos.add(nuevo)
                self.grupo_todos_los_elementos.add(nuevo)
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    bala = self.nave_jugador.disparar()
                    self.grupo_balas.add(bala)
                    self.grupo_todos_los_elementos.add(bala)
                if evento.key == pygame.K_p: self.estado_actual = PAUSA
        
        self.grupo_todos_los_elementos.update()
        
        # Colisiones precisas con máscaras
        for proyectil in self.grupo_balas:
            golpeados = pygame.sprite.spritecollide(proyectil, self.grupo_enemigos, True, pygame.sprite.collide_mask)
            if golpeados:
                proyectil.kill()
                for e in golpeados:
                    self.puntuacion_total += 10
                    enemigo_respawn = Enemigo()
                    self.grupo_enemigos.add(enemigo_respawn)
                    self.grupo_todos_los_elementos.add(enemigo_respawn)

        colisiones_jugador = pygame.sprite.spritecollide(self.nave_jugador, self.grupo_enemigos, True, pygame.sprite.collide_mask)
        for choque in colisiones_jugador:
            # Quitamos vida usando la nueva función que has creado
            self.nave_jugador.recibir_danio(DANIO_POR_ENEMIGO)
            nuevo_enemigo = Enemigo()
            self.grupo_enemigos.add(nuevo_enemigo)
            self.grupo_todos_los_elementos.add(nuevo_enemigo)
            
            # Comprobamos la vida con el nuevo método
            if self.nave_jugador.get_vida() <= 0:
                self.estado_actual = GAMEOVER
            
        # Dibujamos todos los personajes en su nueva posición
        self.grupo_todos_los_elementos.draw(self.ventana)
        
        # Dibujamos la interfaz (puntos y salud usando el nuevo método)
        self.escribir_texto(f"Puntos: {self.puntuacion_total}", self.fuente_pequeña, BLANCO, ANCHO_PANTALLA - 100, 30)
        self.escribir_texto("VIDA:", self.fuente_pequeña, BLANCO, 60, 30)
        self.dibujar_salud_jugador(120, 20, self.nave_jugador.get_vida())
        
        return True

    def controlar_pausa(self):
        """Pantalla de pausa"""
        self.ventana.blit(self.fondo_juego, (0, 0))
        self.grupo_todos_los_elementos.draw(self.ventana)
        self.escribir_texto("PAUSA", self.fuente_grande, ROJO, ANCHO_PANTALLA//2, ALTO_PANTALLA//2)
        self.escribir_texto("Pulsa P para volver", self.fuente_pequeña, BLANCO, ANCHO_PANTALLA//2, ALTO_PANTALLA//2 + 80)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p: self.estado_actual = JUEGO
        return True

    def controlar_gameover(self):
        """Pantalla final de derrota"""
        self.ventana.fill(NEGRO)
        self.escribir_texto("FIN DE LA PARTIDA", self.fuente_grande, ROJO, ANCHO_PANTALLA//2, 150)
        self.escribir_texto(f"Puntuación: {self.puntuacion_total}", self.fuente_pequeña, BLANCO, ANCHO_PANTALLA//2, 250)
        self.escribir_texto("R: Reintentar  -  M: Menú", self.fuente_pequeña, VERDE, ANCHO_PANTALLA//2, 450)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    self.iniciar_partida_nueva()
                    self.estado_actual = JUEGO
                    self.gestionar_musica("game_music.mp3")
                if evento.key == pygame.K_m:
                    self.estado_actual = MENU
                    self.gestionar_musica("menu_music.mp3")
        return True

def bucle_principal():
    """Arranque del juego y bucle de repetición"""
    pygame.init()
    pygame.mixer.init()
    ventana = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption("SPACE ADVENTURE")
    reloj = pygame.time.Clock()
    
    juego = GerenteJuego(ventana)
    pygame.time.set_timer(EVENTO_CREAR_ENEMIGO, TIEMPO_APARICION_ENEMIGO)
    
    seguir = True
    while seguir:
        if juego.estado_actual == MENU: seguir = juego.controlar_menu()
        elif juego.estado_actual == JUEGO: seguir = juego.controlar_juego()
        elif juego.estado_actual == PAUSA: seguir = juego.controlar_pausa()
        elif juego.estado_actual == GAMEOVER: seguir = juego.controlar_gameover()
        
        if seguir:
            pygame.display.flip()
            reloj.tick(FOTOGRAMAS_POR_SEGUNDO)
            
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    bucle_principal()