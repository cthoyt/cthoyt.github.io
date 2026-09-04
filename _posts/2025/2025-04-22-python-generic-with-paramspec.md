---
layout: post
title: Using ParamSpec with Python Generics
date: 2025-04-22 10:31:00 +0200
author: Charles Tapley Hoyt
tags:
  - Python
  - mypy
  - static typing
---

I've been working on applying strict static typing to my Python package
[`class-resolver`](https://github.com/cthoyt/class-resolver) and ran into an
interesting way of using
[generics](https://docs.python.org/3/library/typing.html#generics) in
combination with parameter specification variables (i.e.,
[ParamSpec](https://docs.python.org/3/library/typing.html#typing.ParamSpec)s).

Normally, if you want to type annotate a function, you use the
[`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable),
which works like the following:

```python
from collections.abc import Callable

#: the [int] represents a function that takes in a single integer,
#:  and returns a single floating point number
IntToFloat = Callable[[int], float]

# this function fits the type annotation above, impl omitted
def square_root(x: int) -> float:
    ...

# simple example to show how to write functions that consume functions
def applies_int_to_float(func: Callable[[int], float], x: int) -> float:
    return func(x)


>>> applies_int_to_float(square_root, 9)
3.0
```

However, if you want to get generic, you need to use a combination of
[ParamSpec](https://docs.python.org/3/library/typing.html#typing.ParamSpec) for
the input variable signature and
[TypeVar](https://docs.python.org/3/library/typing.html#typing.TypeVar) for the
return value.

```python
from collections.abc import Callable
from typing import TypeVar

X = TypeVar("X")
T = TypeVar("T")

# simple example to show how to write functions that consume functions
def applies_unary_function(func: Callable[[X], T], x: X) -> T:
    return func(x)


>>> applies_unary_function(square_root, 9)
3.0
```

If you want to make the input fully generic, you can use `ParamSpec` and
reference `P.args` (or `P.kwargs`, not shown here):

```python
from collections.abc import Callable
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")

def applies_unary_function_generic(func: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
    return func(*args, **kwargs)


>>> applies_unary_function_generic(square_root, 9)
3.0
```

This gets even a bit more complicated if you want to type annotate a class that
can take in a generic set of functions. Here's an example on how this works:

```python
from collections.abc import Callable
from typing import Generic, ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")


class ListOfFunctions(Generic[P, T]):
    def __init__(self, functions: list[Callable[P, T]]) -> None:
        self.functions = functions


def identity(x: int) -> int:
    return x


def plus_two(x: int) -> int:
    return x + 2

my_list: ListOfFunctions[[int], int] = ListOfFunctions([identity, plus_two])
```

The most important part of this discovery for me was actually how to
type-annotate the resulting object, which magically is able to accept a list in
the place where the `ParamSpec` should be.

Here's the new way to write the same class using
[PEP-0695](https://peps.python.org/pep-0695/) type parameter syntax, introduced
in Python 3.12:

```python
from collections.abc import Callable


class ListOfFunctions[**P, T]:
    def __init__(self, functions: list[Callable[P, T]]) -> None:
        self.functions = functions
```

---

My two big wishes for typing in the future:

- make the builtin `any` be a valid substitution for `typing.Any`
- make some cute syntax, so I don't need to import
  `from collections.abc import Callable`
