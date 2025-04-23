---
layout: post
title: I wish I could unpack Callables in Python type annotations
date: 2025-04-23 15:23:00 +0200
author: Charles Tapley Hoyt
tags:
  - Python
  - mypy
  - static typing
---

Following the theme of my previous two posts, I've run into another typing
conundrum where I want to unpack a pre-existing `Callable` into a class with
`Generic[P, T]` where P is a parameter specification type (i.e. `ParamsSpec`)

After figuring out the right way to [declare a generic featuring a
`ParamSpec`]({% post_url 2025-04-22-python-generic-with-paramspec %}), I updated
the [`class-resolver`](https://github.com/cthoyt/class-resolver) package to use
the shiny new (and more accurate) annotations. Unfortunately, reality set in,
and within hours, someone
[reported this caused errors](https://github.com/pykeen/pykeen/issues/1539) in
[PyKEEN](https://github.com/pykeen/pykeen), my graph machine learning software
package that heavily uses `class-resolver` to make its knowledge graph embedding
models modular and configurable.

I was able to fix PyKEEN, but the fact that I was previously using a named type
alias for `Normalizer: TypeHint = Callable[[torch.Tensor], torch.Tensor]` and
then had to re-write it yet again the variable declaration's type hint as
`FunctionResolver[[torch.Tensor], torch.Tensor]` was not great. What I would
love is some way to unpack `Normalizer` into the arguments of
`FunctionResolver[...]`.

Let me demonstrate in a more self-contained way:

```python
from typing import Callable, Generic, Unpack, ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")

class Box(Generic[P, T]):
    def __init__(self, func: Callable[P, T]) -> None:
        self.func = func

def f(x: int) -> str:
    return str(x)

# This works!
box_1: Box[[int], str] = Box(f)

FType = Callable[[int], str]

# I wish I could do this, in case I already
# had a type variable referring to Callable[[int], str]
box_2: Box[Unpack[FType]] = Box(f)
```

While I'm abusing the usage of
[`typing.Unpack`](https://docs.python.org/3/library/typing.html#typing.Unpack),
some way of extracting the arguments of one type and splatting them into another
seems like it _might_ have a use case. Maybe.
