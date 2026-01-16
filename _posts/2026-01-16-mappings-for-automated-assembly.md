---
layout: post
title: Automated Assembly Requires Semantic Mappings
date: 2026-01-16 11:42:00 +0100
author: Charles Tapley Hoyt
tags:
  - SSSOM
  - semantic mappings
---

Data and knowledge originating from heterogeneous sources often use
heterogeneous controlled vocabularies and/or ontologies for annotating named
entities. Semantic mappings are essential towards resolving these discrepancies
and integrating in a coherent way. This post highlights how this looks in two
scenarios: when integrating knowledge into a knowledge graph and when
integrating lexica to create integrative corpra for text mining.

## Knowledge Assembly

Generate coherent knowledge assemblies

![](/img/mappings-automated-assembly/knowledge-assembly.svg)

In practice, mapping is typically required on both the subject and object in
parallel. Concretely, ChEBI annotates ethanol as a
[NMDA receptor antagonist (CHEBI:60643)](https://semantic.farm/CHEBI:60643) and
DrugBank annotates ethanol as a
[NMDA Receptor Antagonists (drugbank.category:DBCAT002723)](https://go.drugbank.com/categories/DBCAT002723).
This means that we have to leverage both a mapping between the drug terms and
the classification terms to assemble knowledge coherently (i.e, deduplicated).

In most resources, there isn't a full concordance between a triple. For example,
DrugBank annotates ethanol as a
[Cytochrome P-450 CYP3A4 Inhibitors (drugbank.category:DBCAT003232)](https://go.drugbank.com/categories/DBCAT003232).
There's a corresponding term in ChEBI
[EC 1.14.13.97 (taurochenodeoxycholate 6α-hydroxylase) inhibitor, (CHEBI:86501)](https://www.ebi.ac.uk/chebi/search?query=CYP3A4%20Inhibitors),
but ChEBI does not have this triple.

Most importantly, this scenario is for when there are unique pieces of knowledge
in one resource. For example, DrugBank annotates ethanol as
[Agents Causing Muscle Toxicity (drugbank.category:DBCAT003935)](https://go.drugbank.com/categories/DBCAT003935).
There is no corresponding ChEBI term. In a coherent knowledge assembly, there
can be a variety of vocabularies, as long as they are deduplicated.

Note on hierarchical reasoning - INDRA, MIRA, something more generic that
reasons over is-a and part-of relationships to do hierarchical inference and
assess confidence.

## Lexicon Assembly

Generate and apply coherent biomedical lexical indices for NER and NEN
