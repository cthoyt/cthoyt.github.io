---
layout: post
title: Machine-Actionable Training Materials at BioHackathon Germany 2025
date: 2025-12-09 12:08:00 +0100
author: Charles Tapley Hoyt
tags:
  - LinkML
  - Bioregistry
  - prefix maps
  - CURIEs
  - URIs
---

Last week, I attended the
[4<sup>th</sup> BioHackathon Germany](https://www.denbi.de/de-nbi-events/1840-4th-biohackathon-germany)
hosted by the
[German Network for Bioinformatics Infrastructure (de.NBI)](https://www.denbi.de).
I participated in the project _On the Path to Machine-actionable Training
Materials_ in order to improve the interoperability between
[DALIA](https://search.dalia.education/basic),
[TeSS](https://tess.elixir-europe.org),
[mTeSS-X](https://elixirtess.github.io/mTeSS-X), and
[Bioschemas](https://bioschemas.org). This post gives a summary of the
activities leading up to the hackathon and the results of our happy hacking.

## Team and Goals

![](/img/biohackathon2025/team.jpg)

Our project,
[On the Path to Machine-actionable Training Materials](https://www.denbi.de/de-nbi-events/1939-4th-biohackathon-germany-on-the-path-to-machine-actionable-training-materials),
had the following active participants throughout the week:

- Nick Juty & Phil Reed (University of Manchester)
- Leyla Jael Castro & Roman Baum (Deutsche Zentralbibliothek für Medizin; ZB
  Med)
- Petra Steiner (University of Darmstadt)
- Oliver Knodel & Martin Voigt (Helmholtz-Zentrum Dresden-Rossendorf; HZDR)
- Dilfuza Djamalova (Forschungszentrum Jülich; FZJ)
- Jacobo Miranda (European Molecular Biology Laboratory; EMBL)

Nick and Petra were our team leaders and Phil acted as the project's _de facto_
secretary. On the first day of the hackathon, we were briefly joined by Alban
Gaignard (Nantes University), Dimitris Panouris (SciLifeLab), and Harshita Gupta
(SciLifeLab) to present their current related work. Similarly, Dominik Brilhaus
(Heinrich-Heine-Universität Düsseldorf) joined on the first day to share his
perspective from DataPLANT (the NFDI consortium for plants) as a training
materials creator. Finally, Helena Schnitzer (FZJ) participated in some
Bioschemas discussions through the week.

## Goals

We categorized our work plan into three streams:

1. [**Training Material Interoperability**](#training-material-interoperability) -
   survey the landscape of relevant ontologies and schemas for annotating
   learning materials, curate mappings/crosswalks, and develop a programmatic
   toolbox
2. [**Training Material Analysis**](#training-material-analysis) - analyze
   training materials at scale to group similar training materials, reduce
   redundancy, and semi-automatically construct learning paths
3. [**Modeling Learning Paths**](#modeling-learning-paths) - collect use cases
   and develop a (meta)data model for learning paths

## Training Material Interoperability

Interoperability is third pillar of the
[FAIR data principles](https://www.nature.com/articles/sdata201618).

Metadata describing training materials may be captured and stored in one of
several data models including the DALIA Interchange Format (DIF) v1.3, the
format implicitly defined by the TeSS API, and the Schemas.org Learning Material
profile.

A key step towards interoperability is to identify concepts/entities in a
standard and unambiguous way. Let's unpack this:

- Identifying and indexing relevant ontologies, controlled vocabularies, and
  schemas for learning materials and (open) educational resources
- Curating mappings between ontologies and controlled vocabularies terms and
  crosswalks between schemas. Specifically, we focused on curating crosswalks
  between the representations of learning materials in the schemas from MoDALIA
  and Schema.org
- Implemented in the OERbservatory Python package
- Demonstrated federation in the mTeSS-X platform

The standard identification of concepts and entities

- ontologies and controlled vocabularies cover classes and individuals
- databases like the
  [Galaxy Training Network (GTN)](https://training.galaxyproject.org)
- schemas like [OERSchema](https://semantic.farm/oerschema),
  [Schema.org](https://semantic.farm/sdo), and
  [MoDALIA](https://semantic.farm/modalia)

such as academic disciplines,

We started the week off discussing best practices for identifiers:

- Identifiers support the interoperability aspect of FAIR data
- Linked (open) data - when different resources use the same identifiers, we can
  automatically integrate them Knowledge Graphs and Federated SPARQL Queries
- Resolve structured, machine-readable data to human-readable (and LLM-readable)
  via the web

Where do the identifiers come from? What are the ontologies, controlled
vocabularies, databases, and schemas that mint them?

### Indexing Ontologies and Schemas

Our first concrete goal for training material interoperability at the hackathon
was to survey ontologies, controlled vocabularies, and other resources that mint
(persistent) identifiers that might appear in the metadata describing a learning
material. For example, TeSS uses the [EDAM Ontology](https://semantic.farm/edam)
to annotate topics onto training materials. For the same purpose, DALIA uses the
[Hochschulcampus Ressourcentypen](https://semantic.farm/kim.hcrt) (I'll say more
on how we deal with the conflicting resources in the section below on mappings).

Our second concrete goal was to survey schemas that are used in modeling open
educational resources and training materials, for example,
[Schema.org](https://semantic.farm/sdo),
[OERSchema](https://semantic.farm/oerschema), and
[MoDALIA](https://semantic.farm/modalia), which encodes the DALIA Interchange
Format (DIF) v1.3.

The Semantic Farm ([https://semantic.farm](https://semantic.farm)) is
comprehensive database of metadata about resources that mint (persistent)
identifiers (e.g., ontologies, controlled vocabularies, databases, schemas) such
as their preferred CURIE prefix for usage in SPARQL queries and other semantic
web applications. It imports and aligns with other databases like
[Identifiers.org](https://identifiers.org) (for the life sciences) and
[BARTOC](https://bartoc.org) (for the digital humanities) to support
interoperability and sustainability. It follows the
[open data, open code, and open infrastructure (O3)](https://www.nature.com/articles/s41597-024-03406-w)
guidelines and has well-defined governance to enable community maintenance and
support longevity.

It's the perfect place to index all the learning material and open educational
resource-related ontologies, controlled vocabularies, databases, and schemas.

I gave a tutorial on how to search the Semantic Farm for ontologies, controlled
vocabularies and other resources that mint (persistent) identifiers, and how to
contribute any that are missing. In short, they can be contributed by filling
out the
[new prefix request template](https://github.com/biopragmatics/bioregistry/issues/new?template=new-prefix.yml)
on GitHub. If you're interested to add a new entry, you can directly use the
form, read the
[contribution guidelines](https://github.com/biopragmatics/bioregistry/blob/main/docs/CONTRIBUTING.md#submitting-new-prefixes),
or watch a
[short YouTube tutorial](https://www.youtube.com/watch?v=e-I6rcV2_BE).

While I had done some significant preparatory work before the hackathon by
creating many new entries in the Semantic Farm, the team found and added several
new and important entries to the Semantic Farm during the hackathon too. Here
are two highlights:

[Martin Voigt](https://orcid.org/0000-0001-5556-838X) contributed the prefix
`amb` for the
[Allgemeines Metadatenprofil für Bildungsressourcen](https://dini-ag-kim.github.io/amb/20231019)
(General Metadata Profile for Educational Resources) in
[biopragmatics/bioregistry#1781](https://github.com/biopragmatics/bioregistry/pull/1781).
This is a metadata schema for learning materials produced by the
Kompetenzzentrum Interoperable Metadaten (KIM) within the Deutsche Initiative
für Netzwerkinformation e.V. that was heavily inspired by
[Schema.org](https://schema.org) and the Dublin Core
[Learning Resource Metadata Initiative (LRMI)](https://www.dublincore.org/about/lrmi/)

[Dilfuza Djamalova](https://orcid.org/0009-0004-7782-2894) and
[Jacobo Miranda](https://orcid.org/0009-0005-0673-021X) contributed the prefix
`gtn` for
[Galaxy Training Network](https://training.galaxyproject.org/training-material)
training materials in
[biopragmatics/bioregistry#1779](https://github.com/biopragmatics/bioregistry/pull/1779).
This resource contains multi- and cross-disciplinary training materials for
using the Galaxy workflow management system. Below, I describe how we ingested
transformed the training materials from GTN into a common format such they can
be represented according to the DALIA Interchange Format (DIF) v1.3, the
implicit data model expected by TeSS, and in Bioschemas-compliant RDF.

Ultimately, we collated relevant ontologies, controlled vocabularies, schemas
and other resources that mint (persistent) identifiers in a
[collection](https://semantic.farm/collection/0000018) such that they can be
easily found and shared.

### Semantic Mappings and Crosswalks

![](/img/biohackathon2025/overlaps.svg)

I alluded to the different resources used by TeSS and DALIA to annotate
disciplines. The issue of partially overlapping ontologies, controlled
vocabularies, and database is quite widespread, and can manifest in a few
different ways. The figure above shows that redundancy can arise because of
different focus within a domain (i.e., the chemistry example), different
hierarchical specificity (i.e., the disease example), and due to massive generic
resources having overlap across many domains (e.g., like UMLS, MeSH, NCIT).

This is problematic when integrating learning materials from different sources,
e.g., TeSS and DALIA, because two learning resources may be annotated with
different terms describing the same discipline. Therefore, the solution is to
create semantic mappings between these terms.

I've worked for several years on the
[Simple Standard for Sharing Ontological Mappings (SSSOM)](https://mapping-commons.github.io/sssom/)
standard for storing semantic mappings, so this was naturally the target for our
work. Further, I have been working on a domain-agnostic workflow for predicting
semantic mappings with lexical matching and deploying a curation interface
called [SSSOM Curator](github.com/cthoyt/sssom-curator/). I gave a tutorial for
using SSSOM Curator to the team based on a previous tutorial I made (that can be
found on YouTube [here](https://www.youtube.com/watch?v=FkXkOhT8gdc&t=293s)). We
prepared predicted semantic mappings between several learning resource-related
ontologies in
[biopragmatics/biomappings#204](https://github.com/biopragmatics/biomappings/pull/204),
but we didn't prioritize semantic mapping curation during the hackathon. Here's
what they look like in the SSSOM Curator interface for Biomappings:

![](/img/biohackathon2025/sssom-curator-disciplines.png)

Where curating correspondences between concepts in ontology, controlled
vocabularies, and databases is often called semantic mapping, curating
correspondences between schemas and properties therein is often called
crosswalks. We put a bigger emphasis on producing crosswalks between Schema.org
and MoDALIA. This is actually a more complex problem due to the fact that
correspondences between elements in schemas can be more sophisticated (e.g.,
mapping between two fields for first and last names to a single name field), but
there are at least a few places where properties can be mapped with SSSOM.

![](/img/biohackathon2025/crosswalks.png)

An interesting lesson learned is that there's a lot of pushback on using SKOS
relationships in SSSOM because the narrow and broader relations have the
opposite direction that people expect.

### Operationalizing Mappings

Goals:

1. consume all different schemas
2. produce all different schemas
3. have a well-defined intermediate format
4. consume content that's not actually in a format (data science it up!)

What we did:

1. Improve tess-downloader package
2. Improve DALIA DIF package
3. Implement OERbservatory package to have a generic format that's a superset of
   both, and operationalizes mappings between

Implemented in the OERbservatory Python package

### Scaling Mappings

1. implemented importer for Galaxy w/ Dilfuza and Jacobo
2. implemented importer for OERSI (which itself is an aggregator) and OERhub
3. create an extensible workflow for getting all content from all registered
   sources and outputting to JSONL based on the Unified OER model. This is a
   place where we could also export TeSS JSON or DALIA DIF v1.3 RDF

## Training Material Analysis

- Identify similar training materials to:
- Deduplicate and merge records across registries
- Connect training material producers, consolidate efforts

What we did:

1. Implement workflow for making TF-IDF vectors and also sentence-embedding
   vectors for training materials

## Modeling Learning Paths

- Collect examples of learning paths
  - Developed a schema that groups learning materials into a logical and modular
    ordering
  - Mock a schema by extending Schema.org
