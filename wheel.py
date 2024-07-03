import os
import pygame
import math
import threading

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ruleta de Categorías")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), 
          (0, 255, 255), (128, 0, 128), (255, 165, 0), (0, 128, 128), (128, 128, 0)]

# Categorías
CATEGORIES = ["Categoría 1", "Categoría 2", "Categoría 3", "Categoría 4", "Categoría 5",
              "Categoría 6", "Categoría 7", "Categoría 8", "Categoría 9", "Categoría 10"]

# Configuración de la ruleta
CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 200

# FIFO
FIFO_PATH = "gesture"

# Crear el FIFO si no existe
if not os.path.exists(FIFO_PATH):
    os.mkfifo(FIFO_PATH)

# Función para dibujar la ruleta
def draw_wheel(angle):
    screen.fill(WHITE)
    num_categories = len(CATEGORIES)
    angle_step = 360 / num_categories

    for i in range(num_categories):
        start_angle = math.radians(i * angle_step + angle)
        end_angle = math.radians((i + 1) * angle_step + angle)
        color = COLORS[i % len(COLORS)]
        
        # Dibujar segmento de la ruleta
        pygame.draw.arc(screen, color, (CENTER[0] - RADIUS, CENTER[1] - RADIUS, 2 * RADIUS, 2 * RADIUS), start_angle, end_angle, RADIUS)

        # Dibujar líneas de los segmentos
        pygame.draw.line(screen, BLACK, CENTER, (CENTER[0] + RADIUS * math.cos(start_angle), CENTER[1] + RADIUS * math.sin(start_angle)), 2)

        # Dibujar texto
        text_angle = math.radians((i + 0.5) * angle_step + angle)
        text_x = CENTER[0] + RADIUS // 1.5 * math.cos(text_angle)
        text_y = CENTER[1] + RADIUS // 1.5 * math.sin(text_angle)
        font = pygame.font.Font(None, 30)
        text = font.render(CATEGORIES[i], True, BLACK)
        text_rect = text.get_rect(center=(text_x, text_y))
        screen.blit(text, text_rect)

    pygame.display.flip()

# Función para girar la ruleta
def spin_wheel():
    global spinning
    angle = 0
    speed = 10
    while spinning:
        angle += speed
        speed *= 0.99  # Desacelerar gradualmente
        draw_wheel(angle)
        pygame.time.wait(10)
        if speed < 0.1:
            spinning = False

# Hilo para leer del FIFO
def fifo_reader():
    global spinning
    while True:
        with open(FIFO_PATH, 'r') as fifo:
            while True:
                data = fifo.read()
                if "O" in data:
                    spinning = True
                    spin_thread = threading.Thread(target=spin_wheel)
                    spin_thread.start()

# Iniciar el hilo de lectura del FIFO
fifo_thread = threading.Thread(target=fifo_reader)
fifo_thread.daemon = True
fifo_thread.start()

# Bucle principal de Pygame
running = True
spinning = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_wheel(0)

pygame.quit()

