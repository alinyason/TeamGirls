import pygame

pygame.init()

# Константы
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
BROWN = (50, 35, 12)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
current_question_index = 0  # индекс текущего вопроса


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Обучающие Элементы в Pygame")

font = pygame.font.Font(None, 36)  # Шрифт для текста

class LearningElement:
    def __init__(self, question):
        self.question = question
        self.answered = False

    def display_question(self, screen, font, y_offset=50):
        question_surface = font.render(self.question, True, WHITE)
        question_rect = question_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
        screen.blit(question_surface, question_rect)

    def check_answer(self, answer):
        raise NotImplementedError("Метод check_answer должен быть реализован в дочернем классе.")

    def reward(self, screen, font):
        self.answered = True
        text_surface = font.render("Правильный ответ! Клубничка получена.", True, GREEN)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()
        pygame.time.delay(1000)

    def punish(self, screen, font):
        text_surface = font.render("Неправильный ответ! Больше попыток нет.", True, RED)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()
        pygame.time.delay(1000)

class MultipleChoiceQuestion(LearningElement):
    def __init__(self, question, options, correct_answer_index):
        super().__init__(question)
        self.options = options
        self.correct_answer_index = correct_answer_index
        self.option_rects = []

    def display_question(self, screen, font, y_offset=50):
        super().display_question(screen, font, y_offset)
        self.option_rects = []
        for i, option in enumerate(self.options):
            option_surface = font.render(f"{i+1}. {option}", True, WHITE)
            option_rect = option_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset + 50 + (i * 40)))
            screen.blit(option_surface, option_rect)
            self.option_rects.append(option_rect)

    def check_answer(self, mouse_pos, screen, font):
        for i, rect in enumerate(self.option_rects):
            if rect.collidepoint(mouse_pos):
                if i == self.correct_answer_index:
                    self.reward(screen, font)
                    return True
                else:
                    self.punish(screen, font) # Вызов punish()
                    return False # Важно: возвращаем False при неправильном ответе
        return False
