import random
import pygame
import math
from os import listdir
from os.path import isfile, join
from config import LEVEL_CONFIG


pygame.init()

pygame.display.set_caption("Duck")

BG_COLOR = (255, 255, 255)
WIDTH, HEIGHT = 1100, 800

PROGRESS_HEIGHT = 20
STRAWBERRY_ICON = pygame.transform.scale(pygame.image.load("strawberry/ic_strawberry 1.png"), (30, 30))
ENEMY_ICON = pygame.transform.scale(pygame.image.load("enemy/slime_icon.png"), (35, 30))

BUTTON_COLOR = (1, 11, 64)
BUTTON_HOVER_COLOR = (1, 11, 64)
TEXT_COLOR = (255, 255, 255)

FPS = 60
VEL = 5 #скорость персонажа

window = pygame.display.set_mode((WIDTH, HEIGHT))

#прорисовка фона
bg_images = []
for i in range(1, 4):
    bg_image = pygame.image.load(f"Background/Layer_{i}.png").convert_alpha()
    bg_images.append(pygame.transform.scale(bg_image, (HEIGHT * 1.7, HEIGHT)))

def draw_bg(offset_x):
    for idx, img in enumerate(bg_images):
        speed = 0.2 * (idx+0.3)
        width = img.get_width()
        x_shift = offset_x * speed
        
        current_block = int(x_shift // width)
        for i in range(current_block - 1, current_block + 2):  #! OPT: 3 цикла на кадр × 3 слоя = 9 итераций
            x_pos = (i * width) - x_shift
            window.blit(img, (x_pos, 0))  #! OPT: Множественные blit-вызовы

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
    COLLECTED = 0
    KILLED = 0
    
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
        self.real_x = x
        self.level_up_time = 0
        self.level_completed = False

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
        self.real_x += dx

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
    ANIMATION_DELAY = 6
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
        check_x = self.rect.right + 5 if self.move_direction == 1 else self.rect.left - 5  #! OPT: Пересчет каждый кадр
        ground_check = pygame.Rect(check_x, self.rect.bottom + 5, 10, 10)  #! OPT: Создание новых Rect
        
        for obj in objects:  #! OPT: Линейный поиск по всем объектам
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
        self.time += self.speed  #! OPT: float-операции
        self.rect.y = self.base_y + math.sin(self.time) * self.amplitude

def draw_text(surface, text, x, y, size=13, color=(0,0,0)):
    # Масштабируем размер шрифта относительно базового
    scaled_font = pygame.font.Font('Asset/PublicPixel-rv0pA.ttf', size)
    text_surface = scaled_font.render(text, True, color)
    surface.blit(text_surface, (x, y))

def draw(window, player, objects, enemies, offset_x, max_progress, total_straw, total_enemies):

    for obj in objects:
        obj.draw(window, offset_x)

    for enemy in enemies:
        enemy.draw(window, offset_x)

    player.draw(window, offset_x)

    # Прогресс уровня поверх подложки
    level_progress = min(player.rect.x / max_progress, 1.0)
    pygame.draw.rect(window, (100,100,100), (15, 15, (WIDTH - 30), PROGRESS_HEIGHT))
    pygame.draw.rect(window, (0,200,0), (15, 15, (WIDTH - 30) * level_progress, PROGRESS_HEIGHT))

    # Счетчики коллекций
    y_offset = PROGRESS_HEIGHT + 25
    window.blit(STRAWBERRY_ICON, (15, y_offset))
    draw_text(window, f"{player.COLLECTED}/{total_straw}", 55, y_offset + 10)

    window.blit(ENEMY_ICON, (155, y_offset))
    draw_text(window, f"{player.KILLED}/{total_enemies}", 195, y_offset + 10)

    draw_text(window, f"Урон: {player.DAMAGE}", 335, y_offset + 10)

    draw_text(window, f"Опыт: ", 475, y_offset + 10)
    lvl_progress = min(player.KILLED/2, 1)
    pygame.draw.rect(window, (100,100,100), (545, y_offset + 8, (80), PROGRESS_HEIGHT))
    pygame.draw.rect(window, (0,200,0), (545, y_offset + 8, (80) * lvl_progress, PROGRESS_HEIGHT))

    current_time = pygame.time.get_ticks()
    if player.level_up_time != 0 and (current_time - player.level_up_time) < 2000:
        # Создаем текст
        font = pygame.font.Font('Asset/PublicPixel-rv0pA.ttf', 15)
        text_surface = font.render("Новый уровень! Урон повышен!", True, (0, 0, 0))
        
        # Создаем фон с скругленными краями
        padding = 15
        bg_width = text_surface.get_width() + padding*2
        bg_height = text_surface.get_height() + padding*2
        bg_rect = pygame.Rect(0, 0, bg_width, bg_height)
        bg_surface = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
        
        # Рисуем скругленный прямоугольник
        pygame.draw.rect(bg_surface, (229, 173, 255), bg_rect)
        pygame.draw.rect(bg_surface, (0, 0, 0), bg_rect, width=2)
        
        # Позиционируем внизу экрана
        pos_x = (WIDTH - bg_width) // 2
        pos_y = HEIGHT - 80
        
        # Собираем вместе
        window.blit(bg_surface, (pos_x, pos_y))
        window.blit(text_surface, (pos_x + padding, pos_y + padding))

# Перенесем блок с завершением уровня ВНЕ условия level_up_time
    if player.level_completed:
        # Расчет количества звезд
        stars = 1
        if player.COLLECTED >= total_straw:
            stars += 1
        if player.KILLED >= total_enemies:
            stars += 1

    pygame.display.update()

def vertical_collision(player, objects, dy, enemies):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
                if obj.name == "Strawberry":
                    objects.remove(obj)
                    player.COLLECTED += 1
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
                    player.KILLED += 1
                    if player.KILLED >= 2:  # Измените условие с 3 на 4
                        player.DAMAGE = 2
                    if player.KILLED == 2:  # Устанавливаем время при достижении 4 убийств
                        player.level_up_time = pygame.time.get_ticks()
                player.jump()

    return collided_objects

def collide(player, objects, enemies, dx):
    original_rect = player.rect.copy()
    player.rect.y -= 5 
    player.move(dx, 0)
    collided_object = None
    
    for obj in objects:
        if player.rect.colliderect(obj.rect) and (obj.name != "Plant"):
            collided_object = obj
            if collided_object.name == "Strawberry":
                objects.remove(obj)
                player.COLLECTED += 1
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


def move(player, objects, enemies):
        
    keys = pygame.key.get_pressed()  #все нажатые кнопки

    player.x_vel = 0
    collide_left = collide(player, objects, enemies, -VEL)
    collide_right = collide(player, objects, enemies, VEL)


    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and not collide_left:
        player.move_left(VEL)  
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not collide_right:
        player.move_right(VEL)

    if collide_left == "Game Over!" or collide_right == "Game Over!":
        return False

    vertical_collision(player, objects, player.y_vel, enemies)
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
def run_game():
    clock = pygame.time.Clock()

    block_size = 64
    player = Player(block_size *1, (HEIGHT // block_size) * block_size, 128, 128)

    max_level_progress = 291 * block_size
    total_strawberries = len(LEVEL_CONFIG["strawberries"])
    total_enemies = len(LEVEL_CONFIG["enemies"])

    floor_coords = gen_floor_segments(block_size, LEVEL_CONFIG["floor_segments"])
    all_coords = floor_coords
    
    objects = gen_blocks(block_size, all_coords)
    objects.extend(gen_strawberries(block_size, LEVEL_CONFIG["strawberries"]))
    enemies = gen_enemies(block_size, LEVEL_CONFIG["enemies"])

    offset_x = 0
    scroll_area_width = WIDTH / 2.6
    run = True
    
    while run:
        clock.tick(FPS)
        
        draw_bg(offset_x)

        player.loop(FPS)

        if (player.rect.x // block_size) == (292):
            player.level_completed = True
        
        if player.rect.y >= ((HEIGHT // block_size) + 1) * block_size:
            return ("Game Over", window.copy())  # Возвращаем кортеж

        for enemy in enemies:
            enemy.loop(objects)
            
        game_status = move(player, objects, enemies)
        
        if game_status == False:
            return ("Game Over", window.copy())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "Exit"
            
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w) and player.jump_count < 2:
                    player.jump()

        for obj in objects:
            if isinstance(obj, Strawberry):
                obj.update()

        if player.level_completed:
            snapshot = window.copy()
            return ("Level Completed", 
                    player.COLLECTED, 
                    player.KILLED, 
                    total_strawberries, 
                    total_enemies, 
                    snapshot)

        draw(window, player, objects, enemies, offset_x, max_level_progress, total_strawberries, total_enemies)

        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
            (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

def blur_surface(surface, scale_factor=0.05):
    # Сжать
    small = pygame.transform.smoothscale(surface, (int(surface.get_width() * scale_factor), int(surface.get_height() * scale_factor)))
    # Растянуть обратно
    return pygame.transform.smoothscale(small ,surface.get_size())
    


def game_over_screen():
    run = True

    snapshot = window.copy()
    blurred_bg = blur_surface(snapshot)

    # Загрузка изображения "Game Over" (в PNG)
    game_over_image = pygame.image.load("Asset/GameOver.png")
    game_over_image = pygame.transform.scale(game_over_image, (450, 150))  # по необходимости подгони размер

    # Кнопки
    yes_button = pygame.Rect(WIDTH//2 - 110, HEIGHT//2 + 50, 80, 40)
    no_button = pygame.Rect(WIDTH//2 + 30, HEIGHT//2 + 50, 80, 40)

    while run:
        window.blit(blurred_bg, (0, 0))  # Чёрный фон

        # Отображение изображения
        window.blit(game_over_image, (WIDTH//2 - 230, HEIGHT//2 - 150))

        # Текст "RESTART?"
        draw_text(window, "RESTART?", WIDTH//2 - 80, HEIGHT//2 + 10, 23, (0, 0, 0))

        # Кнопки YES и NO
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.rect(window, (1, 11, 64), yes_button)
        pygame.draw.rect(window, (1, 11, 64), no_button)

        draw_text(window, "YES", yes_button.x + 16, yes_button.y + 8, 16, (255, 255, 255))
        draw_text(window, "NO", no_button.x + 22, no_button.y + 8, 16, (255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if yes_button.collidepoint(event.pos):
                    return True
                elif no_button.collidepoint(event.pos):
                    return False

        pygame.display.update()
        pygame.time.Clock().tick(FPS)

def show_victory_screen(collected, killed, total_straw, total_enemies, snapshot):
    run = True
    clock = pygame.time.Clock()
    blurred_bg = blur_surface(snapshot)

    # Загрузка изображения "Victory" (замените путь на свой)
    victory_image = pygame.image.load("Asset/Victory.png")  # Ваше изображение
    victory_image = pygame.transform.scale(victory_image, (450, 200))

    # Рассчитываем звезды
    stars = 1
    if collected >= total_straw: stars += 1
    if killed >= total_enemies: stars += 1

    # Кнопки
    restart_btn = pygame.Rect(WIDTH//2 - 185, HEIGHT//2 + 100, 180, 40)
    exit_btn = pygame.Rect(WIDTH//2 + 10, HEIGHT//2 + 100, 180, 40)

    while run:
        window.blit(blurred_bg, (0, 0))
        
        # Отображение изображения победы
        window.blit(victory_image, (WIDTH//2 - 225, HEIGHT//2 - 210))

        # Панель статистики

        # Статистика
        stats = [
            f"Собрано клубники: {collected}/{total_straw}",
            f"Уничтожено врагов: {killed}/{total_enemies}"
        ]
        for i, text in enumerate(stats):
            draw_text(window, text, WIDTH / 2 - 170, 
            (HEIGHT / 2) + 180 + i*40, 16, (255, 255, 255))

        # Звезды
        star_y = (HEIGHT / 2)
        for i in range(3):
            star_x = (WIDTH / 2) - 79 + i*80
            color = (255, 215, 0) if i < stars else (150, 150, 150)
            pygame.draw.polygon(window, color, [
                (star_x, star_y), (star_x+8, star_y+25),
                (star_x+35, star_y+25), (star_x+12, star_y+40),
                (star_x+20, star_y+65), (star_x, star_y+50),
                (star_x-20, star_y+65), (star_x-12, star_y+40),
                (star_x-35, star_y+25), (star_x-8, star_y+25)
            ])

        # Кнопки
        mouse_pos = pygame.mouse.get_pos()
        for btn, text in [(restart_btn, "РЕСТАРТ"), (exit_btn, "ВЫХОД")]:
            color = BUTTON_HOVER_COLOR if btn.collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(window, color, btn)
            draw_text(window, text, btn.x + 45, btn.y + 9, 16, TEXT_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_btn.collidepoint(event.pos):
                    return True
                if exit_btn.collidepoint(event.pos):
                    return False

        pygame.display.update()
        clock.tick(FPS)

def main():
    while True:
        game_result = run_game()
        
        # Обработка Game Over
        if game_result[0] == "Game Over":
            restart = game_over_screen()
            if not restart: 
                break
        
        # Обработка завершения уровня
        elif game_result[0] == "Level Completed":
            _, collected, killed, total_straw, total_enemies, snapshot = game_result
            restart = show_victory_screen(
                collected, killed, total_straw, total_enemies, snapshot
            )
            if not restart: 
                break
        
        # Выход из игры
        elif game_result[0] == "Exit":
            break

if __name__ == "__main__":
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    main()
    pygame.quit()