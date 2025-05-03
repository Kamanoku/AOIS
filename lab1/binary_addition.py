# binary_addition.py

from to_signed_binary import to_signed_binary

def binary_addition(bin1, bin2, bits=8):
    """Сложение двух чисел в дополнительном коде."""
    # Преобразуем двоичные строки в десятичные числа
    num1 = int(bin1, 2) if bin1[0] == '0' else int(bin1, 2) - (1 << bits)
    num2 = int(bin2, 2) if bin2[0] == '0' else int(bin2, 2) - (1 << bits)
    result = num1 + num2

    # Ограничение результата битностью
    if result >= (1 << (bits - 1)):
        result -= (1 << bits)  # Приводим к диапазону
    elif result < -(1 << (bits - 1)):
        result += (1 << bits)  # Приводим к диапазону

    # Прямой код
    direct_code = to_signed_binary(result)[0]  # Получаем прямой код
    reverse_code = direct_code if result >= 0 else ''.join('1' if b == '0' else '0' for b in direct_code)  # Обратный код

    # Дополнительный код
    additional_code = to_signed_binary(result)[2]  # Получаем дополнительный код

    return result, direct_code, reverse_code, additional_code