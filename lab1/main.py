# main.py
from to_binary import to_binary
from to_signed_binary import to_signed_binary
from binary_addition import binary_addition
from binary_subtraction import binary_subtraction
from binary_multiply import binary_multiply
from binary_divide import binary_divide
from ieee754_addition import ieee754_addition

def main():
    # Ввод целых чисел
    num1 = int(input("Введите первое целое число: "))
    direct1, reverse1, additional1 = to_signed_binary(num1)
    print(f"\nЧисло введено: {num1}")
    print(f"Прямой код: {direct1}")
    print(f"Обратный код: {reverse1}")
    print(f"Дополнительный код: {additional1}")

    num2 = int(input("Введите второе целое число: "))
    direct2, reverse2, additional2 = to_signed_binary(num2)
    print(f"\nЧисло введено: {num2}")
    print(f"Прямой код: {direct2}")
    print(f"Обратный код: {reverse2}")
    print(f"Дополнительный код: {additional2}")

    # Умножение
    multiply_result = binary_multiply(num1, num2)
    print(f"\nУмножение: {num1} * {num2} = {multiply_result}")

    # Деление
    try:
        divide_result = binary_divide(num1, num2)
        print(f"\nДеление: {num1} / {num2} = {divide_result:.5f}")
    except ValueError as e:
        print(e)

    # Сложение
    print("\nСложение:")
    sum_result, direct_sum, reverse_sum, additional_sum = binary_addition(additional1, additional2)
    print(f"Результат сложения (десятичный): {sum_result}")
    print(f"Результат сложения (двоичный): {direct_sum}")
    print(f"Обратный код: {reverse_sum}")
    print(f"Дополнительный код: {additional_sum}")

    # Вычитание
    print("\nВычитание:")
    (first_result, first_direct, first_reverse, first_additional), (
    second_result, second_direct, second_reverse, second_additional) = binary_subtraction(additional1, additional2)
    print(f"Первая разность (десятичный): {first_result}")
    print(f"Первая разность (двоичный): {first_direct}")
    print(f"Обратный код (первая разность): {first_reverse}")
    print(f"Дополнительный код (первая разность): {first_additional}\n")

    print(f"Вторая разность (десятичный): {second_result}")
    print(f"Вторая разность (двоичный): {second_direct}")
    print(f"Обратный код (вторая разность): {second_reverse}")
    print(f"Дополнительный код (вторая разность): {second_additional}")

    # Ввод чисел с плавающей точкой
    float_num1 = float(input("\nВведите первое число с плавающей точекой: "))
    float_num2 = float(input("Введите второе число с плавающей точкой: "))

    # Сложение
    ieee1, ieee2, result_decimal, ieee_result = ieee754_addition(float_num1, float_num2)
    print(f"\nСложение:")
    print(f"Число 1 в IEEE-754: {ieee1}")
    print(f"Число 2 в IEEE-754: {ieee2}")
    print(f"Результат (десятичный): {result_decimal}")
    print(f"Результат в IEEE-754: {ieee_result}")

if __name__ == "__main__":
    main()