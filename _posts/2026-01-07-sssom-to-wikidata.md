---
layout: post
title: SSSOM to Wikidata
date: 2026-01-08 16:47:00 +0100
author: Charles Tapley Hoyt
tags:
  - SSSOM
  - Wikidata
  - SKOS
  - semantic mappings
  - mappings
  - interoperability
---

This was originally presented at the 4th Ontologies4Chem meeting in Limburg on
November 13th, 2025. The corresponding slides are on Zenodo at
https://doi.org/10.5281/zenodo.17662905

Updates made to sssom-pydantic package:
https://github.com/cthoyt/sssom-pydantic/pull/32

released in https://github.com/cthoyt/sssom-pydantic/releases/tag/v0.1.18

Improvements to Wikidata Client package:
https://github.com/cthoyt/wikidata-client/pull/2

Wikidata encodes semantic mappings in two ways:

1. Using the [exact match (P2888)](https://www.wikidata.org/wiki/Property:P2888)
   property with a URI as the object. For example,
   [cell wall (Q128700)](https://www.wikidata.org/wiki/Q128700) maps to the Gene
   Ontology (GO) term for
   [cell wall](https://purl.obolibrary.org/obo/GO_0005618) by its URI
   `http://purl.obolibrary.org/obo/GO_0005618`.
2. Using semantic space-specific properties (e.g.
   [P683](https://www.wikidata.org/wiki/Property:P683) for ChEBI) with local
   unique identifiers as the object. For example,
   [acetic acid (Q47512)](https://www.wikidata.org/wiki/Q47512) maps to the
   ChEBI term for
   [acetic acid](https://www.ebi.ac.uk/chebi/searchId.do?chebiId=CHEBI:15366)
   using the [P683](https://www.wikidata.org/wiki/Property:P683) property for
   ChEBI and local unique identifier for acetic acid (within ChEBI) `15366`.

Wikidata has a data structure that enables annotating qualifiers onto triples.
Therefore, other parts of semantic mappings modeled in SSSOM can be ported:

1. Authors and reviewers can be mapped from ORCiD identifiers to Wikidata
   identifiers, then encoded using the
   [S50](https://www.wikidata.org/wiki/Property:P50) and
   [S4032](https://www.wikidata.org/wiki/Property:P4032) properties,
   respectively
2. A SKOS-flavored mapping predicate (i.e., exact, narrow, broad, close,
   related) can be encoded using the
   [S4390](https://www.wikidata.org/wiki/Property:P4390) property
3. The publication date can be encoded using the
   [S577](https://www.wikidata.org/wiki/Property:P577) property
4. The license can be mapped from text to a Wikidata identifier, then encoded
   using the [S275](https://www.wikidata.org/wiki/Property:P275) property

Note that properties that normally start with a `P` when used in triples are
changed to start with an `S` when used as qualifiers. Other fields in SSSOM
could potentially be mapped to Wikidata later.

This module implements the following interactive workflows:

1. Read an SSSOM file, convert mappings to Wikidata schema, then open a
   QuickStatements tab in the web browser using
   :func:`read_and_open_quickstatements`
2. Convert in-memory semantic mappings to the Wikidata schema, then open a
   QuickStatements tab in the web browser using :func:`open_quickstatements`

It also implements the following non-interactive workflows, which should be used
with caution since they write directly to Wikidata:

1. Read an SSSOM file, convert mappings to Wikidata schema, then post
   non-interactively to Wikidata via QuickStatements using :func:`read_and_post`
2. Convert in-memory semantic mappings to the Wikidata schema, then post
   non-interactively to Wikidata via QuickStatements using :func:`post`

![A screenshot of the ChEBI mapping section of webpage for Wikidata's acetic acid record](/img/sssom-to-wikidata/acetic-acid.png)

![A screenshot of the exact match section of webpage for Wikidata's cell wall record](/img/sssom-to-wikidata/cell-wall.png)

![A screenshot of the QuickStatements queue](/img/sssom-to-wikidata/quickstatements.png)

![](/img/sssom-to-wikidata/bioregistry.png)
