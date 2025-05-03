import itertools
import re

def evaluate_expression(expr, values):
    expr = expr.replace(' ', '').lower()
    for var in sorted(values.keys(), key=lambda x: -len(x)):
        val = str(values[var])
        expr = expr.replace(var, val)
        expr = expr.replace(f"!{var}", str(1 - values[var]))
    while '!0' in expr or '!1' in expr:
        expr = expr.replace('!0', '1').replace('!1', '0')
    tokens = re.findall(r'(0|1|->|<->|≡|[&|])', expr)
    if not tokens:
        return 0
    result = int(tokens[0])
    i = 1
    while i < len(tokens):
        if tokens[i] == '&':
            result &= int(tokens[i+1])
            i += 2
        elif tokens[i] == '|':
            result |= int(tokens[i+1])
            i += 2
        elif tokens[i] in ('->', '→'):
            result = (1 - result) | int(tokens[i+1])
            i += 2
        elif tokens[i] in ('<->', '≡', '↔'):
            next_val = int(tokens[i+1])
            result = (result & next_val) | ((1 - result) & (1 - next_val))
            i += 2
        else:
            i += 1
    return result

def truth_table(expr, variables):
    table = []
    for values in itertools.product([0, 1], repeat=len(variables)):
        values_dict = {var: val for var, val in zip(variables, values)}
        result = evaluate_expression(expr, values_dict)
        table.append((*values, result))
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
    
    # Правильный расчет индексной формы
    binary_result = ''.join(str(row[-1]) for row in truth_table)
    # Рассчитываем десятичное значение, интерпретируя биты сверху вниз как младший к старшему
    index_num = sum(int(bit) * (2 ** i) for i, bit in enumerate(reversed(binary_result)))
    
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
    
    print("Числовая форма СДНФ:")
    print(forms['numeric_sdnf'])
    print("Числовая форма СКНФ:")
    print(forms['numeric_sknf'])
    
    print("\nИндексная форма:")
    print(forms['index_form'])

if __name__ == "__main__":
    main()