# ieee754_addition.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from float_to_ieee754 import float_to_ieee754

def ieee754_addition(num1, num2):
    """Сложение двух чисел с плавающей точкой в формате IEEE-754 (32-бит)."""
    n1_ieee = float_to_ieee754(num1)
    n2_ieee = float_to_ieee754(num2)
    result = num1 + num2
    result_ieee = float_to_ieee754(result)
    return n1_ieee, n2_ieee, result, result_ieee