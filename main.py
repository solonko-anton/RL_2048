import asyncio
import platform
import pygame
import random
from sprite import Sprite

class Game:
    def __init__(self, width=600, height=600, tile_size=150):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.screen = None
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0
        self.sprites_list = pygame.sprite.Group()
        self.slots = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
    
    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("2048 Game")
    
    def spawn_sprite(self, number):
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
            self.running = False

    def move_left(self):
        for i in range(len(self.slots)):
            for k in range(1, len(self.slots[i])):
                if self.slots[i][-k-1] != self.slots[i][-k] and self.slots[i][-k] > 0 and self.slots[i][-k-1] > 0:
                    continue
                elif self.slots[i][-k-1] == self.slots[i][-k] and self.slots[i][-k] > 0:
                    self.slots[i][-k-1] *= 2
                    self.score += self.slots[i][-k-1]
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

    def move_right(self):
        for i in range(len(self.slots)):
            for k in range(0, len(self.slots[i]) - 1):
                if self.slots[i][k+1] != self.slots[i][k] and self.slots[i][k] > 0 and self.slots[i][k+1] > 0:
                    continue
                elif self.slots[i][k+1] == self.slots[i][k] and self.slots[i][k] > 0:
                    self.slots[i][k+1] *= 2
                    self.score += self.slots[i][k+1]
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

    def move_up(self):
        for i in range(len(self.slots) - 1):
            for k in range(0, len(self.slots[i])):
                if self.slots[i][k] != self.slots[i+1][k] and self.slots[i+1][k] > 0 and self.slots[i][k] > 0:
                    continue
                elif self.slots[i+1][k] == self.slots[i][k] and self.slots[i][k] > 0:
                    self.slots[i][k] *= 2
                    self.score += self.slots[i][k]
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

    def move_down(self):
        for i in range(len(self.slots) - 1, 0, -1):
            for k in range(0, len(self.slots[i])):
                if self.slots[i][k] != self.slots[i-1][k] and self.slots[i-1][k] > 0 and self.slots[i][k] > 0:
                    continue
                elif self.slots[i-1][k] == self.slots[i][k] and self.slots[i][k] > 0:
                    self.slots[i][k] *= 2
                    self.score += self.slots[i][k]
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

    def update(self):
        self.sprites_list.update()
        self.screen.fill("white")
        self.sprites_list.draw(self.screen)
        pygame.display.flip()

    async def run(self):
        self.init_pygame()
        self.spawn_sprite(2)  # Initial tile
        self.spawn_sprite(2)  # Second initial tile

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_left()
                        self.spawn_sprite(2)
                    elif event.key == pygame.K_RIGHT:
                        self.move_right()
                        self.spawn_sprite(2)
                    elif event.key == pygame.K_UP:
                        self.move_up()
                        self.spawn_sprite(2)
                    elif event.key == pygame.K_DOWN:
                        self.move_down()
                        self.spawn_sprite(2)

            self.update()
            self.clock.tick(5)
            await asyncio.sleep(1.0 / 5)

        pygame.quit()

async def main():
    game = Game()
    await game.run()

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())