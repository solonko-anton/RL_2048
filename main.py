import pygame
import random
import numpy as np 
from enum import Enum
from sprite import Sprite

class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

class Game:
    def __init__(self, width=600, height=600, tile_size=150):
        self.reward = 0
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.screen = None
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.running = True
        self.score = 0
        self.sprites_list = pygame.sprite.Group()
        self.slots = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
        self.frame_iterations = 0
        self.init_pygame()
        self.spawn_sprite(2)  
        self.spawn_sprite(2) 

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("2048 Game")
    
    def spawn_sprite(self, number):
        reward = 0
        try:
            object_ = Sprite(self.tile_size, self.tile_size, number)
            free_slots = []

            for i in range(len(self.slots)):
                for k in range(len(self.slots[i])):
                    if self.slots[i][k] == 0:
                        free_slots.append([i, k])
            
            if not free_slots:
                self.running = False
                return
            
            slot_number = random.randint(0, len(free_slots) - 1)
            slot_to_append = free_slots[slot_number]
            x_index, y_index = slot_to_append[1], slot_to_append[0]

            object_.rect.x = x_index * self.tile_size
            object_.rect.y = y_index * self.tile_size

            self.sprites_list.add(object_)
            self.slots[y_index][x_index] = number
        except ValueError:
            reward = -10
            game_over = True
            return reward, game_over

    def move_left(self):
        reward = 0
        for i in range(len(self.slots)):
            for k in range(1, len(self.slots[i])):
                if self.slots[i][-k-1] != self.slots[i][-k] and self.slots[i][-k] > 0 and self.slots[i][-k-1] > 0:
                    continue
                elif self.slots[i][-k-1] == self.slots[i][-k] and self.slots[i][-k] > 0:
                    self.slots[i][-k-1] *= 2
                    self.score += self.slots[i][-k-1]
                    reward += self.slots[i][-k-1]
                    self.slots[i][-k] = 0

                    x1 = (len(self.slots[i]) - abs(-k)) * self.tile_size
                    x2 = (len(self.slots[i]) - abs(-k-1)) * self.tile_size
                    y = i * self.tile_size

                    for s in self.sprites_list:
                        if s.rect.x == x1 and s.rect.y == y:
                            self.sprites_list.remove(s)
                        elif s.rect.x == x2 and s.rect.y == y:
                            new_sprite = Sprite(self.tile_size, self.tile_size, self.slots[i][-k-1])
                            new_sprite.rect.x = x2
                            new_sprite.rect.y = y
                            self.sprites_list.add(new_sprite)
                elif self.slots[i][-k-1] == 0 and self.slots[i][-k] > 0:
                    self.slots[i][-k-1] = self.slots[i][-k]
                    self.slots[i][-k] = 0

                    x1 = (len(self.slots[i]) - abs(-k)) * self.tile_size
                    x2 = (len(self.slots[i]) - abs(-k-1)) * self.tile_size
                    y = i * self.tile_size

                    for s in self.sprites_list:
                        if s.rect.x == x1 and s.rect.y == y:
                            s.number = self.slots[i][-k-1]
                            s.rect.x -= self.tile_size
        return reward

    def move_right(self):
        reward = 0
        for i in range(len(self.slots)):
            for k in range(0, len(self.slots[i]) - 1):
                if self.slots[i][k+1] != self.slots[i][k] and self.slots[i][k] > 0 and self.slots[i][k+1] > 0:
                    continue
                elif self.slots[i][k+1] == self.slots[i][k] and self.slots[i][k] > 0:
                    self.slots[i][k+1] *= 2
                    self.score += self.slots[i][k+1]
                    reward += 10
                    self.slots[i][k] = 0

                    x1 = k * self.tile_size
                    x2 = (k+1) * self.tile_size
                    y = i * self.tile_size

                    for s in self.sprites_list:
                        if s.rect.x == x1 and s.rect.y == y:
                            self.sprites_list.remove(s)
                        elif s.rect.x == x2 and s.rect.y == y:
                            new_sprite = Sprite(self.tile_size, self.tile_size, self.slots[i][k+1])
                            new_sprite.rect.x = x2
                            new_sprite.rect.y = y
                            self.sprites_list.add(new_sprite)
                elif self.slots[i][k+1] == 0 and self.slots[i][k] > 0:
                    self.slots[i][k+1] = self.slots[i][k]
                    self.slots[i][k] = 0

                    x1 = k * self.tile_size
                    x2 = (k+1) * self.tile_size
                    y = i * self.tile_size

                    for s in self.sprites_list:
                        if s.rect.x == x1 and s.rect.y == y:
                            s.number = self.slots[i][k+1]
                            s.rect.x += self.tile_size
        return reward

    def move_up(self):
        reward = 0
        for i in range(len(self.slots) - 1):
            for k in range(0, len(self.slots[i])):
                if self.slots[i][k] != self.slots[i+1][k] and self.slots[i+1][k] > 0 and self.slots[i][k] > 0:
                    continue
                elif self.slots[i+1][k] == self.slots[i][k] and self.slots[i][k] > 0:
                    self.slots[i][k] *= 2
                    self.score += self.slots[i][k]
                    reward += 10
                    self.slots[i+1][k] = 0

                    x = k * self.tile_size
                    y1 = i * self.tile_size
                    y2 = (i+1) * self.tile_size

                    for s in self.sprites_list:
                        if s.rect.x == x and s.rect.y == y2:
                            self.sprites_list.remove(s)
                        elif s.rect.x == x and s.rect.y == y1:
                            new_sprite = Sprite(self.tile_size, self.tile_size, self.slots[i][k])
                            new_sprite.rect.x = x
                            new_sprite.rect.y = y1
                            self.sprites_list.add(new_sprite)
                elif self.slots[i][k] == 0 and self.slots[i+1][k] > 0:
                    self.slots[i][k] = self.slots[i+1][k]
                    self.slots[i+1][k] = 0

                    x = k * self.tile_size
                    y1 = i * self.tile_size
                    y2 = (i+1) * self.tile_size

                    for s in self.sprites_list:
                        if s.rect.x == x and s.rect.y == y2:
                            s.number = self.slots[i][k]
                            s.rect.y -= self.tile_size
        return reward

    def move_down(self):
        reward = 0
        for i in range(len(self.slots) - 1, 0, -1):
            for k in range(0, len(self.slots[i])):
                if self.slots[i][k] != self.slots[i-1][k] and self.slots[i-1][k] > 0 and self.slots[i][k] > 0:
                    continue
                elif self.slots[i-1][k] == self.slots[i][k] and self.slots[i][k] > 0:
                    self.slots[i][k] *= 2
                    self.score += self.slots[i][k]
                    reward += 10
                    self.slots[i-1][k] = 0

                    x = k * self.tile_size
                    y1 = (i-1) * self.tile_size
                    y2 = i * self.tile_size

                    for s in self.sprites_list:
                        if s.rect.x == x and s.rect.y == y1:
                            self.sprites_list.remove(s)
                        elif s.rect.x == x and s.rect.y == y2:
                            new_sprite = Sprite(self.tile_size, self.tile_size, self.slots[i][k])
                            new_sprite.rect.x = x
                            new_sprite.rect.y = y2
                            self.sprites_list.add(new_sprite)
                elif self.slots[i][k] == 0 and self.slots[i-1][k] > 0:
                    self.slots[i][k] = self.slots[i-1][k]
                    self.slots[i-1][k] = 0

                    x = k * self.tile_size
                    y1 = (i-1) * self.tile_size
                    y2 = i * self.tile_size

                    for s in self.sprites_list:
                        if s.rect.x == x and s.rect.y == y1:
                            s.number = self.slots[i][k]
                            s.rect.y += self.tile_size
        return reward

    def update(self):
        self.sprites_list.update()
        self.screen.fill("white")
        self.sprites_list.draw(self.screen)
        pygame.display.flip()

    def play_step(self, action: list[int]):
        reward = 0
        game_over = False
        self.frame_iterations += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self.direction = [0, 0, 0, 0]

        if np.array_equal(action, [1, 0, 0, 0]):
            self.direction = Direction.LEFT
        elif np.array_equal(action, [0, 1, 0, 0]):
            self.direction = Direction.RIGHT
        elif np.array_equal(action, [0, 0, 1, 0]):
            self.direction ==Direction.UP
        else:
            self.direction ==Direction.DOWN

        if self.direction == Direction.LEFT:
            self.move_left()
            reward, game_over = self.spawn_sprite(2)
        elif self.direction == Direction.RIGHT:
            self.move_right()
            reward, game_over = self.spawn_sprite(2)
        elif self.direction == Direction.UP:
            self.move_up()
            reward, game_over = self.spawn_sprite(2)
        elif self.direction == Direction.DOWN:
            self.move_down()
            reward, game_over = self.spawn_sprite(2)

        self.update()

        return reward, game_over, self.score
