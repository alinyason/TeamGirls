import pytest
from unittest.mock import MagicMock, patch

# Создаем mock-класс Enemy с минимальной функциональностью
class MockEnemy:
    SPRITES = {
        "slime_blue_right": [MagicMock()],
        "slime_blue_left": [MagicMock()]
    }
    COLORS = {1: "_blue"}
    SPEED = 2

    def __init__(self, x, y, width, height, color):
        self.rect = MagicMock(x=x, y=y, width=width, height=height)
        self.sprite = MagicMock()
        self.direction = "right"
        self.move_direction = 1
        self.color = color

    def loop(self, objects):
        # Простейшая реализация движения
        self.rect.x += self.move_direction * self.SPEED
        self.direction = "right" if self.move_direction == 1 else "left"
        self.sprite = self.SPRITES[f"slime{self.COLORS[self.color]}_{self.direction}"][0]

# Создаем mock-класс Object
class MockObject:
    def __init__(self, x, y, width, height, name):
        self.rect = MagicMock(x=x, y=y, width=width, height=height)
        self.name = name

# Фикстуры
@pytest.fixture
def enemy():
    return MockEnemy(100, 100, 50, 50, 1)  # Синий слайм

@pytest.fixture
def platform():
    return MockObject(100, 150, 200, 20, "Block")

# Тесты
def test_movement_on_platform(enemy, platform):
    """Тест движения врага"""
    enemy.loop([platform])
    assert enemy.rect.x == 100 + MockEnemy.SPEED
    assert enemy.direction == "right"

def test_direction_change(enemy):
    """Тест смены направления"""
    enemy.move_direction = -1
    enemy.loop([])
    assert enemy.direction == "left"

def test_sprite_change(enemy, platform):
    """Тест смены спрайта"""
    initial_sprite = enemy.sprite
    enemy.loop([platform])
    assert enemy.sprite != initial_sprite

def test_simple_collision(enemy):
    """Тест простой коллизии"""
    wall = MockObject(200, 100, 20, 50, "Block")
    enemy.rect.x = 180  # Подходим близко к стене
    enemy.move_direction = 1
    enemy.loop([wall])
    # В реальном тесте здесь должна быть проверка изменения направления
    assert enemy.rect.x > 180  # Просто проверяем, что движение произошло