'''_

Let's create a few simple decorators.

First, write a decorator called "rounded", that rounds a function's
value to the nearest whole number.  (Hint: use Python's built-in
round() function.)

>>> @rounded
... def multiply(x, y):
...     return x * y

>>> @rounded
... def divide(x, y):
...     return x / y

>>> multiply(1.5, 1.5)
2
>>> multiply(2, 1.99)
4

>>> divide(10, 3)
3
>>> divide(10, 7)
1
>>> divide(8, 3)
3

Remember to support keyword arguments!

>>> multiply(x=3, y=2.99)
9
>>> divide(y=3, x=8)
3


Next, make a "floor" decorator - that always rounds *down*.
(Hint: Python's math module has a floor() function.)

>>> @floor
... def multiply_down(x, y):
...     return x * y

>>> @floor
... def divide_down(x, y):
...     return x / y

>>> multiply_down(1.5, 1.5)
2
>>> multiply_down(2, 1.99)
3

>>> divide_down(10, 3)
3
>>> divide_down(8, 3)
2


EVERYONE LOVES TEXT IN ALL CAPS! SO NOW WRITE A "SHOUT" DECORATOR.

>>> @shout
... def say_hello(who):
...     return f"Hello, {who}!"

>>> @shout
... def recite(items):
...     items = items.copy()
...     items[-1] = "and " + items[-1]
...     return ", ".join(items)

>>> say_hello("George")
'HELLO, GEORGE!'

>>> say_hello("Stephanie")
'HELLO, STEPHANIE!'

>>> recite(["orange", "purple", "silver"])
'ORANGE, PURPLE, AND SILVER'

>>> recite(["Python", "Go", "Javascript", "C"])
'PYTHON, GO, JAVASCRIPT, AND C'


And finally, create a decorator called "printvalue". Which is similar
to printlog, except it gives more information:

>>> @printvalue
... def diff(x, y):
...     return x - y

>>> diff(10, 3)
Got value from diff: 7
7

>>> diff(1, 1)
Got value from diff: 0
0

(HINT: Python function objects have a __name__ attribute.)

'''

# Write your code here:

import math

def rounded(func):
    def wrapper(*args, **kwargs):
        return round(func(*args, **kwargs))
    return wrapper

def shout(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper()
    return wrapper

def floor(func):
    def wrapper(*args, **kwargs):
        return math.floor(func(*args, **kwargs))
    return wrapper

def printvalue(func):
    def wrapper(*args, **kwargs):
        value = func(*args, **kwargs)
        print(f"Got value from {func.__name__}: {value}")
        return value
    return wrapper

# Do not edit any code below this line!

if __name__ == '__main__':
    import doctest
    count, _ = doctest.testmod()
    if count == 0:
        print('*** ALL TESTS PASS ***\nGive someone a HIGH FIVE!')

# Part of Powerful Python. Copyright MigrateUp LLC. All rights reserved.
