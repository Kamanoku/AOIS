from typing import List, Dict

class ExpressionConverter:
    precedence = {
        '!': 5,
        '~': 4,
        '&': 3,
        '|': 2,
        '->': 1,
        '(': 0
    }

    @staticmethod
    def to_postfix(infix_tokens: List[str]) -> List[str]:
        output = []
        ops = []
        for token in infix_tokens:
            if token == '(':
                ops.append(token)
            elif token == ')':
                while ops and ops[-1] != '(':
                    output.append(ops.pop())
                ops.pop()
            elif token in ExpressionConverter.precedence:
                while ops and ExpressionConverter.precedence.get(ops[-1], 0) >= ExpressionConverter.precedence[token]:
                    output.append(ops.pop())
                ops.append(token)
            else:
                output.append(token)

        while ops:
            output.append(ops.pop())

        return output


class PostfixEvaluator:
    @staticmethod
    def evaluate(postfix: List[str], assignments: Dict[str, bool]) -> bool:
        stack = []
        for symbol in postfix:
            if symbol in assignments:
                stack.append(assignments[symbol])
            elif symbol == '!':
                if not stack:
                    raise ValueError("Missing operand for NOT")
                stack.append(not stack.pop())
            elif symbol in {'&', '|', '->'}:
                if len(stack) < 2:
                    raise ValueError("Missing operands for binary operator")
                b, a = stack.pop(), stack.pop()
                if symbol == '&':
                    stack.append(a and b)
                elif symbol == '|':
                    stack.append(a or b)
                elif symbol == '->':
                    stack.append(not a or b)
            else:
                raise ValueError(f"Unknown token: {symbol}")

        if len(stack) != 1:
            raise ValueError("Malformed expression")
        return stack[0]


class TableBuilder:
    @staticmethod
    def build(variable_names: List[str], postfix: List[str]) -> List[List[bool]]:
        rows = 2 ** len(variable_names)
        table = []

        for i in range(rows):
            assignment = {
                var: bool((i >> (len(variable_names) - j - 1)) & 1)
                for j, var in enumerate(variable_names)
            }
            row = [assignment[v] for v in variable_names]
            result = PostfixEvaluator.evaluate(postfix, assignment)
            row.append(result)
            table.append(row)

        return table


class NormalForms:
    @staticmethod
    def dnf(variables: List[str], table: List[List[bool]]) -> str:
        terms = []
        for row in table:
            if row[-1]:
                clause = [var if val else f"!{var}" for var, val in zip(variables, row[:-1])]
                terms.append(f"({' & '.join(clause)})")
        return ' | '.join(terms) if terms else 'Contradiction'

    @staticmethod
    def cnf(variables: List[str], table: List[List[bool]]) -> str:
        clauses = []
        for row in table:
            if not row[-1]:
                clause = [f"!{var}" if val else var for var, val in zip(variables, row[:-1])]
                clauses.append(f"({' | '.join(clause)})")
        return ' & '.join(clauses) if clauses else 'Tautology'


class NumericRepresentation:
    @staticmethod
    def dnf_indices(table: List[List[bool]]) -> List[int]:
        return [i for i, row in enumerate(table) if row[-1]]

    @staticmethod
    def cnf_indices(table: List[List[bool]]) -> List[int]:
        return [i for i, row in enumerate(table) if not row[-1]]

    @staticmethod
    def index_value(table: List[List[bool]]) -> int:
        return sum((1 << (len(table) - i - 1)) for i, row in enumerate(table) if row[-1])
