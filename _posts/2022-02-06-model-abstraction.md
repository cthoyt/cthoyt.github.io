---
layout: post
title: Abstracting the parameters of a Machine Learning Model
date: 2022-02-06 19:00:00 +0100
author: Charles Tapley Hoyt
tags: programming machine-learning deep-learning python
---
As a follow-up to my [previous post]({% post_url 2022-02-06-model-refactoring %})
on refactoring and improving a machine learning model implemented with
[PyTorch](https://pytorch.org), this post will be a tutorial on how to
generalize the implementation of a [multilayer perceptron (MLP)](https://en.wikipedia.org/wiki/Multilayer_perceptron)
to use one of several potential non-linear activation functions in an elegant
way.

We'll pick up with the seventh (final) model version of the MLP from my
previous post:

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

## Incremental Improvements

This MLP uses a
hard-coded [rectified linear unit](https://en.wikipedia.org/wiki/Rectifier_(neural_networks))
as the non-linear activation function between layers. We can initially
generalize MLP7 to use a variety of non-linear activation functions by adding an
argument to its `__init__()` function:

```python
from itertools import chain

from more_itertools import pairwise
from torch import nn


class MLP8(nn.Sequential):
    def __init__(self, dims: list[int], activation: str = "relu"):
        if activation == "relu":
            activation = nn.ReLU()
        elif activation == "tanh":
            activation = nn.Tanh()
        elif activation == "hardtanh":
            activation = nn.Hardtanh()
        else:
            raise KeyError(f"Unsupported activation: {activation}")
        super().__init__(chain.from_iterable(
            (
                nn.Linear(in_features, out_features),
                activation,
            )
            for in_features, out_features in pairwise(dims)
        ))
```

The first issue with this MLP8 is it relies on a hard-coded set of conditional
statements and is therefore hard to extend. It can be improved by using a
dictionary lookup:

```python
from itertools import chain

from more_itertools import pairwise
from torch import nn

activation_lookup: dict[str, nn.Module] = {
    "relu": nn.ReLU(),
    "tanh": nn.Tanh(),
    "hardtanh": nn.Hardtanh(),
}


class MLP9(nn.Sequential):
    def __init__(self, dims: list[int], activation: str = "relu"):
        activation = activation_lookup[activation]
        super().__init__(chain.from_iterable(
            (
                nn.Linear(in_features, out_features),
                activation,
            )
            for in_features, out_features in pairwise(dims)
        ))
```

Unfortunately, the approach in MLP9 rigid because it requires pre-instantiation
of the activations. If we needed to vary the arguments to the `nn.HardTanh`
class (i.e., the minimum and maximum values), the previous approach wouldn't
work. We can change the implementation to lookup on the class *before
instantiation* then optionally pass some arguments:

```python
from itertools import chain

from more_itertools import pairwise
from torch import nn

activation_lookup: dict[str, type[nn.Module]] = {
    "relu": nn.ReLU,
    "tanh": nn.Tanh,
    "hardtanh": nn.Hardtanh,
}


class MLP10(nn.Sequential):
    def __init__(
        self,
        dims: list[int],
        activation: str = "relu",
        activation_kwargs: None | dict[str, any] = None,
    ):
        activation_cls = activation_lookup[activation]
        activation = activation_cls(**(activation_kwargs or {}))
        super().__init__(chain.from_iterable(
            (
                nn.Linear(in_features, out_features),
                activation,
            )
            for in_features, out_features in pairwise(dims)
        ))
```

MLP10 is a big improvement in terms of flexibility, but it has a few remaining
practical issues:

1. you have to manually maintain the `activation_lookup` dictionary,
2. you can't pass a pre-instantiated instance of an activation class via
   the `activation` argument
3. you have to get the casing of the string keys just right
4. the default is hard-coded as a string, which means this has to get copied
   (error-prone) in any place that creates an MLP
5. you have to re-write this logic for all of your classes

## The `class-resolver`

Before showing MLP11, the final solution, I want to first describe the
[`class-resolver`](https://github.com/cthoyt/class-resolver) package. Its job is
to make it easy to generate a dictionary-like object that you can use to look up
classes (like we prepared for MLP10). It's smart and takes care of several
things for you:

1. Automatically assigns keys in the dictionary based on the class name. If all
   the classes in the *resolver* share a suffix, it automatically strips it.
2. It uses some simple string normalization during lookup, so it's insensitive
   to capitalization, varied usage of underscores, or other punctuation.
3. It keeps track of a default value to grab when you pass `None`
4. It allows for classes and instances to be passed through

After making a `ClassResolver` instance, you can use
the `ClassResolver.lookup()` function to get the class you need:

```python
from class_resolver import ClassResolver
from torch import nn

activation_resolver = ClassResolver(
    [nn.ReLU, nn.Tanh, nn.Hardtanh],
    base=nn.Module,
    default=nn.ReLU,
)

# Default lookup
assert nn.ReLU == activation_resolver.lookup(None)

# Name-based lookup
assert nn.ReLU == activation_resolver.lookup("relu")
assert nn.ReLU == activation_resolver.lookup("ReLU")

# Class-based lookup
assert nn.ReLU == activation_resolver.lookup(nn.ReLU)
```

Built on top of the `ClassResolver.lookup()` function is the
`ClassResolver.make()` function, which first looks up the class, then gives you
an instance of it (optionally using keyword arguments you pass).

```python
# Default instantiation
assert nn.ReLU() == activation_resolver.make(None)

# Name-based instantiation
assert nn.ReLU() == activation_resolver.make("relu")
assert nn.ReLU() == activation_resolver.make("ReLU")

# Class-based instantiation
assert nn.ReLU() == activation_resolver.make(nn.ReLU)

# Class-based instantiation w/ keyword arguments
assert nn.Hardtanh(0.0, 6.0) == activation_resolver.make("hardtanh", {
    "min_val": 0.0, "max_value": 6.0
})
```

## Bringing it All Together

Let's apply that to MLP10 and make our final MLP11:

```python
from itertools import chain

from class_resolver import ClassResolver
from more_itertools import pairwise
from torch import nn

activation_resolver = ClassResolver(
    [nn.ReLU, nn.Tanh, nn.Hardtanh],
    base=nn.Module,
    default=nn.ReLU,
)


class MLP11(nn.Sequential):
    def __init__(
        self,
        dims: list[int],
        activation: None | str | nn.Module | type[nn.Module] = None,
        activation_kwargs: None | dict[str, any] = None,
    ):
        super().__init__(chain.from_iterable(
            (
                nn.Linear(in_features, out_features),
                activation_resolver.make(activation, activation_kwargs),
            )
            for in_features, out_features in pairwise(dims)
        ))
```

Now, you can instantiate the MLP with any of the following:

```python
MLP11(dims=[10, 200, 40])  # uses default, which is ReLU
MLP11(dims=[10, 200, 40], activation="relu")  # uses lowercase
MLP11(dims=[10, 200, 40], activation="ReLU")  # uses stylized
MLP11(dims=[10, 200, 40], activation=nn.ReLU)  # uses class
MLP11(dims=[10, 200, 40], activation=nn.ReLU())  # uses instance

MLP11(dims=[10, 200, 40], activation="hardtanh",
      activation_kwargs={"min_val": 0.0, "max_value": 6.0})  # uses kwargs
MLP11(dims=[10, 200, 40], activation=nn.HardTanh,
      activation_kwargs={"min_val": 0.0, "max_value": 6.0})  # uses kwargs
MLP11(dims=[10, 200, 40], activation=nn.HardTanh(0.0, 6.0))  # uses instance
```

In practice, it makes sense to stick to using the strings in combination with
hyper-parameter optimization libraries like [Optuna](https://optuna.org/).

---

Because the usage of `class-resolver` for resolving activation functions from
PyTorch is so common, we've made it available through contrib module
in `class_resolver.contrib.torch`. In fact, the `activation_resolver` comes with
some extra logic to automatically grab *all* activation modules from
`torch.nn.modules.activation`. Therefore, we can rewrite the example for MLP11
to simply import it.

```python
from itertools import chain

from class_resolver.contrib.torch import activation_resolver
from more_itertools import pairwise
from torch import nn


class MLP(nn.Sequential):
    def __init__(
        self,
        dims: list[int],
        activation: None | str | nn.Module | type[nn.Module] = None,
        activation_kwargs: None | dict[str, any] = None,
    ):
        super().__init__(chain.from_iterable(
            (
                nn.Linear(in_features, out_features),
                activation_resolver.make(activation, activation_kwargs),
            )
            for in_features, out_features in pairwise(dims)
        ))
```
