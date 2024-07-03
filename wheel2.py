import pygame

pygame.init()
screen = pygame.display.set_mode((900, 900))
clock = pygame.time.Clock()

def blitRotate(surf, image, pos, originPos, angle):

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
  
    # draw rectangle around the image
    #pygame.draw.rect(surf, (255, 0, 0), (*rotated_image_rect.topleft, *rotated_image.get_size()),2)

def blitRotate2(surf, image, topleft, angle):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect.topleft)
    #pygame.draw.rect(surf, (255, 0, 0), new_rect, 2)

try:
    image = pygame.image.load('airplane.png')
except:
    text = pygame.font.SysFont('Times New Roman', 50).render('image', False, (255, 255, 0))
    image = pygame.Surface((text.get_width()+1, text.get_height()+1))
    #pygame.draw.rect(image, (0, 0, 255), (1, 1, *text.get_size()))
    image.blit(text, (1, 1))
w, h = image.get_size()

FIFO_PATH = "gesture"

import threading
# Hilo para leer del FIFO
def fifo_reader():
    global spinning
    while True:
        with open(FIFO_PATH, 'r') as fifo:
            while True:
                data = fifo.read()
                if "O" in data:
                    spinning = True

angle = 0

def spin_wheel():
    global spinning
    angle = 0
    speed = 10
    while spinning:
        angle += speed
        speed *= 0.99  # Desacelerar gradualmente
        pygame.time.wait(10)
        if speed < 0.1:
            spinning = False

# Iniciar el hilo de lectura del FIFO
fifo_thread = threading.Thread(target=fifo_reader)
fifo_thread.daemon = True
fifo_thread.start()

running = True
spinning = False

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pos = (screen.get_width()/2, screen.get_height()/2)
    
    screen.fill(0)
    blitRotate(screen, image, pos, (w/2, h/2), angle)
    #blitRotate2(screen, image, pos, angle)
    angle += 1
    
    pygame.draw.line(screen, (0, 255, 0), (pos[0]-20, pos[1]), (pos[0]+20, pos[1]), 3)
    pygame.draw.line(screen, (0, 255, 0), (pos[0], pos[1]-20), (pos[0], pos[1]+20), 3)
    pygame.draw.circle(screen, (0, 255, 0), pos, 7, 0)

    if spinning:
        pygame.display.flip()
    
pygame.quit()
exit()
