import pygame

pygame.init()

# Константы
BROWN = (50, 35, 12)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

font = pygame.font.Font('Asset/PublicPixel-rv0pA.ttf', 16)  # Шрифт для текста

class LearningElement:
    def __init__(self, question, second_attempt):
        self.question = question
        self.answered = False
        # Используем переданный флаг второй попытки
        self.attempts_left = 2 if second_attempt else 1

    def display_question(self, screen, font, y_offset=50):
        question_surface = font.render(self.question, True, WHITE)
        question_rect = question_surface.get_rect(center=(screen.get_width() // 2, y_offset))
        screen.blit(question_surface, question_rect)

    def reward(self, screen, font):
        self.answered = True
        text_surface = font.render("Правильный ответ! Клубничка получена.", True, GREEN)
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()
        pygame.time.delay(1000)

    def punish(self, screen, font):
        self.attempts_left -= 1
        if self.attempts_left > 0:
            text_surface = font.render("Неправильный ответ! Попробуйте еще раз.", True, RED)
        else:
            text_surface = font.render("Неправильный ответ! Больше попыток нет.", True, RED)
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()
        pygame.time.delay(1000)
        return self.attempts_left > 0

class MultipleChoiceQuestion(LearningElement):
    def __init__(self, question, options, correct_answer_index, second_attempt):
        super().__init__(question, second_attempt)
        self.options = options
        self.correct_answer_index = correct_answer_index
        self.option_rects = []
        self.selected_option = None

    def display_question(self, screen, font, y_offset=50):
        super().display_question(screen, font, y_offset)
        self.option_rects = []
        for i, option in enumerate(self.options):
            color = GREEN if self.selected_option == i else WHITE
            option_surface = font.render(f"{i+1}. {option}", True, color)
            option_rect = option_surface.get_rect(center=(screen.get_width() // 2, y_offset + 50 + (i * 40)))
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
            return not self.punish(screen, font)

class TextAnswerQuestion(LearningElement):
    def __init__(self, question, correct_answers, second_attempt):
        super().__init__(question, second_attempt)
        self.correct_answers = [ans.lower().strip() for ans in correct_answers]

    def check_answer(self, answer, screen, font):
        normalized_answer = answer.lower().strip()
        normalized_answer = " ".join(normalized_answer.split())
        if normalized_answer in self.correct_answers:
            self.reward(screen, font)
            return True
        else:
            return not self.punish(screen, font)

class MatchingQuestion(LearningElement):
    def __init__(self, question, column1, column2, correct_matches, second_attempt):
        super().__init__(question, second_attempt)
        self.column1 = column1
        self.column2 = column2
        self.correct_matches = correct_matches
        self.current_matches = {}
        self.selected_item = None

    def display_question(self, screen, font, y_offset=100):
        super().display_question(screen, font, y_offset - 50)
        
        col1_x = screen.get_width() // 4
        col2_x = screen.get_width() * 3 // 4
        
        # Отображение элементов первого столбца
        for i, item in enumerate(self.column1):
            item_surface = font.render(item, True, WHITE)
            item_rect = item_surface.get_rect(center=(col1_x, y_offset + i * 50))
            pygame.draw.rect(screen, WHITE, item_rect.inflate(10, 10), 2)
            screen.blit(item_surface, item_rect)
            if self.selected_item == ("column1", i):
                pygame.draw.rect(screen, GREEN, item_rect.inflate(14, 14), 2)

        # Отображение элементов второго столбца
        for i, item in enumerate(self.column2):
            item_surface = font.render(item, True, WHITE)
            item_rect = item_surface.get_rect(center=(col2_x, y_offset + i * 50))
            pygame.draw.rect(screen, WHITE, item_rect.inflate(10, 10), 2)
            screen.blit(item_surface, item_rect)
            if self.selected_item == ("column2", i):
                pygame.draw.rect(screen, GREEN, item_rect.inflate(14, 14), 2)

        # Отрисовка соединений
        for col1_idx, col2_idx in self.current_matches.items():
            start_pos = (col1_x + item_rect.width // 2 + 10, y_offset + col1_idx * 50)
            end_pos = (col2_x - item_rect.width // 2 - 10, y_offset + col2_idx * 50)
            pygame.draw.line(screen, RED, start_pos, end_pos, 2)

    def handle_click(self, mouse_pos, screen, y_offset=100):  # Добавлен параметр screen
        col1_x = screen.get_width() // 4
        col2_x = screen.get_width() * 3 // 4

        # Проверка клика по первому столбцу
        for i in range(len(self.column1)):
            item_rect = pygame.Rect(
                col1_x - 100,
                y_offset + i * 50 - 20,
                200,
                40,
            )
            if item_rect.collidepoint(mouse_pos):
                if self.selected_item == ("column1", i):
                    self.selected_item = None
                else:
                    if self.selected_item and self.selected_item[0] == "column2":
                        col2_idx = self.selected_item[1]
                        for k, v in list(self.current_matches.items()):
                            if v == col2_idx:
                                del self.current_matches[k]
                        self.current_matches[i] = col2_idx
                        self.selected_item = None
                    else:
                        self.selected_item = ("column1", i)
                return

        # Проверка клика по второму столбцу
        for i in range(len(self.column2)):
            item_rect = pygame.Rect(
                col2_x - 100,
                y_offset + i * 50 - 20,
                200,
                40,
            )
            if item_rect.collidepoint(mouse_pos):
                if self.selected_item == ("column2", i):
                    self.selected_item = None
                else:
                    if self.selected_item and self.selected_item[0] == "column1":
                        col1_idx = self.selected_item[1]
                        if col1_idx in self.current_matches:
                            del self.current_matches[col1_idx]
                        self.current_matches[col1_idx] = i
                        self.selected_item = None
                    else:
                        self.selected_item = ("column2", i)
                return
                
    def check_answer(self, screen, font):
        is_correct = True
        for col1_idx, col2_idx in self.correct_matches:
            if self.current_matches.get(col1_idx) != col2_idx:
                is_correct = False
                break

        if is_correct and len(self.current_matches) == len(self.correct_matches):
            self.reward(screen, font)
            return True
        else:
            return not self.punish(screen, font)

# Описания вопросов
question_descriptions = [
    ("multiple", "Что изучает математический анализ?", 
     ["Изменения функций, пределы, производные и интегралы", 
      "Теорию чисел и их делимость", 
      "Свойства геометрических фигур и их соотношения"],
     0),
    ("multiple", "Что такое производная функции в точке?",
     ["Площадь под графиком функции",
      "Предел отношения приращения функции к приращению аргумента",
      "Максимальное значение функции"],
     1),
    ("multiple", "Как называется функция, производная которой равна заданной функции?",
     ["Ряд Тейлора", "Целевая функция", "Первообразная"],
     2),
    ("text", "Чему равно производная функции 2*x^2?",
     ["4*x", "4x", "4 * x", "4х", "4*х", "4 * х"]),
    ("text", "Как называется точка, в которой производная функции равна нулю?",
     ["точка экстремума", "экстремума"]),
    ("text", "Сколько существует замечательных пределов?",
     ["2", "два"]),
    ("matching", "Сопоставьте функцию с её производной:",
     ["e^x", "sin(x)", "ln(x)"],
     ["1/x", "e^x", "cos(x)"],
     [(0, 1), (1, 2), (2, 0)]),
    ("matching", "Сопоставьте функцию с её названием:",
     ["lim (sin(x)/x)", "сумма функции 1/(n^a)", "Интеграл f(x)dx"],
     ["Интеграл Римана", "Обобщённый гармонический ряд", "Первый замечательный предел"],
     [(0, 2), (1, 1), (2, 0)]),
    ("matching", "Сопоставьте интеграл функции с его значением:",
     ["Интеграл функции x", "Интеграл функции e^x", "Интеграл функции 1/(a^2+x^2)"],
     ["1/a*arctg(x/a) + C", "x^2/2 + C", "e^x + C"],
     [(0, 1), (1, 2), (2, 0)])
]

def start_question(player, window, current_question_index, second_attempt):
    if current_question_index >= len(question_descriptions):
        print("Все вопросы заданы.")
        return False
    
    # Создаем вопрос с учетом флага второй попытки
    desc = question_descriptions[current_question_index]
    question_type = desc[0]
    
    if question_type == "multiple":
        question = MultipleChoiceQuestion(desc[1], desc[2], desc[3], second_attempt)
    elif question_type == "text":
        question = TextAnswerQuestion(desc[1], desc[2], second_attempt)
    elif question_type == "matching":
        question = MatchingQuestion(desc[1], desc[2], desc[3], desc[4], second_attempt)
    else:
        return False
    
    input_text = ""
    answered_correctly = False
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if isinstance(question, MultipleChoiceQuestion):
                if event.type == pygame.KEYDOWN:
                    if event.unicode.isdigit():
                        num = int(event.unicode) - 1
                        question.select_option(num)
                    elif event.key == pygame.K_RETURN and question.selected_option is not None:
                        answered_correctly = question.check_answer(window, font)
                        if answered_correctly or question.attempts_left <= 0:
                            running = False
                
            elif isinstance(question, TextAnswerQuestion):
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        answered_correctly = question.check_answer(input_text, window, font)
                        if answered_correctly or question.attempts_left <= 0:
                            running = False
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode
                        
            elif isinstance(question, MatchingQuestion):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # Передаем window в handle_click
                        question.handle_click(event.pos, window, 150)
                    elif event.button == 3:
                        question.selected_item = None
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        answered_correctly = question.check_answer(window, font)
                        if answered_correctly or question.attempts_left <= 0:
                            running = False
                    elif event.key == pygame.K_ESCAPE:
                        question.current_matches = {}
                        question.selected_item = None
        
        # Отрисовка
        window.fill(BROWN)
        question.display_question(window, font, 150)
        
        if isinstance(question, TextAnswerQuestion):
            input_surface = font.render(input_text, True, WHITE)
            input_rect = input_surface.get_rect(center=(window.get_width() // 2, window.get_height() - 100))
            pygame.draw.rect(window, WHITE, input_rect.inflate(10, 10), 2)
            window.blit(input_surface, input_rect)
        
        pygame.display.flip()
    
    if answered_correctly:
        player.COLLECTED += 1
        return True
    
    return False