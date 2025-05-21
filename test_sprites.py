import pytest
import pygame
import os
from os.path import join
from sprites_loader import load_sprite_sheets, flip

@pytest.fixture(scope="module")
def pygame_init():
    """Фикстура для инициализации Pygame"""
    pygame.init()
    pygame.display.set_mode((1, 1))  # Создаем минимальное окно
    yield
    pygame.quit()

@pytest.fixture
def setup_sprite_files(tmp_path, pygame_init):
    """Фикстура для создания временных тестовых файлов спрайтов"""
    sprite_dir = tmp_path / "Spritesheets" / "Test"
    sprite_dir.mkdir(parents=True)
    
    # Создаем тестовые изображения
    for i in range(3):
        surf = pygame.Surface((100, 20), pygame.SRCALPHA)
        surf.fill((i*50, i*50, i*50))
        pygame.image.save(surf, sprite_dir / f"sprite_{i}.png")
    
    return tmp_path

def test_load_sprite_sheets(setup_sprite_files):
    """Тест загрузки спрайтов с направлениями"""
    base_path = setup_sprite_files
    os.chdir(base_path)
    
    result = load_sprite_sheets("Spritesheets", "Test", 20, 20, direction=True)
    
    assert isinstance(result, dict)
    assert len(result) == 6  # 3 спрайта × 2 направления
    
    # Проверка формата спрайтов
    for sprites in result.values():
        assert len(sprites) == 5  # 100/20 = 5 кадров
        for sprite in sprites:
            assert sprite.get_size() == (64, 56)

def test_load_sprite_sheets_no_direction(setup_sprite_files):
    """Тест загрузки спрайтов без направлений"""
    base_path = setup_sprite_files
    os.chdir(base_path)
    
    result = load_sprite_sheets("Spritesheets", "Test", 20, 20, direction=False)
    
    assert len(result) == 3
    assert all(f"sprite_{i}" in result for i in range(3))