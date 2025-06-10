import re
from typing import List

class InputCleaner:
    @staticmethod
    def remove_spaces(expression: str) -> str:
        return expression.replace(' ', '')


class ExpressionValidator:
    allowed_vars = set("abcde")
    allowed_ops = set("&|!()")

    @staticmethod
    def is_valid(expression: str) -> bool:
        pos = 0
        while pos < len(expression):
            char = expression[pos]
            if char.isspace():
                pos += 1
                continue
            if char in ExpressionValidator.allowed_vars | ExpressionValidator.allowed_ops:
                pos += 1
            elif char == '-' and pos + 1 < len(expression) and expression[pos + 1] == '>':
                pos += 2
            else:
                return False
        return True

    @staticmethod
    def has_balanced_parentheses(expression: str) -> bool:
        balance = 0
        for ch in expression:
            if ch == '(': balance += 1
            elif ch == ')': balance -= 1
            if balance < 0:
                return False
        return balance == 0


class VariableExtractor:
    @staticmethod
    def get_variables(expression: str) -> List[str]:
        return sorted(set(filter(lambda c: c in "abcde", expression)))


class Lexer:
    @staticmethod
    def tokenize(expression: str) -> List[str]:
        tokens = []
        pos = 0
        while pos < len(expression):
            ch = expression[pos]
            if ch.isspace():
                pos += 1
            elif ch == '-' and pos + 1 < len(expression) and expression[pos + 1] == '>':
                tokens.append('->')
                pos += 2
            elif ch in "!&|()":
                tokens.append(ch)
                pos += 1
            elif ch in "abcde":
                tokens.append(ch)
                pos += 1
            else:
                return []
        return tokens
    