---
layout: post
title: Re-implementing the N2T ARK Resolver
date: 2023-04-11 20:44:23 +0200
author: Charles Tapley Hoyt
tags: curies arks n2t pids
---
[Archival Resource Keys (ARKs)](https://arks.org/) are flavor of persistent identifiers
like DOIs, URNs, and Handles that have the benefit of being free, flexible with what
metadata gets attached, and natively able to resolve to web pages. [Name-to-Thing (N2T)](https://n2t.net)
implements a resolver for a variety of ARKs, so this blog post is about how that resolver can be
re-implemented with the [`curies`](https://github.com/cthoyt/curies/) Python package.

In a lot of ways, ARKs look and act like CURIEs. For example, `ark:/53355/cl010277627` could be interpreted
as having the prefix `ark` and the local unique identifier `/53355/cl010277627`. The first part of each ARK
between the first two slashes corresponds to the provider. In this example, `53355` corresponds to the
[Louvre](https://www.louvre.fr/en) museum in Paris, France and `cl010277627` is the local unique identifier
corresponding to the Vénus de Milo statue.

However, I might have just committed ARK blasphemy. In N2T, it appears that the ARK prefix and provider code stay
grouped together in the front half like `ark:/53355/` and then the back half `cl010277627` represents the local unique
identifier. This is very similar to the two-layer identifiers in DOI and the arbitrary number of layer identifiers in
OID.

The point is, if we can interpret this enough like CURIEs, we can use the `curies` package to implement a resolver.
The first step we can take is to download the N2T data
from [https://n2t.net/e/n2t_full_prefixes.yaml](https://n2t.net/e/n2t_full_prefixes.yaml). Then we can parse out
the ARKs (there are other things in N2T we'll disregard) with the following code:

```python
import pystow
import yaml

URL = "https://n2t.net/e/n2t_full_prefixes.yaml"
PROTOCOLS = {"https://", "http://", "ftp://"}


def get_prefix_map():
    """Get the prefix map from N2T, not including redundant ``ark:/`` in prefixes."""
    with pystow.ensure_open("n2t", url=URL) as file:
        records = yaml.safe_load(file)
    prefix_map = {}
    for key, record in records.items():
        uri_prefix = record.get("redirect")
        if (
            not uri_prefix
            or all(not uri_prefix.startswith(protocol) for protocol in PROTOCOLS)
            or uri_prefix.count("$id") != 1
            or not uri_prefix.endswith("$id")
            or not key.startswith("ark:/")
        ):
            continue
        key = key.removeprefix("ark:/")
        prefix_map[key] = uri_prefix.removesuffix("$id") + "/" + key + "/"
    return prefix_map
```

This prefix map removes `ark:/` from the beginning of the prefixes in N2T and also adds the provider code into the
URI prefix to make the URIs more focused on the local unique identifiers within each provider, rather than the
entire ARK space.

Once we have a prefix map, we can make a `curies.Converter` and a Flask web application for resolving in a few lines:

```python
from curies import Converter, get_flask_app


def get_app():
    """Get an ARK resolver app, noting that it uses a non-standard delimiter and URL prefix."""
    prefix_map = get_prefix_map()
    print(prefix_map)
    converter = Converter.from_prefix_map(prefix_map, delimiter="/")
    app = get_flask_app(converter, blueprint_kwargs=dict(url_prefix="/ark:"))
    return app
```

The two tricks here are:

1. We want to remove the redundant `ark:/` then interpret the ARK provider code as the prefix and the rest as the local
   unique identifier. However, we still want to be able to write URLs in our resolver that have the `ark:/` prefix.
   Luckily, Flask has the facility to define a default `url_prefix` before a given blueprint that we invoke directly.
2. Unlike CURIEs that use a colon `:` as the delimiter between the prefix and local unique identifier, AKRs use a
   slash `/`. We can also set this in the Converter's settings.

Now, all we need to do is instantiate the app and serve it with any WSGI tool like Gunicorn, Uvicorn, or Flask's
built-in development server (from Werkzeug).
Navigating to http://localhost:5000/ark:/53355/cl010277627
redirects to https://collections.louvre.fr/ark:/53355/cl010277627 and gets some nice art from the Louvre.
In general, you can stick any ARK after http://localhost:5000/ark: that is resolvable via N2T when running this server.

All of this code is on [GitHub](https://github.com/cthoyt/n2t-ark-resolver/tree/main) and can be run with the following:

```shell
git clone https://github.com/cthoyt/n2t-ark-resolver
cd n2t-ark-resolver
python -m pip install -r requirements.txt
python wsgi.py
```

---
Update: since posting this, I have heard from John Kunze that the ARK format is currently being updated to look more
like URNs and therefore not have the slash after `ark:/` anymore. If/when that happens, there are only a few bits of
string pre-processing in this script that need to be updated to keep everything running.
