import itertools
import re
def evaluate_expression(expr, values):
    expr = expr.replace(' ', '')

    def parse_left_to_right(expr):
        # Сначала обрабатываем отрицания и скобки
        left, expr = parse_term(expr)

        # Затем все операции строго слева направо
        while expr:  # Изменено: проверяем, что expr не пустая строка
            if expr.startswith('<->'):
                op = '<->'
                expr = expr[3:]
            elif expr.startswith('->'):
                op = '->'
                expr = expr[2:]
            elif expr and expr[0] in ('&', '|'):  # Изменено: проверяем только & и |
                op = expr[0]
                expr = expr[1:]
            else:
                break  # Выходим из цикла, если нет оператора

            right, expr = parse_term(expr)

            if op == '&':
                left = left and right
            elif op == '|':
                left = left or right
            elif op == '->':
                left = (not left) or right
            elif op == '<->':
                left = (left == right)

        return left, expr

    def parse_term(expr):
        if not expr:
            raise ValueError("Неожиданный конец выражения")

        if expr[0] == '!':
            # Отрицание имеет высший приоритет
            val, rest = parse_term(expr[1:])
            return not val, rest
        elif expr[0] == '(':
            # Скобки - следующий приоритет
            val, rest = parse_left_to_right(expr[1:])
            if not rest or not rest.startswith(')'):  # Изменено: используем startswith
                raise ValueError("Не закрыта скобка")
            return val, rest[1:]
        elif expr[0] in values:
            # Переменная
            return values[expr[0]], expr[1:]
        elif expr[0].isalpha(): # Добавлена проверка на допустимые переменные
            raise ValueError(f"Неизвестная переменная: {expr[0]}")
        else:
            raise ValueError(f"Неизвестный символ: {expr[0]}")

    try:
        result, remaining_expr = parse_left_to_right(expr)  # Сохраняем оставшуюся часть
        if remaining_expr:  # Проверяем, что все выражение было обработано
            raise ValueError(f"Неожиданный символ в конце выражения: {remaining_expr[0]}")
        return int(result)
    except ValueError as e:
        raise  # Просто перебрасываем ValueError, если он возник
    except Exception as e:
        raise ValueError(f"Ошибка вычисления: {e}")

def truth_table(expr, variables):
    table = []
    # Определяем все переменные в выражении
    all_vars = sorted(set(re.findall(r'[a-z]', expr.lower())))
    for values in itertools.product([0, 1], repeat=len(all_vars)):
        values_dict = dict(zip(all_vars, values))
        result = evaluate_expression(expr, values_dict)
        # Добавляем только запрошенные переменные и результат
        table.append(tuple(values_dict[v] for v in variables) + (result,))
    return table


def get_normal_forms(truth_table, variables):
    minterms = []
    maxterms = []
    for i, row in enumerate(truth_table):
        if row[-1]:
            minterms.append(i)
        else:
            maxterms.append(i)
    
    # СДНФ
    sdnf_terms = []
    for m in minterms:
        term = []
        for i, var in enumerate(variables):
            val = (m >> (len(variables)-1-i)) & 1
            term.append(f"!{var}" if not val else var)
        sdnf_terms.append(" ∧ ".join(term))
    sdnf = " ∨ ".join([f"({t})" for t in sdnf_terms]) if sdnf_terms else "0"
    
    # СКНФ
    sknf_terms = []
    for M in maxterms:
        term = []
        for i, var in enumerate(variables):
            val = (M >> (len(variables)-1-i)) & 1
            term.append(var if not val else f"!{var}")
        sknf_terms.append(" ∨ ".join(term))
    sknf = " ∧ ".join([f"({t})" for t in sknf_terms]) if sknf_terms else "1"
    
    # Числовые формы
    numeric_sdnf = f"({', '.join(map(str, minterms))}) ∨" if minterms else "() ∨"
    numeric_sknf = f"({', '.join(map(str, maxterms))}) ∧" if maxterms else "() ∧"
    
    # Исправленный расчет индексной формы
    binary_result = ''.join(str(row[-1]) for row in truth_table)  # '00100000'
    # Убираем reversed() - теперь биты идут от старшего к младшему
    index_num = sum(int(bit) * (2 ** (len(binary_result)-1-i)) for i, bit in enumerate(binary_result))
    index_form = f"{index_num} - {binary_result}"
    
    return {
        'sdnf': sdnf,
        'sknf': sknf,
        'numeric_sdnf': numeric_sdnf,
        'numeric_sknf': numeric_sknf,
        'index_form': index_form
    }

def main():
    print("Введите логическую функцию (переменные a-e, операции &, |, !, ->, <->)")
    expr = input("Функция: ").strip()
    
    variables = sorted(set(re.findall(r'[a-e]', expr.lower())))
    if not variables:
        print("Ошибка: не найдены переменные")
        return
    
    tt = truth_table(expr, variables)
    forms = get_normal_forms(tt, variables)

    print("\nТаблица истинности:")
    header = " | ".join(variables) + " | F"
    print(header)
    print("-" * len(header))
    for row in tt:
        print(" | ".join(map(str, row)))
    
    print("\nСовершенная дизъюнктивная нормальная форма (СДНФ):")
    print(forms['sdnf'])
    
    print("\nСовершенная конъюнктивная нормальная форма (СКНФ):")
    print(forms['sknf'])
    
    print("\nЧисловая форма СДНФ:")
    print(forms['numeric_sdnf'])
    print("Числовая форма СКНФ:")
    print(forms['numeric_sknf'])
    
    print("\nИндексная форма:")
    print(forms['index_form'])

if __name__ == "__main__":
    main()