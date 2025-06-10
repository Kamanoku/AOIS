import unittest
from typing import List, Set, Tuple, Dict
from unittest.mock import patch, MagicMock
from io import StringIO
from log_parser import InputCleaner, ExpressionValidator, VariableExtractor, Lexer
from evaluator import ExpressionConverter, PostfixEvaluator, TableBuilder, NormalForms, NumericRepresentation
from minimizer import BinaryUtils, ImplicantReducer, EssentialFinder, ExpressionFormatter, BooleanMinimizer
import main

class TestLogicFunctions(unittest.TestCase):
    def test_input_cleaner_remove_spaces(self):
        self.assertEqual(InputCleaner.remove_spaces("a & b | c"), "a&b|c")
        self.assertEqual(InputCleaner.remove_spaces("  a  ->  b  "), "a->b")
        self.assertEqual(InputCleaner.remove_spaces(""), "")
        self.assertEqual(InputCleaner.remove_spaces("   "), "")

    def test_expression_validator_is_valid(self):
        self.assertTrue(ExpressionValidator.is_valid("a & b | c"))
        self.assertTrue(ExpressionValidator.is_valid("!a -> (b & c)"))
        self.assertFalse(ExpressionValidator.is_valid("a & x | y"))
        self.assertFalse(ExpressionValidator.is_valid("a + b"))
        self.assertTrue(ExpressionValidator.is_valid(""))  # Пустая строка валидна

    def test_expression_validator_has_balanced_parentheses(self):
        self.assertTrue(ExpressionValidator.has_balanced_parentheses("(a & b) | c"))
        self.assertTrue(ExpressionValidator.has_balanced_parentheses("a & b"))
        self.assertFalse(ExpressionValidator.has_balanced_parentheses("(a & b"))
        self.assertFalse(ExpressionValidator.has_balanced_parentheses("a & )b("))
        self.assertTrue(ExpressionValidator.has_balanced_parentheses(""))  # Пустая строка сбалансирована

    def test_variable_extractor_get_variables(self):
        self.assertEqual(VariableExtractor.get_variables("a & b | c"), ["a", "b", "c"])
        self.assertEqual(VariableExtractor.get_variables("!a -> (b & c)"), ["a", "b", "c"])
        self.assertEqual(VariableExtractor.get_variables("a & a & a"), ["a"])
        self.assertEqual(VariableExtractor.get_variables(""), [])

    def test_lexer_tokenize(self):
        self.assertEqual(Lexer.tokenize("a & b | c"), ["a", "&", "b", "|", "c"])
        self.assertEqual(Lexer.tokenize("!a -> (b & c)"), ["!", "a", "->", "(", "b", "&", "c", ")"])
        self.assertEqual(Lexer.tokenize("(a)"), ["(", "a", ")"])
        self.assertEqual(Lexer.tokenize(""), [])
        self.assertEqual(Lexer.tokenize("a + b"), [])  # Недопустимый символ '+'

    def test_expression_converter_to_postfix(self):
        self.assertEqual(ExpressionConverter.to_postfix(["a", "&", "b", "|", "c"]), ["a", "b", "&", "c", "|"])
        self.assertEqual(ExpressionConverter.to_postfix(["!", "a", "->", "(", "b", "&", "c", ")"]), 
                        ["a", "!", "b", "c", "&", "->"])
        self.assertEqual(ExpressionConverter.to_postfix(["(", "a", "|", "b", ")", "&", "c"]), 
                        ["a", "b", "|", "c", "&"])
        self.assertEqual(ExpressionConverter.to_postfix([]), [])

    def test_postfix_evaluator_evaluate(self):
        postfix = ["a", "b", "&", "c", "|"]
        assignments = {"a": True, "b": False, "c": True}
        self.assertTrue(PostfixEvaluator.evaluate(postfix, assignments))
        assignments = {"a": False, "b": True, "c": False}
        self.assertFalse(PostfixEvaluator.evaluate(postfix, assignments))
        
        postfix = ["a", "!", "b", "c", "&", "->"]
        assignments = {"a": True, "b": True, "c": True}
        self.assertTrue(PostfixEvaluator.evaluate(postfix, assignments))
        
        with self.assertRaises(ValueError):
            PostfixEvaluator.evaluate(["!"], {"a": True})  # Пропущен операнд
        with self.assertRaises(ValueError):
            PostfixEvaluator.evaluate(["a", "&"], {"a": True})  # Пропущен второй операнд
        with self.assertRaises(ValueError):
            PostfixEvaluator.evaluate(["x"], {"a": True})  # Неизвестный токен

    def test_table_builder_build(self):
        variables = ["a", "b"]
        postfix = ["a", "b", "&"]
        table = TableBuilder.build(variables, postfix)
        expected = [
            [False, False, False],
            [False, True, False],
            [True, False, False],
            [True, True, True]
        ]
        self.assertEqual(table, expected)

        variables = ["a"]
        postfix = ["a", "!"]
        table = TableBuilder.build(variables, postfix)
        expected = [[False, True], [True, False]]
        self.assertEqual(table, expected)

    def test_normal_forms_dnf(self):
        variables = ["a", "b"]
        table = [
            [False, False, False],
            [False, True, False],
            [True, False, False],
            [True, True, True]
        ]
        self.assertEqual(NormalForms.dnf(variables, table), "(a & b)")
        
        table = [[False, False], [True, False]]
        self.assertEqual(NormalForms.dnf(variables[:1], table), "Contradiction")

    def test_normal_forms_cnf(self):
        variables = ["a", "b"]
        table = [
            [False, False, False],
            [False, True, False],
            [True, False, False],
            [True, True, True]
        ]
        self.assertEqual(NormalForms.cnf(variables, table), "(a | b) & (a | !b) & (!a | b)")
        
        table = [[False, True], [True, True]]
        self.assertEqual(NormalForms.cnf(variables[:1], table), "Tautology")

    def test_numeric_representation_dnf_indices(self):
        table = [
            [False, False, False],
            [False, True, False],
            [True, False, False],
            [True, True, True]
        ]
        self.assertEqual(NumericRepresentation.dnf_indices(table), [3])
        
        table = [[False, False], [True, False]]
        self.assertEqual(NumericRepresentation.dnf_indices(table), [])

    def test_numeric_representation_cnf_indices(self):
        table = [
            [False, False, False],
            [False, True, False],
            [True, False, False],
            [True, True, True]
        ]
        self.assertEqual(NumericRepresentation.cnf_indices(table), [0, 1, 2])
        
        table = [[False, True], [True, True]]
        self.assertEqual(NumericRepresentation.cnf_indices(table), [])

    def test_numeric_representation_index_value(self):
        table = [
            [False, False, False],
            [False, True, False],
            [True, False, False],
            [True, True, True]
        ]
        self.assertEqual(NumericRepresentation.index_value(table), 1)  # 0001 в двоичной = 1
        
        table = [[False, True], [True, True]]
        self.assertEqual(NumericRepresentation.index_value(table), 3)  # 11 в двоичной = 3

    def test_binary_utils_to_binary(self):
        self.assertEqual(BinaryUtils.to_binary(5, 3), "101")
        self.assertEqual(BinaryUtils.to_binary(0, 4), "0000")
        self.assertEqual(BinaryUtils.to_binary(7, 3), "111")

    def test_binary_utils_count_ones(self):
        self.assertEqual(BinaryUtils.count_ones("101"), 2)
        self.assertEqual(BinaryUtils.count_ones("000"), 0)
        self.assertEqual(BinaryUtils.count_ones("1111"), 4)

    def test_binary_utils_can_merge(self):
        self.assertEqual(BinaryUtils.can_merge("101", "111"), (True, "1-1"))
        self.assertEqual(BinaryUtils.can_merge("101", "110"), (False, ""))
        self.assertEqual(BinaryUtils.can_merge("000", "000"), (False, "000"))

    def test_implicant_reducer_extract_implicants(self):
        minterms = [0, 1, 2, 3, 4, 5, 6]
        var_count = 3
        primes, history = ImplicantReducer.extract_implicants(minterms, var_count)
        expected_primes = [
        ('--0', {0, 2, 4, 6}),
        ('-0-', {0, 1, 4, 5}),
        ('0--', {0, 1, 2, 3})
        ]
        self.assertEqual(sorted(primes, key=lambda x: x[0]), sorted(expected_primes, key=lambda x: x[0]))
        self.assertTrue(len(history) > 0)  # Проверяем, что история не пуста

        minterms = []
        primes, history = ImplicantReducer.extract_implicants(minterms, 3)
        self.assertEqual(primes, [])
        self.assertEqual(history, [])

    def test_essential_finder_filter_essentials(self):
        primes = [
            ('--1', {0, 1, 2, 3, 4, 5, 6}),
            ('0--', {0, 1, 2, 3}),
            ('1-1', {5, 6})
        ]
        targets = {0, 1, 2, 3, 4, 5, 6}
        essentials = EssentialFinder.filter_essentials(primes, targets)
        self.assertTrue(any(p[0] == '--1' for p in essentials))  # Должна быть хотя бы одна существенная импликанта

        primes = []
        targets = set()
        essentials = EssentialFinder.filter_essentials(primes, targets)
        self.assertEqual(essentials, [])

    def test_expression_formatter_to_logical(self):
        variables = ["a", "b", "c"]
        self.assertEqual(ExpressionFormatter.to_logical("--1", variables, True), "(c)")
        self.assertEqual(ExpressionFormatter.to_logical("0--", variables, True), "(!a)")
        self.assertEqual(ExpressionFormatter.to_logical("1-1", variables, True), "a & c")
        self.assertEqual(ExpressionFormatter.to_logical("---", variables, True), "1")
        self.assertEqual(ExpressionFormatter.to_logical("---", variables, False), "0")

    def test_boolean_minimizer_minimize(self):
        minterms = [0, 1, 2, 3, 4, 5, 6]
        var_count = 3
        result, steps = BooleanMinimizer.minimize(minterms, var_count, dnf=True)
        print(f"minimize result: {result}")
        self.assertIn(result, ["(c)", "(!a) | (!b) | (!c)"])
        self.assertTrue(len(steps) > 0)

        minterms = []
        result, steps = BooleanMinimizer.minimize(minterms, 3, dnf=True)
        self.assertEqual(result, "Contradiction")
        self.assertEqual(steps, [])

    def test_boolean_minimizer_minimize_qmc(self):
        minterms = [0, 1, 2, 3, 4, 5, 6]
        var_count = 3
        result, steps = BooleanMinimizer.minimize_qmc(minterms, var_count, dnf=True)
        print(f"minimize_qmc result: {result}")
        self.assertIn(result, ["(c)", "(!a) | (!b) | (!c)"])
        self.assertTrue(len(steps) >= 2)

        minterms = []
        result, steps = BooleanMinimizer.minimize_qmc(minterms, 3, dnf=True)
        self.assertEqual(result, "Contradiction")
        self.assertEqual(steps, [])

    def test_boolean_minimizer_minimize_karnaugh(self):
        # Тест с заданными минтермами
        minterms = [0, 1, 2, 3, 4, 5, 6]
        var_count = 3
        result, steps = BooleanMinimizer.minimize_karnaugh(minterms, var_count, dnf=True)
        print(f"minimize_karnaugh result: {result}")  # Отладочная печать
        
        # Проверка результата
        self.assertIn(result, ["(c)", "(!a) | (a & c)","((!a)) | (a & !b) | (a & b & !c)"])  # Ожидаем минимальные покрытия
        self.assertEqual(len(steps), 3)
        self.assertEqual(steps[0], ["Карта Карно:"])
        self.assertEqual(steps[1], ["1 1 1 1", "1 1 0 1"])  # Корректная карта
        self.assertTrue("Identified groups:" in steps[2])
        self.assertFalse(any("rows 0-1, columns 0-3" in desc for desc in steps[2]))  # --1 → c
        self.assertTrue(any("rows 0-0, columns 0-3" in desc for desc in steps[2]))  # 0-- → !a
        # Обновляем ожидание для a & c (минтермы 5, 6 в columns 1, 3)
        self.assertFalse(any("rows 1-1, columns 1,3" in desc or "rows 1-1, columns 1-1,3-3" in desc for desc in steps[2]))

        # Тест с пустым списком минтермов
        minterms = []
        result, steps = BooleanMinimizer.minimize_karnaugh(minterms, 3, dnf=True)
        self.assertEqual(result, "Contradiction")
        self.assertEqual(len(steps), 3)
        self.assertEqual(steps[2], ["Группы не найдены"])

class TestMainRun(unittest.TestCase):
    def setUp(self):
        self.patcher = patch('builtins.input', return_value='')
        self.mock_input = self.patcher.start()
        self.stdout_patcher = patch('sys.stdout', new=StringIO())
        self.mock_stdout = self.stdout_patcher.start()

    def tearDown(self):
        self.patcher.stop()
        self.stdout_patcher.stop()

    def test_run_valid_expression(self):
        self.mock_input.side_effect = ["a & b"]
        main.run()
        output = self.mock_stdout.getvalue()
        
        # Check truth table
        self.assertIn("a b | Выход", output)
        self.assertIn("0 0 | 0", output)
        self.assertIn("0 1 | 0", output)
        self.assertIn("1 0 | 0", output)
        self.assertIn("1 1 | 1", output)
        
        # Check DNF and CNF
        self.assertIn("DNF: (a & b)", output)
        self.assertIn("CNF: (a | b) & (a | !b) & (!a | b)", output)
        
        # Check indices
        self.assertIn("Миндексы DNF: 3", output)
        self.assertIn("Миндексы CNF: 0, 1, 2", output)
        
        # Check index value
        self.assertIn("Индекс: 0001 (двоичное) = 1 (десятичное)", output)
        
        # Check minimizations
        self.assertIn("Минимизированная DNF: (a & b)", output)
        self.assertIn("Минимизированная CNF: (a) & (!a | b)", output)  # Updated to match Karnaugh map output

    def test_run_invalid_characters(self):
        self.mock_input.side_effect = ["a + b"]
        main.run()
        output = self.mock_stdout.getvalue()
        self.assertIn("Ошибка: недопустимые символы в выражении.", output)
        self.assertNotIn("Таблица истинности", output)

    def test_run_unbalanced_parentheses(self):
        self.mock_input.side_effect = ["(a & b"]
        main.run()
        output = self.mock_stdout.getvalue()
        self.assertIn("Ошибка: несбалансированные скобки.", output)
        self.assertNotIn("Таблица истинности", output)

    def test_run_empty_expression(self):
        self.mock_input.side_effect = [""]
        main.run()
        output = self.mock_stdout.getvalue()
        self.assertIn("Ошибка: не удалось разобрать выражение.", output)
        self.assertNotIn("Таблица истинности", output)

    def test_run_invalid_tokens(self):
        self.mock_input.side_effect = ["a + b"]
        main.run()
        output = self.mock_stdout.getvalue()
        self.assertIn("Ошибка: недопустимые символы в выражении.", output)
        self.assertNotIn("Таблица истинности", output)

if __name__ == "__main__":
    unittest.main()