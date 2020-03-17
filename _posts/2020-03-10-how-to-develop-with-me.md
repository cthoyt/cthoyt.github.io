---
layout: post
title: How to Develop with Me
date: 2020-03-10 00:00:00 -0800
---
This blog post is about all of the very particular ways I do software development in Python.
I try and stick to doing things the ways I've seen other people do them

## Package Structure

After following the debate on [pypa/packaging.python.org#320](https://github.com/pypa/packaging.python.org/issues/320),
I've opted to use the `src/` layout as aptly described by
[Ionel Cristian Mărieș](https://blog.ionelmc.ro/2014/05/25/python-packaging/),
and [Hynek Schlawack](https://hynek.me/articles/testing-packaging/).

This means that there's a top-level `tests/` directory (will come back to that later) and no possibility of mixing up
your working directory when making imports. I also enforce the sole usage of
[relative imports](https://realpython.com/absolute-vs-relative-python-imports/#relative-imports) to make sure there are
no accidental circular imports. While I know this is allowed and reasonable sometimes, I assume others will misuse it.
Additionally, relative imports force users to access their scripts like modules using the command line like
`python -m my_module.my_submodule`. This is good because I believe there should be no such thing as Python scripts.
You should always think about packaging and how someone else will use your code later.

## Licensing

Your package should have a file called LICENSE (no extension) that tells people how they're allowed to use your code.
Even if you're working in a company and won't be sharing code, it's still good practice.

An excellent resource to help you choose a license is [https://choosealicense.com/](https://choosealicense.com/). I
normally pick [MIT License](https://choosealicense.com/licenses/mit/) because it's easy for other people to use and
modify.

## Packaging

I use a [declarative setup](https://setuptools.readthedocs.io/en/latest/setuptools.html) in all of my packages. It's
not easy to figure out everything in this documentation, so I always copy-paste from a previous project, usually
[pybel/pybel](https://github.com/pybel/pybel/blob/master/setup.cfg).

You still need a `setup.py` when using a declarative setup. It should always look exactly like this:

```python
# -*- coding: utf-8 -*-

"""The setup module."""

import setuptools

if __name__ == '__main__':
    setuptools.setup()
```

The first section in the `setup.cfg` is `[metadata]`. The [top](https://github.com/pybel/pybel/blob/dba0c5afd37bef7d162937d0407045f15a515a87/setup.cfg#L5-L8)
of the `setup.cfg` for PyBEL looks like this:

```ini
[metadata]
# The name of the package (should be same as what's in `src/{your project name}`)
name = pybel
# The version of the package (you should start with 0.0.1-dev for new projects)
version = 0.14.6-dev
# A one line description of your package, should be the same as the module-level docstring
# in src/{your project}/__init__.py
description = Parsing, validation, compilation, and data exchange of Biological Expression Language (BEL)
# The `file:` magical preix tells it to load what's in your README.rst. You did write a nice readme, right?
long_description = file: README.rst
```

The [next few lines](https://github.com/pybel/pybel/blob/dba0c5afd37bef7d162937d0407045f15a515a87/setup.cfg#L10-L16)
describe the places where project resources live on the internet:

```ini
# [metadata]
# URLs associated with the project
url = https://github.com/pybel/pybel
download_url = https://github.com/pybel/pybel/releases
project_urls =
    Bug Tracker = https://github.com/pybel/pybel/issues
    Source Code = https://github.com/pybel/pybel
    Documentation = https://pybel.readthedocs.io
```

Next is [author and licensing information](https://github.com/pybel/pybel/blob/dba0c5afd37bef7d162937d0407045f15a515a87/setup.cfg#L18-L26).

```ini
# [metadata]
# Author information
author = Charles Tapley Hoyt
author_email = cthoyt@gmail.com
maintainer = Charles Tapley Hoyt
maintainer_email = cthoyt@gmail.com

# License Information
license = MIT
license_file = LICENSE
```

The `license_file` entry obviously points to the file. The `license` entry is what gets shown on PyPI, and I'm not
exactly sure what the controlled vocabulary is. But for MIT, it works, so happy hunting.

Next comes the [PyBEL classifiers](https://github.com/pybel/pybel/blob/dba0c5afd37bef7d162937d0407045f15a515a87/setup.cfg#L28-L42).
This is a list of [trove classifiers](https://pypi.org/classifiers/) that are a controlled vocabulary for describing
your project's development status, who should use it, its topics, *etc*.

```ini
# [metadata]
# Search tags
classifiers =
    Development Status :: 5 - Production/Stable
    Environment :: Console
    Intended Audience :: Developers
    Intended Audience :: Science/Research
    License :: OSI Approved :: MIT License
    Operating System :: OS Independent
    Programming Language :: Python
    Programming Language :: Python :: 3.7
    Programming Language :: Python :: 3.6
    Programming Language :: Python :: 3.5
    Programming Language :: Python :: 3 :: Only
    Topic :: Scientific/Engineering :: Bio-Informatics
    Topic :: Scientific/Engineering :: Chemistry
```

Again, the license is very important! `pyroma` (see below) won't pass if you don't have this. Also the other things
are important too, because this will tell users that you're cool and only allow the newest Python versions.
Unfortunately, I still have to support Python 3.5 in PyBEL for downstream dependencies :/ 

Next are the [keywords](https://github.com/pybel/pybel/blob/dba0c5afd37bef7d162937d0407045f15a515a87/setup.cfg#L43-L49),
which can be whatever you want. Here's what I've got for PyBEL.

```ini
# [metadata]
keywords =
    Biological Expression Language
    BEL
    Domain Specific Language
    DSL
    Systems Biology
    Networks Biology
```

Next is the `[options]` section. First we'll tell it what the requirements for the package are:

```ini
[options]
install_requires =
    networkx>=2.1
    sqlalchemy
    click
    click-plugins
    bel_resources>=0.0.3
    more_itertools
    requests
    requests_file
    pyparsing
    tqdm
```

This is part that's hard to explain. The `packages` and `package_dir` option are tricky... you just have to do it
this way and everything magically works. Then, you basically say the same thing one more time in the
`[options.packages.find]`.

```ini
# [options]
# You're always supposed to set zip_safe = false
zip_safe = false
# If you have some non-python files inside your `src/{your package/` directory you
# want to come for the ride when other people use your code, do this
include_package_data = True
# Always tell people what python you support! Is redundant of classifiers, but that's how it is.
python_requires = >=3.5

# Where is my code?
packages = find:
package_dir =
    = src

[options.packages.find]
where = src
```

## Testing (The Prequel Series)

To make a tiny little test that shows everything works, make the following file in `tests/test_import.py`:

```python
# -*- coding: utf-8 -*-

"""Test the module can be imported."""

import unittest

class TestImport(unittest.TestCase):
    """A test case for import tests."""

    def test_import(self):
        """Test that PyBEL can be imported."""
        import pybel
```

Now you're ready to run some tests. Do the following in your shell:

```shell script


```

## Building with Tox

## Packaging Metadata

I use `pyroma` to make sure that I remembered to put everything in the packaging metadata. It can be run with

1. `pip install pyroma` (you *do* have Python3's pip3 linked to pip, right?)
2. `pyroma --min=10 .`

I welcome and encourage you to copy my configuration, but don't forget to carefully change everything to your metadata.
It's pretty embarrassing if you accidentally attribute your work to me. I've done it before by accident. I've seen
others do it too...

```ini
[testenv:pyroma]
deps =
    pygments
    pyroma
skip_install = true
commands = pyroma --min=10 .
description = Run the pyroma tool to check the package friendliness of the project.
```

## Making a CLI

### `cli.py`

```python
# -*- coding: utf-8 -*-

"""Command line interface for PyBEL.

Why does this file exist, and why not put this in ``__main__``? You might be tempted to import things from ``__main__``
later, but that will cause problems--the code will get executed twice:

- When you run ``python3 -m pybel`` python will execute``__main__.py`` as a script. That means there won't be any
  ``pybel.__main__`` in ``sys.modules``.
- When you import __main__ it will get executed again (as a module) because
  there's no ``pybel.__main__`` in ``sys.modules``.
.. seealso:: https://click.palletsprojects.com/en/7.x/setuptools/
"""

import click

@click.command()
def main():
    """Command line interface for PyBEL."""

if __name__ == '__main__':
    main()
```

This script can now be run as `python -m pybel.cli`, but there's a better way 


### `__main__.py`

```python
# -*- coding: utf-8 -*-

"""Entrypoint module, in case you use `python -m pybel`.

Why does this file exist, and why __main__? For more info, read:

 - https://www.python.org/dev/peps/pep-0338/
 - https://docs.python.org/3/using/cmdline.html#cmdoption-m
"""

from .cli import main

if __name__ == '__main__':
    main()
```

### Console Scripts

```ini
[options.entry_points]
console_scripts =
    obo = pyobo.cli:main
```

## Where to Put Data

- Make folder in home directory, allow environment variable to change where this goes by default
- use `~.config/` folder for configuration

## Code Style with `flake8`

Mercilessly use `flake8` to check your code has good style. If your code doesn't have good style, nobody else will be
able to read it. I use the following extensions:

```ini
[testenv:flake8]
skip_install = true
deps =
    flake8
    flake8-bandit
    flake8-colors
    flake8-docstrings
    flake8-import-order
    flake8-commas
    pep8-naming
    pydocstyle
    darglint
commands =
    flake8 src/pybel/ tests/ setup.py
description = Run the flake8 tool with several plugins.
```

## Random Code Style Necessities

Every python file must start with the file encoding, a newline, then the module docstring like:

```python
# -*- coding: utf-8 -*-

"""The module-level docstring."""
```

This docstring has to follow `flake8` rules, meaning there's a short description that fits on the first line then
there's a period. After that, there can be a blank line before any other restructured text-formatted documentation
you'd like.

## Static Type Checking with `mypy`


## Documentation with Sphinx


## Bonus Round: How to Develop with Ben Gyori

This isn't something I do, but to maintain a clean git history, [Ben Gyori](https://github.com/bgyori) frequently
reminds me to rebase on master. This keeps a more linear history of what happened and when. Here are his
instructions:

```bash
git fetch --all
# This is your master
git checkout master
# This is their master
git merge --ff-only upstream/master
git rebase master <your branch name>
# Optionally
git push -f origin <your branch name>
```