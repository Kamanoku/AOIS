from typing import List, Tuple, Set
from itertools import combinations
from collections import defaultdict

class BinaryUtils:
    @staticmethod
    def to_binary(n: int, width: int) -> str:
        return format(n, f'0{width}b')

    @staticmethod
    def count_ones(binary: str) -> int:
        return binary.count('1')

    @staticmethod
    def can_merge(a: str, b: str) -> Tuple[bool, str]:
        diffs = 0
        result = []
        for bit_a, bit_b in zip(a, b):
            if bit_a != bit_b:
                diffs += 1
                result.append('-')
            else:
                result.append(bit_a)
            if diffs > 1:
                return False, ''
        return diffs == 1, ''.join(result)

class ImplicantReducer:
    @staticmethod
    def extract_implicants(ones: List[int], bit_width: int) -> Tuple[List[Tuple[str, Set[int]]], List[List[str]]]:
        groups = {}
        for val in ones:
            b = BinaryUtils.to_binary(val, bit_width)
            ones_count = BinaryUtils.count_ones(b)
            groups.setdefault(ones_count, []).append((b, {val}))

        primes = []
        history = []
        
        while groups:
            merged = {}
            step_log = []
            used = set()
            keys = sorted(groups.keys())

            for i in range(len(keys) - 1):
                for a, ta in groups[keys[i]]:
                    for b, tb in groups[keys[i + 1]]:
                        ok, merged_bits = BinaryUtils.can_merge(a, b)
                        if ok:
                            if merged_bits not in [x[0] for x in merged.get(BinaryUtils.count_ones(merged_bits), [])]:
                                merged.setdefault(BinaryUtils.count_ones(merged_bits), []).append((merged_bits, ta | tb))
                                used.update(ta)
                                used.update(tb)
                                step_log.append(f"{a} + {b} => {merged_bits} :: {ta | tb}")

            for lst in groups.values():
                for bits, tset in lst:
                    if not tset <= used and (bits, tset) not in primes:
                        primes.append((bits, tset))

            if not step_log:
                break

            history.append(step_log)
            groups = merged

        return primes, history

class EssentialFinder:
    @staticmethod
    def filter_essentials(primes: List[Tuple[str, Set[int]]], targets: Set[int]) -> List[Tuple[str, Set[int]]]:
        if not targets:
            return []
        
        covers = {t: [] for t in targets}
        for p in primes:
            for m in p[1]:
                if m in targets:
                    covers[m].append(p)
        
        essentials = []
        remaining = set(targets)
        
        for p in primes:
            if p[1] == targets:
                return [p]
        
        for m in list(remaining):
            if len(covers[m]) == 1:
                imp = covers[m][0]
                if imp not in essentials:
                    essentials.append(imp)
                    remaining -= imp[1]
        
        while remaining:
            best = max((p for p in primes if p not in essentials), 
                       key=lambda x: len(x[1] & remaining), default=None)
            if not best:
                break
            essentials.append(best)
            remaining -= best[1]
        
        return essentials

class ExpressionFormatter:
    @staticmethod
    def to_logical(pattern: str, vars: List[str], conjunctive: bool) -> str:
        if all(bit == '-' for bit in pattern):
            return "1" if conjunctive else "0"

        parts = []
        for i, bit in enumerate(pattern):
            if bit == '-':
                continue
            term = vars[i]
            if conjunctive:
                # DNF: 1 → var, 0 → !var
                parts.append(term if bit == '1' else f"!{term}")
            else:
                # CNF: 0 → var, 1 → !var
                parts.append(term if bit == '0' else f"!{term}")

        glue = ' & ' if conjunctive else ' | '
        expr = glue.join(parts) if parts else ("1" if conjunctive else "0")

        return expr




class BooleanMinimizer:
    @staticmethod
    def minimize(minterms: List[int], var_count: int, dnf: bool = True) -> Tuple[str, List[List[str]]]:
        if not minterms:
            return ("Contradiction" if dnf else "Tautology", [])

        primes, steps = ImplicantReducer.extract_implicants(minterms, var_count)
        essentials = EssentialFinder.filter_essentials(primes, set(minterms))

        if not essentials:
            return ("Contradiction" if dnf else "Tautology", steps)

        variables = [chr(97 + i) for i in range(var_count)]
        clauses = []
        for p in essentials:
            expr = ExpressionFormatter.to_logical(p[0], variables, dnf)
            if ('&' in expr and dnf) or ('|' in expr and not dnf):
                expr = f"({expr})"
            clauses.append(expr)

        return (" | ".join(clauses) if dnf else " & ".join(clauses), steps)

    @staticmethod
    def minimize_qmc(minterms: List[int], var_count: int, dnf: bool = True) -> Tuple[str, List[List[str]]]:
        if not minterms:
            return ("Contradiction" if dnf else "Tautology", [])

        primes, steps = ImplicantReducer.extract_implicants(minterms, var_count)
        
        targets = set(minterms)
        covers = {t: [] for t in targets}
        for p in primes:
            for m in p[1]:
                if m in targets:
                    covers[m].append(p)
        
        cover_table = ["Таблица покрытия:"]
        header = "Imp " + " ".join(str(m) for m in sorted(targets))
        cover_table.append(header)
        cover_table.append("-" * len(header))
        
        for idx, (bits, tset) in enumerate(primes):
            row = [f"Imp {idx}"] + ["-" if m in tset else " " for m in sorted(targets)]
            cover_table.append(" ".join(row))
        
        steps.append(cover_table)
        
        essentials = EssentialFinder.filter_essentials(primes, targets)
        
        essential_step = ["Существенные импликанты:" if dnf else "Существенные импликаты:"]
        for idx, (bits, tset) in enumerate(essentials):
            expr = ExpressionFormatter.to_logical(bits, [chr(97 + i) for i in range(var_count)], dnf)
            essential_step.append(f"{bits} покрывает {sorted(tset)} ({expr})")
        steps.append(essential_step)
        
        variables = [chr(97 + i) for i in range(var_count)]
        clauses = []
        for p in essentials:
            expr = ExpressionFormatter.to_logical(p[0], variables, dnf)
            if ('&' in expr and dnf) or ('|' in expr and not dnf):
                expr = f"({expr})"
            clauses.append(expr)
        
        result = (" | ".join(clauses) if dnf else " & ".join(clauses)) or ("Contradiction" if dnf else "Tautology")
        return result, steps

    @staticmethod
    def minimize_karnaugh(indices: List[int], var_count: int, dnf: bool = True) -> Tuple[str, List[List[str]]]:
        def gray_code(n):
            return [i ^ (i >> 1) for i in range(1 << n)]

        if not indices:
            return ("Contradiction" if dnf else "Tautology", [["Карта Карно:"], ["0 0 0 0", "0 0 0 0"], ["Группы не найдены"]])

        rows = 1 << (var_count // 2)
        cols = 1 << ((var_count + 1) // 2)
        grid = [[0] * cols for _ in range(rows)]
        row_gray = [format(g, f'0{var_count//2}b') for g in gray_code(var_count//2)]
        col_gray = [format(g, f'0{(var_count+1)//2}b') for g in gray_code((var_count+1)//2)]

        cell_to_bits = {}
        bit_index_map = {}
        for i in range(rows):
            for j in range(cols):
                bits = (row_gray[i] + col_gray[j])[:var_count]
                index = int(bits, 2)
                cell_to_bits[(i, j)] = bits
                bit_index_map[index] = bits
                if index in indices:
                    grid[i][j] = 1

        steps = [["Карта Карно:"]]
        steps.append([" ".join(map(str, row)) for row in grid])

        # Группировка по переменным: если переменная одинаково во всех индексах
        var_values = defaultdict(set)
        for index in indices:
            bits = bit_index_map[index]
            for i, bit in enumerate(bits):
                var_values[i].add(bit)

        global_groups = []
        for i, values in var_values.items():
            if len(values) == 1:
                pattern = ['-' for _ in range(var_count)]
                pattern[i] = values.pop()
                global_groups.append(("".join(pattern), set(filter(lambda idx: bit_index_map[idx][i] == pattern[i], indices))))

        # Если осталось что-то непокрытое — добавляем явно
        covered = set()
        for _, group_indices in global_groups:
            covered |= group_indices
        for idx in indices:
            if idx not in covered:
                global_groups.append((bit_index_map[idx], {idx}))

        # Минимальное покрытие
        targets = set(indices)
        best_cover = None
        for r in range(1, len(global_groups)+1):
            for combo in combinations(global_groups, r):
                covered_now = set().union(*(g[1] for g in combo))
                if covered_now == targets:
                    if best_cover is None or sum(p.count('0') + p.count('1') for p, _ in combo) < sum(p.count('0') + p.count('1') for p, _ in best_cover):
                        best_cover = combo
            if best_cover:
                break

        variables = [chr(97 + i) for i in range(var_count)]
        expressions = [ExpressionFormatter.to_logical(p, variables, dnf) for p, _ in best_cover] if best_cover else []
        minimized_expr = " | ".join(f"({e})" for e in expressions) if dnf else " & ".join(f"({e})" for e in expressions)
        return minimized_expr if expressions else ("Contradiction" if dnf else "Tautology"), steps