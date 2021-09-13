---
layout: post
title: How to Code with Me: Beyond Linters
date: 2021-09-14 00:18:00 +0100
author: Charles Tapley Hoyt
tags: code-with-me
---
This post is about my personal code style guide that are beyond the enforcement
of my [flake8 plugins](({% post_url 2020-04-25-how-to-code-with-me-flake8 %}))
or [`black`](https://github.com/psf/black). I'll try and update it over time.

## Exit code blocks as early as possible

Sometimes you have an `if` statement that does some stuff when the conditional
is true, or raises an error if it isn't. Here's the wrong way to write this:

```python
if cond:
    ...  # big code block
else:
    raise ValueError
```

It's better to raise the value error as quickly as possible, because then
you can dedent the big code block. This is particularly good if you have lots
of nested code blocks in conditionals, loops, etc.

```python
if not cond:
    raise ValueError

...  # big code block
```

The same thing is true for `return` statements. The following code where
a value is set then returned is bad:

```python
if cond:
    ... # big code block
    value = ... # final line that assigns value
else:
    value = ...  # one-liner assigning value
return value
```

It's better to flip the conditional and return the value quickly, since it only
takes one line to assign it in the `else block`

```python
if not cond:
    return ...  # one-liner assigning value

... # big code block
return ... # final line that assigns value
```
