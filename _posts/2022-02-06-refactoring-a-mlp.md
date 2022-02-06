---
layout: post
title: Refactoring a Machine Learning Model
date: 2022-02-06 16:45:00 +0100
author: Charles Tapley Hoyt
tags: programming machine-learning deep-earning
---
This blog post is a tutorial that will take you from a naive implementation of a
[multilayer perceptron](https://en.wikipedia.org/wiki/Multilayer_perceptron) in
PyTorch to an enlightened implementation that simultaneously leverages the power
of PyTorch, Python's builtins, and some powerful third party Python packages.

This tutorial is going to assume the following imports for all code blocks:

```python
import itertools as itt

import more_itertools
from torch import nn
from torch.nn import functional as F
```

1. [`itertools`](https://docs.python.org/3/library/itertools.html) is a builtin
   library for helping deal with lists, sets, and other iterables.
2. [`more_itertools`](https://github.com/more-itertools/more-itertools) is a
   third-party extension to itertools, highly regarded in the Python community.
3. You should already be familiar with [PyTorch](https://pytorch.org/) and
   writing your own subclasses of `torch.nn.Module` by implementing your
   own `__init__()` and `forward()` functions.

This tutorial isn't really about the theory nor application of machine learning
models - it's just about the best ways to implement them. I'm also going to
commit the sin of omitting docstrings and a lot of type annotations, since most
of the MLP should be pretty obvious.

Let's start with a naive implementation, that reflects a lot of bad habits from
C or Java programming:

```python
import torch
from torch import nn
from torch.nn import functional as F


class MLP1(nn.Module):
    def __init__(self, dims: list[int]):
        super().__init__()
        layers = []
        for i in range(len(dims) - 1):
            in_features, out_features = dims[i], dims[i + 1]
            layer = nn.Linear(in_features, out_features)
            layers.append(layer)
        self.layers = nn.ModuleList(layers)

    def forward(self, x: torch.FloatTensor) -> torch.FloatTensor:
        rv = x
        for layer in self.layers:
            rv = layer(rv)
            rv = F.relu(rv)
        return rv
```

MLP1 uses the dreaded `range(len(...))` pattern, which can almost always be
replaced with direct iteration. However, in this case, it uses the index to get
the next element with it. Luckily, `more_itertools` has a function
[`pairwise()`](https://more-itertools.readthedocs.io/en/stable/api.html#more_itertools.pairwise)
that does exactly this. MLP1 can then be refactored into:

```python
import torch
from more_itertools import pairwise
from torch import nn
from torch.nn import functional as F


class MLP2(nn.Module):
    def __init__(self, dims: list[int]):
        super().__init__()
        layers = []
        for in_features, out_features in pairwise(dims):
            layer = nn.Linear(in_features, out_features)
            layers.append(layer)
        self.layers = nn.ModuleList(layers)

    def forward(self, x: torch.FloatTensor) -> torch.FloatTensor:
        rv = x
        for layer in self.layers:
            rv = layer(rv)
            rv = F.relu(rv)
        return rv
```

The application of `F.relu` in `forward()` is suspect for a few reasons:

1. Because it lives as a hard-coded call in `forward()`, there's no way to make
   it into a hyper-parameter that can be chosen by a user
2. Because it's the functional form `F.relu` and not `nn.ReLU`, it can't be
   stacked with other layers

MLP2 can be refactored to address both of those by using the modular
form `nn.ReLU` in the layers after creating each `nn.Linear`.

```python
import torch
from more_itertools import pairwise
from torch import nn


class MLP3(nn.Module):
    def __init__(self, dims: list[int]):
        super().__init__()
        layers = []
        for in_features, out_features in pairwise(dims):
            layers.append(nn.Linear(in_features, out_features))
            layers.append(nn.ReLU())
        self.layers = nn.ModuleList(layers)

    def forward(self, x: torch.FloatTensor) -> torch.FloatTensor:
        rv = x
        for layer in self.layers:
            rv = layer(rv)
        return rv
```

Now that the `forward()` function is just a successive application of layers, it
can be exchanged with a `nn.Sequential`. MLP3 can be refactored to look like:

```python
import torch
from more_itertools import pairwise
from torch import nn


class MLP4(nn.Module):
    def __init__(self, dims: list[int]):
        super().__init__()
        layers = []
        for in_features, out_features in pairwise(dims):
            layers.append(nn.Linear(in_features, out_features))
            layers.append(nn.ReLU())
        self.layers = nn.Sequential(*layers)

    def forward(self, x: torch.FloatTensor) -> torch.FloatTensor:
        return self.layers(x)
```

The following two improvements will make the construction of the `layers` list
that goes in `nn.Sequential` much more elegant. First, we'll refactor MLP4 to
use the `extend` function of a list rather than `append`:

```python
import torch
from more_itertools import pairwise
from torch import nn


class MLP5(nn.Module):
    def __init__(self, dims: list[int]):
        super().__init__()
        layers = []
        for in_features, out_features in pairwise(dims):
            layers.extend((
                nn.Linear(in_features, out_features),
                nn.ReLU(),
            ))
        self.layers = nn.Sequential(*layers)

    def forward(self, x: torch.FloatTensor) -> torch.FloatTensor:
        return self.layers(x)
```

Anytime we see a pattern like

```python
old_list = ...
new_list = []
for x in old_list:
    new_list.append(transform(x))
```

we know that we can transform it using a list comprehension like

```python
old_list = ...
new_list = [
    transform(x)
    for x in old_list
]
```

There's an analogous pattern for anytime we see something like

```python
old_list = ...
new_list = []
for x in old_list:
    new_list.extend(transform(x))
```

using [`itertools.chain.from_iterable()`](https://docs.python.org/3/library/itertools.html#itertools.chain.from_iterable)
like

```python
import itertools as itt

old_list = ...
new_list = list(itt.chain.from_iterable(
    transform(x)
    for x in old_list
))
```

We'll apply this template to our code to get a one-liner for instantiating
our `nn.Sequential` (though notice it's broken up onto multiple lines for
readability):

```python
from itertools import chain

import torch
from more_itertools import pairwise
from torch import nn


class MLP6(nn.Module):
    def __init__(self, dims: list[int]):
        super().__init__()
        self.layers = nn.Sequential(*chain.from_iterable(
            (
                nn.Linear(in_features, out_features),
                nn.ReLU(),
            )
            for in_features, out_features in pairwise(dims)
        ))

    def forward(self, x: torch.FloatTensor) -> torch.FloatTensor:
        return self.layers(x)
```

Finally, since we're now just creating a module that wraps the exact
functionality of `nn.Sequential`, it's possible to directly
subclass `nn.Sequential`:

```python
from itertools import chain

from more_itertools import pairwise
from torch import nn


class MLP7(nn.Sequential):
    def __init__(self, dims: list[int]):
        super().__init__(*chain.from_iterable(
            (
                nn.Linear(in_features, out_features),
                nn.ReLU(),
            )
            for in_features, out_features in pairwise(dims)
        ))
```

---

There are some other improvements that could be made to this MLP implementation
to make the activation function parametrizable, but I'll save that for a later
post where I describe
the [`class-resolver`](https://github.com/cthoyt/class-resolver)
package and how it can be used to do this.