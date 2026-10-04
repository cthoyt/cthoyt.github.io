---
layout: post
title: The World Avatar, NFDI, and the Anatomy of an Open Science Contribution
date: 2026-09-24 13:45:00 +0200
author: Charles Tapley Hoyt
tags:
  - ontology
  - NFDI4Chem
  - chemistry
  - drive-by curation
  - Bioregistry
  - Semantic Farm
---

The [World Avatar](https://theworldavatar.io) project aspires to model and
simulate the real world at the chemical, municipal, and geological scales. Its
[computational chemistry ontology](https://semantic.farm/worldavatar.compchem),
[ontology for chemical kinetic reaction mechanisms](https://semantic.farm/worldavatar.kin),
and [chemical species ontology](https://semantic.farm/worldavatar.species) are
of particular interest for the [NFDI4Chem](https://nfdi4chem.de) and
[NFDI4Cat](https://nfdi4cat.org) consortia either to reuse, extend, or harmonize
with other related ontologies in the respective
[NFDI4Chem ontology list](https://semantic.farm/collection/0000014) and
[NFDI4Cat ontology list](https://semantic.farm/collection/0000011).

Specifically, while working with [Mario Wolter](https://github.com/MarioWolter)
and [Robin Ströhmann](https://github.com/CodoRob) to develop a
[basis set ontology](https://github.com/NFDI4Chem/basis-set-exchange-ontology),
I manually curated mappings in the
[Simple Standard for Sharing Ontological Mappings (SSSOM)](https://mapping-commons.github.io/sssom)
format between basis sets appearing in the
[Basis Set Exchange](https://www.basissetexchange.org), the
[Gainesville Core Ontology (GC)](https://semantic.farm/gainesville.core),
the
[Elementary Multiperspective Material Ontology (EMMO)](https://semantic.farm/registry/emmo),
and Wikidata in
[NFDI4Chem/basis-set-exchange-ontology#14](https://github.com/NFDI4Chem/basis-set-exchange-ontology/pull/14).

I was also suggested to map to the World Avatar's Computational
Chemistry Ontology, which I wasn't very familiar with, so I went to see what information
was available about it in the Semantic Farm. Initially, it had incomplete and outdated
information, including an Internet Archive link to an old version of the ontology. I searched
the web and found that the World Avatar project not only had created a new website in the last
few months, but also found that they were maintaining their ontologies via a 
repository on GitHub ([TheWorldAvatar/ontology](https://github.com/TheWorldAvatar/ontology)).
This not only let me update the three existing World Avatar records in the Semantic Farm
in [biopragmatics/bioregistry#2074](https://github.com/biopragmatics/bioregistry/pull/2074),
but also got me thinking on how I could systematically construct new records in the Semantic
Farm for _all_ World Avatar ontologies, similarly to what I did for [SWEET](https://github.com/biopragmatics/bioregistry/pull/1772) (geology ontologies)
and [CESSDA](https://github.com/biopragmatics/bioregistry/pull/1756) (humanities ontologies and controlled vocabularies).

This is where the open science story begins. While I would have been nice if I could have just
written a script to download the repository and its contents, loop through the folder of the ontologies,
extract their metadata, and construct new Semantic Farm records, it's never that easy. Instead,
I went down the World Avatar rabbit hole.

1. found some ontology files, but not for everything
2. realized that metadta inside some ontology files was straight up wrong (https://github.com/TheWorldAvatar/ontology/issues/39 and https://github.com/TheWorldAvatar/ontology/pull/40)
3. realized some OWL files didn't reflect their source data
4. had to figure out how to rebuild the OWL files
5. helped make this process reproducible
6. had o construct missing OWL files (https://github.com/TheWorldAvatar/ontology/issues/41)
6. found more issues
7. ultimatley wrote the script I had planned on  in https://github.com/biopragmatics/bioregistry/pull/2051