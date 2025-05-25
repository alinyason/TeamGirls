import pygame
import test_utils  # Должен быть первым!
from main import Player

class TestPlayer:
    def setup_method(self):
        self.player = Player(100, 100, 50, 50)

    def test_initial_state(self):
        assert self.player.rect.x == 100
        assert self.player.rect.y == 100
        assert self.player.direction == "right"
        assert self.player.jump_count == 0
        assert self.player.y_vel == 0

    def test_movement(self):
        self.player.move_left(5)
        assert self.player.x_vel == -5
        assert self.player.direction == "left"

        self.player.move_right(5)
        assert self.player.x_vel == 5
        assert self.player.direction == "right"

    def test_jump_mechanics(self):
        self.player.jump()
        assert self.player.y_vel < 0
        assert self.player.jump_count == 1

        # Двойной прыжок
        self.player.jump()
        assert self.player.jump_count == 2
        assert self.player.y_vel < -self.player.GRAVITY * 6

    def test_landing(self):
        self.player.y_vel = 10
        self.player.fall_count = 30
        self.player.landed()
        
        assert self.player.y_vel == 0
        assert self.player.fall_count == 0
        assert self.player.jump_count == 0