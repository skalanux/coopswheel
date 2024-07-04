import threading
from io import BytesIO

import numpy as np
import matplotlib.pyplot as plt
import pygame

from questions import LABELS, Questions, questions_equivs
pygame.init()
screen_width = 1024
screen_height = 768

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
FIFO_PATH = "gesture"
FORM = 'https://docs.google.com/forms/d/e/1FAIpQLSeQznptrk9y5PC468OhRbMnyO46rObWPWq2kmxB4T38VOn7OQ/viewform?entry.713637523={form}'
# TODO: Agregar sonido de acelerado desaceleado
# Crear preguntas random para las categorias que se respondan con Pulgar arriba o abajo y pantalla
# Aumentar tamaño de la rueda
# Hacer un QR al final para que escaneen y llenen el form de google

def crear_grafico_torta(labels):
    # Número de partes
    plt.rcParams['font.family'] = 'Roboto' 
    num_partes = len(labels)

    # Valores para las partes (iguales entre sí)
    valores = [1] * num_partes
    
    # Generar una lista de colores usando un colormap
    #cmap = plt.get_cmap('tab20')
    cmap = plt.get_cmap('plasma')
    colores = [cmap(i / num_partes) for i in range(num_partes)]
    
    # Crear gráfico de torta
    fig, ax = plt.subplots()
    
    # Ajustar el color de fondo
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    
    # Crear el gráfico de torta
    wedges, texts = ax.pie(valores, labels=None, colors=colores, startangle=90)
    
    # Ajustar las etiquetas para que estén en el centro de cada sección
    for i, wedge in enumerate(wedges):
        angle = (wedge.theta2 - wedge.theta1) / 2.0 + wedge.theta1
        x = 0.5 * np.cos(np.radians(angle))
        y = 0.5 * np.sin(np.radians(angle))
        
        # Rotar el ángulo para que el texto se alinee con el segmento
        rotation = angle if angle < 180 else angle - 180
        
        # Añadir el texto en la posición calculada desde el centro
        ax.text(x, y, labels[i], ha='center', va='center', rotation=rotation, rotation_mode='anchor', color='white')

    # Asegurar que el gráfico sea un círculo
    ax.axis('equal')
    
    # Guardar el gráfico en un stream en memoria
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return buf


def rotate_wheel(surf, image, pos, originPos, angle):
    # offset from pivot to center
    image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    
    # roatated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    # roatetd image center
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)

    # rotate and blit the image
    surf.blit(rotated_image, rotated_image_rect)


def fifo_reader():
    global spinning
    global playing
    while True:
        with open(FIFO_PATH, 'r') as fifo:
            while True:
                data = fifo.read()
                if data[-1:] == "O":
                    playing = True
                    spinning = True
                elif data[-1:] == "V":
                    reset()
                elif data[-1:] == "X":
                    spinning = False

def reset():
    global spinning
    global question_showing
    global speed
    global angle
    global playing
    playing = False
    spinning = False
    question_showing = False
    speed = 0
    angle = 0

def show_question(angle):
    print(angle)
    # Pregunta
    # Colores
    white = (255, 255, 255)
    black = (0, 0, 0)
    screen.fill((black))

    # Fuente y tamaño del texto
    font = pygame.font.Font(None, 74)

    label_chosen = 'Cooperativismo'
    category = questions_equivs.get(label_chosen)
    questions = getattr(Questions, category).value

    message = f'Elegiste {label_chosen}'
    text = font.render(message, True, white)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 100))
    screen.blit(text, text_rect)
    
    pygame.display.flip()
    pygame.time.wait(2000)

    screen.fill((black))
    question = questions[0]

    # Cargar imágenes de los pulgares
    thumbs_up = pygame.image.load("thumbs_up.png")
    thumbs_down = pygame.image.load("thumbs_down.png")

    # Redimensionar imágenes
    thumbs_up = pygame.transform.scale(thumbs_up, (100, 100))
    thumbs_down = pygame.transform.scale(thumbs_down, (100, 100))

    # Posiciones de las imágenes
    thumbs_up_rect = thumbs_up.get_rect(center=(screen_width // 2 - 100, screen_height // 2 + 100))
    thumbs_down_rect = thumbs_down.get_rect(center=(screen_width // 2 + 100, screen_height // 2 + 100))

    # Renderizar el texto de la pregunta
    text = font.render(question[0], True, white)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 100))

    # Dibujar el texto y las imágenes en la pantalla
    screen.blit(text, text_rect)
    screen.blit(thumbs_up, thumbs_up_rect)
    screen.blit(thumbs_down, thumbs_down_rect)

    # Actualizar la pantalla
    pygame.display.flip()
    with open(FIFO_PATH, 'r') as fifo:
        done = False
        while not done:
            data = fifo.read()
            print(data)
            



if __name__ == "__main__":
    angle = 0
    speed = 1
    # Crear gráfico de torta
    buf = crear_grafico_torta(LABELS)

    try:
        image = pygame.image.load(buf)
    except:
        text = pygame.font.SysFont('Roboto', 50).render('image', False, (255, 255, 0))
        image = pygame.Surface((text.get_width()+1, text.get_height()+1))
        image.blit(text, (1, 1))

    w, h = image.get_size()

    # Iniciar el hilo de lectura del FIFO
    fifo_thread = threading.Thread(target=fifo_reader)
    fifo_thread.daemon = True
    fifo_thread.start()

    running = True
    spinning = False
    question_showing = False
    playing = False

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        pos = (screen.get_width()/2, screen.get_height()/2)
        
        screen.fill(0)
        rotate_wheel(screen, image, pos, (w/2, h/2), angle)
        if playing:
            if spinning:
                angle -= 1 * speed
                speed += 0.05
            else:
                if speed > 0.01:
                    speed -= speed/100
                else:
                    speed = 0
                    if not question_showing:
                        question_showing = True
                        show_question(angle)

                angle -= 1 * speed

        if not question_showing:
            pygame.draw.line(screen, (222, 255, 0), (pos[0], pos[1]-180), (pos[0], pos[1]-150), 3)
            pygame.display.flip()
        else:
            ...
    pygame.quit()
    exit()
