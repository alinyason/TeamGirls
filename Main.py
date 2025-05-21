import os
import random
import pygame
import math
from os import listdir
from os.path import isfile, join
pygame.init()

pygame.display.set_caption("Viper")

BG_COLOR = (255, 255, 255)
WIDTH, HEIGHT = 1100,700

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
            sprites.append(pygame.transform.scale(surface, (55, 48))) 

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
        if down:
            blocks_surr = "Mid_Mid"
            if not left and not right:
                blocks_surr = "Mid_Solo"
            elif left and not right:
                blocks_surr = "Mid_Right"
            elif not left and right:
                blocks_surr = "Mid_Left"
        elif not down:
            if right and left:
                blocks_surr = "Bottom_Mid"
            elif right and not left:
                blocks_surr = "Bottom_Left"
            elif not right and left:
                blocks_surr = "Bottom_Right"


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
    DAMAGE = 1

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
        self.y_vel = 0

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


class Enemy(pygame.sprite.Sprite):
    SPRITES = load_sprite_sheets("enemy", "", 24, 20, True)
    ANIMATION_DELAY = 8
    SPEED = 2  # Скорость движения врага
    HEALTH = 2

    COLORS = {
        1: "_blue",
        2: "_pink",
        3: "_yellow",
        4: "_green",
        5: "_purple",
    }

    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.mask = None
        self.direction = "right"
        self.animation_count = 0
        self.move_direction = 1  # 1 - вправо, -1 - влево
        self.color = color

    def check_ground_ahead(self, objects):
        # Создаем область проверки перед врагом
        if self.move_direction == 1:  # Движение вправо
            check_x = self.rect.right + 5  # Смещение вправо
        else:  # Движение влево
            check_x = self.rect.left - 5  # Смещение влево
        
        check_y = self.rect.bottom + 5  # Область под ногами
        
        # Прямоугольник для проверки (10x10 пикселей)
        ground_check = pygame.Rect(check_x, check_y, 10, 10)
        
        # Проверяем коллизии с блоками
        for obj in objects:
            if obj.name == "Block" and ground_check.colliderect(obj.rect):
                return True
        return False

    def move(self, dx):
        self.rect.x += dx

    def check_collision(self, objects, dx):
        # Временное смещение для игнорирования нижних граней
        original_rect = self.rect.copy()
        self.rect.y -= 5  # Смещаем вверх на 5 пикселей
        self.rect.x += dx
        
        collided = False
        for obj in objects:
            # checked_block = check_block(self.rect.x, self.rect.y, obj)
            if (obj.name == "Block" and self.rect.colliderect(obj.rect)):
                collided = True
            elif obj.name == "Player" and self.rect.colliderect(obj.rect):
                # collided = True
                
                break

        self.rect = original_rect
        return collided

    def loop(self, objects):
        # Проверяем, есть ли земля впереди
        if not self.check_ground_ahead(objects):
            self.move_direction *= -1  # Меняем направление

        # Проверка горизонтальных коллизий
        if self.check_collision(objects, self.move_direction * self.SPEED):
            self.move_direction *= -1

        self.move(self.move_direction * self.SPEED)
        self.direction = "right" if self.move_direction == 1 else "left"
        self.update_sprite()

    # Остальные методы остаются без изменений

    def update_sprite(self):
        sprite_sheet = "slime" + self.COLORS[self.color]
        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
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
        self.name = "Block"

class GrassPlant(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        path = join("Grass", "Grass_Plant.png")
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.mask = pygame.mask.Mask((0, 0))  # Пустая маска без коллизий # Все пиксели прозрачны для коллизий
        self.name = "Plant"

class Strawberry(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        path = join("strawberry", "ic_strawberry 1.png")
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.mask = pygame.mask.from_surface(self.image)
        self.name = "Strawberry"
        
        # Параметры анимации
        self.base_y = y  # Исходная позиция по Y
        self.amplitude = 5  # Высота "подпрыгивания"
        self.speed = 0.05  # Скорость анимации
        self.time = 0  # Счетчик времени

    def update(self):
        # Обновляем позицию по синусоиде
        self.time += self.speed
        self.rect.y = self.base_y + math.sin(self.time) * self.amplitude


def draw(window, player, objects, enemies, offset_x ): #прорисовка всего происходящего 

    for obj in objects:
        obj.draw(window, offset_x)

    for enemy in enemies:
        enemy.draw(window, offset_x)

    player.draw(window, offset_x)

    pygame.display.update() 

def vertical_collision(player, objects, dy, enemies, killed_enemies, collected):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
                if obj.name == "Strawberry":
                    objects.remove(obj)
                    collected += 1
                    print(f"Собрано клубничек: {collected}")
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

        collided_objects.append(obj)
    
    for enemy in list(enemies):
        if pygame.sprite.collide_mask(player, enemy):
            if dy > 0:
                player.rect.bottom = enemy.rect.top
                player.landed()
                enemy.HEALTH -= player.DAMAGE
                if enemy in enemies and enemy.HEALTH <= 0:
                    enemies.remove(enemy)
                    killed_enemies += 1
                    print(f"Убито врагов: {killed_enemies}")
                    if killed_enemies >= 4:
                        player.DAMAGE = 2
                player.y_vel -= 4

    return collided_objects

def collide(player, objects, enemies, collected, dx):
    original_rect = player.rect.copy()
    player.rect.y -= 5 
    player.move(dx, 0)
    collided_object = None
    
    for obj in objects:
        if player.rect.colliderect(obj.rect) and (obj.name != "Plant"):
            collided_object = obj
            if collided_object.name == "Strawberry":
                objects.remove(obj)
                collected += 1
                print(f"Собрано клубничек: {collected}")
            break

    for enemy in enemies:
        if player.rect.colliderect(enemy.rect):
            if player.rect.clip(enemy.rect).width < player.rect.clip(enemy.rect).height / 4.75:
                collided_object = enemy
                return "Game Over!"
            elif player.rect.clip(enemy.rect).width > player.rect.clip(enemy.rect).height:
                collided_object = enemy
        

    player.move(-dx, 0)
    player.rect = original_rect

    return collided_object


def move(player, objects, enemies, collected, killed_enemies):
        
    keys = pygame.key.get_pressed()  #все нажатые кнопки

    player.x_vel = 0
    collide_left = collide(player, objects, enemies, collected, -VEL)
    collide_right = collide(player, objects, enemies, collected, VEL)


    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and not collide_left:
        player.move_left(VEL)  
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not collide_right:
        player.move_right(VEL)

    if collide_left == "Game Over!" or collide_right == "Game Over!":
        return False

    vertical_collision(player, objects, player.y_vel, enemies, killed_enemies, collected)
    return True

def coord_gen(x, y, x_shift, y_shift, size):
    coords_x = size * x + x_shift
    coords_y = size * y + y_shift
        
    return coords_x, coords_y

def gen_strawberries(block_size, strawberries_conf):
    strawberries = []

    for block_x, block_y in strawberries_conf:
        x = block_x * block_size + 0.25 * block_size
        y = HEIGHT - block_y * block_size - 0.65 * block_size
        
        strawberry = Strawberry(x, y, block_size / 2, block_size / 2)
        strawberries.append(strawberry)

    return strawberries

def gen_floor_segments(block_size, segments):
    """Генерация сегментов пола"""
    floor_coords = []
    for segment in segments:
        x_start = segment['x_start'] * block_size
        x_end = segment['x_end'] * block_size
        step = block_size if x_end > x_start else -block_size
        
        for x in range(x_start, x_end + step, step):
            for layer in range(segment['layers']):
                y = HEIGHT - (segment['y_level'] + layer) * block_size
                floor_coords.append((x, y))
                
    return floor_coords

def gen_blocks(block_size, all_coords):
    """Создание блоков с автотайлингом"""
    objects = []
    for (x, y) in all_coords:
        is_block_left = check_block(x - block_size, y, all_coords)
        is_block_right = check_block(x + block_size, y, all_coords)
        is_block_top = check_block(x, y - block_size, all_coords)
        is_block_bottom = check_block(x, y + block_size, all_coords)

        block = Block(x, y, block_size, is_block_left, is_block_right, is_block_top, is_block_bottom)
        objects.append(block)
        
        # Добавляем растения
        if (x, y - block_size) not in all_coords and random.randint(1, 7) == 1:
            objects.append(GrassPlant(x, y - block_size, block_size, block_size))
    return objects

def gen_enemies(block_size, enemies_config):
    """Генерация врагов по конфигурации"""
    enemies = []
    for config in enemies_config:
        block_x, block_y, dx, dy, color = config
        x = block_x * block_size + dx * block_size
        y = HEIGHT - block_y * block_size - dy * block_size
        enemies.append(Enemy(x, y, block_size, block_size, color))
    return enemies

# Обновленная функция main
def main(window):
    clock = pygame.time.Clock()
    block_size = 64
    player = Player(100, 100, 128, 128)
    killed_enemies = 0

    # Конфигурация уровня
    LEVEL_CONFIG = {
        "floor_segments": [
            {
                'x_start': 0, 
                'x_end': 3,
                'y_level': 0,  # 1 блок от низа экрана
                'layers': 3
            },
            {
                'x_start': 5,
                'x_end': 5,
                'y_level': 0,  # на 2 блока выше основного пола
                'layers': 3
            },
            {
                'x_start': 6,
                'x_end': 8,
                'y_level': 0,  # на 2 блока выше основного пола
                'layers': 4
            },
            {
                'x_start': 10,
                'x_end': 10,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 11,
                'x_end': 12,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 13,
                'x_end': 13,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 14,
                'x_end': 16,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 17,
                'x_end': 17,
                'y_level': 0,
                'layers': 5
            },
            {
                'x_start': 18,
                'x_end': 20,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 22,
                'x_end': 22,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 24,
                'x_end': 26,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 27,
                'x_end': 27,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 29,
                'x_end': 29,
                'y_level': 5,
                'layers': 1
            },
            {
                'x_start': 31,
                'x_end': 33,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 34,
                'x_end': 35,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 37,
                'x_end': 37,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 39,
                'x_end': 39,
                'y_level': 4,
                'layers': 1
            },
            {
                'x_start': 40,
                'x_end': 45,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 46,
                'x_end': 47,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 48,
                'x_end': 50,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 49,
                'x_end': 49,
                'y_level': 5,
                'layers': 1
            },
            {
                'x_start': 51,
                'x_end': 52,
                'y_level': 4,
                'layers': 1
            },
            {
                'x_start': 54,
                'x_end': 54,
                'y_level': 4,
                'layers': 1
            },
            {
                'x_start': 56,
                'x_end': 56,
                'y_level': 5,
                'layers': 1
            },
            {
                'x_start': 57,
                'x_end': 63,
                'y_level': 0,
                'layers': 3
            },

            {
                'x_start': 58,
                'x_end': 59,
                'y_level': 6,
                'layers': 1
            },
            {
                'x_start': 64,
                'x_end': 64,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 65,
                'x_end': 69,
                'y_level': 5,
                'layers': 1
            },
            {
                'x_start': 68,
                'x_end': 73,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 74,
                'x_end': 74,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 75,
                'x_end': 79,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 78,
                'x_end': 78,
                'y_level': 5,
                'layers': 1
            },
            {
                'x_start': 81,
                'x_end': 81,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 83,
                'x_end': 86,
                'y_level': 4,
                'layers': 1
            },
            {
                'x_start': 87,
                'x_end': 89,
                'y_level': 6,
                'layers': 1
            },
            {
                'x_start': 89,
                'x_end': 93,
                'y_level': 8,
                'layers': 1
            },
            {
                'x_start': 90,
                'x_end': 94,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 95,
                'x_end': 98,
                'y_level': 0,
                'layers': 6
            },
            {
                'x_start': 99,
                'x_end': 100,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 102,
                'x_end': 103,
                'y_level': 5,
                'layers': 1
            },
            {
                'x_start': 104,
                'x_end': 104,
                'y_level': 6,
                'layers': 1
            },
            {
                'x_start': 104,
                'x_end': 113,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 107,
                'x_end': 108,
                'y_level': 6,
                'layers': 1
            },
            {
                'x_start': 109,
                'x_end': 113,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 111,
                'x_end': 113,
                'y_level': 5,
                'layers': 1
            },
            {
                'x_start': 115,
                'x_end': 116,
                'y_level': 5,
                'layers': 1
            },
            {
                'x_start': 114,
                'x_end': 124,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 120,
                'x_end': 122,
                'y_level': 5,
                'layers': 1
            },
            {
                'x_start': 123,
                'x_end': 124,
                'y_level': 5,
                'layers': 2
            },
            {
                'x_start': 121,
                'x_end': 123,
                'y_level': 7,
                'layers': 1
            },
            {
                'x_start': 125,
                'x_end': 127,
                'y_level': 0,
                'layers': 6
            },
            {
                'x_start': 128,
                'x_end': 130,
                'y_level': 0,
                'layers': 7
            },
            {
                'x_start': 131,
                'x_end': 132,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 133,
                'x_end': 142,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 133,
                'x_end': 135,
                'y_level': 7,
                'layers': 1
            },
            {
                'x_start': 137,
                'x_end': 139,
                'y_level': 8,
                'layers': 1
            },
            {
                'x_start': 141,
                'x_end': 142,
                'y_level': 7,
                'layers': 1
            },
            {
                'x_start': 144,
                'x_end': 146,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 144,
                'x_end': 144,
                'y_level': 7,
                'layers': 1
            },
            {
                'x_start': 146,
                'x_end': 148,
                'y_level': 7,
                'layers': 1
            },
            {
                'x_start': 147,
                'x_end': 149,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 150,
                'x_end': 150,
                'y_level': 0,
                'layers': 5
            },
            {
                'x_start': 151,
                'x_end': 153,
                'y_level': 0,
                'layers': 6
            },
            {
                'x_start': 154,
                'x_end': 154,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 155,
                'x_end': 156,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 157,
                'x_end': 159,
                'y_level': 0,
                'layers': 6
            },
            {
                'x_start': 160,
                'x_end': 162,
                'y_level': 0,
                'layers': 7
            },
            {
                'x_start': 163,
                'x_end': 165,
                'y_level': 0,
                'layers': 6
            },
            {
                'x_start': 166,
                'x_end': 167,
                'y_level': 0,
                'layers': 5
            },
            {
                'x_start': 168,
                'x_end': 179,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 170,
                'x_end': 170,
                'y_level': 7,
                'layers': 3
            },
            {
                'x_start': 171,
                'x_end': 172,
                'y_level': 9,
                'layers': 1
            },
            {
                'x_start': 171,
                'x_end': 172,
                'y_level': 7,
                'layers': 1
            },
            {
                'x_start': 172,
                'x_end': 173,
                'y_level': 6,
                'layers': 1
            },
            {
                'x_start': 172,
                'x_end': 172,
                'y_level': 3,
                'layers': 1
            },
            {
                'x_start': 174,
                'x_end': 177,
                'y_level': 4,
                'layers': 1
            },
            {
                'x_start': 175,
                'x_end': 176,
                'y_level': 6,
                'layers': 1
            },
            {
                'x_start': 179,
                'x_end': 179,
                'y_level': 6,
                'layers': 1
            },
            {
                'x_start': 181,
                'x_end': 182,
                'y_level': 7,
                'layers': 1
            },
            {
                'x_start': 181,
                'x_end': 186,
                'y_level': 3,
                'layers': 1
            },
            {
                'x_start': 187,
                'x_end': 189,
                'y_level': 5,
                'layers': 1
            },
            {
                'x_start': 190,
                'x_end': 195,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 197,
                'x_end': 198,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 201,
                'x_end': 207,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 203,
                'x_end': 205,
                'y_level': 5,
                'layers': 1
            },
            {
                'x_start': 209,
                'x_end': 211,
                'y_level': 4,
                'layers': 1
            },
            {
                'x_start': 212,
                'x_end': 213,
                'y_level': 6,
                'layers': 1
            },
            {
                'x_start': 213,
                'x_end': 217,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 219,
                'x_end': 221,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 222,
                'x_end': 222,
                'y_level': 0,
                'layers': 5
            },
            {
                'x_start': 224,
                'x_end': 227,
                'y_level': 0,
                'layers': 6
            },
            {
                'x_start': 228,
                'x_end': 230,
                'y_level': 4,
                'layers': 1
            },
            {
                'x_start': 228,
                'x_end': 228,
                'y_level': 5,
                'layers': 1
            },
            {
                'x_start': 228, #длинная
                'x_end': 240,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 233,
                'x_end': 238,
                'y_level': 4,
                'layers': 1
            },
            {
                'x_start': 240,
                'x_end': 242,
                'y_level': 5,
                'layers': 1
            },
            {
                'x_start': 244,
                'x_end': 245,
                'y_level': 6,
                'layers': 1
            },
            {
                'x_start': 243,
                'x_end': 254,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 245,
                'x_end': 245,
                'y_level': 3,
                'layers': 1
            },
            {
                'x_start': 246,
                'x_end': 249,
                'y_level': 3,
                'layers': 2
            },
            {
                'x_start': 247,
                'x_end': 249,
                'y_level': 5,
                'layers': 1
            },
            {
                'x_start': 250,
                'x_end': 254,
                'y_level': 3,
                'layers': 1
            },
            {
                'x_start': 251,
                'x_end': 257,
                'y_level': 6,
                'layers': 1
            },
            {
                'x_start': 256,
                'x_end': 258,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 259,
                'x_end': 262,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 263,
                'x_end': 266,
                'y_level': 4,
                'layers': 1
            },
            {
                'x_start': 268,
                'x_end': 271,
                'y_level': 3,
                'layers': 1
            },
            {
                'x_start': 272,
                'x_end': 275,
                'y_level': 5,
                'layers': 1
            },
            {
                'x_start': 277,
                'x_end': 284,
                'y_level': 0,
                'layers': 3
            },
            {
                'x_start': 285,
                'x_end': 288,
                'y_level': 0,
                'layers': 4
            },
            {
                'x_start': 289,
                'x_end': 290,
                'y_level': 0,
                'layers': 5
            },
            {
                'x_start': 291,
                'x_end': 293,
                'y_level': 0,
                'layers': 6
            },
        ],
        "strawberries": [
            (12, 2),
            (49, 2),
            (78, 5),
            (122, 5),
            (144, 7),
            (171, 7),
            (204, 5),
            (229, 2),
            (254, 3)
        ],
        "enemies": [
            (41, 2, 0.5, 0.7, random.randint(1, 5)),
            (74, 3, 0.5, 0.7, random.randint(1, 5)),
            (106, 2, 0.5, 0.7, random.randint(1, 5)),
            (119, 2, 0.5, 0.7, random.randint(1, 5)),
            (136, 2, 0.5, 0.7, random.randint(1, 5)),
            (183, 3, 0.5, 0.7, random.randint(1, 5)),
            (215, 2, 0.5, 0.7, random.randint(1, 5)),
            (234, 2, 0.5, 0.7, random.randint(1, 5)),
            (281, 2, 0.5, 0.7, random.randint(1, 5))
        ]
    }

    # Генерация объектов
    floor_coords = gen_floor_segments(
            block_size, 
            LEVEL_CONFIG["floor_segments"]  # передаем список напрямую
        )
    all_coords = floor_coords
    
    objects = gen_blocks(block_size, all_coords)
    objects.extend(gen_strawberries(block_size, LEVEL_CONFIG["strawberries"]))
    enemies = gen_enemies(block_size, LEVEL_CONFIG["enemies"])

    # Игровой цикл (без изменений)
    offset_x = 0
    scroll_area_width = 200
    run = True
    collected = 0
    
    while run:
        clock.tick(FPS)
        draw_bg(offset_x)

        player.loop(FPS)
        for enemy in enemies:
            enemy.loop(objects)
        run = move(player, objects, enemies, collected, killed_enemies)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w) and player.jump_count < 2:
                    player.jump()

        for obj in objects:
            if isinstance(obj, Strawberry):
                obj.update()

        draw(window, player, objects, enemies, offset_x)

        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
            (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)