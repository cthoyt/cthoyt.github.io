---
layout: post
title:
  A dilemma with PEP-696 default generics when using optional static typing in
  Python
date: 2025-04-19 17:45:00 +0200
author: Charles Tapley Hoyt
tags:
  - Python
  - mypy
  - static typing
---

This post describes an issue I've had with writing correct types when using
[PEP-696](https://peps.python.org/pep-0696) defaults in `typing.TypeVar`. I
posted the exploration in a
[companion repository](https://github.com/cthoyt/python-typing-dilemma) on
GitHub.

The motivation behind this comes from my work in biomedical data integration and
the semantic web. I wrote the [`curies`](https://github.com/cthoyt/curies)
Python package to provide a fully generic and reusable data model for
representing pairs of prefixes and local unique identifiers via the
[`curies.Reference`](https://curies.readthedocs.io/en/latest/api/curies.Reference.html)
class.

I extended this class in the
[`bioregistry`](https://github.com/biopragmatics/bioregistry) in order to
validate and standardize prefixes and local unique identifiers using its
detailed set of metadata rules. This is implemented in the
[ `bioregistry.NormalizedReference`](https://bioregistry.readthedocs.io/en/stable/api/bioregistry.Registry.html).

In other places, like [`ssslm`](https://github.com/cthoyt/ssslm), I've built on
the `curies.Reference` data structure for maximum compatibility. However,
sometimes I want to be able to inject the `bioregistry.Reference` class to get
the guarantees of standardization. However, I don't want the `ssslm` package to
have to know about the Bioregistry, since I want to keep `ssslm` package
generic.

The solution might be with [PEP-0696](https://peps.python.org/pep-0696), which
extends the ability to specify generic types with defaults. This means places
where I used to hard-code a `curie.Reference`, I can now use a generic on the
entire class that has `curie.Reference` as the default... in theory.

In practice, it isn't so easy. I boiled it down to a fully self-contained
example (which I also dumped in
[https://github.com/cthoyt/python-typing-dilemma](https://github.com/cthoyt/python-typing-dilemma)).

```python
from typing import Any, TypeVar

type Record = dict[str, Any]


class Element:
    def __init__(self, record: Record) -> None:
        self.record = record


class DerivedElement(Element):
    pass


# note, we're using PEP-696 default keyword, which is available from Python 3.13 onwards
T = TypeVar("T", bound=Element, default=Element)


def from_record_1(record: Record, element_cls: type[T] = Element) -> T:
    return element_cls(record)
```

This _should_ work. In fact, MyPy is able to infer the types correctly for the
return value. The big question is: what's the correct way to type-annotate
`element_cls`? If you run MyPy on this, you get (abridged output):

```console
$ git clone https://github.com/cthoyt/python-typing-dilemma
$ cd python-typing-dilemma
$ uvx --python 3.13 mypy --strict main.py
main.py:23: error: Incompatible default for argument "element_cls" (default has type "type[Element]", argument has type "type[T]")  [assignment]
```

I tried a few other things:

- Defining a second type variable
  `TType = TypeVar("TType", bound=type[Element])` or
  `TType = TypeVar("TType", bound=type[Element], default=type[Element])` (not
  included in the repo)
- Defining a second type based on the first
  `TType = TypeVar("TType", bound=type[T])` (not included in the repo)
- Using `None` as a sentinel value (try #2)
- Using overloads (try #3, suggested by Guido)

None of this worked, so I asked for help. Turns out, other people ran into this
issue already and brought it up with MyPy.

- https://github.com/python/mypy/issues/3737
- https://github.com/python/mypy/issues/12962
- https://github.com/python/mypy/issues/18812

Right now, I don't think my use case can be solved, so I'll have to sit tight!
