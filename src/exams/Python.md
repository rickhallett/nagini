## Python Basics

> The Zen of Python, by Tim Peters
>
> Beautiful is better than ugly.
> Explicit is better than implicit.
> Simple is better than complex.
> Complex is better than complicated.
> Flat is better than nested.
> Sparse is better than dense.
> Readability counts.
> Special cases aren't special enough to break the rules.
> Although practicality beats purity.
> Errors should never pass silently.
> Unless explicitly silenced.
> In the face of ambiguity, refuse the temptation to guess.
> There should be one-- and preferably only one --obvious way to do it.
> Although that way may not be obvious at first unless you're Dutch.
> Now is better than never.
> Although never is often better than *right* now.
> If the implementation is hard to explain, it's a bad idea.
> If the implementation is easy to explain, it may be a good idea.
> Namespaces are one honking great idea -- let's do more of those!

### One Operation per Statement

> Simple is better than complex.
> Readability counts.

I came across this in a blog post and it's generally a great idea.

https://blog.pwkf.org/2023/08/17/one-sloc.html

When you start using comprehensions the temptation is to nest them, as that is how you chain them.
You might well end up writing something like:

```python
urls = ...
url_words = {
    url: {
        word
        for word in requests.get(url).content.split()
    }
    if url in safe_urls
}
```

```harryscript
// Yup, that's me. You're probably wondering how I ended up in this situation.
```

You can imagine this getting arbitrarily complex.
This would be better split up.
Remember that you can just define functions anywhere:

```python
def get_content(url: str) -> str:
    response = requests.get(url)
    return response.content

def get_words(content: str) -> set[str]:
    words = content.split()
    return set(words)

def is_safe(url: str) -> bool:
    return url in safe_urls

urls = ...
filtered_urls = filter(is_safe, urls)
url_contents = {
    url: get_content(url)
    for url in filtered_urls
}
url_words = {
    url: get_words(content)
    for url, content in url_contents.items()
}
```

```ruby
This is a wonderful example. Especially the embedded of requests inside the url_contents comprehension.
It is many times more readable
I like how it is a series of transformations; functional, mixed into procedural
```

Functions should be top level unless there is a good reason not to. One good
reason is to allow the function to close over one or more variables to allow it
to take a single argument. When you do that then the function can be passed to
filter and map and suchlike.

The one operation per statement rule means that you should avoid the walrus
operator (which assigns a variable and returns the value in place).

```ruby
What does 'close over one or more variables' mean?
```

### Comprehensions

> There should be one-- and preferably only one --obvious way to do it.
> Although that way may not be obvious at first unless you're Dutch.

Comprehensions are the array.map and array.filter of python. If you are doing
operations that can be expressed as map and filter you should use
comprehensions (the actual map and filter functions are fine, as I used above,
but they have a subtlety which I will cover later, and using a comprehension in
their place is totally acceptable).

Consider:

```
result = []
for row in data:
    for value in row:
        if value % 2 == 0:
            result.append(value)
```

This is nested and complex code. The problem with it is that the loops can do
literally anything to arrive at the values which accumulate in `result`. The
`result` variable may not be initialized alongside this loop. It obscures the
intent of the code, which is to create a filtered list.

If you have this code then translating it to a comprehension is trivial:

```
result = [
    value
for row in data
    for value in row
        if value % 2 == 0
]
```

(you'd fix the indentation but I've left it to show that I literally just copied the loop across). When I think of these I think of them as:

```
[
    WHAT I GET
    FROM WHERE
    UNDER WHAT CONDITION
]
```

There are four kinds of comprehension, list (most common), dict, set and
generator (least common). The delimiters of the comprehension change what kind
of generator you define:

```
[
    value
    list comprehension
]
{
    key: value
    dict comprehension
}
{
    value
    set comprehension
}
(
    value
    generator comprehension
)
```

If comprehensions are for transforming, when would you use a loop?

You would use a loop if the stopping condition is not easily defined (while
loop). You would use a loop if you need to _do_ something for each element
instead of tranform each element. While you could stick such a thing inside a
comprehension doing so would be as bad as writing a comprehension as a for
loop.

If the comprehension involves a complex transformation, extract the
transformation to a function. If you desire nesting two comprehensions, so that
one produces values for the next, then do that in series and assign the output
of the first comprehension to a variable. Having multiple `for`s in your
comprehension is ok!

### Generators

Generators are important to understand as they turn up a lot, often in places
you do not expect. A generator is something that produces values on demand.

This sounds simple so I will illustrate the difference by considering a list.
When you have a list you can loop over it:

```
for value in values:
    print(value)
```

You can even do that twice:

```
for value in values:
    print(value)
for value in values:
    print(value)
```

You can use indexing to get specific values:

```
print(values[0])
```

This is because a list is defined as a persistent ordered collection of values.

A generator is not persistent. Instead you can ask it for the next value. There
is no way to reset it, once you have a value from a generator the generator has
progressed onwards.

The _type_ that a generator has is iterator. An iterator produces the next
value. You can make an iterator of many things using the `iter` function and,
under the hood, this happens a lot:

```
>>> values = [1, 2, 3]
>>> values_iter = iter(values)
>>> for value in values_iter:
...     print(value)
...
1
2
3
>>> for value in values_iter:
...     print(value)
...
>>>
```

The `map` and `filter` functions return generators. That means that you can
consume them only once. This is the subtlety of them, and means that you
generally should not return the result of calling them from your function.

Converting a generator to a list is easy, just pass it to the `list` function:

```
also_values = list(iter(values))
```

(or `dict` or `set` or `tuple`).

A function can be a generator when you use the `yield` keyword. This is nice
because what happens is that the function produces the yielded value as the
next value in the iteration, and pauses. When you call next again on the
function execution will resume until the next yield. This allows you to have a
lazy function which only performs computation when required, and can be used to
handle larger-than-memory lists (or even produce an infinite number of values).

Finally there is the `yield from` keyword. This is equivalent to yielding each
individual value in a collection. So the following functions are equivalent:

```
def with_yield_from():
    yield from [1, 2, 3]

def without_yield_from():
    for value in [1, 2, 3]:
        yield value
```

`return`ing from one of these functions terminates iteration, and you can force
that at any point.

How is the end of an iterator communicated to the caller? Does it return
`None`? No. `None` is a valid value to return. Instead it throws an exception.

### Exceptions are not Exceptional

The core python language uses exceptions for flow control. They are not
exceptional. This is a significant departure from many other languages:

```
>>> values = [1, 2, 3]
>>> values_iter = iter(values)
>>> next(values_iter)
1
>>> next(values_iter)
2
>>> next(values_iter)
3
>>> next(values_iter)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

A for loop catches a StopIteration exception and uses it to halt the loop. That
is how basic exceptions-as-flow are in python.

So from this we realise that exceptions are not always errors

> Errors should never pass silently.

### With statement

The with statement is used to apply a context manager. What this really means
is that some code is called as the block is entered, and some code is called as
the block is exited. This code is called even if an exception occurs.

The classic motivation that caused them to be defined is this:

```
handle = open(filename)
do_something(handle)
close(handle)
```

If `do_something` throws an exception then the handle is not closed. There are
a finite number of file handles that can be open on a system and you just
leaked one. This is not an idle threat - during my university internship I
wrote the java equivalent of the above and it caused the application to
reliably crash after a few days of continuous operation.

So then people wrote this:

```
handle = open(filename)
try:
    do_something(handle)
finally:
    close(handle)
```

The `finally` block of the `try` is always run even if the code inside the
`try` block throws an exception. However now you've got 5 lines of code to read
a file or do something with it. The more lines of code you take to do
something, the less readable the code is.

So then the with statement was introduced:

```
with open(filename) as handle:
    do_something(handle)
```

This is strictly equivalent to the correct try/finally code, above. How is this
implemented? It's done using a class however we can write our own version using
contextlib:

```
from contextlib import contextmanager

@contextmanager
def with_open(filename):
    handle = open(filename)
    try:
        yield handle
    finally:
        close(handle)
```

When you define try with resources (the java equivalent) in this way you unlock
an incredible amount of stuff. I use context managers heavily, they are used in
pytorch to turn off gradient calculations within the with block. They are used
to provide test fixtures in pytest.

https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager

This really is a wonderful example of

> Simple is better than complex.

By making it this simple - by using a generator function - the with statement
literally transformed what you can do with python. Instead of just closing a
file handle.

But what is that `@contextmanager` thing anyway?

### Decorators

A decorator is a function that takes a function and produces a function BLAH
BLAH BLAH OH GOD MATT SHUT UP WITH THE FUNCTIONAL SHIT.

A decorator is that and it can be useful to know that, however the baby steps
decorator is the with block. The with block can run some code before and after
the code you provide. A decorator can be used to do the same thing:

```
def handle_decorator(function):
    def new_function(filename):
        handle = open(filename)
        try:
            return function(handle)
        finally:
            close(handle)
    return new_function

@handle_decorator
def read_file(handle):
    return read(handle)

read_file("foo.txt")
```

Writing decorators like this is rarely done because context managers _are decorators_:

```
from contextlib import contextmanager

@contextmanager
def with_open(filename):
    handle = open(filename)
    try:
        yield handle
    finally:
        close(handle)

@with_open() # CALL IT
def read_file(handle):
    return read(handle)

read_file("foo.txt")
```

This time the expression after the `@` was a function call! What's the deal
with that?!?

Well the thing after the @ is an expression that returns a function that can
transform the wrapped function. As a demonstration I present to you this crime
against humanity:

```
>>> class HowToPissOffYourCoworkers:
...     def __add__(self, other):
...         return lambda fn: lambda: 1
...
>>> htpoycw = HowToPissOffYourCoworkers()
>>> @(htpoycw + 1)
... def god_matt_i_hate_you():
...     raise NotImplementedError()
...
>>> god_matt_i_hate_you()
1
```

Don't ever do this. Know that you can, but just don't.

```harryscript
Could you give me an example of where you've seen this used in the wild?
```

### What even is a number anyway?

I could add 1 to that class I made above. That was one layer of that shit cake
to unpack. Why did it work?

The python data model (https://docs.python.org/3/reference/datamodel.html)
defines the magic methods that a class must have to have certain behaviour. All
infix operators invoke methods on their operands. The `+` infix operator is
implemented by `__add__`. That is how + is implemented in python. I'm not
joking:

```
In [3]: a = 1

In [4]: a.__class__
Out[4]: int

In [5]: a.__add__
Out[5]: <method-wrapper '__add__' of int object at 0x7fa16d73d388>
```

(finally broke out ipython instead of the plain python interpreter).

From one perspective a number is something that defines a set of things you can
do to it. We could say basic mathematical operations and comparisons. A list is
something where you can call `__getitem__`, `__len__` and `__iter__`. Same for
dictionary, except now `__getitem__` takes anything instead of integers.

So what even is a class? A collection of things. It has `__getattr__` which
allows you to do the `a.b` style variable lookup. A class is a dict with some
fluff:

```harryscript
"A class is a dict with some fluff"
GET OUTTA HERE MAN. That is fn wild
```

```
In [6]: class Example:
   ...:     def __init__(self):
   ...:         self.a = 1
   ...:

In [7]: a = Example()

In [8]: a.__dict__
Out[8]: {'a': 1}
```

(it's a bit more complex, functions are stored elsewhere but yeah this idea has legs).

So how about that simplicity.

Don't start writing classes that make use of this until later. After all,
explicit is better than implicit.

### Pathlib

The pathlib.Path object should be universally used to work with the file system, change my mind.jpg

It has overridden divide to allow you to do this:

```
from pathlib import Path
my_file = Path(__file__) # __file__ is always the current file
my_folder = my_file.parent
my_sibling = my_folder / "sibling.txt"
```

That's amusing. It really shines when you realise you can do this:

```
content = my_sibling.read_text()
```

```harryscript
This is pure enlightenment.
I love this stuff. Understanding the magic behind the scenes is so satisfying.
It is, for me, the very essence of Hogwarts.
```

So why did we need that `with` stuff again... ;-)
