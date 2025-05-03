def to_binary(num, bits=8):
    """Преобразует число в двоичный формат (без знака)."""
    binary = []
    for i in range(bits):
        binary.append(str(num % 2))
        num //= 2
    return ''.join(reversed(binary))