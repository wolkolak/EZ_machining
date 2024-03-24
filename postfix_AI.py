import math
import re

import math


def infix_to_postfix(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, 'sin': 4, 'cos': 4, 'tan': 4}
    stack = []
    postfix = ''
    number = ''

    for char in expression:
        if char.isdigit() or char == '.':
            number += char
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                postfix += stack.pop()
            stack.pop()
        elif char in precedence:
            while stack and stack[-1] in precedence and precedence[char] <= precedence[stack[-1]]:
                postfix += stack.pop()
            stack.append(char)
        elif char.isalpha():  # Variable
            postfix += char
        else:
            postfix += number
            number = ''

    postfix += number
    while stack:
        postfix += stack.pop()

    return postfix


def evaluate_postfix(expression):
    stack = []
    operators = {'+', '-', '*', '/', '^', 'sin', 'cos', 'tan'}
    for token in expression.split():
        if token not in operators:
            stack.append(float(token))
        else:
            if token in {'sin', 'cos', 'tan'}:
                value = stack.pop()
                if token == 'sin':
                    stack.append(math.sin(math.radians(value)))
                elif token == 'cos':
                    stack.append(math.cos(math.radians(value)))
                elif token == 'tan':
                    stack.append(math.tan(math.radians(value)))
            else:
                operand2 = stack.pop()
                operand1 = stack.pop()
                if token == '+':
                    stack.append(operand1 + operand2)
                elif token == '-':
                    stack.append(operand1 - operand2)
                elif token == '*':
                    stack.append(operand1 * operand2)
                elif token == '/':
                    stack.append(operand1 / operand2)
                elif token == '^':
                    stack.append(operand1 ** operand2)
    return stack.pop()


expression = "3 + 4 * 2 / ( 1 - 5 ) ^ 2 + sin(45)"
postfix = infix_to_postfix(expression)
result = evaluate_postfix(postfix)
print(f"Postfix: {postfix}")
print(f"Result: {result}")
