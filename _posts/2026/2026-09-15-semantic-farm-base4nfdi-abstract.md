---
layout: post
title: Semantic Farm at the 3rd Base4NFDI User Conference (UC4B2026)
date: 2026-09-15 12:40:00 +0200
author: Charles Tapley Hoyt
tags:
  - Bioregistry
  - Semantic Farm
  - CURIEs
  - URIs
---

I submitted an abstract to
the [3rd Base4NFDI User Conference (UC4B2026)](https://base4nfdi.de/news-events/events/user-conference-2026)
on behalf of
the [NFDI Section Metadata Working Group for Ontology Harmonization and Mapping](https://github.com/nfdi-de/section-metadata-wg-onto/)
describing the current uses and future prospects for the [Semantic Farm](https://semantic.farm) throughout the NFDI and
Base4NFDI.

We posted the abstract to Zenodo such that it can be cited by <https://doi.org/10.5281/zenodo.21686485>. Special thanks
to co-authors Mark Doerr (University Greifswald), Ulrik Stervbo (Ruhr-Universität Bochum), Benjamin Zapilko (GESIS -
Leibniz Institute for the Social Sciences), and Sonja Herres-Pawlis (RWTH Aachen).

## Abstract: Operationalizing identifier interoperability across the NFDI with the Semantic Farm

A key challenge in achieving the interoperability facet of
the [FAIR data principles](https://doi.org/10.1038/sdata.2016.18) is the consistent identification of researchers,
chemicals, paintings, and other entities relevant for NFDI. Often, this means choosing the correct standard
[uniform resource identifier (URI)](https://www.rfc-editor.org/info/rfc3986/)
or [compact URI (CURIE)](https://www.w3.org/TR/2010/NOTE-curie-20101216/) for an entity from an ontology, controlled
vocabulary, persistent identifier (PID) service, or database.

This presents a challenge when multiple CURIEs or URIs can be constructed for the same entity, which is compounded by
the independent evolution of tools and services relevant for different NFDI consortia. For example, the entry for water
in the Chemical Entities of Biomedical Interest (ChEBI) can be identified by either the
URIs [https://www.ebi.ac.uk/chebi/CHEBI:15377](https://www.ebi.ac.uk/chebi/CHEBI:15377)
or [http://purl.obolibrary.org/obo/CHEBI\_15377](http://purl.obolibrary.org/obo/CHEBI_15377) or by the CURIEs *chebi:
15377*, *CHEBI:15377*, or *CHEBIID:15377*. An organization-wide policy is required to determine and communicate which is
correct.

The NFDI has not yet adopted an actionable, organization-wide policy for standardizing CURIEs and URIs. We present the
[Semantic Farm](https://semantic.farm) (previously called *The Bioregistry*) on behalf of the
[NFDI Section Metadata Working Group for Ontology Harmonization and Mappings](https://github.com/nfdi-de/section-metadata-wg-onto/tree/main)
as a pre-existing, mature solution for the standardization of CURIEs and URIs. It acts as a centralized index of
metadata for resources that mint identifiers that can be readily adopted on the NFDI-level and beyond.

Importantly, the Semantic Farm is a foundational service that can directly support complementary base services
([PID4NFDI](https://base4nfdi.de/projects/pid4nfdi), [TS4NFDI](https://base4nfdi.de/projects/ts4nfdi,
and [KGI4NFDI](https://base4nfdi.de/projects/kgi4nfdi)), NFDI sections, their respective working groups, and researchers
in NFDI consortia towards improving interoperability. We highlight several existing applications of the Semantic Farm
within NFDI:

1. TS4NFDI uses both the flagship instance of the [Ontology Lookup Service](https://www.ebi.ac.uk/ols4/) (hosted by the
   European Bioinformatics Institute) and the [TIB Terminology Service](https://terminology.tib.eu/ts/) instance, which
   both use the Semantic Farm for URI compression, CURIE expansion, and generation of web links for database
   cross-references.

2. Section Metadata Working Group for Ontology Harmonization and Mapping uses the Semantic Farm capture ontology lists
   used by each consortium ([https://semantic.farm/nfdi](https://semantic.farm/nfdi)).

3. The Semantic Farm supports the construction of knowledge graphs with standardized URIs such as in Section
   EduTrain's [DALIA](https://search.dalia.education) platform for open educational resources and Section International
   Engagement Working Group for Landscaping and Outreach's bibliometric knowledge graph. Standardization facilitates the
   integration of external data from ORCiD, ROR, CORDIS, and Wikidata.

4. The Semantic Farm's codebase is used by the [LinkML](https://linkml.io) runtime, which has growing adoption across
   consortia such as NFDI4Chem, NFDI4Cat, and GHGA. It can be further used to standardize the prefix maps in LinkML
   schemas

5. The Semantic Farm supports consortia like NFDI4Chem that must standardize and ultimately harmonize a variety of
   ontology, database, and structural identifiers like InChI.

Further information on the Semantic Farm's KPIs can be found
at [https://cthoyt.com/2025/08/22/bioregistry-impact.html](https://cthoyt.com/2025/08/22/bioregistry-impact.html). We
aspire to submit Semantic Farm to Base4NFDI Service Support Track and to support its integration in more NFDI services
and usage in data resources.

## Extras

About NFDI4Cat using LinkLML schema validated by
SF: [https://cthoyt.com/2026/01/06/bioregistry-linkml-validation.html](https://cthoyt.com/2026/01/06/bioregistry-linkml-validation.html)

KGI - [https://cthoyt.com/2025/09/11/nfdi4culture-prefix-validation.html](https://cthoyt.com/2025/09/11/nfdi4culture-prefix-validation.html)
and [https://cthoyt.com/2025/09/04/bioregistry-turtle-validation.html](https://cthoyt.com/2025/09/04/bioregistry-turtle-validation.html)

Show KPIs about adoption within NFDI and internationally

Demonstrator of integration between NFDI4Chem and NFDI4Culture's KGs which requires standardization that isn't covered
by TS4NFDI nor KGI4NFDI

an open source, domain-agnostic, community curated semantic space registry, meta-registry, and compact identifier
resolver.

Ulrik alternate text:

However, CURIEs are not a standardized namespace: nothing prevents multiple different prefixes from being defined for
the same underlying resource, or from being defined inconsistently in case or form. For instance the CURIE for Medical
Subject Headings (MeSH) may be defined as MeSH, MESH, or mesh. In addition, a nonsense prefix like GAATTC could just as
easily be defined to expand to the same base URI as an existing, established prefix. As a result, the same entity can be
referenced by several different, non-standardized CURIEs. In addition, distinct URIs can be constructed for the same
entity even within a single source, and these are not always interchangeable. The MeSH entry for sea urchin Spec3
protein can be identified by the CURIEs MeSH:C063233, mesh:C063233, or MESH:C063233 and the entry can be reached via
either https://meshb.nlm.nih.gov/record/ui?ui=C063233
or [http://id.nlm.nih.gov/mesh/C063233](http://id.nlm.nih.gov/mesh/C063233).

Sonja alternate text (out of scope since it's about mappings, which isn't specifically a Semantic Farm task, but
something else):

Similar challenges arise in chemistry, where compounds are simultaneously referenced by database-specific accessions
(e.g., ChEBI, PubChem, ChemSpider), registry identifiers, and structure-derived identifiers such as the IUPAC
International Chemical Identifier (InChI). While InChI provides a globally standardized representation of molecular
identity, interoperable workflows still require consistent mappings between InChI, database-specific identifiers, and
their corresponding CURIEs and URIs.

6. Within NFDI4Chem, the Semantic Farm complements the IUPAC International Chemical Identifier (InChI) ecosystem by
   providing harmonized metadata for chemistry identifier namespaces, enabling robust mappings between InChI-derived
   identifiers and database-specific resources such as ChEBI and PubChem. This supports machine-actionable
   interoperability across chemical knowledge graphs and FAIR data infrastructures. Rather than replacing
   chemistry-specific identifiers such as InChI, the Semantic Farm operationalizes their interoperable use by providing
   standardized namespace metadata, CURIE policies, and URI mappings that enable consistent integration across NFDI
   services and international FAIR infrastructures. 