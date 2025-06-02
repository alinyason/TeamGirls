import pygame
#import random

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
        self.selected_option = None  # выбранный вариант (индекс)

    def display_question(self, screen, font, y_offset=50):
        super().display_question(screen, font, y_offset)
        self.option_rects = []
        for i, option in enumerate(self.options):
            color = GREEN if self.selected_option == i else WHITE
            option_surface = font.render(f"{i+1}. {option}", True, color)
            option_rect = option_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset + 50 + (i * 40)))
            screen.blit(option_surface, option_rect)
            self.option_rects.append(option_rect)

    def select_option(self, index):
        if 0 <= index < len(self.options):
            self.selected_option = index

    def check_answer(self, screen, font):
        if self.selected_option == self.correct_answer_index:
            self.reward(screen, font)
            return True
        else:
            self.punish(screen, font)
            return False


class TextAnswerQuestion(LearningElement):
    def __init__(self, question, correct_answers):
        super().__init__(question)
        # Принимаем список вариантов правильных ответов
        self.correct_answers = [ans.lower().strip() for ans in correct_answers]

    def check_answer(self, answer, screen, font):
        normalized_answer = answer.lower().strip()
        # Дополнительно можно убрать лишние пробелы внутри строки
        normalized_answer = " ".join(normalized_answer.split())
        if normalized_answer in self.correct_answers:
            self.reward(screen, font)
            return True
        else:
            self.punish(screen, font)
            return False

class MatchingQuestion(LearningElement):
    def __init__(self, question, column1, column2, correct_matches):
        super().__init__(question)
        self.column1 = column1
        self.column2 = column2
        self.correct_matches = correct_matches
        self.current_matches = {}  # {индекс_из_column1: индекс_из_column2}
        self.selected_item = None  # ('column1' или 'column2', индекс)

    def display_question(self, screen, font, y_offset=100):
        super().display_question(screen, font, y_offset - 50)

        col1_x = SCREEN_WIDTH // 4
        col2_x = SCREEN_WIDTH * 3 // 4

        for i, item in enumerate(self.column1):
            item_surface = font.render(item, True, WHITE)
            item_rect = item_surface.get_rect(center=(col1_x, y_offset + i * 50))
            pygame.draw.rect(screen, WHITE, item_rect.inflate(10, 10), 2)
            screen.blit(item_surface, item_rect)
            if self.selected_item == ("column1", i):
                pygame.draw.rect(screen, GREEN, item_rect.inflate(14, 14), 2)

        for i, item in enumerate(self.column2):
            item_surface = font.render(item, True, WHITE)
            item_rect = item_surface.get_rect(center=(col2_x, y_offset + i * 50))
            pygame.draw.rect(screen, WHITE, item_rect.inflate(10, 10), 2)
            screen.blit(item_surface, item_rect)
            if self.selected_item == ("column2", i):
                pygame.draw.rect(screen, GREEN, item_rect.inflate(14, 14), 2)

        for col1_idx, col2_idx in self.current_matches.items():
            pygame.draw.line(
                screen,
                RED,
                (col1_x + 50, y_offset + col1_idx * 50),
                (col2_x - 50, y_offset + col2_idx * 50),
                2,
            )

    def handle_click(self, mouse_pos, font, screen, y_offset=100):
        col1_x = SCREEN_WIDTH // 4
        col2_x = SCREEN_WIDTH * 3 // 4

    # Проверка клика по первому столбцу
        for i in range(len(self.column1)):
            item_rect = pygame.Rect(
                col1_x - 100,  # Широкая область клика
                y_offset + i * 50 - 20,
                200,  # Ширина области
                40,   # Высота области
            )
            if item_rect.collidepoint(mouse_pos):
                if self.selected_item == ("column1", i):
                    self.selected_item = None  # Сброс выбора
                else:
                    self.selected_item = ("column1", i)
                return

    # Проверка клика по второму столбцу
        for i in range(len(self.column2)):
            item_rect = pygame.Rect(
                col2_x - 100,  # Широкая область клика
                y_offset + i * 50 - 20,
                200,
                40,
            )
            if item_rect.collidepoint(mouse_pos):
            # Если уже выбран элемент из первого столбца — создаём пару
                if self.selected_item and self.selected_item[0] == "column1":
                    col1_idx = self.selected_item[1]
                    self.current_matches[col1_idx] = i  # column1[col1_idx] ↔ column2[i]
                    self.selected_item = None  # Сброс выбора
                else:
                # Иначе просто выбираем элемент второго столбца
                    if self.selected_item == ("column2", i):
                        self.selected_item = None
                    else:
                        self.selected_item = ("column2", i)
                return
    
    def check_answer(self, _, screen, font):
        # Проверяем, все ли правильные пары созданы
        is_correct = True
        for col1_idx, col2_idx in self.correct_matches:
            if self.current_matches.get(col1_idx) != col2_idx:
                is_correct = False
                break

        if is_correct and len(self.current_matches) == len(self.correct_matches):
            self.reward(screen, font)
            return True
        else:
            self.punish(screen, font)
            return False


def attempt_coin_pickup(player, coin):
    global current_question_index
    if current_question_index >= len(questions):
        print("Все вопросы заданы.")
        return False

    question = questions[current_question_index]

    input_text = ""
    answered_correctly = False
    running_question = True

    while running_question:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # Обработка для MultipleChoiceQuestion
            if isinstance(question, MultipleChoiceQuestion):
                if event.type == pygame.KEYDOWN:
                    # Нажатие цифр 1-9 для выбора варианта
                    if event.unicode.isdigit():
                        num = int(event.unicode) - 1
                        question.select_option(num)
                    elif event.key == pygame.K_RETURN and question.selected_option is not None:
                        answered_correctly = question.check_answer(screen, font)
                        running_question = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        answered_correctly = question.check_answer(event.pos, screen, font)
                        running_question = False

            # Обработка для TextAnswerQuestion
            elif isinstance(question, TextAnswerQuestion):
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        answered_correctly = question.check_answer(input_text, screen, font)
                        running_question = False
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

            # Обработка для MatchingQuestion
            elif isinstance(question, MatchingQuestion):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    question.handle_click(event.pos, font, screen)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    answered_correctly = question.check_answer(None, screen, font)
                    running_question = False

        screen.fill(BROWN)
        question.display_question(screen, font)

        if isinstance(question, TextAnswerQuestion):
            input_surface = font.render(input_text, True, WHITE)
            input_rect = input_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
            pygame.draw.rect(screen, WHITE, input_rect.inflate(10, 10), 2)
            screen.blit(input_surface, input_rect)

        pygame.display.flip()

    if answered_correctly:
        player.coins += 1
        print("Клубничка добавлена!")

    current_question_index += 1
    return True

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
    ["4*x","4x","4 * x", "4х", "4*х","4 * х"]
)

textQuestion2 = TextAnswerQuestion(
    "Как называется точка, в которой производная функции равна нулю?",
    ["точка экстремума", "экстремума"]
)

textQuestion3 = TextAnswerQuestion(
    "Сколько существует замечательных пределов?",
    ["2","два"]
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
    screen.fill(BROWN)
    text_surface = font.render(f"Клубнички: {player.coins}", True, WHITE)
    text_rect = text_surface.get_rect(topleft=(10, 10))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()

pygame.quit()

