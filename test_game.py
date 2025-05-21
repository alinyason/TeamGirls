import pytest
import pygame
from game_code import LearningElement, MultipleChoiceQuestion

@pytest.fixture
def pygame_init():
    pygame.init()
    screen = pygame.display.set_mode((1000, 600))
    font = pygame.font.Font(None, 36)
    yield screen, font
    pygame.quit()

class TestLearningElement:
    def test_initialization(self):
        question = "Test question"
        element = LearningElement(question)
        assert element.question == question
        assert not element.answered

    def test_display_question(self, pygame_init):
        screen, font = pygame_init
        question = "Test question"
        element = LearningElement(question)
        element.display_question(screen, font)

    def test_reward(self, pygame_init):
        screen, font = pygame_init
        element = LearningElement("Test question")
        element.reward(screen, font)
        assert element.answered

    def test_punish(self, pygame_init):
        screen, font = pygame_init
        element = LearningElement("Test question")
        element.punish(screen, font)
        assert not element.answered

class TestMultipleChoiceQuestion:
    def test_initialization(self):
        question = "Test question"
        options = ["Option 1", "Option 2", "Option 3"]
        correct_idx = 1
        mcq = MultipleChoiceQuestion(question, options, correct_idx)
        
        assert mcq.question == question
        assert mcq.options == options
        assert mcq.correct_answer_index == correct_idx
        assert not mcq.answered
        assert mcq.option_rects == []

    def test_display_question(self, pygame_init):
        screen, font = pygame_init
        question = "Test question"
        options = ["Option 1", "Option 2", "Option 3"]
        mcq = MultipleChoiceQuestion(question, options, 1)
        mcq.display_question(screen, font)
        assert len(mcq.option_rects) == len(options)

    def test_check_answer_correct(self, pygame_init):
        screen, font = pygame_init
        question = "Test question"
        options = ["Option 1", "Option 2", "Option 3"]
        mcq = MultipleChoiceQuestion(question, options, 1)
        mcq.display_question(screen, font)
        
        # Создаем фиктивную позицию мыши в центре второго варианта ответа
        test_pos = mcq.option_rects[1].center
        result = mcq.check_answer(test_pos, screen, font)
        assert result is True
        assert mcq.answered

    def test_check_answer_incorrect(self, pygame_init):
        screen, font = pygame_init
        question = "Test question"
        options = ["Option 1", "Option 2", "Option 3"]
        mcq = MultipleChoiceQuestion(question, options, 1)
        mcq.display_question(screen, font)
        
        # Создаем фиктивную позицию мыши в центре первого варианта ответа (неправильный)
        test_pos = mcq.option_rects[0].center
        result = mcq.check_answer(test_pos, screen, font)
        assert result is False
        assert not mcq.answered
