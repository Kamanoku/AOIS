# binary_divide.py
precision = 5
def binary_divide(x, y):
    """Делит два числа в прямом коде с точностью до 5 знаков после запятой."""
    if y == 0:
        raise ValueError("Деление на ноль!")
    is_negative = (x < 0) ^ (y < 0)
    x, y = abs(x), abs(y)
    quotient = 0
    remainder = x
    decimal_part = 0.0

    while remainder >= y:
        remainder -= y
        quotient += 1
    for i in range(precision):
        remainder *= 10
        decimal_digit = 0
        while remainder >= y:
            remainder -= y
            decimal_digit += 1
        decimal_part += decimal_digit / (10 ** (i + 1))
    return - (quotient + decimal_part) if is_negative else quotient + decimal_part