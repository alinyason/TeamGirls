import unittest
from unittest.mock import patch
from game import guess_number

class TestGuessNumber(unittest.TestCase):
    """Полный набор тестов для игры 'Угадай число'"""
    
    # ---------------------------
    # 1. Тесты на корректное поведение
    # ---------------------------
    
    @patch('builtins.input', side_effect=['5'])
    def test_win_on_first_try(self, mock_input):
        """Игрок угадывает число с первой попытки"""
        with patch('random.randint', return_value=5):
            result = guess_number()
            self.assertTrue(result, "Должен вернуть True при угадывании")

    @patch('builtins.input', side_effect=['3', '5'])
    def test_win_on_second_try(self, mock_input):
        """Игрок угадывает со второй попытки"""
        with patch('random.randint', return_value=5):
            result = guess_number()
            self.assertTrue(result, "Должен вернуть True при угадывании")

    @patch('builtins.input', side_effect=['1', '2', '3'])
    def test_lose_all_attempts(self, mock_input):
        """Игрок исчерпывает все попытки"""
        with patch('random.randint', return_value=5):
            result = guess_number()
            self.assertFalse(result, "Должен вернуть False при проигрыше")

    # ---------------------------
    # 2. Тесты на обработку ошибок ввода
    # ---------------------------
    
    @patch('builtins.input', side_effect=['hello', '5'])
    def test_invalid_input_text(self, mock_input):
        """Обработка ввода текста вместо числа"""
        with patch('random.randint', return_value=5):
            result = guess_number()
            self.assertTrue(result, "Должен принять число после неверного ввода")

    @patch('builtins.input', side_effect=['0', '11', '5'])
    def test_invalid_input_range(self, mock_input):
        """Обработка чисел вне диапазона"""
        with patch('random.randint', return_value=5):
            result = guess_number()
            self.assertTrue(result, "Должен принять число из диапазона 1-10")

    @patch('builtins.input', side_effect=['-5', '5'])
    def test_negative_input(self, mock_input):
        """Обработка отрицательных чисел"""
        with patch('random.randint', return_value=5):
            result = guess_number()
            self.assertTrue(result, "Должен отклонить отрицательное число")

    # ---------------------------
    # 3. Тест на корректность диапазона
    # ---------------------------
    
    def test_number_in_range_1_to_10(self):
        """Проверка, что число всегда в диапазоне 1-10"""
        with patch('random.randint') as mock_randint:
            # 1. Настраиваем mock всегда возвращать 5
            mock_randint.return_value = 5
            
            # 2. Эмулируем быстрый выигрыш
            with patch('builtins.input', return_value='5'):
                guess_number()
                
                # 3. Проверяем, что randint вызывался с (1, 10)
                mock_randint.assert_called_with(1, 10)
                
                # 4. Дополнительная проверка через call_args
                args, _ = mock_randint.call_args
                self.assertEqual(args, (1, 10), 
                    "randint должен вызываться с аргументами (1, 10)")

if __name__ == "__main__":
    unittest.main(verbosity=2)  # Подробный вывод
