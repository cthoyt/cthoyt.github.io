---
layout: post
title:
  Validating the FAIRness of knowledge graphs and ontologies in RDF using the
  Bioregistry
date: 2025-09-04 14:30:00 +0200
author: Charles Tapley Hoyt
tags:
  - CURIE
  - URI
  - URN
  - IRI
  - identifiers
  - identifier schema
  - Bioregistry
  - biopragmatics
---

Using standard CURIE prefixes and URI prefixes in semantic web artifacts such as
[Resource Description Framework (RDF)](https://en.wikipedia.org/wiki/Resource_Description_Framework)
promotes interoperability, enables reuse in downstream data integration, and
makes data more FAIR. The [Bioregistry](https://bioregistry.io) defines a set of
standard CURIE prefixes and URI prefixes against which RDF files can be
validated/standardized. This blog post describes a new CLI tool
`bioregistry validate ttl` in the Bioregistry Python package that can run
validation on [Turtle](<https://en.wikipedia.org/wiki/Turtle_(syntax)>) files (a
common serialization of RDF).

RDF data stored in Turtle files typically begins with a stanza defining a prefix
map. For example, one of the Turtle files in the
[Chemotion Knowledge Graph (Chemotion-KG)](https://github.com/ISE-FIZKarlsruhe/chemotion-kg/tree/4cb5c24af6494d66fb8cd849921131dbc789c163>)
begins with the following six prefixes:

```turtle
@prefix nfdicore: <https://nfdi.fiz-karlsruhe.de/ontology/> .
@prefix ns1: <http://purls.helmholtz-metadaten.de/mwo/> .
@prefix ns2: <http://purl.obolibrary.org/obo/chebi/> .
@prefix obo: <http://purl.obolibrary.org/obo/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
```

The following command can be used to validate it. Using `--tablefmt github`
results in a nice table that can be formatted into a blog post, otherwise it
outputs text in a more vertical format.

```console
$ bioregistry validate ttl https://github.com/ISE-FIZKarlsruhe/chemotion-kg/raw/4cb5c24af/processing/output_bfo_compliant.ttl
```

| prefix   | uri_prefix                               | issue                     | solution                                                                                                          |
| -------- | ---------------------------------------- | ------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| nfdicore | https://nfdi.fiz-karlsruhe.de/ontology/  | non-standard CURIE prefix | Switch to standard prefix: nfdi.core                                                                              |
| ns1      | http://purls.helmholtz-metadaten.de/mwo/ | unknown CURIE prefix      | Consider switching to the more specific CURIE/URI prefix pair mwo: `http://purls.helmholtz-metadaten.de/mwo/mwo_` |
| ns2      | http://purl.obolibrary.org/obo/chebi/    | unknown CURIE prefix      |                                                                                                                   |

I was able to directly
[open an issue](https://github.com/ISE-FIZKarlsruhe/chemotion-kg/issues/2) on
the GitHub repository to give feedback. In general, I think this is a very
powerful use of the Bioregistry because it can support groups interested in
making knowledge graphs and ontologies towards improving their data and
ultimately making it more FAIR.

---

In case you're interested in how I implemented this,
[check this PR](https://github.com/biopragmatics/bioregistry/pull/1670). I was
able to reuse some ideas from a previous JSON-LD validator, extend them, and
abstract the code. Later, I will be able to implement similar validators for XML
files, ontologies, and any other resource from which I can extract a prefix map.

I also left a TODO inside the code, since this can be extended with several
other ways of validating URI prefixes. Ultimately, this may get upstreamed into
the [`curies`](https://github.com/biopragmatics/curies) package to make it even
more accessible to groups making their own prefix maps or using custom instances
of the Bioregistry.
