from to_binary import to_binary

# Глобальные переменные
EXPONENT_OFFSET = 127  # Смещение для экспоненты
MANTISSA_BITS = 23  # Количество бит для мантиссы


def float_to_ieee754(num):
    """Преобразует число с плавающей точкой в формат IEEE-754 (32-бит)."""
    sign = '0' if num >= 0 else '1'
    num = abs(num)
    exponent = EXPONENT_OFFSET

    while num >= 2:
        num /= 2
        exponent += 1
    while num < 1 and num != 0:
        num *= 2
        exponent -= 1

    mantissa = num - 1
    mantissa_bin = []

    for _ in range(MANTISSA_BITS):
        mantissa *= 2
        if mantissa >= 1:
            mantissa_bin.append('1')
            mantissa -= 1
        else:
            mantissa_bin.append('0')

    exponent_bin = to_binary(exponent, 8)
    return f"{sign} {exponent_bin} {''.join(mantissa_bin)}"