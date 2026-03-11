import pygame
import random
import sys

# --- CONFIGURACIÓN INICIAL ---
pygame.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego del Ahorcado - Versión Sencilla")

# Colores y Fuente
BLANCO = (255, 255, 255)
NEGRO = (30, 30, 30)
ROJO = (231, 76, 60)
VERDE = (46, 204, 113)
GRIS = (100, 100, 100)

FUENTE = pygame.font.SysFont("Arial", 40)

def main():
    # 1. Configuración de la partida
    palabras = ["PYTHON", "AHORCADO", "CODIGO", "JUEGO", "SISTEMA", "TECLADO"]
    secreta = random.choice(palabras)
    
    adivinadas = []
    usadas = []
    fallos = 0
    
    reloj = pygame.time.Clock()
    terminado = False

    # --- BUCLE DEL JUEGO ---
    while True:
        pantalla.fill(BLANCO)
        
        # 2. Gestión de Entradas (Teclado y Ventana)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.KEYDOWN:
                # Si el juego terminó, pulsar cualquier tecla reinicia la partida
                if terminado:
                    main()
                
                # Capturamos la letra pulsada
                letra = pygame.key.name(evento.key).upper()
                
                # Validamos que sea una letra y no se haya usado antes
                if len(letra) == 1 and letra.isalpha() and letra not in usadas:
                    usadas.append(letra)
                    if letra in secreta:
                        adivinadas.append(letra)
                    else:
                        fallos += 1

        # 3. Dibujar la Horca y el Personaje
        # Estructura de la horca (líneas negras)
        pygame.draw.line(pantalla, NEGRO, (100, 500), (300, 500), 5) # Base
        pygame.draw.line(pantalla, NEGRO, (200, 500), (200, 100), 5) # Poste vertical
        pygame.draw.line(pantalla, NEGRO, (200, 100), (400, 100), 5) # Poste horizontal
        pygame.draw.line(pantalla, NEGRO, (400, 100), (400, 150), 5) # Cuerda

        # Dibujo del personaje según el número de fallos
        if fallos >= 1: pygame.draw.circle(pantalla, NEGRO, (400, 180), 30, 5) # Cabeza
        if fallos >= 2: pygame.draw.line(pantalla, NEGRO, (400, 210), (400, 350), 5) # Cuerpo
        if fallos >= 3: pygame.draw.line(pantalla, NEGRO, (400, 240), (350, 300), 5) # Brazo Izquierdo
        if fallos >= 4: pygame.draw.line(pantalla, NEGRO, (400, 240), (450, 300), 5) # Brazo Derecho
        if fallos >= 5: pygame.draw.line(pantalla, NEGRO, (400, 350), (350, 420), 5) # Pierna Izquierda
        if fallos >= 6: pygame.draw.line(pantalla, NEGRO, (400, 350), (450, 420), 5) # Pierna Derecha

        # 4. Mostrar Palabra Oculta y Estado
        # Creamos la cadena con guiones y letras adivinadas
        guiones = " ".join([l if l in adivinadas else "_" for l in secreta])
        
        txt_palabra = FUENTE.render(guiones, True, NEGRO)
        pantalla.blit(txt_palabra, (450, 200))
        
        txt_usadas = FUENTE.render(f"Usadas: {' '.join(usadas)}", True, GRIS)
        pantalla.blit(txt_usadas, (450, 300))
        
        # El contador de fallos se pone rojo si quedan pocos intentos
        color_fallos = ROJO if fallos >= 5 else NEGRO
        txt_intentos = FUENTE.render(f"Fallos: {fallos}/6", True, color_fallos)
        pantalla.blit(txt_intentos, (450, 400))

        # 5. Comprobar Victoria o Derrota
        if "_" not in guiones:
            msg = FUENTE.render("¡GANASTE! Pulsa para reiniciar", True, VERDE)
            pantalla.blit(msg, (200, 530))
            terminado = True
            
        elif fallos >= 6:
            msg = FUENTE.render(f"PERDISTE. Era: {secreta}. ¿Reiniciar?", True, ROJO)
            pantalla.blit(msg, (150, 530))
            terminado = True

        # Actualizar pantalla
        pygame.display.flip()
        reloj.tick(30)

if __name__ == "__main__":
    main()
