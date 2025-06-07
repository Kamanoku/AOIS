import unittest
from unittest.mock import patch, MagicMock
import io
import sys
from main import (
    binary_add,
    process_words,
    apply_logical_function,
    compare_words,
    search_by_gl,
    extract_words_diagonal,
    generate_random_matrix,
    main
)

class TestBinaryFunctions(unittest.TestCase):

    def test_binary_add(self):
        self.assertEqual(binary_add('0011', '0010', 5), '00101')
        self.assertEqual(binary_add('1111', '0001', 4), '0000')  # 15+1 = 16 → 0 (mod 16)
        self.assertEqual(binary_add('0000', '0000', 4), '0000')
        self.assertEqual(binary_add('11111', '00001', 5), '00000')  # 31+1 = 32 → 0 (mod 32)
        self.assertEqual(binary_add('1010', '0101', 5), '01111')  # 10+5 = 15

    def test_process_words_match(self):
        word = '1111010100000000'  # V=111, A=1010 (10), B=0000 (0)
        result = process_words([word], key_v='111')
        # A+B = 10 + 0 = 10 → 01010
        self.assertEqual(result[0], '1111010100010010')

    def test_process_words_no_match(self):
        words = ['1101010100000000']  # V != 111 → no change
        result = process_words(words, key_v='111')
        self.assertEqual(result[0], '1101010100000000')

    def test_apply_logical_function(self):
        self.assertEqual(apply_logical_function('1100', '1010', 'f0'), '0000')
        self.assertEqual(apply_logical_function('1100', '1010', 'f5'), '1010')
        self.assertEqual(apply_logical_function('1100', '1010', 'f10'), '0101')
        self.assertEqual(apply_logical_function('1100', '1010', 'f15'), '1111')

    def test_compare_words(self):
        self.assertEqual(compare_words('1111', '0001'), 'g')
        self.assertEqual(compare_words('0001', '1111'), 'l')
        self.assertEqual(compare_words('1010', '1010'), 'e')

    def test_search_by_gl_greater(self):
        words = ['1111000011110000', '0000000000000000']
        result = search_by_gl(words, '0000000000000000', 'g')
        self.assertEqual(result, [(0, '1111000011110000')])

    def test_search_by_gl_less(self):
        words = ['0000000000000000', '1111000011110000']
        result = search_by_gl(words, '1111000011110000', 'l')
        self.assertEqual(result, [(0, '0000000000000000')])

    def test_search_by_gl_equal_none(self):
        words = ['0000000000000000', '1111111111111111']
        self.assertEqual(search_by_gl(words, '1111111111111111', 'g'), [])
        self.assertEqual(search_by_gl(words, '0000000000000000', 'l'), [])

    def test_extract_words_diagonal(self):
        matrix = [
            list("1000000000000000"),
            list("0100000000000000"),
            list("0010000000000000"),
            list("0001000000000000"),
            list("0000100000000000"),
            list("0000010000000000"),
            list("0000001000000000"),
            list("0000000100000000"),
            list("0000000010000000"),
            list("0000000001000000"),
            list("0000000000100000"),
            list("0000000000010000"),
            list("0000000000001000"),
            list("0000000000000100"),
            list("0000000000000010"),
            list("0000000000000001"),
        ]
        matrix = [[int(c) for c in row] for row in matrix]
        words = extract_words_diagonal(matrix)
        self.assertEqual(len(words), 16)
        for word in words:
            self.assertEqual(len(word), 16)
        self.assertEqual(words[0], '1000000000000000')

    def test_generate_random_matrix(self):
        matrix = generate_random_matrix()
        self.assertEqual(len(matrix), 16)
        for row in matrix:
            self.assertEqual(len(row), 16)
            for bit in row:
                self.assertIn(bit, [0, 1])

class TestMainFunction(unittest.TestCase):
    
    @patch('main.generate_random_matrix')
    @patch('main.print_matrix')
    @patch('main.extract_words_diagonal')
    @patch('main.process_words')
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_full_flow(self, mock_stdout, mock_input, mock_process_words, 
                          mock_extract_words, mock_print_matrix, mock_gen_matrix):
        # Настраиваем моки
        mock_matrix = [[0]*16 for _ in range(16)]
        mock_gen_matrix.return_value = mock_matrix
        
        mock_words = ['0'*16]*16
        mock_extract_words.return_value = mock_words
        
        mock_processed_words = ['1'*16]*16
        mock_process_words.return_value = mock_processed_words
        
        # Эмулируем пользовательский ввод
        mock_input.side_effect = [
            '0', '1',  # Индексы для логической операции
            'f5',      # Выбор функции
            '0000000000000000',  # Шаблон для поиска
            'g'       # Режим поиска
        ]
        
        # Запускаем main
        main()
        
        # Проверяем вывод
        output = mock_stdout.getvalue()
        
        # Основные проверки
        self.assertIn("Сгенерированная матрица 16x16:", output)
        self.assertIn("Извлечённые слова:", output)
        self.assertIn("Обработанные слова", output)
        self.assertIn("Выберите два слова по индексам", output)
        self.assertIn("Выберите логическую функцию:", output)
        self.assertIn("Результат применения функции f5", output)
        self.assertIn("=== Поиск по соответствию (g/l) ===", output)
        
        # Проверяем вызовы функций
        mock_gen_matrix.assert_called_once_with()
        mock_print_matrix.assert_called_once_with(mock_matrix)
        mock_extract_words.assert_called_once_with(mock_matrix)
        mock_process_words.assert_called_once_with(mock_words, '111')
        
    @patch('main.generate_random_matrix')
    @patch('builtins.input')
    def test_main_invalid_inputs(self, mock_input, mock_gen_matrix):
        # Настраиваем моки
        mock_matrix = [[0]*16 for _ in range(16)]
        mock_gen_matrix.return_value = mock_matrix
        
        # Эмулируем неверный ввод
        mock_input.side_effect = [
            '20', '-1',  # Неверные индексы
            'invalid_func',  # Неверная функция
            'short',  # Неверный шаблон
            'x'      # Неверный режим
        ]
        
        # Перенаправляем stdout для проверки вывода
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        # Запускаем main (не должен упасть с ошибкой)
        main()
        
        # Возвращаем stdout
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        self.assertIn("Ошибка: некорректный ввод.", output)
        self.assertIn("Ошибка: неверный шаблон или режим.", output)

if __name__ == '__main__':
    unittest.main()