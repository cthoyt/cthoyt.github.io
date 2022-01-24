---
layout: post
title: The Official Rules of Python Packaging Speedrunning
date: 2022-01-24 01:30:00 +0100
author: Charles Tapley Hoyt
tags: programming
---
I figured over the holiday break or early days of the new year, I'd catch up on
some serious blogging. Instead, here's my first post of 2022: a silly take on
a topic I actually care a lot about. Here are the rules for Python Packaging
Speedruns.

## What's a speedrun?

Speedrunning is the sport of finishing a video game as fast as possible. Some
games are so broken 
(e.g., [The Legend of Zelda: Ocarina of Time](https://www.speedrun.com/oot))
that it's not really even that interesting to just get to the end, so many
games introduce additional variants to Any% such as 100%. For each game,
the speedrunning community decides when the timer should start (e.g., most games
have a start screen and this is usually pretty obvious) and when the timer
should end (e.g., when the credits screen rolls or when the last user input
is given on a final boss). 

## What's a packaging speedrun?

The video game speedrunning community has the benefit that the
same speedrun can be done over and over again, with pretty reliable conditions
on how it starts and end. However, each Python packaging speedrun will be
done on a different repository. It doesn't really make sense for more than one
person to do a packaging speedrun on the same repository, since the goal besides
being fast is to make practical improvements to unpackaged code and submit
a pull request to original authors. 

## Python Packaging Speedrun Any%

I'm going to propose a set of minimal rules for a Python packaging speedrun,
which I'll designate as Any% because it's the simplest version that has the
least restrictions. Other categories can take these rules and build on top
of them.

### Rule 1: Timing

Python packaging speedruns are timed in the following way:

1. Start the clock when you click the fork button on GitHub
2. End the clock after all commits have been made to your fork AND a pull request has been made.

### Rule 2: Package Layout

To ensure imports aren't sneakily being done via directory structure, the
`src/` layout is mandatory for _all_ Python packaging speedruns. Read
Hynek Schlawack's excellent explanation why this restriction is necessary
[here](https://hynek.me/articles/testing-packaging/).

### Rule 3: Minimal Unit Testing

To make sure that packaging was done properly, automated unit tests should check
that the package can be imported using the same directory structure
where `tests/test_trivial.py` contains the following:

```python
# test_trivial.py

import importlib
import unittest

class TestTrivial(unittest.TestCase):
    def test_import(self):
        name = "<your package name goes here>"
        module = importlib.import_module(name)
        self.assertIsNotNone(module)
```

### Rule 4: Automated Application of Testing

This file should be run with `tox` on a `tox.ini` that minimally contains the
following `[testenv]`:

```ini
# tox.ini

[tox]
envlist =
    py

[testenv]
commands =
    pytest tests/
deps =
    pytest
description = Run unit tests.
```

Note the `[tox]` section was included for ergonomic usage of the `tox` command
from the command line.

### Rule 5: Provenance

Finally, like video game speedruns, there needs to be video proof, preferably
uploaded to YouTube or witnessed on Twitch.

## Potential Variants

Since the Any% is pretty simple, I think there is room for all sorts of variants
including:

1. Passes flake8 with a pre-determined set of plugins (e.g., flake8-black, flake8-isort, flake8-docstrings, pydocstyle)
2. Passes flake8 with previous plugins and harder ones (e.g., flake8-print, darglint)
3. Passes mypy

## Parting thoughts

Each speedrun will require a different amount of effort to achieve
these things based on the size of the package and what state the original code
was in. Obviously, Python packaging speedruns can't be so rigorously compared
as video game speedruns. That's okay.

I posted my [first Python packaging speedrunning](https://www.youtube.com/watch?v=-aje6kszNcc)
on YouTube this evening. It doesn't actually follow the rules I proposed here
because I started thinking about this after I was done [tweeting](https://twitter.com/cthoyt/status/1485406393251377159)
about it. Please let me know if you have any ideas on how to improve these
rules, have an idea for a new category, or if you want me to link to your
Python packaging speedrun video.
