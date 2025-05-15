import unittest
import itertools
import re
from unittest.mock import patch, call
from io import StringIO
from main import evaluate_expression, truth_table, get_normal_forms, main

class TestLogicFunctions(unittest.TestCase):
    def setUp(self):
        self.variables = ['a', 'b', 'c']
    
    def test_evaluate_expression_basic_operations(self):
        # Тестирование базовых операций
        self.assertEqual(evaluate_expression("a&b", {'a':1, 'b':1}), 1)
        self.assertEqual(evaluate_expression("a|b", {'a':0, 'b':0}), 0)
        self.assertEqual(evaluate_expression("!a", {'a':1}), 0)
        self.assertEqual(evaluate_expression("a->b", {'a':1, 'b':0}), 0)
        self.assertEqual(evaluate_expression("a<->b", {'a':0, 'b':0}), 1)
    
    def test_evaluate_expression_complex(self):
        # Тестирование комплексных выражений
        self.assertEqual(evaluate_expression("a&(b|c)", {'a':1, 'b':0, 'c':1}), 1)
        self.assertEqual(evaluate_expression("!a|(b<->c)", {'a':1, 'b':0, 'c':1}), 0)
        self.assertEqual(evaluate_expression("(a->b)&(!c|a)", {'a':1, 'b':0, 'c':1}), 0)
    
    def test_evaluate_expression_errors(self):
        # Тестирование обработки ошибок
        with self.assertRaises(ValueError):
            evaluate_expression("a&", {'a':1})
        with self.assertRaises(ValueError):
            evaluate_expression("(a|b", {'a':1, 'b':1})
        with self.assertRaises(ValueError):
            evaluate_expression("a*b", {'a':1, 'b':1})
    
    def test_truth_table_basic(self):
        # Тестирование таблиц истинности для базовых операций
        self.assertEqual(truth_table("a&b", ['a', 'b']), [
            (0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 1, 1)
        ])
        self.assertEqual(truth_table("a|b", ['a', 'b']), [
            (0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 1)
        ])
    
    def test_truth_table_variable_order(self):
        # Тестирование порядка переменных в таблице истинности
        table = truth_table("a&b", ['b', 'a'])
        self.assertEqual(table, [
            (0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 1)
        ])
    
    def test_get_normal_forms(self):
        # Тестирование нормальных форм
        and_table = [(0,0,0), (0,1,0), (1,0,0), (1,1,1)]
        forms = get_normal_forms(and_table, ['a', 'b'])
        self.assertEqual(forms['sdnf'], "(a ∧ b)")
        self.assertEqual(forms['sknf'], "(a ∨ b) ∧ (a ∨ !b) ∧ (!a ∨ b)")
        self.assertEqual(forms['numeric_sdnf'], "(3) ∨")
        self.assertEqual(forms['numeric_sknf'], "(0, 1, 2) ∧")
        self.assertEqual(forms['index_form'], "1 - 0001")
    
    def test_get_normal_forms_empty(self):
        # Тестирование крайних случаев
        always_true = [(0,1), (1,1)]
        forms = get_normal_forms(always_true, ['a'])
        self.assertEqual(forms['sdnf'], "(!a) ∨ (a)")
        self.assertEqual(forms['sknf'], "1")
        
        always_false = [(0,0), (1,0)]
        forms = get_normal_forms(always_false, ['a'])
        self.assertEqual(forms['sdnf'], "0")
        self.assertEqual(forms['sknf'], "(a) ∧ (!a)")

    @patch('builtins.input', return_value='a&b')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_basic(self, mock_stdout, mock_input):
        # Тестирование основного потока выполнения
        main()
        output = mock_stdout.getvalue()
        
        # Проверяем приглашение к вводу
        assert "Введите логическую функцию (переменные a-e, операции &, |, !, ->, <->)" in output
        
        # Проверяем вывод таблицы истинности
        assert "Таблица истинности:" in output
        assert "a | b | F" in output
        assert "0 | 0 | 0" in output
        assert "0 | 1 | 0" in output
        assert "1 | 0 | 0" in output
        assert "1 | 1 | 1" in output
        
        # Проверяем нормальные формы
        assert "Совершенная дизъюнктивная нормальная форма (СДНФ):" in output
        assert "(a ∧ b)" in output
        
        assert "Совершенная конъюнктивная нормальная форма (СКНФ):" in output
        assert "(a ∨ b) ∧ (a ∨ !b) ∧ (!a ∨ b)" in output
        
        # Проверяем числовые формы
        assert "Числовая форма СДНФ:" in output
        assert "(3) ∨" in output
        
        assert "Числовая форма СКНФ:" in output
        assert "(0, 1, 2) ∧" in output
        
        # Проверяем индексную форму
        assert "Индексная форма:" in output
        assert "1 - 0001" in output
    
    @patch('builtins.input', return_value='')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_no_variables(self, mock_stdout, mock_input):
        # Тестирование случая, когда не введены переменные
        main()
        output = mock_stdout.getvalue()
        assert "Ошибка: не найдены переменные" in output



    @patch('builtins.input', return_value='a&b&c')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_three_variables(self, mock_stdout, mock_input):
        # Тестирование случая с тремя переменными
        main()
        output = mock_stdout.getvalue()

        assert "Таблица истинности:" in output
        assert "a | b | c | F" in output
        assert "Совершенная дизъюнктивная нормальная форма (СДНФ):" in output
        assert "(a ∧ b ∧ c)" in output
        assert "Совершенная конъюнктивная нормальная форма (СКНФ):" in output

    @patch('builtins.input', return_value='a|b|c')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_three_variables_or(self, mock_stdout, mock_input):
        # Тестирование случая с тремя переменными и операцией ИЛИ
        main()
        output = mock_stdout.getvalue()

        assert "Таблица истинности:" in output
        assert "a | b | c | F" in output
        assert "Совершенная дизъюнктивная нормальная форма (СДНФ):" in output
        assert "(!a ∧ !b ∧ c) ∨ (!a ∧ b ∧ !c) ∨ (!a ∧ b ∧ c) ∨ (a ∧ !b ∧ !c) ∨ (a ∧ !b ∧ c) ∨ (a ∧ b ∧ !c) ∨ (a ∧ b ∧ c)" in output
        assert "Совершенная конъюнктивная нормальная форма (СКНФ):" in output
        assert "(a ∨ b ∨ c)" in output

if __name__ == '__main__':
    unittest.main()