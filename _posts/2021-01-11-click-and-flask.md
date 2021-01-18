---
layout: post
title: How to Code with Me - Wrapping a Flask App in a CLI
date: 2021-01-11 01:14:00 +0100
author: Charles Tapley Hoyt
tags: code-with-me
---
Previous posts in my "How to Code with Me" series have addressed
[packaging python code]({% post_url 2020-06-03-how-to-code-with-me-organization %}) and
[setting up a command line interface (CLI) using `click`]({% post_url 2020-06-11-click %}). This post is about how to
do this when your Python code is running a web application made with [Flask](https://flask.palletsprojects.com) and
how to set it up to run through your CLI.

The name of the package I'll be referring to in this tutorial is `granola_explosion` (not a real package!) that follows
the `src/` layout. If you're not familiar with this, check my previous post on [organizing a Python package]({% post_url
2020-06-03-how-to-code-with-me-organization %}).

## Example Flask Application

Let's assume that the Flask application is in a module called `granola_explosion.wsgi` located
at `src/granola_explosion/wsgi.py`. This tutorial isn't about building a Flask application, so below I'll give a minimum
working example. Your Flask application may be much larger, even spanning multiple files. The important thing is that
the [`flask.Flask`](https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask) instance is living in this file.

```python
# wsgi.py

from flask import Flask

app = Flask(__name__)


@app.route()
def home():
    return "There's no place like home."


if __name__ == '__main__':
    app.run()
```

Note that the [`app.run()`](https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.run) is enclosed in
`if __name__ == '__main__'`. This means that the app only gets run if
the `granola_explosion.wsgi` is run as a script. Later, we will be importing this module inside our CLI, and we don't
want it to run until we tell it to (and with our very own options).

## Run a Flask Web Application with Click

Let's also assume your command line interface is in a module called `granola_explosion.cli` located
at `src/granola_explosion/cli.py` using a [`click.Group`](https://click.palletsprojects.com/en/7.x/api/#click.Group)
to organize several subcommands. The following example shows  how you can import the `app` object and run it from
inside the command line.

```python
# cli.py
import click


@click.group()
def main():
    """Run the Granola Explosion CLI."""


@click.command()
def web():
    from .wsgi import app
    app.run()


if __name__ == '__main__':
    main()
```

Now, you can run your web application with `python -m granola_explosion.cli web`!

You can actually call your module and `flask.Flask` instance whatever you want, but these two are pretty standard and
recognized by external tools (more on that later), and will make it easier for other people to understand what your code
does.

## Configure Your Application

Normally, you can pass options like `host` and `port` into the `flask.Flask.run()` function. Below, we use `click`
options to pass these through.

```python
# cli.py
import click


@click.group()
def main():
    """Run the Granola Explosion CLI."""


@click.command()
@click.option('--host', default='0.0.0.0')
@click.option('--port', default=5000, type=int)
def web(host: str, port: int):
    from .wsgi import app
    app.run(host=host, port=port)


if __name__ == '__main__':
    main()
```

I've written these options so many times, that I made a package called
[`more_click`](https://github.com/cthoyt/more_click/) that holds them for easy importing like in the following:

```python
# cli.py
import click
from more_click import host_option, port_option


@click.group()
def main():
    """Run the Granola Explosion CLI."""


@main.command()
@host_option
@port_option
def web(host: str, port: str):
    from .wsgi import app
    app.run(host=host, port=port)


if __name__ == '__main__':
    main()
```

## Using GUnicorn

The `flask.Flask.run()` function is convenient, but it's only meant to be a lightweight development server - even your
own server yells at you every time you start it!

![Flask Development Warning](/img/flask-development-warning.png)

The [official documentation](https://flask.palletsprojects.com/en/1.1.x/deploying/) and many excellent tutorials point
to using more powerful servers like [Gunicorn](https://gunicorn.org/), but they start throwing around the
(scary) acronym [WSGI](https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface) and tend to have very dense
documentation that looks like it's written only for sysadmins.

![Flask Gunicorn Tutorial](/img/flask-gunicorn-docs.png)

If you're like me, you're a big fan of keeping as much code in Python as possible, rather than floating around in
various shell scripts and dockerfiles. You would also probably like to be able to run a Flask app with Gunicorn with the
ease of `app.run()`.

It turns out that `gunicorn` is actually written in Python, and this is possible if you're willing to read through the
codebase and understand the complicated design patterns they use. Or, you could use the `more_click.run_app`, which
takes care of all of it for you. The implementation of this function
lives [here](https://github.com/cthoyt/more_click/blob/main/src/more_click/web.py), for the adventurous among you. It's
basically a drop-in replacement for `app.run()` except it's called as `run_app(app)`. Then, you can use
the `with_gunicorn` keyword argument to turn on using Gunicorn.

```python
# cli.py
import click
from more_click import host_option, port_option, run_app


@click.group()
def main():
    """Run the Granola Explosion CLI."""


@main.command()
@host_option
@port_option
def web(host: str, port: str):
    from .wsgi import app
    run_app(app=app, with_gunicorn=True, host=host, port=port)


if __name__ == '__main__':
    main()
```

Now, your app runs with Gunicorn! If you want to be able to quickly switch back and forth between Flask and Gunicorn as
a server, you can use the handy `more_click.with_gunicorn_option`. Further, you can specify the number of workers for
your Gunicorn server based on the following complete example:

```python
# cli.py
import click
from more_click import host_option, port_option, with_gunicorn_option, workers_option, run_app


@click.group()
def main():
    """Run the Granola Explosion CLI."""


@main.command()
@host_option
@port_option
@with_gunicorn_option
@workers_option
def web(host: str, port: str, with_gunicorn: bool, workers: int):
    from .wsgi import app
    run_app(app=app, with_gunicorn=with_gunicorn, host=host, port=port, workers=workers)


if __name__ == '__main__':
    main()
```

## Ultimate Lazy Mode

For ultimate lazy mode, I've written a wrapper around the complete example in `more_click.make_web_command`. This uses a
standard `wsgi`-style string to locate the app. While this is a little less explicit than normal Python code that relies
on the import machinery, it has the benefit that it can lazily import the module in which your Flask application lives.
This could help avoid importing big requirements, as well as allow your package to specify Flask requirements as
optional. You might want to do this if your package can be used to perform a service locally, but also contains a Flask
application that wraps it with a RESTful service as well that not all users might need.

```python
# cli.py
import click
from more_click import make_web_command


@click.group()
def main():
    """My awesome CLI."""


make_web_command('my_package_name.wsgi:app', group=main)

if __name__ == '__main__':
    main()
```

The `make_web_command()` function actually returns the command itself, so you can save it and add it to the group
manually instead of passing the `group` argument.

```python
# cli.py
import click
from more_click import make_web_command


@click.group()
def main():
    """My awesome CLI."""


web = make_web_command('my_package_name.wsgi:app')

main.add_command(web)

if __name__ == '__main__':
    main()
```

Since any click command can be run by itself directly, the following minimal CLI also works well for apps that don't
need the click Group.

```python
# cli.py
from more_click import make_web_command

web = make_web_command('granola_explosion.wsgi:app')

if __name__ == '__main__':
    web()
```

---
I intentionally did not cover the built-in [Flask Script](https://flask.palletsprojects.com/en/1.1.x/cli/) because
it doesn't fit in with my paradigm of "everything must be packaged."

This is my first post of 2021! Happy new year!
