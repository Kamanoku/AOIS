import unittest
import itertools
import re
from main import evaluate_expression, truth_table, get_normal_forms  # Импорт из вашего main.py

class TestLogicFunctions(unittest.TestCase):
    def setUp(self):
        self.variables = ['a', 'b', 'c']
    
    def test_evaluate_expression(self):
        self.assertEqual(evaluate_expression("a&b", {'a':1, 'b':1}), 1)
        self.assertEqual(evaluate_expression("a|b", {'a':0, 'b':0}), 0)
        self.assertEqual(evaluate_expression("!a", {'a':1}), 0)
        self.assertEqual(evaluate_expression("a->b", {'a':1, 'b':0}), 0)
        
    def test_truth_table(self):
        and_table = truth_table("a&b", ['a', 'b'])
        self.assertEqual(len(and_table), 4)
        self.assertEqual(and_table[3], (1, 1, 1))  # Проверяем последнюю строку
    
    def test_normal_forms(self):
        and_table = [(0,0,0), (0,1,0), (1,0,0), (1,1,1)]
        forms = get_normal_forms(and_table, ['a', 'b'])
        self.assertIn("(a ∧ b)", forms['sdnf'])
        self.assertIn("(a ∨ b)", forms['sknf'])

if __name__ == '__main__':
    unittest.main()