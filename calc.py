#!/usr/bin/python
import re
import math

PROMPT = '> '
QUIT = 'q'
RESULT = '='
SEPARATOR = '\n'
NUMBER = 'n'
OPERATOR = 'o'
CONSTANT = 'c'
FUNCTION = 'f'
PATTERN = r'\s*(\d*\.?\d+|[a-zA-Z][a-zA-Z0-9]+|.)'
ADD = '+'
SUB = '-'
MUL = '*'
DIV = '/'
MOD = '%'
LPAREN = '('
RPAREN = ')'
COMMA = ','
FUNCTIONS = {'sin': math.sin, 'cos': math.cos, 'asin': math.asin, 'acos': math.acos,
        'atan': math.atan, 'exp': math.exp, 'fabs': math.fabs,
        'floor': math.floor, 'log10': math.log10,'log2': math.log2, 'modf': math.modf,
        'tan': math.tan, 'sqrt': math.sqrt}
CONSTANTS = {'pi': math.pi, 'e': math.e}
OPERATORS = ['+', '-', '*', '/', '%', '^', '(', ')']

class Token:
    def __init__(self, value):
        self.kind = self.kind(value)
        self.value = float(value) if self.kind == NUMBER else value
    def kind(self, value):
        try:
            float(value)
            return NUMBER
        except ValueError:
            if value in OPERATORS: return OPERATOR
            if value in FUNCTIONS: return FUNCTION
            if value in CONSTANTS: return CONSTANT
            if value in [QUIT, SEPARATOR, COMMA]: return value
            raise Exception('BAD TOKEN')

class Tokenflow:
    def __init__(self, reader):
        self.buffer = []
        self.reader = reader
    def get(self):
        if not self.buffer:
            pattern = re.compile(PATTERN)
            for value in pattern.findall(self.reader()):
                self.buffer.append(Token(value))
            self.buffer.append(Token(SEPARATOR))
        return self.buffer.pop(0)
    def putback(self, token):
        self.buffer.insert(0, token)
    def clear(self):
        self.buffer.clear()

tf = Tokenflow(input)

def primary():
    token = tf.get()
    if LPAREN == token.value:
        d = expression()
        token = tf.get()
        if token.value != RPAREN: raise Exception(RPAREN + ' EXPECTED')
        return d
    elif FUNCTION == token.kind:
        func = token.value
        token = tf.get()
        if LPAREN == token.value:
            d = expression()
            print(d)
            token = tf.get()
            if token.value != RPAREN: raise Exception(RPAREN + ' EXPECTED')
            return FUNCTIONS[func](d)
    elif NUMBER == token.kind:
        return token.value
    elif CONSTANT == token.kind:
        return CONSTANTS[token.value]
    elif SUB == token.value:
        return -primary()
    elif ADD == token.value:
        return primary()
    elif COMMA == token.value:
        return COMMA
    else:
        print(token.value)
        raise Exception('PRIMARY EXPECTED')

def term():
    left = primary()
    token = tf.get()
    while True:
        if LPAREN == token.value:
            tf.putback(token)
            left *= primary()
            token = tf.get()
        elif CONSTANT == token.kind or FUNCTION == token.kind or NUMBER == token.kind:
            tf.putback(token)
            left *= primary()
            token = tf.get()
        elif MUL == token.value:
            left *= primary()
            token = tf.get()
        elif DIV == token.value:
            left /= primary()
            token = tf.get()
        elif MOD == token.value:
            left %= term()
            token = tf.get()
        else:
            tf.putback(token)
            return left

def expression():
    left = term()
    token = tf.get()
    while True:
        if ADD == token.value:
            left += term()
            token = tf.get()
        elif SUB == token.value:
            left -= term()
            token = tf.get()
        else:
            tf.putback(token)
            return left

def calculate():
    while True:
        try:
            print(PROMPT, end='')
            token = tf.get()
            while token.value == SEPARATOR: token = tf.get()
            if token.value == QUIT: return
            tf.putback(token)
            print(RESULT, expression())
        except Exception as e:
            print(e)
            tf.clear()

if __name__ == '__main__':
        calculate()
else:
    def calculate(expr):
        global tf
        tf = Tokenflow(lambda: expr.strip())
        return expression()
