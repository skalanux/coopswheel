import random
import threading
from io import BytesIO
from decimal import Decimal, ROUND_DOWN
from datetime import datetime
import hashlib
import base64

import numpy as np
import matplotlib.pyplot as plt
import pygame
import qrcode

from questions import LABELS, Questions, questions_equivs

pygame.init()
pygame.mixer.init()

CUSTOM_FONT = 'poppins.ttf'

# Cargar el sonido de fondo
ding_sound = pygame.mixer.Sound('ding.mp3')

screen_width = 1920
screen_height = 1080

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
FIFO_PATH = "gesture"
FORM = 'https://docs.google.com/forms/d/e/1FAIpQLSeQznptrk9y5PC468OhRbMnyO46rObWPWq2kmxB4T38VOn7OQ/viewform?entry.713637523={entry}'
COLOR_INDIGO = (186,29,122)
COLOR_WHITE = (255,255,255)
# TODO: Agregar sonido de acelerado desacelerando
# Hacer un R al final para que escaneen y llenen el form de google

def hash_number_with_salt(number, salt):
    # Convertir el número a una cadena de bytes
    salted_number = (str(number)+salt).encode('utf-8')

    # Crear el hash SHA-256
    hash_object = hashlib.sha256(salted_number)
    hash_digest = hash_object.digest()

    # Codificar el hash en base64 para obtener una cadena de letras
    hash_base64 = base64.urlsafe_b64encode(hash_digest).decode('utf-8')

    return hash_base64

def crear_grafico_torta(labels):
    # Número de partes
    from matplotlib import font_manager
    font_manager.fontManager.addfont(CUSTOM_FONT)
    plt.rcParams['font.family'] = 'Poppins' 
    plt.rcParams['font.size'] = 24 
    num_partes = len(labels)

    # Valores para las partes (iguales entre sí)
    valores = [1] * num_partes
    
    # Generar una lista de colores usando un colormap
    #cmap = plt.get_cmap('tab20')
    cmap = plt.get_cmap('plasma')
    colores = [cmap(i / num_partes) for i in range(num_partes)]
    
    # Crear gráfico de torta
    fig, ax = plt.subplots(figsize=(10,10))
    
    # Ajustar el color de fondo
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    
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

def show_qr():
    # Crear el código QR
    entry = datetime.now().timestamp()
    entry = hash_number_with_salt(int(entry), 'saraza')
    qr_data = FORM.format(entry=entry)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=4,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    # Convertir el QR a una imagen
    qr_image = qr.make_image(fill='black', back_color='white')

    # Guardar la imagen en un buffer
    buffer = BytesIO()
    qr_image.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

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
    global question_pending
    global current_answer

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
                elif data[-1:] == "U":
                    current_answer = True
                    question_pending = False
                elif data[-1:] == "D":
                    current_answer = False
                    question_pending = False
                 

def reset():
    global spinning
    global question_showing
    global speed
    global angle
    global playing
    global current_question
    global current_answer
    global question_pending
    playing = False
    spinning = False
    question_showing = False
    question_pending = False
    current_answer = None
    current_question = None
    speed = 0
    angle = 0
    
def show_result(answer):
    # Pregunta
    # Colores
    global question_pending
    global current_question

    white = (255, 255, 255)
    black = (0, 0, 0)
    screen.fill((COLOR_INDIGO))

    # Fuente y tamaño del texto
    font = pygame.font.Font(CUSTOM_FONT, 74)

    response = 'Sí' if answer else 'No' 

    message = f'Contestaste que {response} y ...'
    text = font.render(message, True, white)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 100))
    screen.blit(text, text_rect)
    
    pygame.display.flip()

    pygame.time.wait(2000)

    screen.fill((COLOR_INDIGO))
    correct_answer = current_question[1]
    font = pygame.font.Font(CUSTOM_FONT, 49)
    if correct_answer == answer:
        win = True
        message = 'Ganaste :)'
    else:
        win = False
        message = f'Perdiste :( ... Seguí participando'

    text = font.render(message, True, white)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 150))

    screen.blit(text, text_rect)

    if win:
        message = '¡Escaneá el qr para participar del sorteo!'
        text = font.render(message, True, white)
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 80))
        screen.blit(text, text_rect)

        image_rect = text.get_rect(center=((screen_width // 2) + 370, screen_height // 2 + 20))
        buf = show_qr()
        image = pygame.image.load(buf)
        screen.blit(image, image_rect)
    
    pygame.display.flip()
    #reset()

def get_label(angle):
    cant_labels = len(LABELS)
    angle_open = 360 // cant_labels
    angle_abs = angle % 360
    index = -1
    for slot in range(0,360,angle_open):
        if angle_abs <= slot:
            break
        else:
            index += 1

    return list(reversed(LABELS))[index]

def show_question(angle):
    # Pregunta
    # Colores
    global question_pending
    global current_question

    question_pending = True
    white = (255, 255, 255)
    black = (0, 0, 0)
    screen.fill((COLOR_INDIGO))

    # Fuente y tamaño del texto
    font = pygame.font.Font(CUSTOM_FONT, 74)

    label_chosen = get_label(angle)
    category = questions_equivs.get(label_chosen)
    questions = getattr(Questions, category).value

    message = f'Elegiste {label_chosen}'
    text = font.render(message, True, white)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 100))
    screen.blit(text, text_rect)
    
    pygame.display.flip()
    pygame.time.wait(2000)

    screen.fill((COLOR_INDIGO))
    question = random.choice(questions)

    current_question = question 
    # Cargar imágenes de los pulgares
    thumbs_up = pygame.image.load("thumbs_up.png")
    thumbs_down = pygame.image.load("thumbs_down.png")

    # Redimensionar imágenes
    thumbs_up = pygame.transform.scale(thumbs_up, (100, 100))
    thumbs_down = pygame.transform.scale(thumbs_down, (100, 100))

    # Posiciones de las imágenes
    thumbs_up_rect = thumbs_up.get_rect(center=(screen_width // 2 - 100, screen_height // 2 + 100))
    thumbs_down_rect = thumbs_down.get_rect(center=(screen_width // 2 + 100, screen_height // 2 + 100))

    font = pygame.font.Font(CUSTOM_FONT, 36)
    # Renderizar el texto de la pregunta
    text = font.render(question[0], True, white)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 100))

    # Dibujar el texto y las imágenes en la pantalla
    screen.blit(text, text_rect)
    screen.blit(thumbs_up, thumbs_up_rect)
    screen.blit(thumbs_down, thumbs_down_rect)

    # Actualizar la pantalla
    pygame.display.flip()



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
    question_pending = False
    playing = False

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        pos = (screen.get_width()/2, screen.get_height()/2)
        
        screen.fill((COLOR_WHITE))
        
        rotate_wheel(screen, image, pos, (w/2, h/2), angle)

        if playing:
            decimal_speed = Decimal(speed)
            truncated_speed = decimal_speed.quantize(Decimal('0.01'), rounding=ROUND_DOWN)
            truncated_speed = truncated_speed - int(truncated_speed)

            if float(truncated_speed) % 0.01 == 0.0 and speed!=0:
                ding_sound.play()

            if spinning:
                angle -= 1 * speed
                speed += 0.05
            else:
                if speed > 0.05:
                    speed -= speed/100
                else:
                    speed = 0

                if speed == 0 and not question_showing and not question_pending:
                    question_showing = True
                    question_pending = True
                    show_question(angle)

                if speed == 0 and question_showing and not question_pending:
                    playing=False
                    show_result(current_answer)
                 
            angle -= 1 * speed

        if not question_showing:
            triangle_height = 50
            triangle_base = 30

            # Coordenadas del centro del triángulo
            center_x = screen_width // 2
            center_y = (screen_height // 2) - 360

            # Puntos del triángulo
            point1 = (center_x, center_y + triangle_height // 2)
            point2 = (center_x - triangle_base // 2, center_y - triangle_height // 2)
            point3 = (center_x + triangle_base // 2, center_y - triangle_height // 2)
            pygame.draw.polygon(screen, COLOR_INDIGO, [point1, point2, point3])
            #pygame.draw.line(screen, (('black')), (pos[0], pos[1]-180), (pos[0], pos[1]-150), 3)
            pygame.display.flip()
        else:
            ...

        # Quit with escape
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

    pygame.quit()
    exit()
