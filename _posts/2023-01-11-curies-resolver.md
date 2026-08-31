---
layout: post
title: Deploying a Resolver using the CURIEs Package
date: 2023-01-10 15:44:00 +0100
author: Charles Tapley Hoyt
tags: semantic-web curies prefixes iris uris python
---
A resolver is a web application with a route that accepts a CURIE, converts to a URI, then sends a redirect to the URI
as a response. Several resolvers for life and natural sciences resources exist such as the Bioregistry, Identifiers.org,
Name-to-Thing, and the OBO Foundry's PURL service. However, most of these services' implementations are either opaque,
difficult to configure, or not extensible. The `curies` Python package provides the ability to generate a web service
from any user-defined prefix map (or related format).


The following is an end-to-end example of using this function to create
a small web resolver application. This uses a `flask.Blueprint` which allows the resolver to be mounted on any
pre-existing Flask application.

```python
# flask_example.py
from flask import Flask
from curies import Converter, get_flask_blueprint, get_obo_converter

# Create a converter
converter: Converter = get_obo_converter()

# Create a blueprint from the converter
blueprint = get_flask_blueprint(converter)

# Create the Flask app and mount the router
app = Flask(__name__)
app.register_blueprint(blueprint)

if __name__ == "__main__":
    app.run()
```

If you don't need the flexibility of mounting on a pre-existing application, you can use the
`curies.get_flask_app` as a shortcut.

```python
# flask_example.py
from flask import Flask
from curies import Converter, get_flask_app, get_obo_converter

# Create a converter
converter: Converter = get_obo_converter()

# Create the Flask app and mount the router
app: Flask = get_flask_app(converter)

if __name__ == "__main__":
    app.run()
```

In the command line, either run your Python file directly, or via with `gunicorn`:

```shell
$ pip install gunicorn
$ gunicorn --bind 0.0.0.0:5000 flask_example:app
```

Test a request in the Python REPL. Note that Flask's development
server runs on port 5000 by default.

```python-repl
>>> import requests
>>> requests.get("http://localhost:5000/GO:0032571").url
'http://amigo.geneontology.org/amigo/term/GO:0032571'
```