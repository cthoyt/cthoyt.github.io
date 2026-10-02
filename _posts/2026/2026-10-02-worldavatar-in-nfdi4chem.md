---
layout: post
title: Worldavatar, NFDI4Chem, and the Anatomy of an Open Science Contribution
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

During this process, I was suggested to map to the World Avatar's Computational
Chemistry Ontology. The existing metadata in the Semantic Farm included a
download link imported from the TIB Terminology Service which

`worldavatar.compchem`

<https://github.com/biopragmatics/bioregistry/pull/2074>

While my work in NFDI4Chem
and
[NFDI Section Metadata Working Group on Ontology Harmonization and Mappings](https://github.com/nfdi-de/section-metadata-wg-onto)
motivated the curation of semantic mappings between these World Avatar
ontologies and other well-known ontologies in the space.

While the story

<https://github.com/NFDI4Chem/basis-set-exchange-ontology/pull/14/changes>

This meant it was important to get access to the ontologies in a standard form
such that they could be indexed in the [Semantic Farm](https://semantic.farm)
then ingested into the [SSSOM Curator](https://github.com/cthoyt/sssom-curator)
workflow.

However, my more generic work on indexing ontologies in the
[Semantic Farm](https://semantic.farm) to support the interdiscipinary consortia
of NFDI motivated me to add not only relevant information about the chemistry
ontologies, but also the other ones.

This led me down quite a rabbit hole, and I want to report on what I had to do
to make this work.

---

The first thing I found is that the World Avatar project has
a repository on GitHub ( <https://github.com/TheWorldAvatar/ontology>)
containing the source for all their ontologies.
