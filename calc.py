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
FUNCTIONS = ['sin', 'cos']
CONSTANTS = ['pi', 'e']
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
            if value in [QUIT, SEPARATOR]: return value
            raise Exception('BAD_TOKEN')

class Tokenflow:
    def __init__(self):
        self.buffer = []
    def get(self):
        if not self.buffer:
            pattern = re.compile(PATTERN)
            for value in pattern.findall(input()):
                self.buffer.append(Token(value))
            self.buffer.append(Token(SEPARATOR))
        return self.buffer.pop(0)
    def putback(self, token):
        self.buffer.insert(0, token)
    def clear(self):
        self.buffer.clear()

tf = Tokenflow()

def primary():
    token = tf.get()
    if LPAREN == token.value:
        d = expression()
        token = tf.get()
        if token.value != RPAREN: print(RPAREN, 'expected')
        return d
    elif FUNCTION == token.kind:
        func = token.value
        token = tf.get()
        if LPAREN == token.value:
            d = expression()
            token = tf.get()
            if token.value != RPAREN: raise Exception(RPAREN + ' EXPECTED')
            return eval('math.' + func + '(' + str(d) + ')')
    elif NUMBER == token.kind:
        return token.value
    elif CONSTANT == token.kind:
        return eval('math.' + token.value)
    elif SUB == token.value:
        return -primary()
    elif ADD == token.value:
        return primary()
    else:
        print('primary expected')

def term():
    left = primary()
    token = tf.get()
    while True:
        if LPAREN == token.value:
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
