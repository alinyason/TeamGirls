import os
import random
import pygame
import math
from os import listdir
from os.path import isfile, join
pygame.init()

pygame.display.set_caption("Viper")

BG_COLOR = (255, 255, 255)
WIDTH, HEIGHT = 800,600

FPS = 60
VEL = 5 #скорость персонажа

window = pygame.display.set_mode((WIDTH, HEIGHT))

bg_images = []
for i in range(1, 4):
    bg_image = pygame.image.load(f"Background/Layer_{i}.png").convert_alpha()
    #bg_images.append(bg_image)
    bg_images.append(pygame.transform.scale(bg_image, (HEIGHT * 1.7, HEIGHT)))

def draw_bg(offset_x):
    for idx, img in enumerate(bg_images):
        if idx <= 0:
            window.blit(img, (0, 0))
        else:
            speed = 0.2 * (idx)
            width = img.get_width()
            x_shift = offset_x * speed
            
            current_block = int(x_shift // width)
            for i in range(current_block - 1, current_block + 2):
                x_pos = (i * width) - x_shift
                window.blit(img, (x_pos, 0))

def check_block(x, y, objects):
    for (obj_x, obj_y) in objects:
        if obj_x == x and obj_y == y:
            return True
    return False


def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheets(dir1, dir2, width, height, direction = False):
    path = join("", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path,f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i*width, 0, width, height)
            surface.blit(sprite_sheet, (0,0), rect)
            sprites.append(pygame.transform.scale(surface, (64, 56))) 

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites

def get_block(size, left, right, up, down):
    blocks_surr = "Top_Mid"
    if not up: 
        if not down:
            blocks_surr = "Tile"
            if left and not right:
                blocks_surr += "_Right"
            elif right and not left:
                blocks_surr += "_Left"
            elif right and left:
                blocks_surr += "_Mid"
            elif not left and not right:
                blocks_surr += "_Solo"
        elif down:
            if not left and not right:
                blocks_surr = "Top_Solo"
            elif right and left:
                blocks_surr = "Top_Mid"
            elif right and not left:
                blocks_surr = "Top_Left"
            elif not right and left:
                blocks_surr = "Top_Right"
                
    elif up:
        blocks_surr = "Mid_Mid"


    path = join("Grass", "", "Grass_" + blocks_surr + ".png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect  = pygame.Rect(0, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale(image, (size, size))

class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("Spritesheets", "", 23, 20, True)
    ANIMATION_DELAY = 8

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "right"
        self.animation_count = 0
        self.fall_count = 0
        self.is_falling = True
        self.jump_count = 0

        if self.fall_count > 0:
            self.is_falling = True
    
    def jump(self):
        self.y_vel = -self.GRAVITY  * 6
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0
        elif self.jump_count == 2:
            self.y_vel = -self.GRAVITY *   10
            
    
    def move(self, dx, dy): #функция движения персонажа
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0


    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self,fps): #основной цикл персонажа(отслеживание действий)
        self.y_vel += min(1,(self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0
        self.is_falling = False

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.y_vel < 0:
            if self.jump_count == 1 or self.jump_count == 2:
                sprite_sheet = "jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "walk"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft = (self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)
    
    def draw(self,win, offset_x): #отрисовка персонажа
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name = None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))

class Block(Object):
    def __init__(self, x, y, size, is_block_left, is_block_right, is_block_top, is_block_bottom):
        super().__init__(x, y, size, size)  # ← исправили здесь
        self.x = x
        self.y = y
        self.size = size
        block = get_block(size, is_block_left, is_block_right, is_block_top, is_block_bottom)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)



def draw(window, player, objects, offset_x): #прорисовка всего происходящего 

    #window.fill(BG_COLOR)

    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x)


    pygame.display.update() 

def vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

        collided_objects.append(obj)

    return collided_objects

def collide(player, objects, dx):
    original_rect = player.rect.copy()
    player.rect.y -= 5 
    player.move(dx, 0)
    collided_object = None

    for obj in objects:
        if player.rect.colliderect(obj.rect):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.rect = original_rect

    return collided_object


def move(player, objects):
        
    keys = pygame.key.get_pressed()  #все нажатые кнопки

    player.x_vel = 0
    collide_left = collide(player, objects, -VEL)
    collide_right = collide(player, objects, VEL)

    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and not collide_left:
        player.move_left(VEL)  
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not collide_right:
        player.move_right(VEL)

    vertical_collision(player, objects, player.y_vel)

def main(window):
    clock = pygame.time.Clock()
    block_size = 64
    player = Player(100, 100, 128, 128)

    # создаём заготовку всех координат блоков
    floor_coords = []
    for i in range(-WIDTH // block_size, WIDTH * 2 // block_size):
        x = i * block_size
        y1 = HEIGHT - block_size
        y2 = HEIGHT
        floor_coords.append((x, y1))
        floor_coords.append((x, y2))
        
    other_coords = [
        (block_size * 1, HEIGHT - block_size * 2),
        (block_size * 2, HEIGHT - block_size * 2), # одиночный блок
        (block_size * 5, HEIGHT - block_size * 4),  # начало платформы в 4 блока
        (block_size * 6, HEIGHT - block_size * 4),
        (block_size * 7, HEIGHT - block_size * 4),
        (block_size * 3, HEIGHT - block_size * 4),
        (block_size * 8, HEIGHT - block_size * 5)
    ]
    all_coords = floor_coords + other_coords

    # создаём блоки с правильной проверкой соседей
    objects = []
    for (x, y) in all_coords:
        is_block_left = check_block(x - block_size, y, all_coords)
        is_block_right = check_block(x + block_size, y, all_coords)
        is_block_top = check_block(x, y - block_size, all_coords)
        is_block_bottom = check_block(x, y + block_size, all_coords)

        block = Block(x, y, block_size, is_block_left, is_block_right, is_block_top, is_block_bottom)
        objects.append(block)

    offset_x = 0
    scroll_area_width = 200

    run = True
    while run:
        clock.tick(FPS)
        draw_bg(offset_x)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_SPACE or event.key == pygame.K_w or event.key == pygame.K_UP) and player.jump_count < 2:
                    player.jump()

        player.loop(FPS)
        move(player, objects)
        draw(window, player, objects, offset_x)

        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
            (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)