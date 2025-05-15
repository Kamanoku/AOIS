# binary_subtraction.py

from binary_addition import binary_addition

def binary_subtraction(minuend, subtrahend, bits=8):
    """Вычитание двух чисел в дополнительном коде с использованием двух разностей."""

    # Первая разность: minuend - subtrahend
    subtrahend_neg = ''.join('1' if b == '0' else '0' for b in subtrahend)

    # Прибавляем 1 к обратному коду
    carry = 1
    for i in range(len(subtrahend_neg) - 1, -1, -1):
        if carry == 0:
            break
        if subtrahend_neg[i] == '1':
            subtrahend_neg = subtrahend_neg[:i] + '0' + subtrahend_neg[i + 1:]
        else:
            subtrahend_neg = subtrahend_neg[:i] + '1' + subtrahend_neg[i + 1:]
            carry = 0

    # Сложение первого результата
    result_first, direct_first, _, additional_first = binary_addition(minuend, subtrahend_neg, bits)

    # Устанавливаем обратный код
    reverse_first = direct_first if result_first >= 0 else ''.join('1' if b == '0' else '0' for b in direct_first)

    # Вторая разность: subtrahend - minuend
    minuend_neg = ''.join('1' if b == '0' else '0' for b in minuend)

    # Прибавляем 1 к обратному коду
    carry = 1
    for i in range(len(minuend_neg) - 1, -1, -1):
        if carry == 0:
            break
        if minuend_neg[i] == '1':
            minuend_neg = minuend_neg[:i] + '0' + minuend_neg[i + 1:]
        else:
            minuend_neg = minuend_neg[:i] + '1' + minuend_neg[i + 1:]
            carry = 0

    # Сложение второго результата
    result_second, direct_second, _, additional_second = binary_addition(subtrahend, minuend_neg, bits)

    # Устанавливаем обратный код
    reverse_second = direct_second if result_second >= 0 else ''.join('1' if b == '0' else '0' for b in direct_second)

    return (result_first, direct_first, reverse_first, additional_first), (result_second, direct_second, reverse_second, additional_second)