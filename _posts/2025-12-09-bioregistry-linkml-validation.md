---
layout: post
title: Validating Prefix Maps in LinkML Schemas
date: 2025-12-09 12:08:00 +0100
author: Charles Tapley Hoyt
tags:
  - LinkML
  - Bioregistry
  - prefix maps
  - CURIEs
  - URIs
---

follow-up to https://cthoyt.com/2025/09/11/nfdi4culture-prefix-validation.html

https://github.com/biopragmatics/bioregistry/pull/1786

[LinkML](https://linkml.io) enables defining a data model with YAML. Each
definition also includes a prefix map, which can be validated against the
Bioregistry. Here's an abridged excerpt of one
[such configuration](https://github.com/HendrikBorgelt/CatCore/blob/main/src/catcore/schema/catcore.yaml)

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

The `bioregistry validate linkml` command can be used to check the prefix map in
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

Note that LinkML is developed by members of the OBO Community, and therefore,
its prefixes often skew towards OBO community preferences. Therefore, you might
want to use the `--use-preferred` flag.

Follow-up curations:

https://github.com/biopragmatics/bioregistry/pull/1788
