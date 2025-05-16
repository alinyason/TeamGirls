
import pygame
#import random

pygame.init()

# Константы
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
PINK = (255, 140, 155)
BLACK = (0, 0, 0)
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
        question_surface = font.render(self.question, True, BLACK)
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
            option_surface = font.render(f"{i+1}. {option}", True, BLACK)
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

class TextAnswerQuestion(LearningElement):
    def __init__(self, question, correct_answer):
        super().__init__(question)
        self.correct_answer = correct_answer.lower()

    def check_answer(self, answer, screen, font):
        if answer.lower() == self.correct_answer:
            self.reward(screen, font)
            return True
        else:
            self.punish(screen, font) # Вызов punish()
            return False # Важно: возвращаем False при неправильном ответе


class MatchingQuestion(LearningElement):
    def __init__(self, question, column1, column2, correct_matches):
        """
        question: текст вопроса
        column1: элементы первого столбца
        column2: элементы второго столбца
        correct_matches: список кортежей вида (индекс из column1, индекс из column2),
                         которые представляют правильные пары.
        """
        super().__init__(question)
        self.column1 = column1
        self.column2 = column2
        self.correct_matches = correct_matches
        self.current_matches = {}  # {индекс_из_column1: индекс_из_column2}
        self.selected_item = None  # (колонка, индекс)

    def display_question(self, screen, font, y_offset=100):
        """Отрисовка вопроса и столбцов"""
        super().display_question(screen, font, y_offset - 50)

        # Отрисовка первого столбца
        col1_x = SCREEN_WIDTH // 4
        col2_x = SCREEN_WIDTH * 3 // 4
        for i, item in enumerate(self.column1):
            item_surface = font.render(item, True, BLACK)
            item_rect = item_surface.get_rect(center=(col1_x, y_offset + i * 50))
            pygame.draw.rect(screen, BLACK, item_rect.inflate(10, 10), 2)
            screen.blit(item_surface, item_rect)
            if self.selected_item == ("column1", i):
                pygame.draw.rect(screen, GREEN, item_rect.inflate(14, 14), 2)

        # Отрисовка второго столбца
        for i, item in enumerate(self.column2):
            item_surface = font.render(item, True, BLACK)
            item_rect = item_surface.get_rect(center=(col2_x, y_offset + i * 50))
            pygame.draw.rect(screen, BLACK, item_rect.inflate(10, 10), 2)
            screen.blit(item_surface, item_rect)
            if self.selected_item == ("column2", i):
                pygame.draw.rect(screen, GREEN, item_rect.inflate(14, 14), 2)

        # Отрисовка текущих соединений
        for col1_idx, col2_idx in self.current_matches.items():
            pygame.draw.line(
                screen,
                RED,
                (col1_x + 50, y_offset + col1_idx * 50),
                (col2_x - 50, y_offset + col2_idx * 50),
                2,
            )

    def handle_click(self, mouse_pos, font, screen, y_offset=100):
        """Обработка кликов для выбора и соединения"""
        col1_x = SCREEN_WIDTH // 4
        col2_x = SCREEN_WIDTH * 3 // 4

        # Проверка нажатия на элементы первого столбца
        for i, item in enumerate(self.column1):
            rect = pygame.Rect(0, y_offset + i * 50 - 25, col1_x * 2, 50)
            if rect.collidepoint(mouse_pos):
                if self.selected_item == ("column1", i):
                    self.selected_item = None  # Снимаем выделение
                else:
                    self.selected_item = ("column1", i)
                return

        # Проверка нажатия на элементы второго столбца
        for i, item in enumerate(self.column2):
            rect = pygame.Rect(col2_x - col1_x, y_offset + i * 50 - 25, col1_x * 2, 50)
            if rect.collidepoint(mouse_pos):
                if self.selected_item == ("column2", i):
                    self.selected_item = None  # Снимаем выделение
                else:
                    # Если элемент из первого столбца уже выбран, связываем
                    if self.selected_item and self.selected_item[0] == "column1":
                        self.current_matches[self.selected_item[1]] = i
                        self.selected_item = None  # Сбрасываем выбор
                    else:
                        self.selected_item = ("column2", i)
                return

    def check_answer(self, mouse_pos, screen, font):
        """Проверка правильности всех соединений"""
        if set(self.correct_matches) == set(self.current_matches.items()):
            self.reward(screen, font)
            return True
        else:
            self.punish(screen, font)
            return False


def attempt_coin_pickup(player, coin):
    global current_question_index  # используем глобальный индекс
    if current_question_index >= len(questions):
        print("Все вопросы заданы.")
        return False  # или current_question_index = 0 для повтора

    question = questions[current_question_index]

    input_text = ""
    answered_correctly = False
    running_question = True

    while running_question:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if isinstance(question, MultipleChoiceQuestion) and event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    answered_correctly = question.check_answer(event.pos, screen, font)
                    running_question = False

            elif isinstance(question, TextAnswerQuestion) and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    answered_correctly = question.check_answer(input_text, screen, font)
                    running_question = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

            elif isinstance(question, MatchingQuestion):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    question.handle_click(event.pos, font, screen)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    answered_correctly = question.check_answer(None, screen, font)
                    running_question = False

        screen.fill(PINK)
        question.display_question(screen, font)

        if isinstance(question, TextAnswerQuestion):
            input_surface = font.render(input_text, True, BLACK)
            input_rect = input_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
            pygame.draw.rect(screen, BLACK, input_rect.inflate(10, 10), 2)
            screen.blit(input_surface, input_rect)

        pygame.display.flip()

    if answered_correctly:
        player.coins += 1
        print("Клубничка добавлена!")

    current_question_index += 1  # переходим к следующему вопросу

    return True


#def attempt_coin_pickup(player, coin):
    import random
    question = random.choice(questions)

    input_text = ""  # Для TextAnswerQuestion
    answered_correctly = False  # Флаг, чтобы знать, правильно ли ответили

    running_question = True
    while running_question:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # Обработка MultipleChoiceQuestion
            if isinstance(question, MultipleChoiceQuestion) and event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    answered_correctly = question.check_answer(event.pos, screen, font)
                    running_question = False

            # Обработка TextAnswerQuestion
            if isinstance(question, TextAnswerQuestion) and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    answered_correctly = question.check_answer(input_text, screen, font)
                    running_question = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

            # Обработка MatchingQuestion
            if isinstance(question, MatchingQuestion):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    question.handle_click(event.pos, font, screen)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    answered_correctly = question.check_answer(None, screen, font)
                    running_question = False

        # Отрисовка вопроса
        screen.fill(PINK)
        question.display_question(screen, font)

        # Отрисовка текста ввода для TextAnswerQuestion
        if isinstance(question, TextAnswerQuestion):
            input_surface = font.render(input_text, True, BLACK)
            input_rect = input_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
            pygame.draw.rect(screen, BLACK, input_rect.inflate(10, 10), 2)
            screen.blit(input_surface, input_rect)

        pygame.display.flip()

    # Добавление монетки за правильный ответ
    if answered_correctly:
        player.coins += 1
        print("Клубничка добавлена!")

    return True  # Игра продолжается


# Пример игрока
class Player:
    def __init__(self):
        self.coins = 0


player = Player()

# Создание вопросов 
multiQstion1 = MultipleChoiceQuestion(
    "Что изучает математический анализ?",
    ["Изменения функций, пределы, производные и интегралы", 
     "Теорию чисел и их делимость", "Свойства геометрических фигур и их соотношения"],
    0
)

multiQstion2 = MultipleChoiceQuestion(
    "Что такое производная функции в точке?",
    ["Площадь под графиком функции",
      "Предел отношения приращения функции к приращению аргумента",
        "Максимальное значение функции"],
    1
)

multiQstion3 = MultipleChoiceQuestion(
    "Как называется функция, производная которой равна заданной функции?",
    ["Ряд Тейлора", "Целевая функция", "Первообразная"],
    2
)

textQuestion1 = TextAnswerQuestion(
    "Чему равно производная функции 2*x^2?",
    "4*x"
)

textQuestion2 = TextAnswerQuestion(
    "Как называется точка, в которой производная функции равна нулю?",
    "точка экстремума"
)

textQuestion3 = TextAnswerQuestion(
    "Сколько существует замечательных пределов?",
    "2"
)

matchQuestion1 = MatchingQuestion(
    "Сопоставьте функцию с её производной:",
    ["e^x", "sin(x)", "ln(x)"],
    ["1/x", "e^x", "cos(x)"],
    [(0, 1), (1, 2), (2, 0)]
)

matchQuestion2 = MatchingQuestion(
    "Сопоставьте функцию с её названием:",
    ["lim (sin(x)/x)", "сумма функции 1/(n^a)", "Интеграл f(x)dx"],
    ["Интеграл Римана", "Обобщённый гармонический ряд", "Первый замечательный предел"],
    [(0, 2), (1, 1), (2, 0)]
)

matchQuestion3 = MatchingQuestion(
    "Сопоставьте интеграл функции с его значением:",
    ["Интеграл функции x", "Интеграл функции e^x", "Интеграл функции 1/(a^2+x^2)"],
    ["1/a*arctg(x/a) + C", "x^2/2 + C", "e^x + C"],
    [(0, 1), (1, 2), (2, 0)]
)


questions = [multiQstion1, multiQstion2,multiQstion3,textQuestion1, textQuestion2, textQuestion3, matchQuestion1, matchQuestion2, matchQuestion3]

# Основной игровой цикл 
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Нажатие пробела вызывает вопрос
                attempt_coin_pickup(player, None)

    # Отрисовка интерфейса
    screen.fill(PINK)
    text_surface = font.render(f"Клубнички: {player.coins}", True, BLACK)
    text_rect = text_surface.get_rect(topleft=(10, 10))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()

pygame.quit()