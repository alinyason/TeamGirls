import pygame
from unittest.mock import MagicMock
import sys

# Глобальная настройка для тестового режима
sys.modules['TESTING'] = True

# Заглушка для pygame.image.load
pygame.image.load = MagicMock(return_value=pygame.Surface((32, 32)))

# Заглушка для os.listdir
def mock_listdir(path):
    return ["dummy_sprite.png"] if "Spritesheets" in path else []

# Заглушка для load_sprite_sheets
def mock_load_sprite_sheets(*args, **kwargs):
    return {
        "idle_right": [pygame.Surface((32, 32))],
        "idle_left": [pygame.Surface((32, 32))],
        "walk_right": [pygame.Surface((32, 32))],
        "walk_left": [pygame.Surface((32, 32))],
        "jump_right": [pygame.Surface((32, 32))],
        "jump_left": [pygame.Surface((32, 32))],
    }

# Применяем заглушки
import os
os.listdir = mock_listdir
from main import load_sprite_sheets
load_sprite_sheets = mock_load_sprite_sheets