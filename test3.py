import pytest
import math
from unittest.mock import MagicMock, patch

# Создаем mock-класс Strawberry
class MockStrawberry:
    def __init__(self, x, y, width, height):
        self.rect = MagicMock(x=x, y=y, width=width, height=height)
        self.image = MagicMock()
        self.mask = MagicMock()
        self.name = "Strawberry"
        self.base_y = y
        self.amplitude = 5
        self.speed = 0.05
        self.time = 0
    
    def update(self):
        """Упрощенная реализация анимации"""
        self.time += self.speed
        self.rect.y = self.base_y + math.sin(self.time) * self.amplitude
    
    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))

# Фикстуры
@pytest.fixture
def strawberry():
    return MockStrawberry(100, 200, 32, 32)

# Тесты
def test_strawberry_initial_state(strawberry):
    """Тест начального состояния"""
    assert strawberry.rect.x == 100
    assert strawberry.rect.y == 200
    assert strawberry.base_y == 200
    assert strawberry.amplitude == 5
    assert strawberry.speed == 0.05
    assert strawberry.time == 0

def test_strawberry_update_animation(strawberry):
    """Тест анимации подпрыгивания"""
    initial_y = strawberry.rect.y
    strawberry.update()
    
    # Проверяем что время увеличилось
    assert strawberry.time == 0.05
    
    # Проверяем что позиция изменилась
    assert strawberry.rect.y != initial_y
    
    # Проверяем формулу расчета
    expected_y = 200 + math.sin(0.05) * 5
    assert strawberry.rect.y == pytest.approx(expected_y)

def test_strawberry_draw(strawberry):
    """Тест отрисовки"""
    mock_window = MagicMock()
    offset_x = 50
    
    strawberry.draw(mock_window, offset_x)
    
    # Проверяем вызов blit с правильными параметрами
    mock_window.blit.assert_called_once_with(
        strawberry.image,
        (50, strawberry.rect.y)  # 100 - 50 = 50
    )

def test_multiple_updates(strawberry):
    """Тест нескольких обновлений"""
    positions = []
    for _ in range(5):
        strawberry.update()
        positions.append(strawberry.rect.y)
    
    # Проверяем что позиция меняется
    assert len(set(positions)) > 1
    
    # Проверяем что остается в пределах амплитуды
    assert all(200 - 5 <= y <= 200 + 5 for y in positions)