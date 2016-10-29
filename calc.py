from sys import stdin 
import re

PROMPT = '> '
QUIT = 'q'
RESULT = '='
SEPARATOR = '\n'
NUMBER = 'n'
OPERATOR = 'o'
PATTERN = '\s*(?:(\d+\.?\d+)|(.))'
ADD = '+'
SUB = '-'
MUL = '*'
DIV = '/'
MOD = '%'
LPAREN = '('
RPAREN = ')'

class Token:
    def __init__(self, value):
        self.kind = self.kind(value)
        self.value = float(value) if self.kind == NUMBER else value
    def kind(self, value):
        try:
            float(value)
            return NUMBER
        except ValueError:
            return OPERATOR

class Tokenflow:
    def __init__(self):
        self.buffer = []
    def get(self):
        if not self.buffer:
            pattern = re.compile(PATTERN)
            for number, operator in pattern.findall(input()):
                self.buffer.append(Token(number or operator))
            self.buffer.append(Token(SEPARATOR))
        return self.buffer.pop(0)
    def putback(self, token):
        self.buffer.insert(0, token)

tf = Tokenflow()

def primary():
    token = tf.get()
    if LPAREN == token.value:
        d = expression()
        token = tf.get()
        if token.value != RPAREN: print(RPAREN, 'expected')
        return d
    elif NUMBER == token.kind:
        return token.value
    elif SUB == token.value:
        return - primary()
    elif ADD == token.value:
        return primary()
    else:
        print('primary expected')

def term():
    left = primary()
    token = tf.get()
    while True:
        if MUL == token.value:
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

def statement():
    t = tf.get()
    tf.putback(t)
    return expression()

def calculate():
    while True:
        print(PROMPT, end='')
        token = tf.get()
        while token.value == SEPARATOR: token = tf.get()
        if token.value == QUIT: return
        tf.putback(token)
        print(RESULT, statement())

try:
    calculate()
except Exception as e:
    print(e)
