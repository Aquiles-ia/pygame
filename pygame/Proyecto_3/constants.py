import pygame

# --- CONFIGURACIÓN DE LA PANTALLA ---
ANCHO_PANTALLA = 800  # Ancho de la ventana en píxeles
ALTO_PANTALLA = 600   # Alto de la ventana en píxeles
FOTOGRAMAS_POR_SEGUNDO = 60  # Velocidad del juego (FPS)

# --- COLORES (Formato RGB: Rojo, Verde, Azul) ---
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AMARILLO = (255, 255, 0)

# --- ESTADOS DEL JUEGO (Para saber en qué pantalla estamos) ---
MENU = "MENU"           # Pantalla de inicio
JUEGO = "JUEGO"         # El juego en marcha
PAUSA = "PAUSA"         # Juego pausado
GAMEOVER = "GAMEOVER"   # Pantalla de derrota

# --- AJUSTES DE EQUILIBRIO (Dificultad) ---
VELOCIDAD_JUGADOR = 5         # Qué tan rápido se mueve el jugador
VELOCIDAD_ENEMIGO = 3         # Velocidad mínima de los enemigos
VELOCIDAD_BALA = -10          # Qué tan rápido suben los disparos (negativo es hacia arriba)
ENEMIGOS_INICIALES = 3        # Cuántos enemigos aparecen al principio
TIEMPO_APARICION_ENEMIGO = 5000 # Un enemigo nuevo aparece cada 5 segundos (5000 milisegundos)
VIDA_JUGADOR_MAXIMA = 100     # Vida inicial del jugador
DANIO_POR_ENEMIGO = 20        # Cuánta vida quita un enemigo al chocar

# --- EVENTOS PERSONALIZADOS ---
EVENTO_CREAR_ENEMIGO = pygame.USEREVENT + 1  # Evento que dispara el temporizador
