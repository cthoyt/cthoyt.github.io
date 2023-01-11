---
layout: post
title: Idiomatic conversion between URIs and compact URIs
date: 2023-01-10 13:28:00 +0100
author: Charles Tapley Hoyt
tags: semantic-web curies prefixes iris uris python
---
The semantic web and ontology communities needed a reusable Python package for converting between uniform resource
identifiers (URIs) and compact URIs (CURIEs) that is reliable, idiomatic, generic, and performant. This post describes
the [`curies`](https://github.com/cthoyt/curies) Python package that I wrote to fill this need.

After installing with `pip install curies` or checking out the code on [GitHub](https://github.com/cthoyt/curies) and
installing a local copy, you can directly jump in to using the `curies` package. Its main data structure is
[`curies.Converter`](https://curies.readthedocs.io/en/latest/api/curies.Converter.html#converter).
It can be instantiated with various class methods corresponding to data in one of several formats.

The most common format is a prefix map, a dictionary containing a one-to-many mapping from CURIE prefixes to URI
prefixes. It can be used in combination with the
[`Converter.from_prefix_map`](https://curies.readthedocs.io/en/latest/api/curies.Converter.html#curies.Converter.from_prefix_map)
class method. The following example includes some (but not all) of the CURIE and URI prefixes used by ontologies in the
[Open Biological and Biomedical Ontology (OBO) Foundry](https://obofoundry.org).

```python
from curies import Converter

prefix_map = {
    "CHEBI": "http://purl.obolibrary.org/obo/CHEBI_",
    "MONDO": "http://purl.obolibrary.org/obo/MONDO_",
    "GO": "http://purl.obolibrary.org/obo/GO_",
    # ... and so on
    "OBO": "http://purl.obolibrary.org/obo/",
}
converter = Converter.from_prefix_map(prefix_map)
```

The `Converter` class indexes the prefix map using a [trie](https://en.wikipedia.org/wiki/Trie) data structure, which
makes search of the beginning of sequences (such as strings) efficient. My implementation builds on the implementation
of this data structure in the [`PyTrie`](https://github.com/gsakkis/pytrie/) package.

## Conversion

A uniform resource identifier (URI) that corresponds to one of the URI prefixes registered in the converter can be
compressed into a compact URI (CURIE)
using
the [`Converter.compress`](https://curies.readthedocs.io/en/latest/api/curies.Converter.html#curies.Converter.compress)
method. In the following example, we use the canonical URI (within the scope of the OBO Foundry) for the
[Gene Ontology](http://geneontology.org/) term
for [response to vitamin K (GO:0032571)](http://purl.obolibrary.org/obo/GO_0032571).

```python-repl
>>> converter.compress("http://purl.obolibrary.org/obo/GO_0032571")
'GO:0032571'
```

When some URI prefixes are partially overlapping (e.g., `http://purl.obolibrary.org/obo/CHEBI_` for `GO`
and `http://purl.obolibrary.org/obo/` for ``OBO``), the longest URI prefix will always be matched. For example,
compressing `http://purl.obolibrary.org/obo/GO_0032571` returns `GO:0032571` instead of `OBO:GO_0032571`.

If there's no matching URI prefix, then `compress()` will return `None`.

```python-repl
>>> converter.compress("http://example.com/missing:0000000") is None
True
```

Similarly, a CURIE can be expanded into a URI using
the [`Converter.expand`](https://curies.readthedocs.io/en/latest/api/curies.Converter.html#curies.Converter.expand)
method.

```python-repl
>>> converter.expand("GO:0032571")
'http://purl.obolibrary.org/obo/GO_0032571'
```

If there's no matching CURIE prefix, then `expand()` will return `None`.

```python-repl
>>> converter.expand("missing:0000000") is None
True
```

## Getting Prefix Maps

The `curies` package includes functions for loading several prefix maps from external resources. These are not cached
in order to take advantage of the most recent versions. This is particularly important for resources like the
[Bioregistry](https://bioregistry.io) that are updated frequently.

| Name           | Function                                                                                                                    | Description                                                                                                       |
|----------------|-----------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| Bioregistry    | [`curies.get_bioregistry_converter`](https://curies.readthedocs.io/en/latest/api/curies.get_bioregistry_converter.html)     | A high-coverage, general purpose registry for the life and natural sciences.                                      |
| OBO Foundry    | [`curies.get_obo_converter`](https://curies.readthedocs.io/en/latest/api/curies.get_obo_converter.html)                     | A set of orthogonal ontologies for the life sciences constructed for mutual interoperability                      |
| Prefix Commons | [`curies.get_prefixcommons_converter`](https://curies.readthedocs.io/en/latest/api/curies.get_prefixcommons_converter.html) | A medium-coverage, general purpose registry for the life and natural sciences                                     |
| Gene Ontology  | [`curies.get_go_converter`](https://curies.readthedocs.io/en/latest/api/curies.get_go_converter.html)                       | A project-specific prefix map for the Gene Ontology, includes several duplicate and non-standard definitions      |
| Monarch        | [`curies.get_monarch_converter`](https://curies.readthedocs.io/en/latest/api/curies.get_monatch_converter.html)             | A project-specific prefix map for the Monarch Initiative, includes several duplicate and non-standard definitions |

### Loading from the Bioregistry

The [`bioregistry`](https://github.com/biopragmatics/bioregistry) Python package has first-class support for
the `curies` package through the generic function
[`bioregistry.get_converter`](https://bioregistry.readthedocs.io/en/stable/api/bioregistry.get_converter.html).
This can be used as an alternative to `curies.get_bioregistry_converter` in cases when the Bioregistry is installed
and it's desired to use local data.

```python
import bioregistry

converter = bioregistry.get_converter()
```

### Loading from `prefixmaps`

The [`prefixmaps`](https://github.com/linkml/prefixmaps) Python package keeps various prefix maps under version control
that also has first-class support for the `curies` package.

```python
from prefixmaps import load_context
from curies import Converter

extended_prefix_map = load_context("obo").as_extended_prefix_map()
converter = Converter.from_extended_prefix_map(extended_prefix_map)
```

## Related

Here's a short (probably incomplete) list of other packages I've found that have related functionalities:

- https://github.com/prefixcommons/prefixcommons-py (Python)
- https://github.com/prefixcommons/curie-util (Java)
- https://github.com/geneontology/curie-util-py (Python)
- https://github.com/geneontology/curie-util-es5 (Node.js)
- https://github.com/endoli/curie.rs (Rust)

---
This post didn't touch the more advanced features of the `Converter` class such as its support for CURIE prefix synonyms
and URI prefix synonyms. It also didn't touch the `curies.chain()` function which enables several pre-instantiated
converters to be used in succession, similarly to the Python built-in `collections.ChainMap` class. These are described
in the documentation at [curies.readthedocs.io](https://curies.readthedocs.io)
