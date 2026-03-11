import pygame
import os
import sys
from constants import *
from sprites import Jugador, Enemigo

class EstadosJuego:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.estado = MENU
        self.puntos = 0
        # Fuentes para los textos del juego
        # Intentamos cargar una letra personalizada si tienes el archivo .ttf
        ruta_letra = "assets/fonts/letra.ttf"
        if os.path.exists(ruta_letra):
            self.fuente_titulo = pygame.font.Font(ruta_letra, 64)
            self.fuente_puntos = pygame.font.Font(ruta_letra, 32)
        else:
            # Si no hay archivo, usamos Arial del sistema (lo más simple)
            self.fuente_titulo = pygame.font.SysFont("Arial", 64, bold=True)
            self.fuente_puntos = pygame.font.SysFont("Arial", 32)
        
        # Cargamos las imágenes de fondo de forma sencilla
        self.bg_menu = pygame.image.load("assets/images/menu_fondo.png")
        self.bg_menu = pygame.transform.scale(self.bg_menu, (ANCHO, ALTO))
        self.bg_juego = pygame.image.load("assets/images/juego_fondo.png")
        self.bg_juego = pygame.transform.scale(self.bg_juego, (ANCHO, ALTO))
        
        # Grupos de Sprites: Son como "listas inteligentes" que guardan todos los objetos 
        # (jugador, enemigos, balas) para poder dibujarlos o moverlos todos a la vez.
        self.todos_los_sprites = pygame.sprite.Group()
        self.enemigos = pygame.sprite.Group()
        self.balas = pygame.sprite.Group()
        self.jugador = None
        
        # Configuración de los sonidos (si no existen, no pasa nada)
        self.snd_disparo = None
        self.snd_impacto = None
        
        # Intentamos cargar los sonidos por su nombre
        if os.path.exists("assets/sounds/disparo.wav"):
            self.snd_disparo = pygame.mixer.Sound("assets/sounds/disparo.wav")
        if os.path.exists("assets/sounds/explosion.wav"):
            self.snd_impacto = pygame.mixer.Sound("assets/sounds/explosion.wav")

        # Iniciar música del menú al arrancar
        self.reproducir_musica("menu_music.mp3")

    def reproducir_musica(self, nombre_archivo):
        # Función simple para poner la música
        ruta = "assets/sounds/" + nombre_archivo
        if os.path.exists(ruta):
            pygame.mixer.music.load(ruta)
            pygame.mixer.music.play(-1) # Bucelo infinito

    # Función para preparar el juego desde cero (al empezar o al reiniciar)
    def reiniciar_juego(self):
        self.puntos = 0
        # Vaciamos los grupos por si había algo de la partida anterior
        self.todos_los_sprites = pygame.sprite.Group()
        self.enemigos = pygame.sprite.Group()
        self.balas = pygame.sprite.Group()
        
        # Creamos al jugador y lo metemos en la lista de dibujos
        self.jugador = Jugador()
        self.todos_los_sprites.add(self.jugador)
        
        # Creamos los enemigos iniciales según hayamos puesto en constants.py
        for i in range(ENEMIGOS_INICIALES):
            e = Enemigo()
            self.todos_los_sprites.add(e)
            self.enemigos.add(e)

    def ejecutar_menu(self):
        self.pantalla.blit(self.bg_menu, (0, 0))
        titulo = self.fuente_titulo.render("SPACE ADVENTURE", True, BLANCO)
        info = self.fuente_puntos.render("Presiona ESPACIO para comenzar", True, VERDE)
        
        self.pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 100))
        self.pantalla.blit(info, (ANCHO // 2 - info.get_width() // 2, 400))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.reiniciar_juego()
                    self.estado = JUEGO
                    self.reproducir_musica("game_music.mp3")
        return True

    def ejecutar_juego(self):
        self.pantalla.blit(self.bg_juego, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == CREAR_ENEMIGO:
                e = Enemigo()
                self.todos_los_sprites.add(e)
                self.enemigos.add(e)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    b = self.jugador.disparar()
                    self.todos_los_sprites.add(b)
                    self.balas.add(b)
                    if self.snd_disparo:
                        self.snd_disparo.play()
                if event.key == pygame.K_p: # Pausa
                    self.estado = PAUSA
                if event.key == pygame.K_m: # Volver al menú
                    self.estado = MENU
                    self.reproducir_musica("menu_music.mp3")
        
        # Continuar con el resto del juego si no hay QUIT event
        # ... (actualización y colisiones)

        # Actualización: Llama automáticamente a la función 'update' de cada objeto en el grupo
        self.todos_los_sprites.update()
        
        # Colisiones de BALAS con ENEMIGOS:
        # groupcollide mira si algún objeto de 'bullets' toca a 'enemies'.
        # El primer True borra la bala, el False deja al enemigo vivo (pero lo reseteamos arriba)
        impactos_balas = pygame.sprite.groupcollide(self.balas, self.enemigos, True, False)
        for impacto in impactos_balas:
            self.puntos += 50 # Sumamos puntos por cada acierto
            if self.snd_impacto:
                self.snd_impacto.play()
            # Al ser impactado, el enemigo vuelve a aparecer arriba en una posición nueva
            for enemigo_impactado in impactos_balas[impacto]:
                enemigo_impactado.reiniciar_posicion()
        
        # Colisiones de JUGADOR con ENEMIGOS:
        # spritecollide mira si nuestro jugador toca algún enemigo de la lista
        impactos_jugador = pygame.sprite.spritecollide(self.jugador, self.enemigos, False)
        if impactos_jugador:
            # Si una nave enemiga nos toca, morimos y vamos a Game Over
            self.estado = GAMEOVER
            if self.snd_impacto:
                self.snd_impacto.play()
            
        # Un pequeño marcador que sube solo con el tiempo
        self.puntos += 0.1

        # Dibujado
        self.todos_los_sprites.draw(self.pantalla)
        
        # Marcador
        score_text = self.fuente_puntos.render(f"Puntos: {int(self.puntos)}", True, BLANCO)
        self.pantalla.blit(score_text, (10, 10))
        return True

    def ejecutar_pausa(self):
        # Dibujar una capa semitransparente o solo texto
        info = self.fuente_titulo.render("PAUSA", True, ROJO)
        self.pantalla.blit(info, (ANCHO // 2 - info.get_width() // 2, ALTO // 2))
        sub_info = self.fuente_puntos.render("Presiona P para continuar", True, BLANCO)
        self.pantalla.blit(sub_info, (ANCHO // 2 - sub_info.get_width() // 2, ALTO // 2 + 70))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.estado = JUEGO
        return True

    def ejecutar_gameover(self):
        # Fondo oscuro y mensaje de Game Over
        self.pantalla.fill(NEGRO)
        titulo = self.fuente_titulo.render("GAME OVER", True, ROJO)
        score_final = self.fuente_puntos.render(f"Puntuación Final: {int(self.puntos)}", True, BLANCO)
        info = self.fuente_puntos.render("Presiona ESPACIO para Menú o R para Reiniciar", True, VERDE)
        
        self.pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 150))
        self.pantalla.blit(score_final, (ANCHO // 2 - score_final.get_width() // 2, 250))
        self.pantalla.blit(info, (ANCHO // 2 - info.get_width() // 2, 400))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.estado = MENU
                    self.reproducir_musica("menu_music.mp3")
                if event.key == pygame.K_r:
                    self.reiniciar_juego()
                    self.estado = JUEGO
        return True
