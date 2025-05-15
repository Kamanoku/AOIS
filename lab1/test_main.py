# tests/test_binary_multiply.py
import sys
import os
import unittest
from unittest.mock import patch
from io import StringIO

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from to_binary import to_binary
from to_signed_binary import to_signed_binary
from binary_addition import binary_addition
from binary_multiply import binary_multiply
from binary_subtraction import binary_subtraction
from binary_divide import binary_divide
from float_to_ieee754 import float_to_ieee754
from ieee754_addition import ieee754_addition
from main import main

class TestBinaryOperations(unittest.TestCase):

    @patch('builtins.input', side_effect=[3, 4, 1.5, 1.5])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main(self, mock_stdout, mock_input):
        main()
        output = mock_stdout.getvalue()

        # Checking the output for first integer
        self.assertIn("Число введено: 3", output)
        self.assertIn("Прямой код:", output)
        self.assertIn("Обратный код:", output)
        self.assertIn("Дополнительный код:", output)

        # Checking the output for second integer
        self.assertIn("Число введено: 4", output)
        self.assertIn("Умножение: 3 * 4 =", output)
        self.assertIn("Деление: 3 / 4 =", output)

        # Checking the addition result
        self.assertIn("Сложение:", output)
        self.assertIn("Результат сложения (десятичный):", output)

        # Checking the subtraction results
        self.assertIn("Вычитание:", output)

        # Checking floating-point addition
        self.assertIn("Сложение:", output)
        self.assertIn("Число 1 в IEEE-754:", output)
        self.assertIn("Число 2 в IEEE-754:", output)
        self.assertIn("Результат (десятичный):", output)
        self.assertIn("Результат в IEEE-754:", output)

    def test_binary_multiply(self):
        self.assertEqual(binary_multiply(3, 4), 12)
        self.assertEqual(binary_multiply(-3, 4), -12)
        self.assertEqual(binary_multiply(-3, -4), 12)

    def test_binary_divide(self):
        self.assertEqual(binary_divide(10, 2), 5.0)
        self.assertEqual(binary_divide(-10, 2), -5.0)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            binary_divide(10, 0)

    def test_binary_subtraction(self):
        (result_first, direct_first, reverse_first, additional_first), (
            result_second, direct_second, reverse_second, additional_second) = binary_subtraction('00001000', '00000101')
        self.assertEqual(result_first, 3)
        self.assertEqual(direct_first, '00000011')
        self.assertEqual(reverse_first, '00000011')
        self.assertEqual(additional_first, '00000011')

    def test_float_to_ieee754(self):
        self.assertEqual(float_to_ieee754(1.5), '0 01111111 10000000000000000000000')
        self.assertEqual(float_to_ieee754(-1.5), '1 01111111 10000000000000000000000')

    def test_ieee754_addition(self):
        ieee1, ieee2, result_decimal, ieee_result = ieee754_addition(1.5, 1.5)
        self.assertEqual(result_decimal, 3.0)

    def test_to_binary(self):
        self.assertEqual(to_binary(5), '00000101')
        self.assertEqual(to_binary(0), '00000000')
        self.assertEqual(to_binary(255, bits=8), '11111111')

    def test_to_signed_binary(self):
        self.assertEqual(to_signed_binary(5), ('00000101', '00000101', '00000101'))
        self.assertEqual(to_signed_binary(-5), ('10000101', '11111010', '11111011'))
        self.assertEqual(to_signed_binary(0), ('00000000', '00000000', '00000000'))

    def test_binary_addition(self):
        result, direct, reverse, additional = binary_addition('00000101', '00000011')
        self.assertEqual(result, 8)
        self.assertEqual(direct, '00001000')
        self.assertEqual(reverse, '00001000')
        self.assertEqual(additional, '00001000')

    def test_binary_subtraction(self):
        (result_first, direct_first, reverse_first, additional_first), (
            result_second, direct_second, reverse_second, additional_second) = binary_subtraction('00001000', '00000101')
        self.assertEqual(result_first, 3)
        self.assertEqual(direct_first, '00000011')
        self.assertEqual(reverse_first, '00000011')
        self.assertEqual(additional_first, '00000011')


if __name__ == '__main__':
    unittest.main()