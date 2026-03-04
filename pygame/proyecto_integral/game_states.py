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
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.player = None
        
        # Configuración de los sonidos (si no existen, no pasa nada)
        self.snd_shoot = None
        self.snd_hit = None
        
        # Intentamos cargar los sonidos por su nombre
        if os.path.exists("assets/sounds/disparo.wav"):
            self.snd_shoot = pygame.mixer.Sound("assets/sounds/disparo.wav")
        if os.path.exists("assets/sounds/explosion.wav"):
            self.snd_hit = pygame.mixer.Sound("assets/sounds/explosion.wav")

        # Iniciar música del menú al arrancar
        self.play_music("menu_music.mp3")

    def play_music(self, nombre_archivo):
        # Función simple para poner la música
        ruta = "assets/sounds/" + nombre_archivo
        if os.path.exists(ruta):
            pygame.mixer.music.load(ruta)
            pygame.mixer.music.play(-1) # Bucelo infinito

    # Función para preparar el juego desde cero (al empezar o al reiniciar)
    def reset_game(self):
        self.score = 0
        # Vaciamos los grupos por si había algo de la partida anterior
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        
        # Creamos al jugador y lo metemos en la lista de dibujos
        self.player = Player()
        self.all_sprites.add(self.player)
        
        # Creamos 3 enemigos iniciales
        for i in range(3):
            e = Enemy()
            self.all_sprites.add(e)
            self.enemies.add(e)

    def run_menu(self):
        self.pantalla.blit(self.bg_menu, (0, 0))
        titulo = self.fuente_titulo.render("SPACE ADVENTURE", True, BLANCO)
        info = self.fuente_puntos.render("Presiona ESPACIO para comenzar", True, VERDE)
        
        self.pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 100))
        self.pantalla.blit(info, (ANCHO // 2 - info.get_width() // 2, 400))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.reiniciar_juego()
                    self.estado = JUEGO
                    self.play_music("game_music.mp3") # Cambiar música al empezar juego

    def run_game(self):
        self.pantalla.blit(self.bg_juego, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == CREAR_ENEMIGO:
                e = Enemigo()
                self.all_sprites.add(e)
                self.enemigos.add(e)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    b = self.jugador.disparar()
                    self.all_sprites.add(b)
                    self.balas.add(b)
                    if self.snd_shoot:
                        self.snd_shoot.play()
                if event.key == pygame.K_p: # Pausa
                    self.estado = PAUSA
                if event.key == pygame.K_m: # Volver al menú
                    self.estado = MENU
                    self.play_music("menu_music.mp3") # Cambiar música al volver al menú

        # Actualización: Llama automáticamente a la función 'update' de cada objeto en el grupo
        self.all_sprites.update()
        
        # Colisiones de BALAS con ENEMIGOS:
        # groupcollide mira si algún objeto de 'bullets' toca a 'enemies'.
        # El primer True borra la bala, el False deja al enemigo vivo (pero lo reseteamos arriba)
        hits_bullets = pygame.sprite.groupcollide(self.bullets, self.enemies, True, False)
        for hit in hits_bullets:
            self.score += 50 # Sumamos puntos por cada acierto
            if self.snd_hit:
                self.snd_hit.play()
            # Al ser impactado, el enemigo vuelve a aparecer arriba en una posición nueva
            for enemy_hit in hits_bullets[hit]:
                enemy_hit.reset_position()
        
        # Colisiones de JUGADOR con ENEMIGOS:
        # spritecollide mira si nuestro jugador toca algún enemigo de la lista
        hits_player = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if hits_jugador:
            # Si una nave enemiga nos toca, morimos y vamos a Game Over
            self.estado = GAMEOVER
            if self.snd_hit:
                self.snd_hit.play()
            
        # Un pequeño marcador que sube solo con el tiempo
        self.puntos += 0.1

        # Dibujado
        self.all_sprites.draw(self.pantalla)
        
        # Marcador
        score_text = self.fuente_puntos.render(f"Puntos: {int(self.puntos)}", True, BLANCO)
        self.pantalla.blit(score_text, (10, 10))

    def run_pause(self):
        # Dibujar una capa semitransparente o solo texto
        info = self.fuente_titulo.render("PAUSA", True, ROJO)
        self.pantalla.blit(info, (ANCHO // 2 - info.get_width() // 2, ALTO // 2))
        sub_info = self.fuente_puntos.render("Presiona P para continuar", True, BLANCO)
        self.pantalla.blit(sub_info, (ANCHO // 2 - sub_info.get_width() // 2, ALTO // 2 + 70))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.estado = JUEGO

    def run_gameover(self):
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
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.estado = MENU
                    self.play_music("menu_music.mp3")
                if event.key == pygame.K_r:
                    self.reiniciar_juego()
                    self.estado = JUEGO
