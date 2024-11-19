---
layout: post
title: Dependency Groups and ReadTheDocs
date: 2024-11-19 13:39:00 +0200
author: Charles Tapley Hoyt
tags:
  - Python
  - Packaging
  - Cookiecutter
  - Documentation
---

[PEP 735](https://peps.python.org/pep-0735/) introduced dependency groups in
packaging metadata, which are complementary to
[optional dependencies](https://peps.python.org/pep-0631/) in that they might
not correspond to features in the package, but rather be something like
development or release dependencies. I am slowly working towards
[updating](https://github.com/cthoyt/cookiecutter-snekpack/pull/32) my
cookiecutter template
[cookiecutter-snekpack](https://github.com/cthoyt/cookiecutter-snekpack) to use
PEP 735. So far, uv and tox have released support - all that's left is
[ReadTheDocs](https://about.readthedocs.com/). This post summarizes the issue I
added to their issue tracker and the following discussion.

## Summary of optional dependencies and dependency groups.

Before PEP 735, optional dependencies were often used both for extra features
(e.g., installing `lxml` for faster XML parsing) as well as development
dependencies (e.g., for testing and documentation build). Here's what the syntax
for this looks like:

```toml
[project.optional-dependencies]
faster-xml = [
    "lxml",
]
tests = [
    "pytest",
    "coverage",
]
docs = [
    "sphinx>=8",
    "sphinx-rtd-theme>=3.0",
    "sphinx-click",
    "sphinx_automodapi",
]
```

When you're using `pip` (or uv) to install, you can use square bracket notation
to say which ones go in.

```console
$ pip install .[tests,docs,faster-xml]
```

This is a bit problematic since it conflates what the purpose of optional
dependencies are. Some build tools tried to address with their on custom
configuration for development dependencies in `pyproject.toml` or elsewhere.
However, dependency groups gives us a more principled approach towards
categorizing dependencies that are not necessarily relevant for the code itself.
Now, we can split up the example from before like this:

```toml
[project.optional-dependencies]
faster-xml = [
    "lxml",
]

[dependency-groups]
tests = [
    "pytest",
    "coverage",
]
docs = [
    "sphinx>=8",
    "sphinx-rtd-theme>=3.0",
    "sphinx_automodapi",
]
```

When you're using `pip` (or uv) to install, you can use `--dependency-groups` to
say which ones go in.

```console
$ pip install --dependency-groups=tests,typing .[faster-xml]
```

## Preparing an environment on ReadTheDocs

ReadTheDocs currently supports specifying optional dependencies (see
https://docs.readthedocs.io/en/stable/config-file/v2.html#packages) with
configuration like the following:

```yaml
version: 2

python:
  install:
    - method: pip
      path: .
      extra_requirements:
        - docs
```

In my issue
[#11766](https://github.com/readthedocs/readthedocs.org/issues/11766), I
suggested defining an alternate key `dependency_groups` that could work the same
way.

```yaml
version: 2

python:
  install:
    - method: pip
      path: .
      dependency_groups:
        - docs
```

## ReadTheDocs code deep dive and implementation suggestion

I found a few places that would be relevant for a theoretical implementation.
First, there's a data structure that represents the slots available in the
configuration for `python > install`. Here's the code
([permalink](https://github.com/readthedocs/readthedocs.org/blob/404d82a448295c81a271c3143d0fc9c10a924555/readthedocs/config/models.py#L77-L82)):

```python
class PythonInstall(Base):
    __slots__ = (
        "path",
        "method",
        "extra_requirements",
    )
```

I'd simply add a new slot `dependency_groups` and update the related processing
code
([permalink](https://github.com/readthedocs/readthedocs.org/blob/404d82a448295c81a271c3143d0fc9c10a924555/readthedocs/doc_builder/python_environments.py#L66-L67)):

```python
...
if install.extra_requirements:
    extra_req_param = "[{}]".format(",".join(install.extra_requirements))
...
```

Here's what I'd do:

```python
# Added these next lines
dependency_group_args = []
if install.dependency_groups:
    # not clear if the equals is necessary or if
    # this can be broken into two parts
    dependency_group_args.append("--dependency-groups={}".format(",".join(install.dependency_groups))

extra_req_param = ""
if install.extra_requirements:
    extra_req_param = "[{}]".format(",".join(install.extra_requirements))
self.build_env.run(
    self.venv_bin(filename="python"),
    "-m",
    "pip",
    "install",
    "--upgrade",
    "--upgrade-strategy",
    "only-if-needed",
    "--no-cache-dir",
    "{path}{extra_requirements}".format(
        path=local_path,
        extra_requirements=extra_req_param,
    ),
    *dependency_group_args,
    cwd=self.checkout_path,
    bin_path=self.venv_bin(),
)
```

As a minor note, I would also do a bit of refactoring to store all the args into
the list and then splat all of them into `run()`

## There Has To Be A Better Way (TM)

As Raymond H. always says, there has to be a better way. Turns out, the RTD team
is already working on a more generic way to override the installation command
via the configuration in
[#11710](https://github.com/readthedocs/readthedocs.org/pull/11710).

```yaml
version: 2

build:
  jobs:
    install:
      - pip install --dependency-groups=tests,typing
```

This reduces the need to make potentially lots of update to the rigid code I
worked on above. This makes me very happy!

---

I've received a lot of poorly written issues and requests in my open source work
(see the PyKEEN issue tracker) so I thought it was incredibly important to write
this issue very well. It occurred to me that the thought process here is also
maybe generally interesting, so that's why I copied it to my blog.
