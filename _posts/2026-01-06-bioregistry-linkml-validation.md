---
layout: post
title: Validating Prefix Maps in LinkML Schemas
date: 2026-01-05 10:36:00 -0500
author: Charles Tapley Hoyt
tags:
  - LinkML
  - Bioregistry
  - prefix maps
  - CURIEs
  - URIs
---

[LinkML](https://linkml.io) enables defining data models and data schemas
in YAML informed by semantic web best practices. As such, each definition
includes a prefix map. Similarly to my previous posts on validating the
prefix maps appearing in [Turtle files]({% post_url 2025-09-04-bioregistry-turtle-validation %}) and [in unfamiliar SPARQL endpoints]({% post_url 2025-09-11-nfdi4culture-prefix-validation %}),
this post showcases describes a new extension to [the Bioregistry](https://github.com/biopragmatics/bioregistry)
that validates prefix maps in LinkML definitions.

Here's an abridged excerpt of a LinkML
[definition](https://github.com/HendrikBorgelt/CatCore/blob/main/src/catcore/schema/catcore.yaml)
borrowed from [CatCore](https://github.com/HendrikBorgelt/CatCore), a data model under
development by NFDI4Cat, the NFDI consortium interested in catalysis:

```yaml
id: https://w3id.org/nfdi4cat/catcore
name: catcore-metadata
title: CatCore Metadata Reference Model

prefixes:
  catcore: https://w3id.org/nfdi4cat/catcore/
  voc4cat: https://w3id.org/nfdi4cat/voc4cat_
  CHMO: http://purl.obolibrary.org/obo/CHMO_
  OBI: http://purl.obolibrary.org/obo/OBI_
  AFR: http://purl.allotrope.org/ontologies/result#AFR_
  AFP: http://purl.allotrope.org/ontologies/process#AFP_
  AFQ: http://purl.allotrope.org/ontologies/quality#AFQ_
  NCIT: http://purl.obolibrary.org/obo/NCIT_
  nmrCV: "http://nmrML.org/nmrCV#NMR:"
  linkml: https://w3id.org/linkml/
  AFRL: http://purl.allotrope.org/ontologies/role#AFRL_
  APOLLO_SV: http://purl.obolibrary.org/obo/APOLLO_SV_
  SIO: http://semanticscience.org/resource/SIO_

default_prefix: catcore
```

In [biopragmatics/bioregistry#1786](https://github.com/biopragmatics/bioregistry/pull/1786),
I implemented the `bioregistry validate linkml` command. It can be used to check the prefix map in
this file and give feedback on non-standard CURIE prefix usage, unknown CURIE
prefixes, etc. while giving suggestions for fixes, when possible.

Running the command on the file that contains the example prefixes from above
gives the following output:

```console
$ bioregistry validate linkml --tablefmt github --use-preferred https://github.com/HendrikBorgelt/CatCore/raw/refs/heads/main/src/catcore/schema/catcore.yaml
```

| prefix  | uri_prefix                                        | issue                     | solution                        |
| ------- | ------------------------------------------------- | ------------------------- | ------------------------------- |
| catcore | https://w3id.org/nfdi4cat/catcore/                | unknown CURIE prefix      |                                 |
| AFR     | http://purl.allotrope.org/ontologies/result#AFR_  | unknown CURIE prefix      |                                 |
| AFP     | http://purl.allotrope.org/ontologies/process#AFP_ | unknown CURIE prefix      |                                 |
| AFQ     | http://purl.allotrope.org/ontologies/quality#AFQ_ | unknown CURIE prefix      |                                 |
| nmrCV   | http://nmrML.org/nmrCV#NMR:                       | non-standard CURIE prefix | Switch to preferred prefix: NMR |
| AFRL    | http://purl.allotrope.org/ontologies/role#AFRL_   | unknown CURIE prefix      |                                 |
| SIO     | http://semanticscience.org/resource/SIO_          | non-standard CURIE prefix | Switch to preferred prefix: sio |

Curation feedback is not absolute - it's always possible that the Bioregistry
is missing key content. Luckily, it conforms to the [open data, open code, open infrastructure (O3)](https://www.nature.com/articles/s41597-024-03406-w) guidelines,
so it's easy for anyone to perform a [drive-by curation](https://doi.org/10.32388/KBX9VO) to fix any minor issues.
Based on the output above, I made improvements to the Bioregistry in 
[biopragmatics/bioregistry#1788](https://github.com/biopragmatics/bioregistry/pull/1788) to add four new prefixes
for the Allotrope semantic spaces and add `SIO` (stylized with capital letters) as the "preferred prefix" for
the [Semantic Science Integrated Ontology](https://semantic.farm/sio).

Note that LinkML is developed by members of the OBO Community, and therefore,
its prefixes often skew towards OBO community preferences. Therefore, you might
want to use the `--use-preferred` flag if a lot of your prefixes are stylized in
uppercase or with mixed case.
