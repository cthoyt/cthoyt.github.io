---
layout: post
title: Switching from using Tox to Just
date: 2025-09-21 11:21:00 +0200
author: Charles Tapley Hoyt
tags:
  - packaging
  - python
  - tox
  - just
  - cookiecutter-snekpack
  - automation
  - CI/CD
---

I became aware of [`just`](https://github.com/casey/just) while watching Hynek's [second video on
`uv`](https://youtu.be/TiBIjouDGuI?si=dh3HFkXx_RThdsEq&t=741) a few months ago. I immediately fell
in love with its elegance
and simplicity, so I have begun replacing task running in my repositories that
relied on [`tox`](https://github.com/tox-dev/tox) with `just`. This post gives a bit of background, context,
and walks through making the switch on one of my repositories that has some annoying dependencies.

## What is Tox

## What is Just

## What I did

The goal of this PR is to replace testing from using tox (involved with `tox -e py`) to using `just` (involved with
`just test`).

Why?

1. `tox` is feeling very slow these days. The `tox-uv` extension was a nice respite, but it only uses `uv` for virtual
   environment construction (iirc) and doesn't take advantage of the other fast parts of uv.
2. `tox` creates a wastefully large cache in every project
3. `uvx` is a more fit-for-purpose solution for many of the things I use `tox` for, i.e., installing and running a tool
   in an isolated virtual environment

How?

I had to start with two other PRs #31 and #33 that did some restructuring of tests and the way dependencies were
declared such that it would even be possible to run tests without all extras/groups installed.

Then, I had to look into the issue caused by ScispaCy, which is running based on notoriously old dependencies (only
works on Python <= 3.12 and with NumPy < 2.0). FYI, I'm not just complaining, I've been making lots of PRs to their
repository to help get to broader compatibility.

The biggest problem with old NumPy dependencies is they're often either 1) not available as a wheel or 2) difficult to
compile in an automated setting.

One solution is to use the `tool.uv.conflicts` configuration to say that the `pandas` and `scispacy` extras can't be
installed at the same time because their (transitive) dependencies have conflicts. Don't confuse these names with the
packages - the extras include a list of related things that are defined in the `project.optional-dependencies` block of
my project configuration.

Ultimately, I did give up on getting ScispaCy test to work. I wanted to have two back-to-back calls to `uv run` like
this:

```console
$ uv run --group tests --all-extras --no-extra scispacy --no-extra gilda -m coverage run -p -m pytest
$ uv run --group tests --group en-core-sci-sm --extra scispacy --extra ontology -m coverage run -p -m pytest
```

Where the first one runs most tests, and the second one just installs the scispacy extras and runs that. However, this
didn't work (it didn't seem to manage to install the `scispacy` extra). This can be follow-up.

## What We Really Want

It would be great if `uv` had a built-in notion of task definitions, since most of the things I had
in my `tox` configuration (and now `justfile`) are calls to install Python environments or run Python
things inside them (this is true for testing, linting, documentation building, publishing, etc.).

There's a long-standing issue on their tracker [https://github.com/astral-sh/uv/issues/5903](astral-sh/uv#5903)
that I'm sure will be addressed in the future, when they've made an excellent design for the developer experience.
I'm looking forward to the future where I can write a follow-up post entitled _Switching from `just` + `uv` to
just `uv`_.
