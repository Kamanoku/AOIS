from log_parser import InputCleaner, ExpressionValidator, VariableExtractor, Lexer
from evaluator import ExpressionConverter, TableBuilder, NormalForms, NumericRepresentation
from minimizer import BooleanMinimizer

def run():
    expr = input("Введите логическое выражение: ").strip()
    cleaned = InputCleaner.remove_spaces(expr)

    if not ExpressionValidator.is_valid(cleaned):
        print("Ошибка: недопустимые символы в выражении.")
        return

    if not ExpressionValidator.has_balanced_parentheses(cleaned):
        print("Ошибка: несбалансированные скобки.")
        return

    variables = VariableExtractor.get_variables(cleaned)
    tokens = Lexer.tokenize(cleaned)
    if not tokens:
        print("Ошибка: не удалось разобрать выражение.")
        return

    postfix = ExpressionConverter.to_postfix(tokens)
    table = TableBuilder.build(variables, postfix)

    print("\nТаблица истинности:")
    header = " ".join(variables) + " | Выход"
    print(header)
    print("-" * len(header))
    for row in table:
        values = " ".join("1" if val else "0" for val in row[:-1])
        print(f"{values} | {'1' if row[-1] else '0'}")

    dnf_expr = NormalForms.dnf(variables, table)
    cnf_expr = NormalForms.cnf(variables, table)
    print(f"\nDNF: {dnf_expr}")
    print(f"CNF: {cnf_expr}")

    dnf_indices = NumericRepresentation.dnf_indices(table)
    cnf_indices = NumericRepresentation.cnf_indices(table)
    print(f"Миндексы DNF: {', '.join(map(str, dnf_indices)) or 'null'}")
    print(f"Миндексы CNF: {', '.join(map(str, cnf_indices)) or 'null'}")

    index_value = NumericRepresentation.index_value(table)
    binary_str = ''.join(['1' if row[-1] else '0' for row in table])
    print(f"Индекс: {binary_str} (двоичное) = {index_value} (десятичное)")

    # Расчётная минимизация
    dnf_min, dnf_steps = BooleanMinimizer.minimize(dnf_indices, len(variables), dnf=True)
    cnf_min, cnf_steps = BooleanMinimizer.minimize(cnf_indices, len(variables), dnf=False)

    print("\nМинимизация (расчётная):")
    print("Минимизированная DNF:", dnf_min)
    for i, step in enumerate(dnf_steps, 1):
        print(f"  Этап {i}:")
        for line in step:
            print("   ", line)

    print("\nМинимизированная CNF:", cnf_min)
    for i, step in enumerate(cnf_steps, 1):
        print(f"  Этап {i}:")
        for line in step:
            print("   ", line)

    # Таблично-расчётная минимизация (Квайна-МакКласки)
    dnf_qmc, qmc_dnf_steps = BooleanMinimizer.minimize_qmc(dnf_indices, len(variables))
    cnf_qmc, qmc_cnf_steps = BooleanMinimizer.minimize_qmc(cnf_indices, len(variables), dnf=False)

    print("\nМинимизация (таблично-расчётная, Квайна-МакКласки):")
    print("Минимизированная DNF:", dnf_qmc)
    for i, step in enumerate(qmc_dnf_steps, 1):
        print(f"  Этап {i}:")
        for line in step:
            print("    ", line)

    print("\nМинимизированная CNF:", cnf_qmc)
    for i, step in enumerate(qmc_cnf_steps, 1):
        print(f"  Этап {i}:")
        for line in step:
            print("    ", line)

    # Табличная минимизация (Карно)
    dnf_karnaugh, kmap_dnf_steps = BooleanMinimizer.minimize_karnaugh(dnf_indices, len(variables))
    cnf_karnaugh, kmap_cnf_steps = BooleanMinimizer.minimize_karnaugh(cnf_indices, len(variables), dnf=False)

    print("\nМинимизация (табличная, Карно):")
    print("Минимизированная DNF:", dnf_karnaugh)
    for i, step in enumerate(kmap_dnf_steps, 1):
        print(f"  Этап {i}:")
        for line in step:
            print("   ", line)

    print("\nМинимизированная CNF:", cnf_karnaugh)
    for i, step in enumerate(kmap_cnf_steps, 1):
        print(f"  Этап {i}:")
        for line in step:
            print("   ", line)

if __name__ == "__main__":
    run()