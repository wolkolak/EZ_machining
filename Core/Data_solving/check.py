#print(2**2**3)
import re
#my regards to wiki and Ahens | An Initiative to Initial
class Stack:
    def __init__(self) -> None:
        self.STACK = list()

    def isEmpty(self) -> bool:
        if self.STACK == []:
            return True
        return False

    def push(self, item: str) -> None:
        self.STACK.append(item)

    def pop(self) -> str:
        if self.isEmpty():
            return "Underflow"
        item: str = self.STACK.pop()
        return item

    def peek(self) -> str:
        if self.isEmpty():
            return "Underflow"
        else:
            return self.STACK[-1]


def isHigherPrecedence(val1: str, val2: str) -> bool:
    """Returns True if 1st value have higher precedence than 2nd value."""
    PRECEDENCE: list = ["^", "*/", "+-"]
    val1_index: int = None
    val2_index: int = None
    for i in range(len(PRECEDENCE)):
        if val1 in PRECEDENCE[i]:
            val1_index = i
        if val2 in PRECEDENCE[i]:
            val2_index = i
    if val1_index != None and val2_index != None:
        if val1_index > val2_index or (val1_index == 0 and val2_index == 0):
            return False
        else:
            return True
    else:
        return False




def tokenize(input_string:str):
    print('input_string = ', input_string)
    p_l = input_string.split(' ')
    new_p_l = []
    for p in p_l:
        print('symbol = |{}|'.format(p))
        if p != ' ' and p != '':
            try:
                p = float(p)
            except:
                pass
            new_p_l.append(p)
    print('rez = ', new_p_l)

    #return output

#gg = '55 6.2   / *   -'
#tokenize(gg)

def postfix(infix: str) :#todo from -> str to -> list
    #todo STACK should be list
    STACK: object = Stack()
    if infix[0] != "(" or infix[-1] != ")":
        infix = "("+infix+")"
    postfix: str = ""
    #postfix_list = []
    for i in infix:
        if i in "(+-*/^":
            while isHigherPrecedence(STACK.peek(), i):
                item: str = STACK.pop()
                if item not in ("Underflow", "(", ")"):
                    postfix += item

            STACK.push(i)
        elif i == ")":
            while STACK.peek() != "(":
                item: str = STACK.pop()
                if item not in ("Underflow", "(", ")"):
                    postfix += ' ' + item + ' '#edited
            item: str = STACK.pop()
            if item not in ("Underflow", "(", ")"):
                postfix += item
        else:
            postfix += i

    tokenize(input_string=postfix)
    return postfix






#from infix_postfix.infix_postfix import infix,postfix
#p = postfix('20.1 + (5.2 ^ 2.01 / 2.6)')
#p = postfix('20.1 + (5. ^ 2. / 2.)')
#p = postfix('20.1 + ( 5. ^ 2. / 2. )')
##p = postfix('ab + ( 5 ^ 2 / 2 )')
#print(p)
print(5.1//1)
print(5.1%1)