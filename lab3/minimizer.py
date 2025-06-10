from typing import List, Tuple, Set

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
            if (bit == '1' and conjunctive) or (bit == '0' and not conjunctive):
                parts.append(term)
            else:
                parts.append(f"!{term}")
        glue = ' & ' if conjunctive else ' | '
        expr = glue.join(parts) if parts else ("1" if conjunctive else "0")
        if conjunctive and len(parts) == 1:
            expr = f"({expr})"
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
    def minimize_karnaugh(minterms: List[int], var_count: int, dnf: bool = True) -> Tuple[str, List[List[str]]]:
        def gray_code(n):
            return [i ^ (i >> 1) for i in range(1 << n)]

        if not minterms:
            return ("Contradiction" if dnf else "Tautology", [["Карта Карно:"], ["0 0 0 0", "0 0 0 0"], ["Группы не найдены"]])

        rows = 1 << (var_count // 2)
        cols = 1 << ((var_count + 1) // 2)
        grid = [[0] * cols for _ in range(rows)]
        row_gray = [format(g, f'0{var_count//2}b') for g in gray_code(var_count//2)]
        col_gray = [format(g, f'0{(var_count+1)//2}b') for g in gray_code((var_count+1)//2)]

        cell_to_bits = {}
        for i in range(rows):
            for j in range(cols):
                bits = (row_gray[i] + col_gray[j])[:var_count]
                index = int(bits, 2)
                if index in minterms:
                    grid[i][j] = 1
                cell_to_bits[(i, j)] = bits

        def find_groups(grid, rows, cols, cell_to_bits):
            groups = []
            used_cells = set()
            
            def is_valid_group(cells):
                return all(0 <= i < rows and 0 <= j < cols and grid[i][j] == 1 and (i, j) not in used_cells for i, j in cells)
            
            def add_group(cells):
                if cells:
                    groups.append(set(cells))
                    used_cells.update(cells)
            
            for size in [4, 2, 1]:
                for i in range(rows):
                    for j in range(cols):
                        if j + size <= cols and is_valid_group([(i, j + k) for k in range(size)]):
                            add_group([(i, j + k) for k in range(size)])
                        if size != 1 and i + size <= rows and is_valid_group([(i + k, j) for k in range(size)]):
                            add_group([(i + k, j) for k in range(size)])
                        if size == 2 and i + size <= rows and j + size <= cols:
                            if is_valid_group([(i + di, j + dj) for di in range(size) for dj in range(size)]):
                                add_group([(i + di, j + dj) for di in range(size) for dj in range(size)])
            
            if cols == 4:
                for i in range(rows):
                    if is_valid_group([(i, 0), (i, cols-1)]):
                        add_group([(i, 0), (i, cols-1)])
            if rows == 4:
                for j in range(cols):
                    if is_valid_group([(0, j), (rows-1, j)]):
                        add_group([(0, j), (rows-1, j)])
            
            return groups

        steps = []
        steps.append(["Карта Карно:"])
        grid_str = [" ".join(map(str, row)) for row in grid]
        steps.append(grid_str)
        
        groups = find_groups(grid, rows, cols, cell_to_bits)
        
        if groups:
            group_descriptions = []
            for idx, group in enumerate(groups, 1):
                rows_in_group = sorted({i for i, j in group})
                cols_in_group = sorted({j for i, j in group})
                desc = f"Group {idx}: rows {rows_in_group[0]}-{rows_in_group[-1]}, columns {cols_in_group[0]}-{cols_in_group[-1]}"
                group_descriptions.append(desc)
            steps.append(["Identified groups:"] + group_descriptions)
        else:
            steps.append(["Группы не найдены"])

        targets = set(minterms)
        covers = {t: [] for t in targets}
        group_minterms = []
        for idx, group in enumerate(groups):
            minterms = {int(cell_to_bits[cell], 2) for cell in group}
            group_minterms.append((group, minterms))
            for m in minterms:
                if m in targets:
                    covers[m].append((idx, group, minterms))
        
        essentials = []
        remaining = set(targets)
        while remaining:
            best = max((g for g, mt in group_minterms if g not in [e[1] for e in essentials]), 
                       key=lambda g: len({int(cell_to_bits[cell], 2) for cell in g} & remaining), 
                       default=None)
            if not best:
                break
            minterms = {int(cell_to_bits[cell], 2) for cell in best}
            essentials.append((len(essentials) + 1, best, minterms))
            remaining -= minterms
        
        variables = [chr(97 + i) for i in range(var_count)]
        expressions = []
        for _, group, minterms in essentials:
            bits_list = [cell_to_bits[cell] for cell in group]
            common_bits = list(bits_list[0])
            for bits in bits_list[1:]:
                for i in range(var_count):
                    if common_bits[i] != bits[i]:
                        common_bits[i] = '-'
            expr = ExpressionFormatter.to_logical(''.join(common_bits), variables, dnf)
            if expr and expr != "1" and expr != "0":
                expressions.append(expr)
        
        minimized_expr = " | ".join(f"({expr})" for expr in expressions) if dnf else " & ".join(f"({expr})" for expr in expressions)
        minimized_expr = minimized_expr if expressions else ("Contradiction" if dnf else "Tautology")
        
        return minimized_expr, steps