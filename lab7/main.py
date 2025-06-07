import random

def generate_random_matrix(size=16):
    """Генерирует случайную бинарную матрицу size x size"""
    return [[random.randint(0, 1) for _ in range(size)] for _ in range(size)]

def print_matrix(matrix):
    for row in matrix:
        print(' '.join(str(cell) for cell in row))

def extract_words_diagonal(matrix):
    """Извлекает 16 слов из матрицы по диагоналям со смещением"""
    size = len(matrix)
    words = []
    for col in range(size):
        word = ''
        for row in range(size):
            i = (row + col) % size
            word += str(matrix[i][col])
        words.append(word)
    return words

def binary_add(a: str, b: str, bits: int) -> str:
    """Сложение двух бинарных строк фиксированной длины"""
    result = bin(int(a, 2) + int(b, 2))[2:]
    return result.zfill(bits)[-bits:]

def process_words(words, key_v, v_bits=3, a_bits=4, b_bits=4, s_bits=5):
    """Сложение A и B, если V совпадает с ключом"""
    new_words = []
    for word in words:
        v = word[:v_bits]
        a = word[v_bits:v_bits + a_bits]
        b = word[v_bits + a_bits:v_bits + a_bits + b_bits]
        s = word[v_bits + a_bits + b_bits:]

        if v == key_v:
            s_new = binary_add(a, b, s_bits)
            new_word = v + a + b + s_new
        else:
            new_word = word
        new_words.append(new_word)
    return new_words

def apply_logical_function(word1, word2, func_code):
    """Применяет логическую функцию к каждому биту двух слов"""
    result = ''
    for b1, b2 in zip(word1, word2):
        if func_code == 'f0':
            result += '0'
        elif func_code == 'f5':
            result += b2
        elif func_code == 'f10':
            result += '1' if b2 == '0' else '0'
        elif func_code == 'f15':
            result += '1'
        else:
            raise ValueError("Неподдерживаемая функция")
    return result

def compare_words(word1: str, word2: str) -> str:
    """Сравнивает два слова как числа. Возвращает 'g', 'l' или 'e'."""
    int1 = int(word1, 2)
    int2 = int(word2, 2)
    if int1 > int2:
        return 'g'
    elif int1 < int2:
        return 'l'
    else:
        return 'e'

def search_by_gl(words, pattern, mode='g'):
    """Ищет слова по критерию 'g' (>) или 'l' (<) относительно шаблона"""
    matches = []
    for i, word in enumerate(words):
        relation = compare_words(word, pattern)
        if relation == mode:
            matches.append((i, word))
    return matches

# === Основная программа ===
def main():
    matrix = generate_random_matrix()
    print("Сгенерированная матрица 16x16:")
    print_matrix(matrix)

    words = extract_words_diagonal(matrix)
    print("\nИзвлечённые слова:")
    for i, word in enumerate(words):
        print(f"S{i}: {word}")

    key = '111'
    processed_words = process_words(words, key)

    print("\nОбработанные слова (после сложения A + B при совпадении V):")
    for i, word in enumerate(processed_words):
        print(f"S{i}: {word}")

    # === Логическая операция ===
    print("\nВыберите два слова по индексам для логической операции (0–15):")
    idx1 = int(input("Индекс первого слова: "))
    idx2 = int(input("Индекс второго слова: "))

    print("\nВыберите логическую функцию:")
    print("f0 – Константа 0")
    print("f5 – Повторение второго аргумента (x₂)")
    print("f10 – Отрицание второго аргумента (¬x₂)")
    print("f15 – Константа 1")

    func_code = input("Введите код функции (f0, f5, f10, f15): ").strip()

    if 0 <= idx1 < 16 and 0 <= idx2 < 16 and func_code in ['f0', 'f5', 'f10', 'f15']:
        word1 = processed_words[idx1]
        word2 = processed_words[idx2]
        result = apply_logical_function(word1, word2, func_code)

        print(f"\nРезультат применения функции {func_code} к S{idx1} и S{idx2}:")
        print(result)
    else:
        print("Ошибка: некорректный ввод.")

    # === Поиск по соответствию с g и l ===
    print("\n=== Поиск по соответствию (g/l) ===")
    pattern = input("Введите бинарный шаблон (длиной 16 бит): ").strip()
    mode = input("Выберите режим поиска: 'g' – больше, 'l' – меньше: ").strip()

    if len(pattern) == 16 and mode in ['g', 'l']:
        matches = search_by_gl(processed_words, pattern, mode)
        print(f"\nСлова, {'больше' if mode == 'g' else 'меньше'} шаблона {pattern}:")
        for i, w in matches:
            print(f"S{i}: {w}")
    else:
        print("Ошибка: неверный шаблон или режим.")

if __name__ == "__main__":
    main()
