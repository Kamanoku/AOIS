# binary_multiply.py

def binary_multiply(x, y):
    """Умножает два числа в прямом коде, учитывая знак."""
    is_negative = (x < 0) ^ (y < 0)
    x, y = abs(x), abs(y)
    result = 0
    while y > 0:
        if y % 2 == 1:
            result += x
        x <<= 1
        y >>= 1
    return -result if is_negative else result