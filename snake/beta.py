import os
import sys
import pygame
import random

pygame.init()
size = width, height = 496, 496
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
score_font = pygame.font.SysFont("comicsansms", 15)
tail = [[240, 240]]
way = 'none'
all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
flag = True
speed = 0


def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

f = load_image('screen.jpg')


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗМЕЙКА", "",
                  "Выберите скорость", "",
                  "Для этого нажмите на нужную цифру от 1 до 4"]
    fon = pygame.transform.scale(load_image('screen.jpg'), (496, 496))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return event
                if event.key == pygame.K_2:
                    return event
                if event.key == pygame.K_3:
                    return event
                if event.key == pygame.K_4:
                    return event
        pygame.display.flip()
        clock.tick(100)


def death_screen(score):
    intro_text = ["Игра окончена", "",
                  f"Ваш счет: {score}", "",
                  "Чтобы выйти, нажмите Q"]
    fon = pygame.transform.scale(load_image('screen.jpg'), (496, 496))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
        pygame.display.flip()
        clock.tick(100)


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Head(pygame.sprite.Sprite):
    head_up = load_image("head_up.png")
    head_down = load_image("head_down.png")
    head_left = load_image("head_left.png")
    head_right = load_image("head_right.png")

    def __init__(self, group):
        super().__init__(group)
        self.image = Head.head_up
        self.rect = self.image.get_rect()
        self.rect.x = 240
        self.rect.y = 240
        self.update_x = 0
        self.update_y = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.way = way
        self.speed = speed

    def update(self, *args):
        clock.tick(args[-1])
        if args[0].type == pygame.KEYDOWN:
            if args and args[0].key == pygame.K_DOWN:
                self.image = self.head_down
                self.update_x = 0
                self.update_y = 16
                self.way = 'down'
            if args and args[0].key == pygame.K_UP:
                self.image = self.head_up
                self.update_x = 0
                self.update_y = -16
                self.way = 'up'
            if args and args[0].key == pygame.K_LEFT:
                self.image = self.head_left
                self.update_x = -16
                self.update_y = 0
                self.way = 'left'
            if args and args[0].key == pygame.K_RIGHT:
                self.image = self.head_right
                self.update_x = 16
                self.update_y = 0
                self.way = 'right'
        self.rect.x += self.update_x
        self.rect.y += self.update_y
        self.way = way
        for i in range(len(tail) - 1, 0, -1):
            tail[i] = tail[i - 1]
        tail[0] = [self.rect.x, self.rect.y]
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            death_screen(rabbit.score)
        if pygame.sprite.spritecollideany(self, vertical_borders):
            death_screen(rabbit.score)


class Tail(pygame.sprite.Sprite):
    tail_up = load_image("tail_up.png")
    tail_down = load_image("tail_down.png")
    tail_left = load_image("tail_left.png")
    tail_right = load_image("tail_right.png")

    def __init__(self, group):
        super().__init__(group)
        self.image = Tail.tail_up
        self.rect = self.image.get_rect()
        self.rect.x = -100
        self.rect.y = -100
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args):
        if len(tail) > 1:
            if tail[-1][0] - 16 == tail[-2][0]:
                self.image = Tail.tail_left
            elif tail[-1][0] + 16 == tail[-2][0]:
                self.image = Tail.tail_right
            elif tail[-1][1] + 16 == tail[-2][1]:
                self.image = Tail.tail_down
            else:
                self.image = Tail.tail_up
            self.rect.x = tail[-1][0]
            self.rect.y = tail[-1][1]
        if pygame.sprite.collide_mask(self, head):
            death_screen(rabbit.score)



class Body(pygame.sprite.Sprite):
    body_vert = load_image("body_vert.png")
    body_hor = load_image("body_hor.png")
    turn_ld = load_image("turn_ld.png")
    turn_rd = load_image("turn_rd.png")
    turn_lu = load_image("turn_lu.png")
    turn_ru = load_image("turn_ru.png")

    def __init__(self, group, i):
        super().__init__(group)
        self.image = Body.body_vert
        self.rect = self.image.get_rect()
        self.rect.x = -200
        self.rect.y = -100
        self.mask = pygame.mask.from_surface(self.image)
        self.i = i

    def update(self, *args):
        if ((tail[self.i - 1][0] - 16 == tail[self.i][0] == tail[self.i + 1][0] + 16) or
                (tail[self.i - 1][0] + 16 == tail[self.i][0] == tail[self.i + 1][0] - 16)):
            self.image = Body.body_hor
        elif ((tail[self.i - 1][1] - 16 == tail[self.i][1] == tail[self.i + 1][1] + 16) or
              (tail[self.i - 1][1] + 16 == tail[self.i][1] == tail[self.i + 1][1] - 16)):
            self.image = Body.body_vert
        elif ((tail[self.i - 1][0] - 16 == tail[self.i][0] and tail[self.i + 1][1] - 16 == tail[self.i][1]) or
              (tail[self.i + 1][0] - 16 == tail[self.i][0] and tail[self.i - 1][1] - 16 == tail[self.i][1])):
            self.image = Body.turn_rd
        elif ((tail[self.i - 1][0] + 16 == tail[self.i][0] and tail[self.i + 1][1] - 16 == tail[self.i][1]) or
              (tail[self.i + 1][0] + 16 == tail[self.i][0] and tail[self.i - 1][1] - 16 == tail[self.i][1])):
            self.image = Body.turn_ld
        elif ((tail[self.i - 1][0] - 16 == tail[self.i][0] and tail[self.i + 1][1] + 16 == tail[self.i][1]) or
              (tail[self.i + 1][0] - 16 == tail[self.i][0] and tail[self.i - 1][1] + 16 == tail[self.i][1])):
            self.image = Body.turn_ru
        else:
            self.image = Body.turn_lu
        self.rect.x = tail[self.i][0]
        self.rect.y = tail[self.i][1]
        if pygame.sprite.collide_mask(self, head):
            death_screen(rabbit.score)


class Rabbit(pygame.sprite.Sprite):
    rabbit = load_image("rabbit.png")

    def __init__(self, group):
        super().__init__(group)
        self.image = Rabbit.rabbit
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,480,16)
        self.rect.y = random.randrange(0,480, 16)
        self.mask = pygame.mask.from_surface(self.image)
        self.score = 0

    def update(self, *args):
        if pygame.sprite.collide_mask(self, head):
            self.rect.x = random.randrange(0, 480, 16)
            self.rect.y = random.randrange(0, 480, 16)
            self.score += 1
            if way == 'left':
                tail.append([tail[0][0] + 16, tail[0][1]])
            elif way == 'right':
                tail.append([tail[0][0] - 16, tail[0][1]])
            elif way == 'up':
                tail.append([tail[0][0], tail[0][1] + 16])
            else:
                tail.append([tail[0][0], tail[0][1] - 16])

sprites = []
rabbit = Rabbit(all_sprites)
head = Head(all_sprites)
taill = Tail(all_sprites)
Border(-1, -1, width + 1, -1)
Border(-1, height + 1, width + 1, height + 1)
Border(-1, -1, -1, height + 1)
Border(width + 1, -1, width + 1, height + 1)
running = True
while running:
    if flag:
        event = start_screen()
        flag = False
        if event.key == pygame.K_1:
            speed = 8
        if event.key == pygame.K_2:
            speed = 11
        if event.key == pygame.K_3:
            speed = 14
        if event.key == pygame.K_4:
            speed = 17
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    all_sprites.update(event, speed)
    screen.blit(f, (0, 0))
    for i in range(1, len(tail) - 1):
        sprites.append(Body(all_sprites, i))
    for sprite in sprites:
        sprite.update(event)
    value = score_font.render("Score: " + str(rabbit.score), True, 'purple')
    screen.blit(value, [0, 0])
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()