import os
import pygame
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

# Configuración de la ruleta
CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 200

# Cargar la imagen de la ruleta
image = pygame.image.load('airplane.png')
image = pygame.transform.scale(image, (2 * RADIUS, 2 * RADIUS))

# FIFO
FIFO_PATH = "gesture"

# Crear el FIFO si no existe
if not os.path.exists(FIFO_PATH):
    os.mkfifo(FIFO_PATH)

# Función para dibujar la imagen rotada
def draw_rotated_image(angle):
    screen.fill(WHITE)
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=CENTER).center)
    screen.blit(rotated_image, new_rect.topleft)
    pygame.display.flip()

# Función para girar la ruleta
def spin_wheel():
    global spinning, stop_spinning
    angle = 0
    speed = 10
    while not stop_spinning:
        angle += speed
        speed *= 0.99  # Desacelerar gradualmente
        draw_rotated_image(angle)
        pygame.time.wait(10)
        if speed < 0.1:
            break
    spinning = False
    stop_spinning = False

# Hilo para leer del FIFO
def fifo_reader():
    global spinning, stop_spinning
    while True:
        with open(FIFO_PATH, 'r') as fifo:
            while True:
                data = fifo.read().strip()
                if data == "O" and not spinning:
                    spinning = True
                    stop_spinning = False
                    spin_thread = threading.Thread(target=spin_wheel)
                    spin_thread.start()
                elif data == "V" and spinning:
                    stop_spinning = True

# Iniciar el hilo de lectura del FIFO
fifo_thread = threading.Thread(target=fifo_reader)
fifo_thread.daemon = True
fifo_thread.start()

# Bucle principal de Pygame
running = True
spinning = False
stop_spinning = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not spinning:
     draw_rotated_image(0)

pygame.quit()

