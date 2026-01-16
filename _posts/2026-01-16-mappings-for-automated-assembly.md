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

## Background

### Conceptual Overlap, Redundancies, and Discrepancies

Below, I'll give a few concrete examples of where these issues occur.

![](/img/mappings-automated-assembly/overlaps.svg)

In chemistry, there are dozens of resources that assign identifiers to small
molecules. Many have been constructed with unique scope or purpose such as
MetaboLights for metabolites, SwissLipids for lipids, DrugBank for drugs. Some
have similar scope and purpose, but have been constructed in parallel due to
scientific modeling reasons, such as different disease ontologies modeling
diseases with different parts of the Basic Formal Ontology (BFO). Some have
similar scope and purpose, but have been constructed in parallel due to
non-scientific reasons, such as PubChem and ChEMBL for small molecules with
assay information. As an aside, building resources in an open and collaborative
manner can help reduce proliferation, with the (major) caveat that they don't
satisfy funding bodies nor the requirements for career progression so easily.

In medicine and epidemiology, there are many resources describing diseases,
transmission, response, adverse outcomes, and other facets. Particularly during
the COVID-19 pandemic, many independent controlled vocabularies were constructed
to model information at various levels of specificity. The figure shows the
hierarchical relationships betwee the
[Disease Ontology (DOID)](https://semantic.farm/doid), the
[Infectious Disease Ontology (IDO)](https://semantic.farm/ido), the
[Viral Infectious Disease Ontology (VIDO)](https://semantic.farm/vido), the
[Coronavirus Infectious Disease Ontology (CIDO)](https://semantic.farm/cido),
and the
[COVID-19 Infectious Disease Ontology (IDOCOVID19)](https://semantic.farm/idocovid19).
When effectively reusing terms (as OBO Foundry Ontologies often do), this
doesn't create an issue, but in practice, many resources do not reuse terms for
various reasons.

In the life sciences, there are several controlled vocabularies that cover a
large number of topics such as the
[Medical Subject Headings (MeSH)](https://semantic.farm/mesh),
[National Cancer Institute Thesaurus (NCIT)](https://semantic.farm/ncit), and
[Unified Medical Language System (UMLS)](https://semantic.farm/umls). While they
give good coverage across many topics, these resources are often neither
detailed, precise enough, nor curated as ontologies. Therefore, many controlled
vocabularies use terms from these resources as a base and curate further.
However, this causes redundancy, and in many cases, the group does not correctly
cross-reference back. The
[Ontology for MicroRNA Target (OMIT)](https://semantic.farm/registry/omit) even
imported the entirety of MeSH, but didn't make any cross-references back to the
source, creating even more redundancy.

If you were wondering why for each domain, we couldn't just have a single
resource, then please have a look at
[https://xkcd.com/927](https://xkcd.com/927) :) Though, some resources that have
been around for a long time basically have a monopoly. For example, nobody in
their right mind in 2026 would start their own protein database to compete with
[UniProt](https://uniprot.org).

### Needs of The Many

![](/img/mappings-automated-assembly/overlaps-deal-with-it.svg)

In the end, data scientists and curators often don't want to deal with the
proliferation of vocabularies nor the ontological commitments made by them
(e.g., in the cases of disease). they just want to be able to pick a single term
for their concept, and have all information connected there.

This leads to the goal of this post, which is to align two high-level workflows
on how this can be accomplished. I am not going to go into the nitty-gritty of
where to get the mappings and how to apply them - that will be for a future post
about SeMRA.

## Assembly

### Knowledge Assembly

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

### Lexicon Assembly

Generate and apply coherent biomedical lexical indices for NER and NEN
