import pygame
import random
import copy
from sprite import Sprite

WIDTH = 600
HEIGHT = 600

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
score = 0
sprites_list = pygame.sprite.Group()
slots = [
    [0, 0, 0 ,0],
    [0, 0, 0 ,0],
    [0, 0, 0 ,0],
    [0, 0, 0 ,0],
]

def spawn_sprite(number, w=150, h=150, x=None, y=None):
    try:
        object_ = Sprite(w, h, number)

        free_slots = []

        l = len(slots)

        for i in range(l):
            for k in range(len(slots[i])):
                if slots[i][k] == 0:
                    free_slots.append([i, k])
        slot_number = random.randint(0, len(free_slots) - 1)

        slot_to_append = free_slots[slot_number]

        x_index = slot_to_append[1]  
        y_index = slot_to_append[0]

        object_.rect.x = x_index * w
        object_.rect.y = y_index * h

        sprites_list.add(object_)
        slots[y_index][x_index] = number 
    except ValueError as e:
        global running
        running = False

def move_left():
    slot_len = len(slots)
    for i in range(slot_len):
        for k in range(1, len(slots[i])):
            if slots[i][-k-1] != slots[i][-k] and slots[i][-k] > 0 and slots[i][-k-1] > 0:
                continue   
            elif slots[i][-k-1] == slots[i][-k] and slots[i][-k] > 0:
                slots[i][-k-1] *= 2
                slots[i][-k] = 0

                x1 = (len(slots[i]) - abs(-k)) * 150
                x2 = (len(slots[i]) - abs(-k-1)) * 150 
                y = i * 150

                for s in sprites_list:
                    if s.rect.x == x1 and s.rect.y == y:
                        sprites_list.remove(s)
                    elif s.rect.x == x2 and s.rect.y == y:
                        new_sprite = Sprite(150, 150, slots[i][-k-1])
                        new_sprite.rect.x = x2
                        new_sprite.rect.y = y
                        sprites_list.add(new_sprite) 
                break

            elif slots[i][-k-1] == 0 and slots[i][-k] > 0:
                slots[i][-k-1] = slots[i][-k]
                slots[i][-k] = 0

                x1 = (len(slots[i]) - abs(-k)) * 150
                x2 = (len(slots[i]) - abs(-k-1)) * 150 
                y = i * 150
                
                for s in sprites_list:
                    if s.rect.x == x1 and s.rect.y == y:
                       s.number = slots[i][-k]
                       s.rect.x -= 150 
                    elif s.rect.x == x2 and s.rect.y == y:
                        s.number = slots[i][-k-1]
                        s.rect.x += 150 

def move_right():
    slot_len = len(slots)
    for i in range(slot_len):
        for k in range(0, len(slots[i]) - 1):
            if slots[i][k+1] != slots[i][k] and slots[i][k] > 0 and slots[i][k+1] > 0:
                continue   
            elif slots[i][k+1] == slots[i][k] and slots[i][k] > 0:
                slots[i][k+1] *= 2
                slots[i][k] = 0

                x1 = k * 150
                x2 = (k+1) * 150 
                y = i * 150

                for s in sprites_list:
                    if s.rect.x == x1 and s.rect.y == y:
                        sprites_list.remove(s)
                    elif s.rect.x == x2 and s.rect.y == y:
                        new_sprite = Sprite(150, 150, slots[i][k+1])
                        new_sprite.rect.x = x2
                        new_sprite.rect.y = y
                        sprites_list.add(new_sprite) 
                break

            elif slots[i][k+1] == 0 and slots[i][+k] > 0:
                slots[i][k+1] = slots[i][k]
                slots[i][k] = 0

                x1 = k * 150
                x2 = k+1 * 150 
                y = i * 150
                
                for s in sprites_list:
                    if s.rect.x == x1 and s.rect.y == y:
                       s.number = slots[i][k]
                       s.rect.x += 150 
                    elif s.rect.x == x2 and s.rect.y == y:
                        s.number = slots[i][k+1]
                        s.rect.x -= 150 

def move_up():
    slot_len = len(slots) - 1
    for i in range(slot_len):
        for k in range(0, len(slots[i])):
            if slots[i][k] != slots[i+1][k] and slots[i+1][k] > 0 and slots[i][k] > 0:
                continue   
            elif slots[i+1][k] == slots[i][k] and slots[i][k] > 0:
                slots[i][k] *= 2
                slots[i+1][k] = 0

                x = k * 150 
                y1 = i * 150
                y2 = (i+1) * 150

                for s in sprites_list:
                    if s.rect.x == x and s.rect.y == y2:
                        sprites_list.remove(s)
                    elif s.rect.x == x and s.rect.y == y1:
                        new_sprite = Sprite(150, 150, slots[i][k])
                        new_sprite.rect.x = x
                        new_sprite.rect.y = y1
                        sprites_list.add(new_sprite) 

            elif slots[i][k] == 0 and slots[i+1][k] > 0:
                slots[i][k] = slots[i+1][k]
                slots[i+1][k] = 0

                x = k * 150 
                y1 = i * 150
                y2 = (i+1) * 150

                for s in sprites_list:
                    if s.rect.x == x and s.rect.y == y1:
                       s.number = slots[i+1][k]
                       s.rect.y += 150 
                    elif s.rect.x == x and s.rect.y == y2:
                        s.number = slots[i][k]
                        s.rect.y -= 150 

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left()
                spawn_sprite(2)
                print(slots)
            elif event.key == pygame.K_RIGHT:
                move_right()
                spawn_sprite(2)
                print(slots)
            elif event.key == pygame.K_UP:
                move_up()
                spawn_sprite(2)
                print(slots)
            elif event.key == pygame.K_DOWN:
                spawn_sprite(2)


    sprites_list.update()
    screen.fill("white")
    sprites_list.draw(screen)

    pygame.display.flip()

    clock.tick(5)  

pygame.quit()