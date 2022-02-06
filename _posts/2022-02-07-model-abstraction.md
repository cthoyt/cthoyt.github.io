This blog post is a tutorial that will take you illustrate how to generalize the
implementation of a [multilayer perceptron](https://en.wikipedia.org/wiki/Multilayer_perceptron)

We'll pick up with the final model from my previous post:

```python
from itertools import chain

from more_itertools import pairwise
from torch import nn


class MLP(nn.Sequential):
    def __init__(self, dims: list[int]):
        super().__init__(*chain.from_iterable(
            (
                nn.Linear(in_features, out_features),
                nn.ReLU(),
            )
            for in_features, out_features in pairwise(dims)
        ))
```

This MLP uses a hard-coded [rectified linear unit](https://en.wikipedia.org/wiki/Rectifier_(neural_networks))
as the non-linear activation function between layers. We can generalize this MLP
to use a variety of non-linear activation functions by adding an argument to its
`__init__()` function like in:

```python
from itertools import chain

from more_itertools import pairwise
from torch import nn


class MLP2(nn.Sequential):
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

The first issue with this implementation is it relies on a hard-coded set of
conditional statements and is therefore hard to extend. It can be improved by
using a dictionary lookup:

```python
from itertools import chain

from more_itertools import pairwise
from torch import nn

activation_lookup: dict[str, nn.Module] = {
    "relu": nn.ReLU(),
    "tanh": nn.Tanh(),
    "hardtanh": nn.Hardtanh(),
}


class MLP3(nn.Sequential):
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

This approach is rigid because it requires pre-instantiation of the activations.
If we needed to vary the arguments to the `nn.HardTanh` class, the previous
approach wouldn't work. We can change the implementation to lookup on the
class *before instantiation* then optionally pass some arguments:

```python
from itertools import chain

from more_itertools import pairwise
from torch import nn

activation_lookup: dict[str, type[nn.Module]] = {
    "relu": nn.ReLU,
    "tanh": nn.Tanh,
    "hardtanh": nn.Hardtanh,
}


class MLP4(nn.Sequential):
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

This is pretty good, but it still has a few issues:

1. you have to manually maintain the `activation_lookup` dictionary,
2. you can't pass an instance or class through the `activation` keyword
3. you have to get the casing just right
4. the default is hard-coded as a string, which means this has to get copied
   (error-prone) in any place that creates an MLP
5. you have to re-write this logic for all of your classes

Enter the `class_resolver` package, which takes care of all of these things
using the following:

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


Now, you can instantiate the MLP with any of the following:

```python
MLP(dims=[10, 200, 40])  # uses default, which is ReLU
MLP(dims=[10, 200, 40], activation="relu")  # uses lowercase
MLP(dims=[10, 200, 40], activation="ReLU")  # uses stylized
MLP(dims=[10, 200, 40], activation=nn.ReLU)  # uses class
MLP(dims=[10, 200, 40], activation=nn.ReLU())  # uses instance

MLP(dims=[10, 200, 40], activation="hardtanh",
    activation_kwargs={"min_val": 0.0, "max_value": 6.0})  # uses kwargs
MLP(dims=[10, 200, 40], activation=nn.HardTanh,
    activation_kwargs={"min_val": 0.0, "max_value": 6.0})  # uses kwargs
MLP(dims=[10, 200, 40], activation=nn.HardTanh(0.0, 6.0))  # uses instance
```

In practice, it makes sense to stick to using the strings in combination with
hyper-parameter optimization libraries like [Optuna](https://optuna.org/).

---

Because this is such a common pattern, we've made it available through contrib
module in `class_resolver.contrib.torch`:

```python
from itertools import chain

from class_resolver import Hint
from class_resolver.contrib.torch import activation_resolver
from more_itertools import pairwise
from torch import nn


class MLP(nn.Sequential):
    def __init__(
        self,
        dims: list[int],
        activation: Hint[nn.Module] = None,
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
