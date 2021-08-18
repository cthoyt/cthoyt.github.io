---
layout: post
title: Machine Learning Needs More Generators
date: 2021-08-18 12:21:00 +0100
author: Charles Tapley Hoyt
tags: machine-learning
---
I've spent the last two days cleaning up some research machine learning code that blew up when I
tried applying it to my own data due to memory constraints. This post is about the anti-pattern that
caused this, how I fixed it, and how you can avoid it too.

The [INDRA Lab](https://indralab.github.io/) has been collaborating with my old PhD
cellmate [Daniel Domingo-Fernández](https://github.com/ddomingof) and his master's
student [Helena Balabin](https://github.com/helena-balabin/) on cross-modal transformers. We've
jointly pre-trained a transformer ([STonKGs](https://github.com/stonkgs/stonkgs)) on knowledge graph
embeddings on the [INDRA database](https://db.indra.bio) and the associated evidence text for each
triple.

We then fine-tuned models for various downstream tasks, including one for rating the correctness of
a given statement (relevant since most are from large-scale text mining). We're very interested in
comparing this to INDRA's belief system that will be described in an upcoming publication from our
group.

I wanted to apply this fine-tuned model to the self-updating models
in [EMMAA](https://emmaa.indra.bio/), but ran into some memory errors since the code was building up
big lists, converting the lists into DataFrames using [pandas](https://emmaa.indra.bio/), then
exporting to disk as a TSV. The solution is to use generator functions (that create iterable for use
with for loops) and write the results to a file directly. The basic anti-pattern looks like this:

```python
import pandas as pd


def f(df: pd.DataFrame) -> pd.DataFrame:
    new_rows = []
    for _, row in df.iterrows():
        new_row = {
            ...  # somehow build up a new row, as a dictionary
        }
        new_rows.append(new_row)
    return pd.DataFrame(new_rows)
```

There are two problems with this:

1. The input must be completely built up before calling `f()`
2. The output must be completely built up before returning

This compounds for every function `f()`, `g()`, `h()`, and so on that takes in the result from the
last dataframe transformation, since they all have to keep everything in memory.
In [STonKGs](https://github.com/stonkgs/stonkgs), the first transformation is to look up the
embeddings for a given source/target/evidence triple from both the knowledge graph embedding and the
pre-trained BERT language model. The second transformation is to pre-process the embeddings. The
third is to actually apply the STonKGs model to jointly embed them. The fourth is to apply the
fine-tuned model. Each of these happens at varying speeds, but are unfortunately decoupled.

Python has really powerful tool for using ideas
from [functional programming](https://en.wikipedia.org/wiki/Functional_programming)
in an approachable way that allows us to solve this issue. Rather than building up a huge list, we
can simply yield each piece so another function can consume them with a for loop. When I refactor
code that looks like this, I make a second helper function that does the hard work, and try and
maintain the original function's interface by calling the helper function:

```python
import pandas as pd


def f(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(f_helper(df))


def f_helper(df: pd.DataFrame) -> Iterable[Mapping[Any, Any]]:
    # new_rows = []  # we don't need this anymore!
    for _, row in df.iterrows():
        new_row = {
            ...  # somehow build up a new row, as a dictionary
        }
        yield new_row
```

If you're not familiar with `yield`, here are a two videos to get you thinking aboout how to use
loops like a Pythonista:

- [Loop like a native: while, for, iterators, generators (PyCon US 2013)](https://www.youtube.com/watch?v=EnSu9hHGq5o&list=PLPFmTfhIBiumfYT3rsa35fHJxabB78er1&index=5)
- [Trey Hunner - Comprehensible Comprehensions (PyCon 2020)](https://www.youtube.com/watch?v=ei71YpmfRX4&list=PLPFmTfhIBiumfYT3rsa35fHJxabB78er1&index=6)

Now that we have `f_helper`, we solved issue #2. The solution to issue #1 is to have functions that
take in only the parts that are needed to build up each new row. This means you should accept an
iterable, and have the high level function slice up the dataframe or do whatever pre-procesing is
necessary first:

```python
import pandas as pd


def f(df: pd.DataFrame) -> pd.DataFrame:
    it = (row for _, row in df.iterrows())
    return pd.DataFrame(f_helper(it))


def f_helper(rows: Iterable[Mapping[Any, Any]]) -> Iterable[Mapping[Any, Any]]:
    for row in rows:
        new_row = {
            ...  # somehow build up a new row, as a dictionary
        }
        yield new_row
```

With this refactoring, the code still does what it used to, but now you can think about how you
might string together `f_helper()`, `g_helper()`, `h_helper()`, and so on directly, since they don't
need to get completely materialized as a list. If you do the composition of several functions that
take in iterables and yield stuff (i.e., they return an iterable of the stuff that gets yielded),
then you don't have to worry about running out of memory since it only needs to have the results of
one set of transformations from the compositions of all functions at a time. In my case, I just
printed the results to a file and then it no longer needed to be in memory.

---

This was a quick blog post I wrote while the code I updated was running. The full PR I did can be
found at https://github.com/stonkgs/stonkgs/pull/7 for reference. Feel free to chime in on that PR
if you have some questions about how I did this or get in touch with any of the contact info on the
bottom of my blog.
