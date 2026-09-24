---
layout: post
title: Deploying a Resolver using the CURIEs Package
date: 2026-09-24 13:45:00 +0200
author: Charles Tapley Hoyt
tags:
  - semantic web
  - CURIEs
  - prefixes
  - IRIs
  - URIs
  - URLs
  - python
  - prefix maps
---

A resolver is a web application that returns a redirect response for the uniform
resource identifier (URI) expansion of a compact URI (CURIE). This post
demonstrates the resolver implemented as part of the
[`curies`](https://github.com/biopragmatics/curies) Python package, which is
used by the [Bioregistry](https://bioregistry.io) and
[Semantic Farm](https://semantic.farm).

I actually wrote the first version of this post in 2023 as I started
externalizing functionality from the `bioregistry` that could be made more
generic. At the time, there were already several other resolvers (sometimes
called meta-resolvers):

- [Identifiers.org](https://identifiers.org) and
  [Name-to-Thing](https://n2t.net) both implement custom resolver code
- the OBO Foundry's PURL service, w3id.org, purl.org, and others implement
  resolution using `.htaccess` rules

However, there are issues here with transparency, easy of configuration, and
extensibility. I had already begun writing about the `curies` package as a
_final_ implementation of CURIE and URI conversion logic in a [previous post]({%
post_url 2023/2023-01-10-curies-package %}) on the `curies` package.

## Flask

The following is an end-to-end example of using this function to create a small
web resolver application. This uses a `flask.Blueprint` which allows the
resolver to be mounted on any pre-existing Flask application.

```python
# flask_example.py
from flask import Flask
from curies import Converter, get_obo_converter
from curies.resolver_service import get_flask_blueprint

# Create a converter
converter: Converter = get_obo_converter()

# Create a blueprint from the converter
blueprint = get_flask_blueprint(converter)

# Create the Flask app and register the blueprint
app = Flask(__name__)
app.register_blueprint(blueprint)

if __name__ == "__main__":
    app.run()
```

If you don't need the flexibility of mounting on a pre-existing application, you
can use the `curies.get_flask_app` as a shortcut.

```python
# flask_example.py
from flask import Flask
from curies import get_obo_converter, Converter
from curies.resolver_service import get_flask_app

# Create a converter
converter: Converter = get_obo_converter()

# Create the Flask app and register the blueprint
app: Flask = get_flask_app(converter)

if __name__ == "__main__":
    app.run()
```

In the command line, either run your Python file directly, or via with
`gunicorn`:

```console
$ uvx gunicorn --bind 0.0.0.0:5000 flask_example:app
```

Test a request in the Python REPL. Note that Flask's development server runs on
port 5000 by default.

```python-repl
>>> import requests
>>> requests.get("http://localhost:5000/GO:0032571").url
'http://amigo.geneontology.org/amigo/term/GO:0032571'
```

## FastAPI

The same thing works for FastAPI applications, except with a `fastapi.Router`:

```python
# fastapi_example.py
from fastapi import FastAPI
from curies.resolver_service import get_fastapi_router
from curies import Converter, get_obo_converter

# Create a converter
converter: Converter = get_obo_converter()

# Create a router from the converter
router = get_fastapi_router(converter)

# Create the app and mount the router
app = FastAPI()
app.mount(router)

if __name__ == "__main__":
    app.run()
```

If you don't need the flexibility of mounting on a pre-existing application, you
can use the `curies.get_flask_app` as a shortcut.

```python
# fastapi_example.py
from fastapi import FastAPI
from curies import get_obo_converter, Converter
from curies.resolver_service import get_fastapi_app

# Create a converter
converter: Converter = get_obo_converter()

# Create the Flask app and mount the router
app: FastAPI = get_fastapi_app(converter)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
```

In the command line, either run your Python file directly, or via with
`gunicorn`:

```console
$ uvicorn --bind 0.0.0.0:5000 fastapi_example:app
```

## Command Line

There's a high-level CLI built in to the `curies` package that can be pointed at
a given local or remove prefix map, extended prefix map, or JSON-LD context to
make a resolver:

```console
$ uvx \
    --with click \
    --with flask \
    curies resolver
    --format prefix_map \
    https://prefix.zazuko.com/api/v1/prefixes
Installed 15 packages in 11ms
 * Serving Flask app 'curies.resolver_service'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8764
 * Running on http://192.168.2.118:8764
Press CTRL+C to quit
```

Flags can be used to toggle the implementation (FastAPI or Flask) and the server
(werkzeug, gunicorn, uvicorn). See `--help` for more information.
