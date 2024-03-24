# Expression Calculation

![ffff](icon.png)

The project can translate infix expressions to postfix(str to tuple with members of different types). 
And can calculate if needed. 

Used algorithm from **[Алгоритм сортировочной станции](https://ru.wikipedia.org/wiki/Алгоритм_сортировочной_станции)** ,
also known as **[Shunting yard algorithm](https://en.wikipedia.org/wiki/Shunting_yard_algorithm)**. I used less detailed russian wiki and had no choice but improove it a little - degree('^') handler added. Unary minus was created too - better fix negatives in postfixing than in calculating.


You can see files here https://github.com/wolkolak

I tried to find suitable module on PYPI but failed unfortunately: 

<font color="#089F0">**Firstly**</font> expression can contain functions: <font color="#c589F0">**sin**</font> , <font color="#c589F0">**pow**</font> , <font color="#c589F0">**mod**</font> , <font color="#c589F0">**neg**</font> , etc. Most projects can't do that.
<details> 
  <summary>Why? </summary>
    Now then i started to think about it, isn't it because trigonometry only for sinners? 
</details>

<font color="#089F0">**Secondly**</font> module should handle logic operators too: <font color="#f03c15">**'<'**</font> , <font color="#f03c15">**'=='**</font> , <font color="#f03c15">**'AND'**</font> , <font color="#f03c15">**'OR'**</font> , etc.

<font color="#089F0">**The third point**</font> - i need to create postfix expressions **tens of times**, and calculate it **thousands of times**.
Because of that postfix expressions had to be turned into **tuples**. Entire module is a part of my CNC interpreter.
----
To calculate infix expression You need next functions:
1.  <font color="#1589F0">tokenize</font>\
a = tokenize(<font color="#089F0">'-2^ -(sin(5)*3)</font>')\
   print(a)\
->><font color=gray>['-', 2.0, '^', '(', '-', '(', 'sin', '(', 5.0, ')', '*', 3.0, ')', ')']</font>'
2. <font color="#1589F0">tokensPostfixing</font>\
   b = tokensPostfixing(a)\
   print(b)\
   --><font color=gray>(2.0, 5.0, 'sin', 3.0, '*', '_', '^', '_')</font>'
3. <font color="#1589F0">postfixTokenCalc</font>\
   print(postfixTokenCalc(b, VARdict=None))\
    <font color="gray">-0.8342390624578879</font>
   
    print(postfixTokenCalc((5, 1.0, '+', 6, '=='), DICT_VARS=None))\
    <font color="gray">True</font>
   
    print('complex?: ', postfixTokenCalc((5, 3j, '-',)))\
    <font color="gray">complex?:  (5-3j)</font>
   

As you can see, even complex numeric type didn't break the program. For now. I do not require complex in CNC, so I run only one test with it.\
And '=' is not a mathematical or logical operator - your expression for calculation should not contain assignments in the middle(You can start from "=" though). Best time to handle assignments would be after tokenization, I believe. 


If You need  different operators and functions (or sin in radians for example), look at the  followed dicts and modify:

* OPERATORs_DICT_math: &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;  +, -, /, *, ^
* OPERATORs_DICT_logic_L &nbsp; &nbsp;  &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;AND, NOT, OR', GT...
* OPERATORs_DICT_func_1 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; sqrt, pow1', abc, neg, mod, sin ...  &nbsp; &nbsp; &nbsp;  # functions with 1 arg
* OPERATORs_DICT_func_2 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; pow2  &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; # functions with 2 args
* OPERATORs_DICT_compare1 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; <, =, >  **(= should only be used as a part of '<=', '>=', '==')**
* OPERATORs_DICT_compare2 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; <=, ==, <>, >=
* OPERATORs_PRECEDENCE_DICT &nbsp; &nbsp; &nbsp; functions and operators precedence, obviously

Also, You can use DICT_VARS to look for your variables. You can throw away some operators like 'GT' or 'EQ' - this is the same as '>' and '==' in some CNC and other languages, and not required for You, probably.

<font color="#c03c15">PS: This is my first attempt to share code with others, tell me if something wrong.</font>