from math import inf as infinity
from decimal import Decimal


def remove_whitespace(string: str):
    return "".join(filter(lambda c: not c.isspace(), string))


class Token:
    def __init__(self, type: str, value: str) -> None:
        self.type = type  # number or term
        self.value = value

    def __repr__(self) -> str:
        return f"{self.value}"


class Tokenizer:
    def __init__(self, expression: str) -> None:
        self.expression = remove_whitespace(expression)
        self.pos = 0
        self.len = len(self.expression)
        self.tokens: list[Token] = []

    def tokenize(self) -> tuple[list[Token], str]:
        while self.pos < self.len:
            cur_char = self.expression[self.pos]
            if cur_char.isdigit() or cur_char in ["+", "-"]:
                self.make_decimal()
            elif cur_char in ["*", "/", "^", "\\"]:
                self.tokens.append(Token("term", cur_char))
                self.pos += 1
            else:
                return ([], f"Invalid character: {cur_char}")
        return (self.tokens, None)

    def make_decimal(self):
        num = self.expression[self.pos]
        self.pos += 1
        while self.pos < self.len and self.expression[self.pos].isdigit():
            num += self.expression[self.pos]
            self.pos += 1
        if num in ["+", "-"]:
            self.tokens.append(Token("number", Decimal("1") if num == "+" else "-1"))
            self.tokens.append(Token("term", "*"))
        if num[0] != "+" and num[0] != "-":
            num = "+" + num
        self.tokens.append(Token("number", Decimal(num)))


class Evaluator:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0
        self.len = len(self.tokens)
        self.numbers: list[float] = []
        self.term_dict = {
            "*": self.do_multiplication,
            "/": self.do_division,
            "^": self.do_power,
            "\\": self.do_root,
        }

    def evaluate(self) -> tuple[Decimal, str]:
        while self.pos < self.len:
            cur_tok = self.tokens[self.pos]
            if cur_tok.type == "number":
                number = Decimal(cur_tok.value)
                if self.is_next_number():
                    self.numbers.append(number)
                self.pos += 1
            elif cur_tok.type == "term":
                term = cur_tok.value
                func = self.term_dict.get(term)
                if func == None:
                    return (0, f"Invalid character: {term}")
                result, error = func()
                if error != None:
                    return (0, error)
                self.numbers.append(result)
                self.pos += 2
        return (sum(self.numbers), None)

    def do_multiplication(self) -> tuple[Decimal, str]:
        a: Decimal = 0
        b: Decimal = 0
        if self.is_next_number() and self.is_last_number():
            a = Decimal(self.tokens[self.pos - 1].value)
            b = Decimal(self.tokens[self.pos + 1].value)
            return (a * b, None)
        else:
            return (
                0,
                f"Invalid expression. Can't multiply {self.tokens[self.pos - 1].value} and {self.tokens[self.pos + 1].value}",
            )

    def do_division(self) -> tuple[Decimal, str]:
        a: Decimal = 0
        b: Decimal = 0
        if self.is_next_number() and self.is_last_number():
            a = Decimal(self.tokens[self.pos - 1].value)
            b = Decimal(self.tokens[self.pos + 1].value)
            if b == 0:
                return infinity
            return (a / b, None)
        else:
            return (
                0,
                f"Invalid expression. Can't divide {self.tokens[self.pos - 1].value} and {self.tokens[self.pos + 1].value}",
            )

    def do_power(self) -> tuple[Decimal, str]:
        a: Decimal = 0
        b: Decimal = 0
        if self.is_next_number() and self.is_last_number():
            a = Decimal(self.tokens[self.pos - 1].value)
            b = Decimal(self.tokens[self.pos + 1].value)
            return (a**b, None)
        else:
            return (
                0,
                f"Invalid expression. Can't raise {self.tokens[self.pos - 1].value} and {self.tokens[self.pos + 1].value}",
            )

    def do_root(self) -> tuple[Decimal, str]:
        a: Decimal = 0
        b: Decimal = 0
        if self.is_next_number() and self.is_last_number():
            a = Decimal(self.tokens[self.pos - 1].value)
            b = Decimal(self.tokens[self.pos + 1].value)
            return (b ** (1 / a), None)
        else:
            return (
                0,
                f"Invalid expression. Can't raise {self.tokens[self.pos - 1].value} and {self.tokens[self.pos + 1].value}",
            )

    def is_next_number(self):
        return self.pos + 1 < self.len and self.tokens[self.pos + 1].type == "number"

    def is_last_number(self):
        return self.pos - 1 >= 0 and self.tokens[self.pos - 1].type == "number"


def calculate(expression) -> tuple[float, str]:
    tokenizer = Tokenizer(expression)
    tokens, error = tokenizer.tokenize()
    if error != None:
        return (0, error)
    evaluator = Evaluator(tokens)
    result, error = evaluator.evaluate()
    return (float(result), error)


if __name__ == "__main__":
    while True:
        expression = input("Expression >>> ")
        result, error = calculate(expression)
        if error != None:
            print(error)
        else:
            print(result)
