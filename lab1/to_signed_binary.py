# to_signed_binary.py

from to_binary import to_binary # type: ignore

def to_signed_binary(num, bits=8):
    """Преобразует число в прямой, обратный и дополнительный коды."""
    if abs(num) >= 2 ** (bits - 1):
        raise ValueError(f"Число {num} выходит за пределы {bits}-битного диапазона.")

    # Прямой код
    sign = '0' if num >= 0 else '1'
    magnitude = to_binary(abs(num), bits - 1)  # Прямой код без знака
    direct_code = sign + magnitude

    # Обратный код
    if num >= 0:
        reverse_code = direct_code
    else:
        reverse_magnitude = ''.join('1' if b == '0' else '0' for b in magnitude)
        reverse_code = '1' + reverse_magnitude  # Знак 1 для отрицательных

    # Дополнительный код
    if num >= 0:
        additional_code = direct_code
    else:
        additional_magnitude = to_binary(int(reverse_magnitude, 2) + 1, bits - 1)
        additional_code = '1' + additional_magnitude  # Знак 1 для отрицательных

    return direct_code, reverse_code, additional_code