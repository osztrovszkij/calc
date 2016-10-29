from sys import stdin 
import re

prompt = '> '
quit = 'q'
result = '= '

class Token:
    def __init__(self, value):
        self.kind = self.kind(value)
        self.value = float(value) if self.kind == 'number' else value
    def kind(self, value):
        try:
            float(value)
            return 'number'
        except ValueError:
            return 'operator'

class Tokenflow:
    def __init__(self):
        self.buffer = []
        self.pattern = '\s*(?:(\d+\.?\d+)|(.))'
    def get(self):
        if self.buffer: return self.buffer.pop(0)
        pattern = re.compile(self.pattern)
        for number, operator in pattern.findall(input()):
            self.buffer.append(Token(number or operator))
        return self.buffer.pop(0)
    def putback(self, token):
        self.buffer.insert(0, token)

tf = Tokenflow()

def primary():
    token = tf.get()
    if '(' == token.value:
        d = expression()
        token = tf.get()
        if token.value != ')': print('")" expected')
        return d
    elif 'number' == token.kind:
        return token.value
    elif '-' == token.value:
        return - primary()
    elif '+' == token.value:
        return primary()
    else:
        print('primary expected')

def term():
    left = primary()
    token = tf.get()
    while True:
        if '*' == token.value:
            left *= primary()
            token = tf.get()
        elif '/' == token.value:
            left /= primary()
            token = tf.get()
        elif '%' == token.value:
            left %= term()
            token = tf.get()
        else:
            tf.putback(token)
            return left

def expression():
    left = term()
    token = tf.get()
    while True:
        if '+' == token.value: 
            left += term()
            token = tf.get()
        elif '-' == token.value:
            left -= term()
            token = tf.get()
        else:
            tf.putback(token)
            return left

def declaration(k): pass

def statement():
    t = tf.get()
    tf.putback(t)
    return expression()

def clean(): pass

def calculate():
    while True:
        print(prompt, end='')
        token = tf.get()
        while token.value == ';': token = tf.get()
        if token.value == quit: return
        tf.putback(token)
        print(result, statement())

try:
    calculate()
except Exception as e:
    print(e)
