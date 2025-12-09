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
I participated in the track _On the Path to Machine-actionable Training
Materials_ in order to improve the interoperability between
[DALIA](https://search.dalia.education/basic),
[TeSS](https://tess.elixir-europe.org),
[mTeSS-X](https://elixirtess.github.io/mTeSS-X), and
[Bioschemas](https://bioschemas.org). This post gives a summary of the
activities leading up to the hackathon and the results of our happy hacking.

We had the following active participants throughout the week:

- Nick Juty & Phil Reed (University of Manchester)
- Leyla Jael Castro & Roman Baum (Deutsche Zentralbibliothek für Medizin; ZB
  Med)
- Petra Steiner (University of Darmstadt)
- Oliver Knodel & Martin Voigt (Helmholtz-Zentrum Dresden-Rossendorf; HZDR)
- Dilfuza Djamalova (Forschungszentrum Jülich; FZJ)
- Jacobo Miranda (European Molecular Biology Laboratory; EMBL)

I'd like to give a big s/o to Nick and Petra, who were our team leads and Phil
for not only being the project's _de facto_ secretary but also hacking his heart
out at the same time.

We also had a few pop-ins including Alban Gaignard (Nantes University), Dimitris
Panouris (SciLifeLab), and Harshita Gupta (SciLifeLab), who joined us on the
first day to give background on their related work. Helena Schnitzer (FZJ)
joined for some Bioschemas discussions, and Dominik Brilhaus
(Heinrich-Heine-Universität Düsseldorf) who joined to share his perspective on
preparing training materials in DataPLANT.

We organized our work into three task streams:

1. Training Material Interoperability
   - Identifying and indexing relevant ontologies, controlled vocabularies, and
     schemas for learning materials and ( open) educational resources
   - Curating mappings between ontologies and controlled vocabularies terms and
     crosswalks between schemas. Specifically, we focused on curating crosswalks
     between the representations of learning materials in the schemas from
     MoDALIA and Schema.org
   - Implemented in the OERbservatory Python package
   - Demonstrated federation in the mTeSS-X platform
2. Training Material Analysis
   - Identify similar training materials to:
   - Deduplicate and merge records across registries
   - Connect training material producers, consolidate efforts
3. Organization into Learning Paths
   - Collect examples of learning paths
   - Developed a schema that groups learning materials into a logical and
     modular ordering
   - Mock a schema by extending Schema.org

## Identifying and Indexing Ontologies, Controlled Vocabularies, and Schemas

We started the week off discussing best practices for identifiers:

- Identifiers support the interoperability aspect of FAIR data
- Linked (open) data - when different resources use the same identifiers, we can
  automatically integrate them Knowledge Graphs and Federated SPARQL Queries
- Resolve structured, machine-readable data to human-readable (and LLM-readable)
  via the web

The Semantic Farm ([https://semantic.farm](https://semantic.farm)) is:

1. The most comprehensive database of CURIE prefixes, URI prefixes, identifier
   standards, and metadata about (semantic web) identifiers
2. Imports and aligns related efforts like Identifiers.org, Name-to-Thing,
   BARTOC
3. Open data, open code, and open infrastructure + well-defined governance to
   enable community maintenance and support longevity
4. Domain- and community-driven collections, subsets, and conflict resolution

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

Both before and during the hackathon, we contributed several other records for
ontologies, controlled vocabularies, databases, and schemas to the Semantic
Farm. Finally, we collated them in a
[collection](https://semantic.farm/collection/0000018) such that they can be
easily found and shared.
