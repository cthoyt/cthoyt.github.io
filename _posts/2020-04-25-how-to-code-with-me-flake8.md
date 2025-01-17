---
layout: post
title: How to Code with Me - Flake8 Hell
date: 2020-04-25 00:00:00 -0800
author: Charles Tapley Hoyt
tags: code-with-me
---

As scientists, we place huge importance on the communication of our results. We
spend lots of time on editing, revising, and formatting so people can understand
what we did. We also write a lot of code, so why aren't we investing the same
amount of love? Enter, [flake8](https://flake8.pycqa.org/en/latest/).

It's incredibly important that we write following community standards so when
other people read our work, they don't have to think about how it's organized.
For scientific prose, this usually means the IMRD
(introduction-methods-results-discussion) format. In Python, my current favorite
programming language for science, this means using a standardized number of
spaces for indents (4), using triple-double quotes for docstrings in the
beginning of each module, class, and function, and lots more.

It's pretty intimidating to figure out style. For english prose, Strunk and
White wrote
[_The Elements of Style_](http://www.jlakes.org/ch/web/The-elements-of-style.pdf).
For Python, Guido van Rossum wrote
[PEP-8](https://www.python.org/dev/peps/pep-0008/) and Raymond Hettinger
presented [Beyond PEP-8](https://www.youtube.com/watch?v=wf-BqAjZb8M). Even with
these resources, it's still hard to learn which are rules and which
[are more like guidelines](https://www.youtube.com/watch?v=k9ojK9Q_ARE).

This post is a short explanation of how I use `flake8` to keep a consistent
style in the code in my Python projects. There's a similar command line tool for
fixing the style in R projects that's already built into most operating
systems - `rm -rf *`, but I won't get more into that here.

It's pretty easy to get up and running with `flake8` - just run
`pip install flake8` then use it from the shell on a python file like
`flake8 my_file.py` or `flake8 my_directory/`. Then, it outputs a list of
problems that need to be fixed on a line-by-line basis in your code.

![Flake8 Feedback](/img/flake8_output.png)

You can also install plugins with `pip` like that extend the kinds of things it
checks. A few that I install are:

- [flake8-builtins](https://github.com/gforcada/flake8-builtins) - make sure you
  don't accidentally name a variable the same thing as a builtin. This happens a
  lot with `id`.
- [flake8-bugbear](https://github.com/PyCQA/flake8-bugbear) - "find likely bugs
  and design problems in your program", like when you have an unused variable in
  a loop
- [flake8-colors](https://github.com/and3rson/flake8-colors) - add color to the
  `flake8` output (explanation how to set up is below)
- [flake8-commas](https://github.com/PyCQA/flake8-commas) - add trailing commas
  where appropriate
- [flake8-comprehensions](https://github.com/adamchainz/flake8-comprehensions)
  reminders to use list comprehensions where appropriate
- [flake8-docstrings](https://github.com/PyCQA/flake8-docstrings) - make sure
  your docstrings are present and written in the right format
- [flake8-import-order](https://github.com/PyCQA/flake8-import-order) - make
  sure your imports are organized properly
- [flake8-print](https://github.com/JBKahn/flake8-print) - make sure you never
  ever ever use `print()`. The literal only exception is when using print to get
  text into a file with `print(..., file=...)`
- [flake8-use-fstring](https://github.com/MichaelKim0407/flake8-use-fstring) -
  make sure you're using f-strings instead of `%` or `.format()` formatting.
  Exception being for logging.
- [pep8-naming](https://github.com/PyCQA/pep8-naming) - make sure names of
  variables, classes, and modules look right.
- [pydocstyle](https://github.com/PyCQA/pydocstyle/) - docstring style checker

In each of my repositories, I put all of the information on how to install
`flake8` and its plugins then run them in a `tox` configuration under the
`[testenv:flake8]` header so they can easily reproducibly run with
`tox -e flake8`. An example of part of one of my `tox.ini` files (which always
lives in the root of the repository) is below:

```ini
[testenv:flake8]
skip_install = true
deps =
    flake8
    flake8-bandit
    flake8-builtins
    flake8-bugbear
    flake8-colors
    flake8-commas
    flake8-comprehensions
    flake8-docstrings
    flake8-import-order
    flake8-print
    flake8-use-fstring
    pep8-naming
    pydocstyle
commands =
    flake8 src/pybel/ tests/ setup.py
description = Run the flake8 tool with several plugins (bandit, docstrings, import order, pep8 naming).
```

Another configuration file you can set up in the root of the repository is
`.flake8`. Unfortunately, the Python configuration file reader doesn't allow
some of the crazy characters that I want to use for the colors so this can't be
included in `setup.cfg` or `tox.ini` like most of your other configuration.

```ini
[flake8]
ignore =
    # line break before binary operator
    W503
exclude =
    .tox,
    .git,
    __pycache__,
    docs/source/conf.py,
    build,
    dist,
    tests/fixtures/*,
    *.pyc,
    *.egg-info,
    .cache,
    .eggs
max-line-length = 120
import-order-style = pycharm
application-import-names =
    pybel
    bel_resources
    tests
format = ${cyan}%(path)s${reset}:${yellow_bold}%(row)d${reset}:${green_bold}%(col)d${reset}: ${red_bold}%(code)s${reset} %(text)s
```

First thing you'll notice is the `ignore` list. This isn't here to turn `flake8`
off because you're feeling lazy. If somebody includes a change in this list in
their PR, you have to explain to them that compliance is not optional, then help
them work through the problem that they obviously gave up on solving. It's
actually there for you, as the project maintainer, to enumerate the `flake8`
rules that you don't agree with. For example, I totally disagree with the `W503`
line break before operator rule. I want to write long conditionals with and
statements on the first line, like this:

```python
if (
   condition_1
   and condition_2
   and condition_3
):
    print('all true')
```

One of the benefits of this style is you can add more lines with only single
line diffs. The other is that the reader always sees the operation that goes
with each line. Same could be done with arithmatic that could incorporate not
only `+` but also `-`.

Next is the `exclude` block. Just copy/paste this each time, since it has lots
of garbage you don't want `flake8` to bother with. One of the checkers in
`flake8` is for function "cyclomatic" complexity. You can make the maximum
number higher with `max-complexity`. Normally, you want this to be enforced, but
sometimes there's no way around a complex function. For this, you can add a code
comment `noqa` followed by the error code like `# noqa:W123`. Again, adding tags
to ignore bad style just to pass `flake8` is against the point.

The `max-line-length` is a very contentious setting. I think 120 is fine. Some
people think 78, 79, or 80 is best because of the standard sizes of old computer
screens or punch cards... When I get older and I can't read my computer screen,
I'll probably make the text bigger and change my mind about this. If you find
yourself breaking up lines in a totally non-sensical, unstyled way, then you're
conforming too tightly to the rules. Sorry about the mixed messages!

```
import-order-style = pycharm
application-import-names =
    pybel
    bel_resources
    tests
```

I copied this again because this part is really important. You have to tell
`flake8` what rules you use for import order. I use the pycharm rules, which
group python builtin packages, then 3rd party packages, then my packages. The
`application-import-names` is a place to list what are your packages.

Last is the `format` entry, which gives the nice colorful output. Copy paste
this! I borrowed mine from [Scott Colby](https://github.com/scolby33).

---

After all of that, I set up Travis CI to run `tox` every time code is pushed to
the repository. If you're working in a team, you probably do something like the
fork/pull request or branch/pull request workflow on GitHub to support doing
code review before merging new code. The best part is that there's a big box on
each pull request that checks if `flake8` passed (among other tests), which
means that there were no errors detected.

I encourage my teammates to make pull requests as soon as they start working on
code. GitHub even has a "draft pull request" mode now. However, before asking
anyone to review your code, it has to pass `flake8`. And obviously, no code that
isn't passing flake8 can be merged.

This is a _very_ painful process to get people used to. I've done it with many
groups of people and always got pushback. However, everyone who has gone through
the process with me has come out the other side happy that they did it. It's
important that when you start enforcing coding rules on other people that you
are a resource for them - when somebody is frustrated by a flake8 error code
they have never seen, they will likely forget how to use Google. They will
probably ask you for help. You have to resist the urge to send
[lmgtfy](https://lmgtfy.com) links to them and be patient. Because eventually,
they will do it on their own, and spread the gospel of `flake8`.

While a good arsenal of `flake8` plugins provides a solid foundation, it's not
all that needs to be done to make your code readable and look good. Just like
with reading and speaking, the best way to develop a sense of style is by
reading _lots_ of code (with the caveat that reading poorly written code
probably won't teach you much). Within the rules imposed by `flake8`, there is
lots of space for style. If you watch lectures from David Beazley, you'll notice
a very different style from Raymond Hettinger, and also from me.

Now that you've made it to the end of this short guide, I wish you the best of
luck on developing your own style!

---

Are you working with people who are particularly unsusceptible to Travis CI
emails or checking the big red box on pull requests? You could try getting them
set up with [pre-commit hooks](https://pre-commit.com/), which run the style
checks locally any time they try and push (even if it's to a branch) and it will
give them the message in the console.

Is style not your thing at all / you're not ready to let go of your identity as
a Java/Perl developer? Maybe consider [Black](https://github.com/psf/black),
which actually re-writes your code in a deterministic style. I don't live by it,
but it's a great tool to run on a code base that's never been loved before going
back and stylizing it.
