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

I became aware of [`just`](https://github.com/casey/just) while watching Hynek's
[second video on `uv`](https://youtu.be/TiBIjouDGuI?si=dh3HFkXx_RThdsEq&t=741) a
few months ago. I immediately fell in love with its elegance and simplicity, so
I have begun replacing task running in my repositories that relied on
[`tox`](https://github.com/tox-dev/tox) with `just`. This post gives a bit of
background, context, and walks through making the switch on one of my
repositories that has some annoying dependencies.

## What is Tox

[`tox`](https://github.com/tox-dev/tox) is a tool tailored for developing Python
packages. It takes care of creating a virtual environment for the configuration
then installing the current package with the specified extras and dependency
groups. Here's what my testing configuration in the
[`ssslm`](https://github.com/cthoyt/ssslm/blob/129200609ad6dc9254112364c6ba96bc0b08a1c6/tox.ini#L33-L51)
package looked like:

```ini
[testenv]
description = Run unit and integration tests.
commands =
    coverage run -p -m pytest --durations=20 {posargs:tests}
    coverage combine
    coverage xml
extras =
    gilda-slim
    web
    scispacy
    gliner
    rdflib
    ontology
    pandas
dependency_groups =
    tests
    en-core-sci-sm
```

This can be run with `tox -e py` after installing tox (e.g., `uvx tox -e py` or
`uvx --with tox-uv tox -e py` to enable virtual environment creation with uv)

Tox can actually do a lot more things than this, including skipping installing
the current repository as a Python package to instead install/run development
tools like `ruff`. It also has the ability to refer from the parts of one
configuration to another, which is useful for having different flavors of the
same command (e.g., documentation build vs. documentation test).

Check the Tox documentation or see the `tox.ini` file in SSSLM v0.1.2, the last
version before I switched from Tox to Just:
[https://github.com/cthoyt/ssslm/blob/v0.1.2/tox.ini](https://github.com/cthoyt/ssslm/blob/v0.1.2/tox.ini).

## What is Just

[`just`](https://github.com/casey/just) is a more generic tool for writing
tasks, which is a much better fit than Makefiles - read the Just homepage for
excellent arguments which I won't recapitulate here. Here's what the previous
Tox configuration looks using Just's custom syntax in a file called `justfile`,
this time using uv to do the heavy lifting:

```justfile
[doc("run unit and integration tests")]
test:
    just coverage erase
    uv run --group tests --all-extras --no-extra scispacy --no-extra gilda -m coverage run -p -m pytest
    just coverage combine
    just coverage xml

[doc("run `coverage` with a given subcommand")]
@coverage command:
    uvx --from coverage[toml] coverage {% raw %}{{command}}{% endraw %}
```

This can be run with `just test` after installing just (e.g.,
`uvx --from rust-just just test`).

Note that `uv` is now doing the heavy lifting for environment management and
installation instead of Tox, and Just simply ties it all together.

## Making the Switch

I finally got around to testing replacing running my tests with tox with running
my tests with just in
[cthoyt/ssslm#32](https://github.com/cthoyt/ssslm/pull/32). I did this because:

1. `tox` is feeling very slow these days. The `tox-uv` extension was a nice
   respite, but it only uses `uv` for virtual environment construction (iirc)
   and doesn't take advantage of the other fast parts of uv.
2. `tox` creates a wastefully large cache in every project
3. `uvx` is a more fit-for-purpose solution for many of the things I use `tox`
   for, i.e., installing and running a tool in an isolated virtual environment

I had to start with two other PRs to SSSLM
([cthoyt/ssslm#31](https://github.com/cthoyt/ssslm/pull/31) and
[cthoyt/ssslm#33](https://github.com/cthoyt/ssslm/pull/33)) that did some
restructuring of tests and the way dependencies were declared such that it would
even be possible to run tests without all extras/groups installed.

Then, I had to look into the issue caused by
[ScispaCy](https://github.com/allenai/scispacy/), which is running based on
notoriously old dependencies (only works on Python <= 3.12 and with NumPy <
2.0). FYI, I'm not just complaining, I've been making upstream PRs to their
repository to help get to broader compatibility.

The biggest problem with old NumPy dependencies is they're often either 1) not
available as a wheel or 2) difficult to compile in an automated setting.

One solution is to use the `tool.uv.conflicts` configuration to say that the
`pandas` and `scispacy` extras can't be installed at the same time because their
(transitive) dependencies have conflicts. Don't confuse these names with the
packages - the extras include a list of related things that are defined in the
`project.optional-dependencies` block of my project configuration.

Ideally, I wanted my test configuration in my `justfile` to have two
back-to-back calls to `uv run` like this:

```console
$ uv run --group tests --all-extras --no-extra scispacy --no-extra gilda -m coverage run -p -m pytest
$ uv run --group tests --group en-core-sci-sm --extra scispacy --extra ontology -m coverage run -p -m pytest
```

The first command runs most tests, and the second one just installs the scispacy
extras and runs that. However, this didn't work (it didn't seem to manage to
install the `scispacy` extra). I think there is a solution for this, but I am
still learning about the nuances of `uv run` and uv's notion of locking.

I tabled getting ScispaCy tests for SSSLM to work for now, since this is not a
generic concern of most packages. The next steps are to test replacing all Tox
environments with corresponding just commands in SSSLM, then upstream this to my
cookiecutter template
[https://github.com/cthoyt/cookiecutter-snekpack](https://github.com/cthoyt/cookiecutter-snekpack)
so all of my repositories can benefit.

## What We Really Want

It would be great if `uv` had a built-in notion of task definitions, since most
of the things I had in my `tox` configuration (and now `justfile`) are calls to
install Python environments or run Python things inside them (this is true for
testing, linting, documentation building, publishing, etc.).

There's a long-standing issue on their tracker
[https://github.com/astral-sh/uv/issues/5903](astral-sh/uv#5903) that I'm sure
will be addressed in the future, when they've made an excellent design for the
developer experience. I'm looking forward to the future where I can write a
follow-up post entitled _Switching from `just` + `uv` to just `uv`_ (wordplay
intended).
